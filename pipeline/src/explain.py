"""Turn a score into what Gulnara apa sees: band, trigger phrase, red flags and one action in her language.

Trigger phrase = word-window occlusion: drop each window of up to 3 words, re-score, keep the window whose removal
lowers the scam score most. Red flags = official keyword categories (keyword_rule.py, unchanged since B1 was
scored), refined here only for the advice text. Kazakh lines need a native speaker's final check before the demo.
"""
import re
from keyword_rule import fold, hits
from textnorm import lang_tag

FLAG_NAMES = {  # category -> (kk, ru) human-readable red flag
    "code_request": ("SMS-код сұрайды", "просят код из SMS"),
    "security_service": ("«қауіпсіздік қызметі» атынан", "от имени «службы безопасности»"),
    "authority": ("полиция / ҰҚК / тергеуші атынан", "от имени полиции / КНБ / следователя"),
    "safe_account": ("«қауіпсіз шотқа» аударуды сұрайды", "просят перевести на «безопасный счёт»"),
    "loan_pressure": ("несие рәсімдеуге итермелейді", "склоняют оформить кредит"),
    "secrecy": ("«ешкімге айтпаңыз» дейді", "просят «никому не говорить»"),
    "remote_access": ("қосымша орнатуды сұрайды", "просят установить приложение"),
    "prize_payout": ("ұтыс, сыйлық не төлем уәдесі", "обещают выигрыш, приз или выплату"),
    "link_urgency": ("сілтеме және асықтыру", "ссылка и срочность"),
    "card_details": ("карта деректерін сұрайды", "просят данные карты"),
    "investment": ("кепілдендірілген табыс уәдесі", "обещают гарантированный доход"),
    "card_rental": ("картаны жалға беруді ұсынады", "предлагают сдать карту"),
}
ADVICE = {  # category -> (kk, ru): one concrete action
    "code_request": ("Кодты ешкімге айтпаңыз. Банк SMS-кодты ешқашан сұрамайды.", "Никому не называйте код. Банк никогда не спрашивает код из SMS."),
    "security_service": ("Қоңырауды үзіңіз. Банкке картаның артындағы не ресми қосымшадағы нөмір арқылы өзіңіз хабарласыңыз.",
                         "Положите трубку. Сами позвоните в банк по номеру на обороте карты или в официальном приложении."),
    "authority": ("Полиция мен ҰҚК телефонмен ақша, код не несие сұрамайды. Қоңырауды үзіп, 102 нөміріне өзіңіз хабарласыңыз.",
                  "Полиция и КНБ не просят по телефону деньги, коды или кредит. Положите трубку и сами позвоните по номеру 102."),
    "safe_account": ("«Қауіпсіз шот» деген болмайды. Ақшаңызды ешқайда аудармаңыз.", "«Безопасного счёта» не существует. Никуда не переводите деньги."),
    "loan_pressure": ("Ешкімнің нұсқауымен несие алмаңыз. eGov-та «Стоп-кредит» қосыңыз.", "Не берите кредит по чьей-то инструкции. Включите «Стоп-кредит» в eGov."),
    "secrecy": ("«Ешкімге айтпаңыз» деу алаяқтың белгісі. Жақыныңызға қазір хабарласыңыз.", "Просьба «никому не говорить» — признак мошенника. Позвоните близким прямо сейчас."),
    "remote_access": ("Бейтаныс адамның өтінішімен ешқандай қосымша орнатпаңыз.", "Не устанавливайте приложения по просьбе незнакомцев."),
    "prize_payout": ("Нағыз ұтыс не төлем үшін карта деректерін сұрамайды.", "За настоящий выигрыш или выплату не просят данные карты."),
    "link_urgency": ("Сілтемені ашпаңыз. Ресми қосымшаны өзіңіз ашып тексеріңіз.", "Не открывайте ссылку. Проверьте в официальном приложении сами."),
    "card_details": ("Карта деректерін ешкімге бермеңіз.", "Никому не сообщайте данные карты."),
    "investment": ("Табысқа кепілдік беретін компания алаяқ болуы мүмкін. Лицензиясын ҚНРДА не AFSA тізілімінен тексеріңіз.",
                   "Гарантированный доход — признак мошенников. Проверьте лицензию в реестре АРРФР или AFSA."),
    "card_rental": ("Картаңызды басқаға беру не жалға беру заңсыз.", "Передавать или сдавать свою карту другим людям незаконно."),
}
DEFAULT = ("Қоңырауды үзіңіз. Банкке не 102 нөміріне өзіңіз хабарласыңыз.", "Положите трубку. Сами позвоните в банк или по номеру 102.")
BANDS = {"scam": ("Алаяқтық болуы ықтимал", "Похоже на мошенничество"),
         "suspicious": ("Күмәнді", "Подозрительно"),
         "safe": ("Анық белгі табылмады", "Явных признаков не найдено")}
SAFE_NOTE = ("Бірақ код, ақша не несие сұраса, бұл алаяқ.", "Но если просят код, деньги или кредит, это мошенник.")
AUTHORITY_RE = re.compile(r"(кнб|ункк|укк|полиц|следств|следовател|прокурат|тергеу|мвд|иим|мониторинг)")
INVEST_RE = re.compile(r"(доход|инвест|пассивн|прибыл|табыс|пайда)")


def band(p, thr_scam, thr_susp):
    return "scam" if p >= thr_scam else ("suspicious" if p >= thr_susp else "safe")


def categories(text):
    cats = list(hits(text).keys())
    t = fold(text)
    out = []
    for c in cats:
        if c == "security_service" and AUTHORITY_RE.search(t):
            c = "authority"
        if c == "easy_money":
            c = "investment" if INVEST_RE.search(t) else "card_rental"
        if c not in out:
            out.append(c)
    return out


def trigger(text, score_fn, max_window=3):
    words = text.split()
    if len(words) <= 1:
        return text, 0.0
    base = float(score_fn([text])[0])
    cands, spans = [], []
    for w in range(1, min(max_window, len(words)) + 1):
        for i in range(0, len(words) - w + 1):
            cands.append(" ".join(words[:i] + words[i + w:])); spans.append((i, i + w))
    drops = base - score_fn(cands)
    i, j = spans[int(drops.argmax())]
    return " ".join(words[i:j]), float(drops.max())


def explain(text, score_fn, thr_scam, thr_susp, ui_lang="auto"):
    p = float(score_fn([text])[0])
    lang = lang_tag(text)
    li = {"kk": 0, "ru": 1}.get(ui_lang, 1 if lang in ("ru", "en", "other", "unk") else 0)
    b = band(p, thr_scam, thr_susp)
    cats = categories(text)
    phrase, drop = trigger(text, score_fn) if b != "safe" else ("", 0.0)
    if b == "safe":
        advice = [SAFE_NOTE[li]]
    else:
        advice = [ADVICE[c][li] for c in cats[:2]] or [DEFAULT[li]]
    return {"score": p, "band": b, "band_text": BANDS[b][li], "language": lang, "trigger": phrase, "trigger_drop": drop,
            "red_flags": [FLAG_NAMES[c][li] for c in cats] if b != "safe" else [], "red_flag_keys": cats if b != "safe" else [], "advice": advice}
