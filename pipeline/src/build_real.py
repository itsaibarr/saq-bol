"""Merge the hand-collected real items, map schemes to the training taxonomy, and split real-dev / real-test.

Split: items are grouped by source page (URL without ?lang=) and by parallel_group, so the same text in two
languages, or two phrases from one list, never straddle dev and test. ~30% of groups -> dev, rest -> test.
Fixed before any model was trained (2026-11-14 ~16:00 UTC+5).
"""
import json, random, re, sys
import pandas as pd
sys.path.insert(0, "pipeline/src")
from textnorm import lang_tag, normalize, to_kbd

SEEN = {  # real scheme name -> canonical scheme that appears in the synthetic training taxonomy
    "account_blocked_phishing": "account_blocked", "card_blocked_phishing_link": "account_blocked",
    "account_verification_phishing": "account_blocked", "fake_bank_security": "fake_bank_security",
    "whatsapp_bank_logo": "fake_bank_security", "pressure_phrase": "fake_bank_security",
    "fake_bonus_payout": "fake_bonus_payout", "fake_prize": "fake_bonus_payout", "fake_prize_giveaway": "fake_bonus_payout",
    "fake_social_payment": "fake_social_payment", "fake_egov_payout": "fake_social_payment",
    "fake_investment_app": "investment_platform", "fake_investment_deepfake": "investment_platform",
    "fake_investment_kmg": "investment_platform", "investment_platform": "investment_platform",
    "fake_job_posting": "fake_job_offer", "fake_loan_approval": "loan_in_your_name",
    "fake_loan_status_link": "loan_in_your_name", "loan_in_your_name": "loan_in_your_name",
    "fake_parcel_delivery": "fake_parcel_delivery", "fake_parcel_kazpost": "fake_parcel_delivery",
    "fake_police_investigation": "fake_police_investigation", "fake_police_knb_investigation": "fake_police_investigation",
    "hacked_account_money_request": "relative_in_trouble", "relative_in_trouble": "relative_in_trouble",
    "relative_in_trouble_voice_clone": "relative_in_trouble", "marketplace_fake_buyer_kolesa": "marketplace_payment_link",
    "marketplace_payment_link": "marketplace_payment_link", "remote_access_app": "tech_support",
    "second_device_screen_share": "tech_support", "safe_account": "safe_account", "sms_code_request": "sms_code_request",
    "sms_code_1414": "sms_code_request", "sms_code_1414_voice_robot": "sms_code_request",
    "fake_telecom_sms_code": "sms_code_request",
}
HELD_OUT_BY_DESIGN = {"meter_replacement", "meter_replacement_biometrics", "fake_egov_ecp_renewal", "fake_utility_meter_registration", "fake_utility_meter", "egov_ecp"}
for _canon, _names in {'drop_card_rental': 'money_mule_recruitment', 'telecom': 'sim_expiry card_sim_expiry fake_mobile_operator fake_family_tariff', 'fake_parcel_delivery': 'fake_delivery_code qr_phishing_delivery fake_parcel_gift fake_relative_parcel_payment fake_delivery_refund', 'investment_platform': 'investment_ad fake_broker_investment pyramid_network real_estate_investment_fraud fake_foreign_property_investment', 'relative_in_trouble': 'account_takeover_vote hacked_account_vote_link hacked_account_malicious_link hacked_account_boss_money_request fake_boss relative_in_trouble_deepfake fake_police_relative_in_trouble', 'fake_bank_security': 'voice_yes_capture voice_bot_biometric_harvest', 'loan_in_your_name': 'fake_bank_security_loan_cancel fake_loan_cancellation account_takeover_loan fake_loan_phishing fake_loan_telegram loan_writeoff_fraud', 'safe_account': 'fake_national_bank_safe_account fake_law_enforcement_safe_account fake_national_bank', 'romance': 'romance', 'mistaken_transfer': 'mistaken_transfer', 'sms_code_request': 'otp_request_messenger whatsapp_code_theft whatsapp_code_takeover account_takeover_code fake_kaspi_manager_1414 fake_clinic_sms_code fake_gift_code_request', 'tech_support': 'fake_antivirus_alert fake_bank_app_update fake_parental_control malicious_apk_photo malicious_link_photo', 'marketplace_payment_link': 'fake_online_seller fake_buyer_payment_link fake_rental fake_cheap_car_sale game_item_prepayment', 'account_blocked': 'account_takeover_fake_security account_security_phishing account_takeover_link account_phishing_link_teens', 'fake_police_investigation': 'fake_police_terror_financing fake_knb fake_police_cash_pickup fake_police_property_transfer', 'fake_bonus_payout': 'prize_advance_fee fake_gift_birthday fake_promo_cashback loan_bonus_lure', 'utility_debt_or_fine': 'fake_tax_declaration fake_tax_notice fake_tax_authority fake_fine fake_traffic_fine', 'fake_census': 'fake_census', 'fake_job_offer': 'job_offer', 'fake_social_payment': 'fake_state_payout pension_withdrawal_fraud fake_pension_fund_seniority'}.items():
    for _n in _names.split():
        SEEN.setdefault(_n, _canon)


for _canon, _names in {'drop_card_rental': 'money_mule_job_offer', 'account_blocked': 'whatsapp_security_phishing', 'marketplace_payment_link': 'fake_rental_ad marketplace_off_platform_payment fake_online_seller_prepayment car_dealer_consignment_fraud', 'safe_account': 'fake_police_safe_account fake_bank_security_safe_account fake_bank_credit_safe_account fake_antifraud_center', 'fake_parcel_delivery': 'fake_courier_delivery fake_courier_sms_code fake_gift_delivery', 'relative_in_trouble': 'fake_boss_colleague hacked_account_message', 'fake_bank_security': 'fake_official_call_opener', 'fake_bonus_payout': 'fake_prize_payout', 'telecom': 'fake_family_tariff_offer'}.items():
    for _n in _names.split():
        SEEN.setdefault(_n, _canon)


def page_key(url):
    return re.sub(r"[?&]lang=\w+", "", str(url)).rstrip("/")


def main():
    import glob as _g
    files = [f for f in ["data/real_test/ru_collected.jsonl", "data/real_test/kk_collected.jsonl",
                         "data/real_test/ru2_collected.jsonl", "data/real_test/kk2_collected.jsonl"] if _g.os.path.exists(f)]
    r = pd.concat([pd.read_json(f, lines=True).assign(round=2 if "2_" in f else 1) for f in files], ignore_index=True)
    r = r.drop_duplicates("text").reset_index(drop=True)
    if "unit" in r:  # round-2 collectors pre-filled unit; recomputed below from text + kind for consistency
        r = r.rename(columns={"unit": "unit_collector"})
    r["text"] = r.text.map(normalize)
    r["tag"] = r.text.map(lang_tag)
    if "evidence" not in r:
        r["evidence"] = None
    r["evidence"] = r.evidence.fillna(r.kind.map(lambda k: "paraphrase" if k == "paraphrase" else "quoted"))
    if "unit_collector" in r:
        r.loc[r.unit_collector == "description", "evidence"] = "paraphrase"
    r["year"] = r.published_date.astype(str).str[:4]
    r["scheme_canon"] = r.scheme.map(lambda s: SEEN.get(s, s))
    r["novel_scheme"] = (r.label == "scam") & ~r.scheme.isin(SEEN)
    r["held_out_by_design"] = r.scheme.isin(HELD_OUT_BY_DESIGN)
    # --- A2: unit of each item (decided from text + kind only, before any trained model existed) ---
    r["n_words"] = r.text.str.split().str.len()
    def unit(x):
        if x.label == "scam":
            if x.evidence == "paraphrase" or x.kind == "paraphrase":
                return "description"
            if x.n_words <= 4:
                return "fragment"
            return "call_phrase" if x.kind == "call_quote" else "message"
        if x.kind in ("sms", "push") or x.scheme in ("bank_app_notification", "delivery_code", "otp_1414", "otp_warning", "tax_debt_reminder", "bank_info"):
            return "notification"
        return "advice_text"
    r["unit"] = r.apply(unit, axis=1)
    r["headline"] = r.unit.isin(["message", "call_phrase"])
    # --- link translations / near-duplicates by LaBSE cosine (A2): pairs = mutual-best kk<->ru >= 0.85, same label ---
    from embed import embed
    import numpy as np
    r["page"] = r.source_url.map(page_key)
    r["pair_id"] = None
    E = embed(r.text.tolist())
    S = E @ E.T
    kk, ru = r.index[r.language == "kk"].values, r.index[r.language == "ru"].values
    sub = S[np.ix_(kk, ru)]
    links = []
    for i, j in enumerate(sub.argmax(1)):
        if sub[:, j].argmax() == i and sub[i, j] >= 0.85 and r.label[kk[i]] == r.label[ru[j]]:
            r.loc[[kk[i], ru[j]], "pair_id"] = f"pair_{r.id[kk[i]]}_{r.id[ru[j]]}"
            links.append((kk[i], ru[j]))
    iu = np.triu_indices(len(r), 1)
    links += [(i, j) for i, j in zip(*iu) if S[i, j] >= 0.90]
    # union-find over page and parallel_group
    parent = list(range(len(r)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i, j in links:
        parent[find(int(i))] = find(int(j))
    for key in [r.page, r.parallel_group]:
        first = {}
        for i, k in enumerate(key):
            if pd.isna(k) or k is None:
                continue
            if k in first:
                parent[find(i)] = find(first[k])
            else:
                first[k] = i
    r["group"] = [find(i) for i in range(len(r))]
    # language-stratified split: fill dev up to ~30% of headline scams per language, ~30% of legit
    groups = list(r.group.unique()); random.Random(2026).shuffle(groups)
    hs = r[r.headline]
    need = {l: 0.3 * (hs.language == l).sum() for l in ["kk", "ru"]}
    need_legit = 0.3 * (r.label == "legit").sum()
    got = {"kk": 0, "ru": 0}; got_legit = 0; dev = set()
    for g in groups:
        sub = r[r.group == g]
        h = sub[sub.headline]
        k_, r_ = (h.language == "kk").sum(), (h.language == "ru").sum()
        l_ = (sub.label == "legit").sum()
        fits = got["kk"] + k_ <= need["kk"] + 2 and got["ru"] + r_ <= need["ru"] + 2 and got_legit + l_ <= need_legit + 3
        useful = (k_ and got["kk"] < need["kk"]) or (r_ and got["ru"] < need["ru"]) or (not len(h) and l_ and got_legit < need_legit)
        if fits and useful:
            dev.add(g); got["kk"] += k_; got["ru"] += r_; got_legit += l_
    r["split"] = r.group.map(lambda g: "real_dev" if g in dev else "real_test")
    import os as _os
    if _os.path.exists("data/processed/real_selfcontained.jsonl"):  # blind annotation, done without model scores
        _t = {json.loads(l)["id"]: json.loads(l)["self_contained"] for l in open("data/processed/real_selfcontained.jsonl")}
        r["self_contained"] = r.id.map(_t)
    if _os.path.exists("data/processed/split_lock.json"):  # A4b: text re-normalized, split/group/pairs kept fixed
        _l = json.load(open("data/processed/split_lock.json"))
        assert set(r.id) == set(_l), "split lock does not cover the same items"
        r["split"] = r.id.map(lambda i: _l[i]["split"]); r["group"] = r.id.map(lambda i: _l[i]["group"]); r["pair_id"] = r.id.map(lambda i: _l[i]["pair_id"])
    r.to_json("data/processed/real_all.jsonl", orient="records", lines=True, force_ascii=False)
    # controlled perturbation: keyboard-Kazakh version of every real Kazakh item (same label, same split)
    kb = r[r.language == "kk"].copy()
    kb["text"] = [to_kbd(t, p=1.0) for t in kb.text]
    kb["language"] = "kbd_perturbed"; kb["id"] = kb.id + "_kbd"
    kb.to_json("data/processed/real_kbd_perturbed.jsonl", orient="records", lines=True, force_ascii=False)
    print(pd.crosstab([r.split, r.unit], r.language))
    print("headline scams by split x lang:"); print(pd.crosstab(r[r.headline].split, r[r.headline].language))
    print("pairs:", r.pair_id.notna().sum() // 2, "| pair labels:", r[r.pair_id.notna()].groupby("label").size().to_dict(), "| pairs split consistent:", r[r.pair_id.notna()].groupby("pair_id").split.nunique().max())
    print("novel scheme scams:", int(r.novel_scheme.sum()), "| held out by design:", int(r.held_out_by_design.sum()))
    print("kbd-perturbed:", len(kb))
    print(pd.crosstab(r.split, r.year))


if __name__ == "__main__":
    main()
