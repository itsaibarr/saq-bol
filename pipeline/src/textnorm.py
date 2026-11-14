"""Text normalization, language tagging (kk / ru / mixed / kbd / en) and keyboard-Kazakh augmentation.

kbd = Kazakh typed on a Russian keyboard: Kazakh-only letters replaced by Russian look-alikes (қ->к, ү->у ...).
"""
import random
import re

KK_LETTERS = set("әғқңөұүһіӘҒҚҢӨҰҮҺІ")
KBD_MAP = str.maketrans({"ә": "а", "ғ": "г", "қ": "к", "ң": "н", "ө": "о", "ұ": "у", "ү": "у", "һ": "х", "і": "и",
                         "Ә": "А", "Ғ": "Г", "Қ": "К", "Ң": "Н", "Ө": "О", "Ұ": "У", "Ү": "У", "Һ": "Х", "І": "И"})

# Common Kazakh words (proper spelling). Words that are also common Russian words (да, не, бар, банк, код) are left out.
KK_WORDS = set("""
мен сен ол біз сіз сендер олар бұл сол мына осы және бірақ жоқ емес керек қалай қайда неге қашан кім қандай қанша
ғой ғана тек деп дейді екен еді болды болса болып болады жатыр жатырмын келді кел бер беріңіз алу алып айт айтыңыз
жаз жібер жіберіңіз салып рахмет сәлем сәлеметсіз сәлеметсізбе бе ба ме па пе иә ия жақсы жаман үй үйде бүгін ертең кеше
қазір енді тағы өте көп ақша картаңыз картаңызға шот шотқа несие несиені сіздің сенің менің оның біздің қызмет қызметі
қауіпсіздік хабарлама сілтеме сілтемеге өтіңіз басыңыз ұтыс сыйлық апа ата әже аға балам бала жұмыс уақыт сағат күн
жыл туралы үшін дейін кейін бірге сондықтан себебі мүмкін әрине білмеймін білесің түсіндім жарайды болмайды қой ау
құрметті клиент тапсырыс сәлемдеме төлем төлеу ақшаны аудар аударыңыз растау кодты ешкімге айтпаңыз нөмір нөмірім
ауысты тез шұғыл көмектес көмек қайтарамын алаяқ алаяқтар алаяқтық абай болыңыз мұнда сізге саған маған оған бізге
""".split())
RU_WORDS = set("""
и в во на что это как так но я ты он она мы вы они мне тебе вас нас его её их у с со к по за из от до для о об же ли бы
уже еще ещё есть был была было будет нет все всё только если когда где потому чтобы очень можно нужно надо вот тоже
сейчас сегодня завтра здравствуйте привет спасибо пожалуйста ваш ваша вашей ваши вам свой этот эта эти тот кто чем там
тут здесь просто может хорошо ну ладно сразу срочно деньги карта карты карту вашу вашего ваше скажите назовите переведите
короче щас приду подожди давай блин че чё типа вообще потом пока всем кстати сколько почему зачем буду будешь хочу знаю
понял поняла иду пиши напиши скажи сделай говорит говорю могу можешь делать сделать скинь кинь верну
""".split())
KBD_WORDS = {w.translate(KBD_MAP) for w in KK_WORDS if any(c in KK_LETTERS for c in w)} - RU_WORDS
KBD_WORDS |= {"калай", "кайда", "жок", "гой", "ушин", "бугин", "кеше", "сагат", "салем", "салеметсиз", "кызмет", "сиздин", "сизге", "керек"}

# Suffix evidence for words with no Kazakh-only letters (noisy, only used for words of length >= 5).
RU_SUFFIXES = ("ость", "ости", "ние", "ния", "нии", "ция", "ции", "ая", "ое", "ые", "ый", "ий", "ого", "ому", "ыми", "ами",
               "ться", "тся", "ешь", "ете", "ите", "ает", "ают", "ует", "уют", "ишь", "ить", "ать", "ять", "лся", "лась",
               "ным", "ной", "ную", "ных", "ство", "ства", "ться", "ются", "ется")
KK_SUFFIXES = ("лар", "лер", "дар", "дер", "тар", "тер", "ныз", "низ", "мыз", "миз", "сыз", "сиз", "нын", "нин", "дагы",
               "деги", "тагы", "теги", "ганын", "генин", "ымыз", "имиз", "ыныз", "иниз")
UA_WORDS = set("якщо хочеш тобі або більше щодо він вона мене тебе дуже також можу як".split())
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁёӘәҒғҚқҢңӨөҰұҮүҺһІі]+")
PHONE_RE = re.compile(r"(?<!\w)(?:\+?7|8)[\s\-()]*\d{3}[\s\-()]*\d{3}[\s\-]*\d{2}[\s\-]*\d{2}(?!\w)")
CARD_RE = re.compile(r"(?<!\d)(?:\d{4}[\s\-]?){3}\d{4}(?!\d)")
IIN_RE = re.compile(r"(?<!\d)\d{12}(?!\d)")
URL_RE = re.compile(r"(?i)(\[(link|url|ссылка|сілтеме)\]|<url>|h[tx]{2}ps?://\S+|www\.\S+|t\.me/\S+|"
                    r"\b[\w-]+(?:\.[\w-]+)*\.(?:kz|ru|com|net|org|info|online|site|top|xyz|me|io|app|shop|club|pro|biz|cc|su|uz|kg|example|link|vip|live)\b(?:/\S*)?)")
OFFICIAL_RE = re.compile(r"(?i)(?<![\w.\-])(?:https?://)?(?:[a-z0-9]+\.)*(?:kaspi\.kz|kaspi\.me|halykbank\.kz|halyk\.kz|egov\.kz|gov\.kz|bcc\.kz|rbk24\.kz|"
                         r"homecredit\.kz|jusan\.kz|ffin\.kz|freedombank\.kz|forte\.kz|berekebank\.kz|otbasybank\.kz|eubank\.kz|atfbank\.kz|"
                         r"altynbank\.kz|beeline\.kz|kcell\.kz|activ\.kz|tele2\.kz|altel\.kz|kazpost\.kz|post\.kz|nationalbank\.kz|1414\.kz)(?![\w\-]|\.[\w\-])(?:/\S*)?")
MD_RE = re.compile(r"(\*\*|__|`+|^#+\s*)", re.M)


def normalize(text: str) -> str:
    """Same placeholders everywhere (train, test, demo) so the model cannot key on scrubbing artefacts."""
    t = str(text).replace("\u00a0", " ").replace("[.]", ".").replace("(.)", ".")
    t = MD_RE.sub("", t).replace("║", " ")
    t = OFFICIAL_RE.sub(" <url_official> ", t)
    t = URL_RE.sub(lambda m: m.group(0) if m.group(0).strip() == "<url_official>" else " <url> ", t)
    t = CARD_RE.sub("[CARD]", t)
    t = IIN_RE.sub("[IIN]", t)
    t = PHONE_RE.sub("[PHONE]", t)
    return re.sub(r"[ \t]+", " ", t).strip()


def lang_tag(text: str) -> str:
    words = [w.lower() for w in WORD_RE.findall(str(text))]
    if not words:
        return "unk"
    cyr = sum(1 for w in words if re.search(r"[А-Яа-яЁёӘәҒғҚқҢңӨөҰұҮүҺһІі]", w))
    if cyr == 0:
        return "en"
    low = str(text).lower()
    if any(c in low for c in "їєґ") or sum(w in UA_WORDS for w in words) >= 2:
        return "other"
    if any(c in low for c in "өүң") and not any(c in low for c in "әқғұһі"):
        return "other"  # Kyrgyz-like: shares ө ү ң but lacks Kazakh-only letters
    has_kk_letters = any(c in KK_LETTERS for c in str(text))
    kk = kbd = ru = 0.0
    kbd_lex = 0
    for w in words:
        if w in KK_WORDS or any(c in KK_LETTERS for c in w):
            kk += 1
        elif w in KBD_WORDS:
            kbd += 1
            kbd_lex += 1
        elif w in RU_WORDS:
            ru += 1
        elif len(w) >= 5 and w.endswith(RU_SUFFIXES):
            ru += 0.5
        elif len(w) >= 6 and w.endswith(KK_SUFFIXES):
            kbd += 0.5
    kk_total = kk + kbd
    if kk_total == 0 and ru == 0:
        return "kk" if has_kk_letters else "ru"
    share = kk_total / (kk_total + ru)
    if share >= 0.75:
        if has_kk_letters:
            return "kk"
        return "kbd" if (kbd_lex + kk) >= 2 else "ru"
    if share <= 0.25 and not has_kk_letters:
        return "ru"
    if not has_kk_letters and (kbd_lex + kk) < 2:
        return "ru"
    return "mixed"


def to_kbd(text: str, p: float = 0.92, seed: int | None = None) -> str:
    """Keyboard-Kazakh augmentation: replace each Kazakh-only letter with its Russian look-alike with prob p."""
    rng = random.Random(seed)
    return "".join(c.translate(KBD_MAP) if c in KK_LETTERS and rng.random() < p else c for c in str(text))


if __name__ == "__main__":
    for s in ["Сәлеметсіз бе, сіздің картаңызға несие рәсімделді, кодты айтыңыз",
              "Здравствуйте, это служба безопасности Kaspi, назовите код из SMS",
              "Сәлеметсіз бе, это служба безопасности, сіздің картаңыздан подозрительная операция",
              "апа калайсыз, мен гой, номерим ауысты, тез акша салшы",
              "Your parcel is on hold, pay the fee at [LINK]",
              "Позвони мне +7 701 123 45 67, карта 4400 4301 2345 6789"]:
        print(lang_tag(s), "|", normalize(s), "|", to_kbd(s, seed=0)[:60])
