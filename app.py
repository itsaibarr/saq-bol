"""Сақ бол demo: paste a message or a call transcript, get a risk band, the trigger phrase and advice.

usage: python app.py [run_dir]   (run_dir holds best/ and final_report.json; default runs/FINAL)
Prototype, not financial advice.
"""
import json, os, sys
import gradio as gr
import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipeline", "src"))
from explain import explain
from textnorm import normalize

RUN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SAQBOL_RUN", "runs/kg_e5L_v8b_s1")
_rep = next((f"{RUN}/{n}" for n in ["final_report_testC.json", "final_report.json", "final_report_testB.json"] if os.path.exists(f"{RUN}/{n}")), None)
cfg = json.load(open(_rep)) if _rep else {}
THR, THR_LOW = cfg.get("thr_scam", 0.5), cfg.get("thr_suspicious", 0.2)
run_cfg = json.load(open(f"{RUN}/config.json")) if os.path.exists(f"{RUN}/config.json") else {}
dev = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
# An ensemble run lists its members; a single run is its own only member. Each member keeps its own prefix,
# max length and positive class, exactly as in training.
METHOD = run_cfg.get("method", "pct")


def _logit(p):
    p = np.clip(np.asarray(p, dtype=float), 1e-7, 1 - 1e-7)
    return np.log(p / (1 - p))


MEMBERS = []
for m in run_cfg.get("members", [RUN]):
    mc = json.load(open(f"{m}/config.json"))
    tok = AutoTokenizer.from_pretrained(f"{m}/best")
    tok.truncation_side = "left"  # calls: keep the latest turns, where the ask usually is
    mod = AutoModelForSequenceClassification.from_pretrained(f"{m}/best", dtype=torch.float16 if dev != "cpu" else torch.float32).to(dev).eval()
    ref, mu, sd = None, 0.0, 1.0
    if "members" in run_cfg:  # chat-dev reference scores: same normalisation as pipeline/src/ensemble.py
        pr = pd.read_json(f"{m}/preds.jsonl", lines=True)
        tg = pr[pr.set == "tg_dev"].score.values
        ref = np.sort(tg)
        zt = _logit(tg); mu, sd = float(zt.mean()), float(zt.std())
    MEMBERS.append({"tok": tok, "model": mod, "pos": mc.get("pos_idx", 1), "prefix": mc.get("prefix", ""), "max_len": mc.get("max_len", 128),
                    "ref": ref, "mu": mu, "sd": sd})


@torch.no_grad()
def member_scores(m, texts):
    out = []
    for i in range(0, len(texts), 32):
        enc = m["tok"]([m["prefix"] + normalize(t) for t in texts[i:i + 32]], padding=True, truncation=True, max_length=m["max_len"], return_tensors="pt").to(dev)
        out.append(torch.softmax(m["model"](**enc).logits.float(), -1)[:, m["pos"]].cpu().numpy())
    return np.concatenate(out)


def score(texts):
    texts = list(texts)
    if "members" not in run_cfg:
        return member_scores(MEMBERS[0], texts)
    acc = np.zeros(len(texts))
    for m in MEMBERS:
        s = member_scores(m, texts)
        if METHOD == "logit_z":  # mean z-scored logit, exactly as the frozen model was scored
            acc += (_logit(s) - m["mu"]) / (m["sd"] + 1e-9)
        else:
            acc += np.searchsorted(m["ref"], s, side="right") / len(m["ref"]) + 1e-6 * s
    acc /= len(MEMBERS)
    return 1 / (1 + np.exp(-acc)) if METHOD == "logit_z" else acc


COLORS = {"scam": "#c0392b", "suspicious": "#d68910", "safe": "#1e8449"}


LANG_UI = {"Авто / Auto": "auto", "Қазақша": "kk", "Русский": "ru"}


def check_message(text, ui="Авто / Auto"):
    if not text or not text.strip():
        return "", [], ""
    r = explain(text.strip(), score, THR, THR_LOW, LANG_UI.get(ui, "auto"))
    head = f"<h2 style='color:{COLORS[r['band']]};margin:0'>{r['band_text']}</h2>"
    spans = []
    if r["trigger"] and r["trigger"] in text:
        a = text.index(r["trigger"])
        spans = [(text[:a], None), (r["trigger"], "trigger"), (text[a + len(r["trigger"]):], None)]
    else:
        spans = [(text, None)]
    body = ""
    if r["red_flags"]:
        body += "**Белгілер / Признаки:** " + "; ".join(r["red_flags"]) + "\n\n"
    body += "\n\n".join(f"### → {x}" for x in r["advice"])
    return head, spans, body


def check_call(transcript):
    turns = [t.strip() for t in str(transcript).split("\n") if t.strip()]
    if not turns:
        return pd.DataFrame({"turn": [], "risk (log-odds)": [], "line": []}), ""
    prefixes = [" ".join(turns[:i + 1]) for i in range(len(turns))]
    s = score(prefixes)
    lo = _logit(s); t_hi = float(_logit([THR])[0])
    df = pd.concat([pd.DataFrame({"turn": np.arange(1, len(turns) + 1), "risk (log-odds)": lo, "line": "risk"}),
                    pd.DataFrame({"turn": np.arange(1, len(turns) + 1), "risk (log-odds)": t_hi, "line": "scam threshold"})])
    first = next((i + 1 for i, v in enumerate(s) if v >= THR), None)
    first_s = next((i + 1 for i, v in enumerate(s) if v >= THR_LOW), None)
    msg = (f"**Ескерту {first}-сөйлемде / Предупреждение на реплике {first}** (күмән / подозрение: {first_s})." if first else
           (f"{first_s}-сөйлемнен бастап күмәнді / Подозрительно с реплики {first_s}." if first_s else "Ескерту жоқ / Предупреждений нет."))
    return df, msg


EX_MSG = [
    "Сәлеметсіз бе, мен Қаржылық мониторинг агенттігінің тергеушісімін. Сіздің шотыңызды алаяқтар пайдаланып жатыр, ақшаңызды сақтау үшін оны қауіпсіз шотқа аудару керек. Бұл туралы ешкімге айтпаңыз.",
    "Құрметті зейнеткер! Сізге 2026 жылғы мемлекеттік өтемақы 87 500 теңге тағайындалды. Алу үшін карта деректерін egov-tolem.kz сайтына енгізіңіз.",
    "Курметти зейнеткер! Сизге 2026 жылгы мемлекеттик отемакы 87 500 тенге тагайындалды. Алу ушин карта деректерин egov-tolem.kz сайтына енгизиниз.",
    "Здравствуйте, служба безопасности банка. На ваше имя оформляется кредит. Чтобы его отменить, нужно оформить встречный кредит и перевести деньги на безопасный счёт. Никому не говорите об этом звонке.",
    "Ваш код для входа в Kaspi.kz: 5821. Никому не сообщайте этот код.",
    "Апа, кешке барамын, нан алып келейін бе?",
]
EX_CALL = ("Сәлеметсіз бе, Гүлнара Сериковна, сізге ыңғайлы ма сөйлесуге?\n"
           "Мен банктен хабарласып тұрмын, бір минут уақытыңызды алайын.\n"
           "Соңғы аптада қосымшаға кірдіңіз бе, бәрі дұрыс па?\n"
           "Мен банктің қауіпсіздік қызметінен хабарласып тұрмын.\n"
           "Сіздің картаңыздан күдікті аударым жасалып жатыр.\n"
           "Ақшаңызды сақтап қалу үшін біз оны қауіпсіз шотқа аударамыз.\n"
           "Қазір сізге SMS-код келеді, соны айтыңызшы.")

with gr.Blocks(title="Сақ бол — scam early warning") as demo:
    gr.Markdown("# Сақ бол · Будь осторожен\nScam early warning for Kazakhstan, in Kazakh, Russian and the mix people actually write. "
                "*Prototype, not financial advice.*")
    with gr.Tab("Хабарлама / Сообщение"):
        inp = gr.Textbox(lines=4, label="Хабарламаны осы жерге қойыңыз / Вставьте сообщение (SMS, WhatsApp, Telegram)")
        ui = gr.Radio(list(LANG_UI), value="Авто / Auto", label="Кеңес тілі / Язык советов")
        btn = gr.Button("Тексеру / Проверить", variant="primary")
        head = gr.HTML(); hl = gr.HighlightedText(label="Неге? / Почему?", color_map={"trigger": "#f5b7b1"}); adv = gr.Markdown()
        btn.click(check_message, [inp, ui], [head, hl, adv])
        gr.Examples(EX_MSG, inp)
    with gr.Tab("Қоңырау / Звонок"):
        call = gr.Textbox(lines=8, label="Қоңырау мәтіні, әр сөйлем жаңа жолда / Текст звонка, каждая реплика с новой строки (if the call were transcribed)", value=EX_CALL)
        cbtn = gr.Button("Әр сөйлемнен кейінгі тәуекел / Риск после каждой реплики", variant="primary")
        plot = gr.LinePlot(x="turn", y="risk (log-odds)", color="line", label="Тәуекел әр сөйлемнен кейін / Риск после каждой реплики"); cmsg = gr.Markdown()
        cbtn.click(check_call, call, [plot, cmsg])

if __name__ == "__main__":
    demo.launch(share=os.environ.get("SAQBOL_SHARE") == "1")
