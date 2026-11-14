"""Baseline B1: the official red-flag keyword rule.

Phrases are taken from public warnings (Bank CenterCredit scheme list 2026-09-24, NBK/ARDFM 7-question
anti-fraud questionnaire of 1 Oct 2026, bank "we never ask for your code" notices). Written 2026-11-14
before any real test item was looked at. A message is flagged if it matches at least `min_hits` patterns.
Matching runs on lowercased text with Kazakh letters folded to Russian look-alikes, so keyboard-Kazakh is
not penalised by spelling alone.
"""
import re
from textnorm import KBD_MAP

RED_FLAGS = {
    # asks for codes / secrets
    "code_request": [r"код\w* (из|с) (смс|sms)", r"назов\w+ код", r"продикту\w+ код", r"сообщ\w+ код",
                     r"кодты айт", r"кодты айтын", r"кодты жибер", r"смс.?код", r"cvv", r"cvc", r"пин.?код"],
    # impersonated security / authority
    "security_service": [r"служб\w* безопасност", r"кауипсиздик кызмет", r"финмониторинг", r"кнб", r"ункк",
                         r"следств", r"тергеу", r"следовател", r"прокурат"],
    # safe account / transfer to protect money
    "safe_account": [r"безопасн\w* сч[её]т", r"резервн\w* сч[её]т", r"кауипсиз шот", r"защищ[её]нн\w* сч[её]т"],
    # loan pressure
    "loan_pressure": [r"оформ\w* (на вас )?кредит", r"встречн\w* кредит", r"несие расимдел", r"атыныз\w* несие",
                      r"отмен\w* заявк"],
    # secrecy
    "secrecy": [r"никому не (говор|сообщ|рассказ)", r"ешкимге айтпа", r"ешкимге айтпаныз", r"сохраня\w+ в тайне", r"конфиденциальн"],
    # remote access / app install
    "remote_access": [r"anydesk", r"rustdesk", r"teamviewer", r"установ\w+ приложени", r"скача\w+ приложени", r"косымшаны орнат"],
    # payout / prize lures
    "prize_payout": [r"вы выиграл", r"ваш выигрыш", r"получ\w+ выплат", r"компенсаци", r"утыс", r"сыйлык", r"бонус\w* (зачисл|ждет|ждёт)"],
    # links with urgency
    "link_urgency": [r"(перейд|пройд)\w* по ссылк", r"силтемеге (отиниз|басыныз)", r"срочно", r"шугыл", r"в течение \d+ (час|минут)"],
    # card details
    "card_details": [r"данные карт", r"номер карт\w* и", r"срок действия карт", r"карта\w* деректер", r"реквизит"],
    # drop / easy money
    "easy_money": [r"заработ\w+ от", r"доход от", r"пассивн\w+ доход", r"гарантирован\w+ доход", r"онай акша",
                   r"сдай карт", r"аренд\w* карт", r"картанды жалга"],
}
_COMPILED = {k: [re.compile(p) for p in v] for k, v in RED_FLAGS.items()}


def fold(text: str) -> str:
    return str(text).lower().translate(KBD_MAP).replace("ё", "е")


def hits(text: str) -> dict:
    t = fold(text)
    return {k: [p.pattern for p in ps if p.search(t)] for k, ps in _COMPILED.items() if any(p.search(t) for p in ps)}


def score(text: str) -> float:
    """Number of red-flag categories matched (0..10). Used as a ranking score for PR-AUC."""
    return float(len(hits(text)))


def predict(text: str, min_hits: int = 1) -> int:
    return int(score(text) >= min_hits)
