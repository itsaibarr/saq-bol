"""Rule-based generator of LEGIT service notifications (bank SMS/push, OTP, eGov, delivery, telecom, civil defence).

Why: the e5-large model flagged real bank SMS (OTP codes, transfers, top-ups) as scams, because LLM-written legit
examples did not look like real notifications. Written after inspecting real-DEV false alarms (real-test
notifications were never opened); near-copies of any real item are removed later by the leakage filter.
Output: data/processed/notif_synth.jsonl (label 0, synthetic, source "notif_gen").
"""
import json, random
R = random.Random(2026)
BANKS = ["Kaspi", "Kaspi.kz", "Halyk", "Halyk Bank", "Freedom", "Jusan", "BCC", "Forte", "Home Credit", "Bereke", "RBK", "Eurasian", "Otbasy", "ATF", "Altyn"]
MERCH = ["SMALL", "MAGNUM", "GALMART", "ANVAR", "Wildberries", "OZON", "KASPI MAGAZIN", "SULPAK", "TECHNODOM", "YANDEX GO", "GLOVO", "WOLT",
         "APTEKA PLUS", "SPOTIFY", "NETFLIX.COM", "STEAM", "AIR ASTANA", "SCAT", "KTZ", "BURGER KING", "COFFEE BOOM", "ASTANA ENERGY", "ALSECO"]
NAMES = ["Айгерим К.", "Нурлан С.", "Дана Б.", "Ерлан Т.", "Мадина А.", "Алексей П.", "Асель Ж.", "[NAME]"]
CITIES = ["ASTANA", "ALMATY", "SHYMKENT", "KARAGANDA", "AKTOBE", "PAVLODAR"]


def amt():
    a = R.choice([R.randint(100, 9999), R.randint(1000, 99999), R.randint(10000, 500000)])
    return R.choice([f"{a:,}".replace(",", " "), str(a), f"{a}.00", f"{a:,}.{R.randint(0, 99):02d}".replace(",", " ")])


def code(n=None):
    n = n or R.choice([4, 4, 6])
    return str(R.randint(10 ** (n - 1), 10 ** n - 1))


def cur():
    return R.choice(["₸", "тг", "KZT", "т", "тенге"])


def card():
    return R.choice([f"*{R.randint(1000, 9999)}", f"**{R.randint(1000, 9999)}", f"{R.randint(1000, 9999)}", f"ECMC{R.randint(1000, 9999)}", f"VISA{R.randint(1000, 9999)}"])


def date():
    return f"{R.randint(1, 28):02d}.{R.randint(1, 12):02d}.{R.choice(['25', '26', '2025', '2026'])}"


def tm():
    return f"{R.randint(0, 23):02d}:{R.randint(0, 59):02d}"


def hashcode():
    return "".join(R.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for _ in range(11))


RU = [
    lambda: f"Код: {code()}. Никому не сообщайте код, даже сотрудникам банка.",
    lambda: f"{R.choice(BANKS)}: код подтверждения {code()}. Не сообщайте его никому!",
    lambda: f"<#>Вы переводите {amt()}{cur()} на {R.choice(NAMES)}. Код:{code()} {hashcode()}",
    lambda: f"Код:{code()} Вы переводите {amt()}{cur()}. НИКОМУ НЕ ГОВОРИТЕ КОД!",
    lambda: f"Код для входа в {R.choice(BANKS)}: {code(6)}. Если это не вы, не вводите код.",
    lambda: f"Покупка {amt()} {cur()} {R.choice(MERCH)} {R.choice(CITIES)}. Доступно {amt()} {cur()}",
    lambda: f"Пополнение {amt()} {cur()}. Баланс {amt()} {cur()}",
    lambda: f"Вы перевели: {amt()} {cur()} {R.choice(NAMES)}",
    lambda: f"Перевод: {amt()}{cur()} Доступно: {amt()}{cur()} Детали: Оплата кредита {R.choice(BANKS)}",
    lambda: f"По карточке {card()} поступил возврат {amt()} KZT по операции от {date()} {tm()} {R.choice(MERCH)}, {R.choice(CITIES)}, KZ",
    lambda: f"Платеж: {amt()}{cur()} Категория: {R.choice(['Мобильная связь', 'Коммунальные услуги', 'Интернет', 'Транспорт'])} По счёту: {card()} Доступно: {amt()} {cur()}",
    lambda: f"-{amt()} {cur()} Вы внесли платеж по кредиту. Оплата принята",
    lambda: f"Задолженность полностью погашена {amt()} {cur()} Доступно: {amt()} {cur()}",
    lambda: f"Превышен лимит на покупки в интернете. Попытка оплаты: {R.randint(5, 500)}.{R.randint(0, 99):02d} USD {R.choice(MERCH)} Лимит: {amt()} {cur()}",
    lambda: f"Операция отклонена: недостаточно средств. {R.choice(MERCH)} {amt()} {cur()}",
    lambda: f"Карта {card()} заблокирована по вашему запросу. Разблокировать можно в приложении {R.choice(BANKS)}.",
    lambda: f"Ваша карта готова. Заберите её в отделении {R.choice(BANKS)} с удостоверением личности.",
    lambda: f"Напоминаем: платеж по кредиту {amt()} {cur()} до {date()}. Оплатить можно в приложении {R.choice(BANKS)}.",
    lambda: f"Зачислена заработная плата {amt()} {cur()}. Доступно {amt()} {cur()}",
    lambda: f"Код для подтверждения на eGov: {code(6)}. Никому не сообщайте этот код.",
    lambda: f"Ваша заявка на услугу «{R.choice(['Справка о несудимости', 'Регистрация по месту жительства', 'Пособие при рождении', 'Замена удостоверения'])}» принята. Номер {R.randint(100000, 999999)}",
    lambda: "Не беспокойтесь. Проводится проверка системы оповещения населения",
    lambda: f"Штормовое предупреждение: {date()} в {R.choice(['Астане', 'Алматы', 'Караганде'])} ожидается {R.choice(['сильный ветер', 'гололед', 'метель'])}. Будьте осторожны.",
    lambda: f"Ваш заказ №{R.randint(10000000, 99999999)} доставлен в постамат по адресу {R.choice(['ул. Кенесары 40', 'пр. Абая 12', 'ТРЦ Mega'])}. Код получения: {code()}",
    lambda: f"Kaspi Доставка: курьер привезёт заказ {date()} с {tm()} до {tm()}.",
    lambda: f"Ваш баланс {amt()} тг. Пополните счёт, чтобы оставаться на связи.",
    lambda: f"Подключён тариф «{R.choice(['Супер', 'Безлимит', 'Семейный', 'Онлайн'])}». Абонентская плата {amt()} тг в месяц.",
    lambda: "O-CITY. Оплата проезда по Kaspi QR. Покажите QR-код контролёру",
    lambda: f"Запись к врачу подтверждена: {date()} в {tm()}, кабинет {R.randint(100, 450)}. Поликлиника №{R.randint(1, 15)}",
    lambda: f"Счёт за электроэнергию за {R.choice(['октябрь', 'ноябрь', 'сентябрь'])}: {amt()} тг. Оплатить до {date()}.",
]
KK = [
    lambda: f"Растау коды: {code()}. Кодты ешкімге айтпаңыз.",
    lambda: f"{R.choice(BANKS)}: бір реттік код {code()}. Оны ешкімге, тіпті банк қызметкеріне де бермеңіз.",
    lambda: f"Шотыңызға {amt()} {cur()} түсті. Қолжетімді: {amt()} {cur()}",
    lambda: f"Сатып алу {amt()} {cur()} {R.choice(MERCH)}. Қалдық {amt()} {cur()}",
    lambda: f"{amt()} {cur()} аударым жасалды. Алушы: {R.choice(NAMES)}",
    lambda: f"Еске саламыз: {date()} дейін несие бойынша {amt()} {cur()} төлеу қажет. Төлемді {R.choice(BANKS)} қосымшасында жасауға болады.",
    lambda: f"eGov растау коды: {code(6)}. Кодты ешкімге айтпаңыз.",
    lambda: f"Сіздің өтінішіңіз қабылданды. Өтінім нөмірі {R.randint(100000, 999999)}",
    lambda: "Алаңдамаңыз. Халықты хабардар ету жүйесі тексерілуде",
    lambda: f"Тапсырысыңыз {date()} күні жеткізіледі. Алу коды: {code()}",
    lambda: f"Карта {card()} сіздің өтінішіңіз бойынша бұғатталды.",
    lambda: f"Жалақы түсті: {amt()} {cur()}",
    lambda: f"Дәрігерге жазылуыңыз расталды: {date()}, сағат {tm()}.",
    lambda: f"Балансыңыз {amt()} тг. Байланыста болу үшін шотыңызды толтырыңыз.",
    lambda: f"Картаңыз дайын. Оны {R.choice(BANKS)} бөлімшесінен жеке куәлігіңізбен алыңыз.",
]
TR = [  # transliterated Latin, as some banks and phones send
    lambda: f"NIKOMU NE SOOBSHAITE 3D-kod {code()} Summa {amt()} KZT ({R.choice(MERCH)})",
    lambda: f"{card()} Karazhattyn kolma-kol emes turde audaru/Beznalichny perevod sredstv. {amt()} KZT; INTERNET BANKING;",
    lambda: f"Kod podtverzhdeniya: {code()}. Nikomu ne soobshayte.",
    lambda: f"Pokupka {amt()} KZT {R.choice(MERCH)} {R.choice(CITIES)}. Dostupno {amt()} KZT",
    lambda: f"Rastau kody: {code()}. Eshkimge aitpanyz.",
    lambda: f"Popolnenie {amt()} KZT. Balans {amt()} KZT",
]
KK += [
    lambda: f"{R.choice(BANKS)}: {amt()} {cur()} аударым түсті. Жіберуші: {R.choice(NAMES)}",
    lambda: f"Төлем қабылданды: {amt()} {cur()}. Санат: {R.choice(['Ұялы байланыс', 'Коммуналдық қызметтер', 'Интернет'])}",
    lambda: f"Несие бойынша төлем қабылданды: {amt()} {cur()}. Рахмет!",
    lambda: f"Картаңыздан {amt()} {cur()} шешілді, {R.choice(MERCH)}. Қалдық: {amt()} {cur()}",
    lambda: f"Kaspi Gold: {amt()} {cur()} толықтырылды",
    lambda: f"Депозитке сыйақы есептелді: {amt()} {cur()}",
    lambda: f"Қосымшаға кіру коды: {code()}. Егер бұл сіз болмасаңыз, кодты енгізбеңіз.",
    lambda: f"ХҚКО: құжатыңыз дайын. Алу үшін жеке куәлікпен келіңіз.",
    lambda: f"Сіздің {R.choice(['анықтамаңыз', 'өтінішіңіз', 'құжатыңыз'])} eGov жеке кабинетінде қолжетімді.",
    lambda: f"Сәлемдемеңіз {R.choice(['№' + str(R.randint(100000, 999999)), ''])} бөлімшеге келді. Алу коды: {code()}",
    lambda: f"Жаңа тариф қосылды. Ай сайынғы төлем {amt()} тг.",
    lambda: f"Ескерту: {date()} күні {R.choice(['қатты жел', 'көктайғақ', 'боран'])} күтіледі. Сақ болыңыз.",
]
def _stack():
    pairs = [(f"Растау коды: {{c}}. Кодты ешкімге айтпаңыз.", f"Код подтверждения: {{c}}. Никому не сообщайте."),
             (f"Шотыңызға {{a}} ₸ түсті.", f"Пополнение счёта на {{a}} ₸."),
             (f"Несие бойынша төлем {{d}} дейін.", f"Платёж по кредиту до {{d}}.")]
    kk, ru = R.choice(pairs)
    vals = {"c": code(), "a": amt(), "d": date()}
    return kk.format(**vals) + "\n" + ru.format(**vals)
MIX = [_stack]
rows = []
for lang, pool, n in [("ru", RU, 3200), ("kk", KK, 1900), ("other", TR, 600), ("mixed", MIX, 300)]:
    seen = set()
    while len([r for r in rows if r["language"] == lang]) < n:
        t = R.choice(pool)()
        u = R.random()
        if u < 0.12:
            t += R.choice([" Справки: [PHONE]", " Анықтама: [PHONE]", " Call-центр: [PHONE]", " Тел.: [PHONE]"])
        elif u < 0.26:
            t += R.choice([" kaspi.kz", " halykbank.kz", " egov.kz", " bcc.kz", " jusan.kz", " homecredit.kz", " beeline.kz", " post.kz"])
        if t not in seen:
            seen.add(t); rows.append({"text": t, "label": "legit", "language": lang, "source": "notif_gen", "synthetic": True})
with open("data/processed/notif_synth.jsonl", "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows), {l: sum(r["language"] == l for r in rows) for l in ["ru", "kk", "other", "mixed"]})


# ---- Scam twins (council round 2): same notification formats, but the ASK is a scam action. Built from the scheme
# taxonomy (code to a caller, link + card data, safe account, fake fee, remote app), not from dev items.
RU_S = [
    lambda: f"Код: {code()}. Сообщите его сотруднику службы безопасности, который вам звонит, чтобы отменить операцию.",
    lambda: f"{R.choice(BANKS)}: на ваше имя оформляется кредит {amt()} {cur()}. Если это не вы, введите код {code()} по ссылке <url>",
    lambda: f"<#>Вы переводите {amt()}{cur()} на защищённый счёт. Продиктуйте код:{code()} оператору {hashcode()}",
    lambda: f"Покупка {amt()} {cur()} {R.choice(MERCH)} не подтверждена. Для отмены перейдите по ссылке <url> и введите данные карты",
    lambda: f"Карта {card()} заблокирована. Для разблокировки позвоните по номеру [PHONE] и назовите код из SMS",
    lambda: f"Задолженность {amt()} {cur()} будет передана в суд. Оплатите сегодня по ссылке <url>",
    lambda: f"Зачисление {amt()} {cur()} ожидает подтверждения. Установите приложение для получения: <url>",
    lambda: f"Код для подтверждения на eGov: {code(6)}. Сообщите его специалисту ЦОН, который вам перезвонит.",
    lambda: f"Ваш заказ №{R.randint(10000000, 99999999)} задержан на таможне. Оплатите сбор {amt()} тг по ссылке <url>",
    lambda: f"Срок действия SIM-карты истекает. Для продления назовите код {code()} сотруднику оператора.",
    lambda: f"Вам начислена выплата {amt()} {cur()}. Для получения введите номер карты и CVV: <url>",
    lambda: f"{R.choice(BANKS)}: подозрительная операция {amt()} {cur()}. Переведите средства на резервный счёт до выяснения.",
    lambda: f"Зарплата {amt()} {cur()} не может быть зачислена. Подтвердите данные карты по ссылке <url>",
]
KK_S = [
    lambda: f"Растау коды: {code()}. Операцияны тоқтату үшін кодты сізге қоңырау шалған банк қызметкеріне айтыңыз.",
    lambda: f"Сіздің атыңызға {amt()} {cur()} несие рәсімделуде. Тоқтату үшін кодты <url> сілтемесіне енгізіңіз.",
    lambda: f"Шотыңыздағы {amt()} {cur()} қауіпсіз шотқа аударылуы керек. Кодты операторға айтыңыз: {code()}",
    lambda: f"Картаңыз бұғатталды. Ашу үшін [PHONE] нөміріне хабарласып, SMS-кодты айтыңыз.",
    lambda: f"Сізге {amt()} {cur()} төлем есептелді. Алу үшін карта деректерін енгізіңіз: <url>",
    lambda: f"Тапсырысыңыз кідіртілді. {amt()} тг кеден алымын <url> арқылы төлеңіз.",
    lambda: f"eGov растау коды: {code(6)}. Кодты сізге хабарласқан ХҚКО маманына айтыңыз.",
    lambda: f"Күдікті операция: {amt()} {cur()}. Ақшаңызды сақтау үшін оны резервтік шотқа аударыңыз.",
    lambda: f"Жалақыңыз түспей тұр. Карта деректерін <url> сілтемесі арқылы растаңыз.",
]
TR_S = [
    lambda: f"Kod podtverzhdeniya: {code()}. Soobshite ego operatoru dlya otmeny operacii.",
    lambda: f"Rastau kody: {code()}. Kodty bank kyzmetkerine aitynyz.",
    lambda: f"Vasha karta {card()} zablokirovana. Pereidite po ssylke <url> i vvedite dannye karty",
]
twins = []
for lang, pool, n in [("ru", RU_S, 1300), ("kk", KK_S, 900), ("other", TR_S, 300)]:
    seen = set()
    while len([r for r in twins if r["language"] == lang]) < n:
        t = R.choice(pool)()
        if t not in seen:
            seen.add(t); twins.append({"text": t, "label": "scam", "language": lang, "source": "notif_scam_twin", "synthetic": True})
with open("data/processed/notif_scam_twins.jsonl", "w") as f:
    for r in twins:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("scam twins", len(twins))
