# 10 — AI + Health track: evidence, gaps, candidate projects

Researched 2026-11-14. Every number below has a URL. "Accessed" = 2026-11-14 unless stated. Figures I computed myself from a primary file are labelled "(computed)".

---

## 0. Bottom line

**Recommend C1: "Hidden heart disease from a routine ECG". It helps a rural Kazakh GP decide who gets one of the few echocardiography slots, using the EchoNext-Mini dataset (100,000 ECGs with echo-confirmed labels, released 2025/2026, NEJM AI 2026).**

Why it wins:
- It matches a Kazakhstan Ministry of Health plan announced in January 2026: early detection of chronic heart failure with a "Smart ECG" system in clinics that have no functional-diagnostics staff.
- Its labels come from echocardiograms, not from ECG text, so it catches disease *sooner*, which is exactly the track's wording.
- It has age, sex and race/ethnicity columns, so the subgroup-fairness analysis the judges ask for comes built in.
- Almost nobody uses it yet. The Kaggle mirror has 6 downloads, against 715k for the pneumonia X-ray set.
- A published benchmark exists to compare against honestly (AUROC 82.0).

**Fallback:** C2, fully open data with no DUA (PTB-XL → CODE-15%). Use it if a team member cannot register or sign the PhysioNet data use agreement.

**Highest-scoring LLM option:** C4. It fits Yanshan Wang's own 2026 work best, but it relies on synthetic data.

---

## 1. Where AI works in health (2024–2026), where it fails, and the gaps

### Works (trial or deployment evidence)
| Area | Evidence | Source |
|---|---|---|
| Mammography screening | MASAI RCT (Sweden, ~106k women). AI-supported screening was non-inferior on interval cancers: 1.55 vs 1.76 per 1,000 (82 vs 93); sensitivity 80.5% vs 73.8% at the same specificity. Earlier analysis: 44% less screen-reading workload. | Lancet 2026;407:505–514, doi:10.1016/S0140-6736(25)02464-X (https://pubmed.ncbi.nlm.nih.gov/41620232/); figures per Lund Univ. release https://www.lunduniversity.lu.se/article/ai-support-breast-cancer-screening-fewer-missed-cancer-cases |
| AI-ECG, hospital | Pragmatic RCT, 15,965 patients, 39 physicians. An AI-ECG mortality alert cut 90-day all-cause mortality from 4.3% to 3.6% (HR 0.83, 0.70–0.99). | Lin et al., Nat Med 2024;30:1461, https://pubmed.ncbi.nlm.nih.gov/38684860/ |
| AI-ECG → structural heart disease | EchoNext (Nature 2025) was trained on >1M ECG–echo pairs; internal AUROC ≈0.85, ~77% of SHD flagged vs ~64% by cardiologists in a reader study. EchoNext-Mini (NEJM AI, Apr 2026): 100k ECGs public; baseline AUROC 82.0, sens 70.1, spec 77.9. | Nature doi:10.1038/s41586-025-09227-0; NEJM AI doi:10.1056/AIdbp2500516 (https://pubmed.ncbi.nlm.nih.gov/42932679/) |
| TB chest X-ray CAD | WHO-recommended for screening since 2021. WHO 2025 policy statement on independently evaluated CAD products. | https://www.who.int/publications/i/item/9789240110373 |
| Regulatory volume | FDA AI-enabled device list (update to 29 Jun 2026): **1,614 devices**. Radiology 1,230 (76%), cardiovascular 154 (9.5%), ophthalmic 10. 335 cleared in 2025. **Zero** devices for cough, TB, dementia/cognition or speech. (computed) | CSV https://www.fda.gov/media/178541/download, page https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices |
| Kazakhstan deployments | Cerebra stroke-CT AI in 9 stroke centres, with thrombolysis use reported +40%. WDsoft radiology AI in 190 facilities. Planned: Smart ECG for early chronic heart failure detection, "remote interpretation of ECGs in clinics that lack specialized functional diagnostics staff". ALIMA assistant in 700+ clinics. Government/press figures, not independently verified. | MoH 10 Mar 2026 https://www.gov.kz/memleket/entities/dsm/press/news/details/1177761?lang=ru ; Times of Central Asia 26 Jan 2026 https://timesca.com/kazakhstan-to-expand-use-of-ai-for-early-detection-of-strokes-and-cancer/ |

### Fails or unproven
| Problem | Evidence | Source |
|---|---|---|
| LLMs advising the public | RCT with 1,298 people. LLMs alone identified conditions in 94.9% of cases, but people *using* them did so in <34.5% (disposition <44.2%), **no better than control**. Benchmarks did not predict this. | Bean et al., Nat Med 2026;32:609, https://pubmed.ncbi.nlm.nih.gov/41663592/ |
| Regulatory ≠ validated | 226 of 521 FDA-authorised AI devices (43%) had no published clinical validation; only 22 had RCTs. | Chouffani El Fassi et al., Nat Med 2024, https://pubmed.ncbi.nlm.nih.gov/39187696/ |
| Few trials | Only 86 RCTs of AI in clinical practice worldwide; mostly single-centre, imaging-heavy, 81% report positive results (publication bias). | Han et al., Lancet Digit Health 2024, https://pubmed.ncbi.nlm.nih.gov/38670745/ |
| Cough-sound TB AI | CODA TB DREAM (2,143 patients, 7 countries): cough-only AUROC 0.69–0.74; with clinical data 0.78–0.83. Best cough-only model reached 55.5% specificity at 80% sensitivity, below the WHO target product profile. WHO will only evaluate cough AI at a late-2026 guideline meeting. | Jaganath et al., OFID 2025 doi:10.1093/ofid/ofaf572; WHO call for data https://www.who.int/news-room/articles-detail/public-call-for-data-to-inform-who-policy-updates-on-tools-for-screening-for-tb-disease |
| GenAI patient education | "Generative AI is not ready for clinical use in patient education … even with RAG" (Wang group). | AMIA Summits 2025, https://pubmed.ncbi.nlm.nih.gov/40502233/ |
| Synthetic → real images | PhysioNet Challenge 2024 (ECG images). Training images were synthetic and the hidden test set held real photos/scans. Top classification F1 was 0.817, while many teams collapsed (e.g., F1 0.08). | https://moody-challenge.physionet.org/2024/ , https://moody-challenge.physionet.org/2024/results |
| Kazakhstan | A 2026 scoping review (11 studies) found AI use in Kazakhstan diagnostics still limited, especially in rural areas (infrastructure, skills). | West Kazakhstan Med J 2026, doi:10.4103/wkmj.wkmj_75_26 (abstract via https://www.citedrive.com/en/discovery/a-scoping-review-of-artificial-intelligence-applications-for-diagnostic-accuracy-in-kazakhstans-healthcare-system/) |

### Gaps a 30-hour project can credibly address
1. **External validation and dataset shift.** Most models are tested only on their home dataset. Training on one country and testing on another is both cheap and valued.
2. **Subgroup reporting.** Sex, age and race/ethnicity breakdowns are rarely reported. The judges explicitly ask for them.
3. **Prevalence shift and decision thresholds.** Enriched research datasets inflate PPV. Re-computing PPV at realistic screening prevalence, and choosing thresholds by capacity (e.g., echo slots), ties the model to an actual decision.
4. **Low-resource languages.** I found no Kazakh-language medical dataset on Hugging Face (searched 2026-11-14). Kazakh LLMs exist (ISSAI KazLLM; Qwen3.5-Kazakh), but no one has evaluated them on health tasks.
5. **Human-facing reliability.** Bean 2026 shows that model-alone accuracy does not transfer to users. Designing for a trained intermediary (GP or feldsher) rather than the public is the evidence-backed choice.

---

## 2. Problem size

### Global
- CVD: **19.8M deaths in 2022 (32% of all deaths)**, >75% in low- and middle-income countries. WHO fact sheet, 31 Jul 2025, https://www.who.int/news-room/fact-sheets/detail/cardiovascular-diseases-(cvds)
- TB: **10.6M fell ill, 1.13M died in 2025**. WHO fact sheet, 12 Nov 2026, https://www.who.int/news-room/fact-sheets/detail/tuberculosis
- Anaemia: 30.7% of women 15–49 (35.5% of pregnant women), 2023. WHO GHO `NUTRITION_ANAEMIA_REPRODUCTIVEAGE_PREV`, https://ghoapi.azureedge.net/api/
- Suicide: 9.2/100k (2023). WHO GHO `SDGSUICIDE`

### Kazakhstan (population 20.84M, 37.6% rural, World Bank 2025: https://api.worldbank.org/v2/country/KAZ/indicator/SP.RUR.TOTL.ZS)
| Burden | Number | Source |
|---|---|---|
| Deaths 2024 | 132.9k. Circulatory **22.3%**, nervous system 19.1%, neoplasms 10.2%, respiratory 10.0%. Under-5 deaths 3,404; infant mortality 6.8/1,000. | Bureau of National Statistics, 12 Mar 2025, https://stat.gov.kz/en/industries/social-statistics/demography/publications/328609/ |
| Premature NCD death (30–69) | 19.5% overall; **men 26.9%** vs global men 21.1% (2023) | WHO GHO `NCDMORT3070` |
| Hypertension | **42%** prevalence (30–79 y), only **30.5% controlled** (2019) | WHO GHO `NCD_HYP_PREVALENCE_A`, `NCD_HYP_CONTROL_A` |
| Diabetes | 10.2% of adults 18+ (age-standardised, 2022) | WHO GHO `NCD_DIABETES_PREVALENCE_AGESTD` |
| Heart failure | **526,766 adults** with HF in national e-health records 2014–19; 35% rural; all-cause mortality rose 336 → 975 per million; male HR 1.35 | Zhakhina et al., Eur J Public Health 2025, https://pmc.ncbi.nlm.nih.gov/articles/PMC12196695/ |
| Heart failure trend | 87,260 CHF patients examined in 2024 (+19% vs 2023) — Russian-language abstract, treat as indicative | Nauka i Zdravookhranenie 2025, https://newjournal.ssmu.kz/upload/iblock/dd8/9hw2ni9adq3vodadqs1dtxw38pspctqr/7_15_3_27_2025.pdf |
| Myocardial infarction | 79,172 first-ever AMI 2014–19; 33% rural; 30-day mortality 9%; AMI mortality 101 → 210 per million | Frontiers Cardiovasc Med 2023, https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2023.1127320/full |
| TB / MDR-TB (2024 est.) | Incidence 45/100k (9,200 cases). **Rifampicin resistance in 33% of new and 55% of previously treated cases**; 3,600 MDR/RR-TB. Neighbours: KGZ 22%, UZB 21%, TJK 23%, TKM 35% of new cases. (computed from WHO CSVs) | https://extranet.who.int/tme/generateCSV.asp?ds=mdr_rr_estimates and ds=estimates |
| TB genomics, local | Astana L2/Beijing isolates: genotypic prediction matched phenotype for every drug **except bedaquiline** | Antibiotics 2023, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10604462/ ; Almaty WGS 2023–24: 29% MDR among 272 isolates, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12479430/ |
| Measles | 13,677 cases in 2023 (>639/million, highest incidence in WHO European Region); 28,147 in 2024 (2nd in region) | WHO/Europe https://www.who.int/europe/news/item/23-01-2024-kazakhstan-responds-to-rapid-escalation-of-measles-cases ; WHO/UNICEF Mar 2025 via https://www.developmentaid.org/api/frontend/cms/file/2025/03/European-Region-reports-highest-number-of-measles-cases-in-more-than-25-years.pdf |
| Air pollution | 11,575 deaths attributable to ambient air pollution (2021). National mean PM2.5 16.5 µg/m³ (2023) vs WHO guideline 5. Almaty: **2,108 ± 144 PM2.5-attributable deaths/yr (2022–24)**. | WHO GHO `AIR_41`, `SDGPM25`; Env. Sci.: Advances 2026, https://pubs.rsc.org/en/content/articlehtml/2026/va/d5va00194c |
| Suicide | 15.5/100k (men 26.1) vs global 9.2 (men 12.9), 2023 | WHO GHO `SDGSUICIDE` |
| Anaemia | 30.5% of women 15–49; 32.3% of pregnant women (2023) | WHO GHO |
| Maternal mortality | 10/100k live births (2023); spiked to 23 in 2021 | WHO GHO `MDG_0000000026` |

**Open Kazakhstan data:** stat.gov.kz open data (aggregate only); WHO GHO API; WHO TB CSVs; OpenAQ for Almaty and Astana. **There are no open patient-level Kazakh clinical datasets**, so local relevance has to come from the user, the language and the decision rather than from local training data.

---

## 3. The "generic" projects other teams will build (avoid)
Kaggle all-time downloads (Kaggle API, accessed 2026-11-14) show where the crowd goes:
| Generic project | Dataset (downloads) |
|---|---|
| Pneumonia X-ray CNN (brief 4.1.1) | paultimothymooney/chest-xray-pneumonia (**715,419**) |
| Breast cancer tabular | uciml/breast-cancer-wisconsin-data (574,127) |
| Stroke / heart-failure tabular (≈ brief 4.1.2) | fedesoriano/stroke-prediction-dataset (316,759); heart-failure-prediction (289,382) |
| Skin cancer CNN | kmader/skin-cancer-mnist-ham10000 (299,065) |
| Brain-tumour MRI CNN | masoudnickparvar/brain-tumor-mri-dataset (222,160) |
| Diabetes indicators | alexteboul/diabetes-health-indicators-dataset (167,899); Pima |
| ECG beats (MIT-BIH) | shayanfazeli/heartbeat (143,586) |
| Malaria cells | iarunava/cell-images-for-detecting-malaria (85,477) |
| Fetal health (tabular CTG) | andrewmvd/fetal-health-classification (56,667) |
| TB X-ray | tawsifurrahman/tuberculosis-tb-chest-xray-dataset (45,317) |
| Diabetic retinopathy | APTOS / resized EyePACS (~38k each) |
| "Symptom-checker / mental-health chatbot" wrapping ChatGPT/Gemini | — Bean 2026 shows these do not help the public |
| Country-level risk from WHO/OWID (brief 4.1.3) | — |

**Less-used datasets in this report:** PTB-XL mirror 71,717 (moderately used). EchoNext waveforms mirror: **6** downloads. CRyPTIC: no Kaggle presence. Eyes-defy-anemia mirror: 5,610.

---

## 4. Judge fit (what each judge will find credible)

**Niranjani Prasad**, Senior Researcher, Microsoft Research Cambridge (https://www.microsoft.com/en-us/research/people/niprasa/):
- Princeton PhD on RL for ICU decisions: optimal lab-test ordering (PSB 2019) and electrolyte repletion (J Pers Med 2022).
- Project Talia: deep learning to predict iCBT outcomes (PLOS One 2023).
- Microsoft Immunomics: immune-repertoire sequencing for diagnosis.
- 2026 work: reliable reasoning in generative AI (ICLR 2026; arXiv agents paper). Publications: https://www.microsoft.com/en-us/research/people/niprasa/publications/

→ She will reward decision-focused evaluation (thresholds tied to an action or capacity), calibration and uncertainty, "when to test" framing, honest failure analysis, and sequence/genomic ML done carefully.

**Yanshan Wang**, CAIO of Arecibo AI; Assoc. Prof., Pitt DBMI; director of PittNAIL and the Center for Clinical NLP (https://sites.pitt.edu/~yaw89/).

**Arecibo AI** (founded 2024, https://arecibo.ai/about.html):
- **Arecibo ARC**, a conversational AI companion app for older adults with cognitive impairment that turns life stories into health insights for caregivers.
- **AI-as-a-Service**: NLP, human-in-the-loop agents, operational decision tech, ML resource allocation, forecasting, synthetic data, smart medical devices.
- Positioning: "verifiable, regulation-ready systems."

Wang's 2025–26 papers (PubMed):
- **CPGPrompt** turns clinical guidelines into LLM-executable decision trees, evaluated on *synthetic vignettes*. Referral F1 0.85–1.00, pathway F1 0.47–0.77 (JAMIA 2026, https://pubmed.ncbi.nlm.nih.gov/41746783/).
- Multi-agent CDS for secondary headache in primary care (JAMIA 2026, PMID 42364078).
- MedError systematic error analysis (Nat Commun 2026, PMID 42786185).
- Geriatric care constructs from EHR (npj Health Syst 2026, PMID 42749862).
- Delirium detection (J Gerontol 2025, PMID 41017643).
- **LLM health inequity mitigation** (npj Digit Med 2025, PMID 40319154).
- GenAI not ready for patient education (AMIA 2025, PMID 40502233).

→ He will reward rigorous evaluation, systematic error taxonomies, equity across groups and languages, guideline-grounded and auditable LLMs, geriatric/elder-care relevance, and human-in-the-loop design.

**Fit by problem type:** cardiology decision support with fairness analysis (both judges) > guideline-grounded multilingual LLM (Wang strong, Prasad good) > genomics AMR (Prasad strong) > signal and audio screening (moderate).

---

## 5. Candidate projects (none is the brief's pneumonia / UCI-heart / country-risk)

Shared rules for all candidates:
- Report FN and FP separately.
- Include a subgroup table.
- Show at least one failure case.
- Include "This project is a prototype and is not medical advice."

### C1. Hidden structural heart disease from a routine ECG → who gets the echo slot (EchoNext-Mini)
**User and moment:** A GP at a rural polyclinic in, say, Kyzylorda oblast reviews the routine 12-lead ECG from an annual dispensary check-up. The district hospital has a handful of echo slots per week. The tool ranks today's patients by risk of echo-confirmed structural heart disease (reduced EF, LVH, valve disease, pulmonary hypertension), so the GP refers the top-k.

**Evidence:** See sections 1–2.
- KZ: HF 526,766 adults (2014–19), HF mortality roughly tripled, circulatory diseases 22.3% of deaths.
- MoH Smart ECG CHF plan (Jan 2026).
- EchoNext (Nature 2025); EchoNext-Mini (NEJM AI 2026).
- AI-ECG mortality RCT (Nat Med 2024).

**Data:** EchoNext-Mini, v1.1.1 (20 Apr 2026), https://physionet.org/content/echonext/1.1.1/ (DOI 10.13026/7cfw-d091).
- Size: 100,000 12-lead ECGs from 36,286 patients, 10 s at 250 Hz, `EchoNext_<split>_waveforms.npy` with shape N×1×2500×12. Estimated **~6–12 GB** (my estimate; verify after login).
- Labels: 11 SHD labels plus composite `shd_moderate_or_greater_flag`; 52% positive.
- Columns: `sex`, `age_at_ecg`, `race_ethnicity`, HR/PR/QRS/QTc, LVEF; predefined train/val/test splits.
- **Access:** PhysioNet *Restricted*: free account plus click-sign the PhysioNet Restricted Health Data Use Agreement 1.5.0. No credentialing or approval wait. Download: `wget -r -N -c -np --user <physionet_user> --ask-password https://physionet.org/files/echonext/1.1.1/`.
- Reference model code and weights: https://github.com/PierreElias/IntroECG (folder "7-EchoNext Minimodel").
- ⚠ The DUA forbids redistribution. Do not upload the data to a public Kaggle dataset (someone already did; don't use it). Train on Colab, or use a private Kaggle upload. Confirm a minor may sign the DUA. Otherwise use C2.

**Baselines:**
1. "Refer everyone" / majority class.
2. **Logistic regression or XGBoost on the tabular ECG measurements** (age, sex, HR, PR, QRS, QTc). Strong, honest, clinician-readable.
3. Published Mini-model AUROC 82.0 as the ceiling to approach (cite, don't copy).

**ML:**
- 1D ResNet over 12×2500, plus tabular late fusion; augmentation with lead dropout and noise.
- Threshold set by capacity (refer top 10% / 20%) and by target sensitivity.
- Recalibrate PPV/NPV from 52% to a realistic screening prevalence (e.g., 5–15%).
- Subgroup AUROC, sensitivity and specificity by sex, age band (<50 / 50–69 / ≥70) and race_ethnicity (Asian subgroup as the closest proxy, with the caveat stated).
- **Own question: does it still work with lead I only, or 6 limb leads?** These are the cheap portable or smartwatch devices a feldsher actually has.
- Saliency over leads for interpretation.

**Original because:** echo-confirmed labels (rare in student work); a capacity-constrained decision framing; a reduced-lead deployment test; tied to a live Kazakh MoH program. It is new data (NEJM AI, April 2026).

**Feasibility (30 h, Colab T4):**
- Download and memmap loading: 2 h.
- Tabular baseline: 1 h.
- CNN: ~10–20 min per epoch on a 60–70k train split (estimate); 3–4 runs.
- Analysis and figures: 6 h; Gradio demo: 3 h.
- Use `np.load(..., mmap_mode='r')` to stay under RAM limits.

**Demo:** Pick a held-out ECG (or upload a .npy/CSV), see the 12-lead plot, risk score, "refer / don't refer at today's capacity", a lead-saliency overlay and the subgroup card. Output text in Kazakh/Russian/English.

**Risks:**
- US tertiary-hospital population ≠ rural Kazakhstan. Say so; this is the headline limitation.
- Spectrum bias: everyone had an echo ordered.
- Data size and Colab disk.
- DUA eligibility.
- Must train our own model, not just run theirs.

### C2. "Is this ECG urgent?" for a feldsher, trained in Germany and tested in Brazilian primary care (PTB-XL → CODE-15%)
**User and moment:** A feldsher at a village feldsher-midwife post (FAP) records an ECG for a patient with chest discomfort and must decide: call the ambulance now, send to a cardiologist remotely, or routine follow-up.

**Evidence:**
- KZ AMI: 79,172 cases, 33% rural, 30-day mortality 9%.
- 37.6% of Kazakhstan's population is rural.
- Almaty EMS remote-ECG study: 19,265 paramedic-recorded ECGs (2015–19), all sent to a cardiologist; the automatic read had sensitivity 83.8% and specificity 95.5% (Arch Acad Emerg Med 2022, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8771155/).
- AI-ECG RCT (Nat Med 2024).

**Data:**
- **PTB-XL v1.0.3**, open, CC BY 4.0: 21,799 records from 18,869 patients, age/sex, 5 superclasses plus 71 statements, recommended folds (1–8 train / 9 val / 10 test). 1.7 GB zip. `wget -r -N -c -np https://physionet.org/files/ptb-xl/1.0.3/` or `aws s3 sync --no-sign-request s3://physionet-open/ptb-xl/1.0.3/ .` (https://physionet.org/content/ptb-xl/1.0.3/)
- **CODE-15%**, Zenodo 4916206, CC BY 4.0: 345,779 exams from 233,770 patients, Telehealth Network of Minas Gerais (Brazil, primary care), 2010–16. Labels: 1dAVb, RBBB, LBBB, SB, AF, ST; age, sex, death. 18 zips of ~2.7 GB each plus `exams.csv`; **download 1–2 parts only** for an external test (https://zenodo.org/records/4916206).
- Optional: PhysioNet Challenge 2021 (open, CC BY 4.0, 12.6 GB; Chapman-Shaoxing, Georgia etc.), https://physionet.org/content/challenge-2021/1.0.3/

**Baselines:** Majority class; HR/QRS rule (tachy/brady/wide QRS); and CODE-15%'s own `normal_ecg` automatic-system flag as the "existing machine read" baseline.

**ML:** 1D CNN or ResNet (or the pretrained ECG-FM); harmonise labels to the shared set (AF, RBBB, LBBB, 1dAVb, brady, tachy). Measure the in-domain vs cross-continent drop; single-lead ablation; subgroups by sex and age.

**Original because:** cross-continent shift into a real primary-care tele-ECG network (the analogue of Kazakh remote ECG). Moderate originality, since PTB-XL is used fairly often.

**Feasibility:** High; 100 Hz PTB-XL trains in minutes.

**Demo:** Upload ECG → urgency card.

**Risks:**
- Label-mapping errors between datasets.
- CODE-15% labels partly come from automated text reports.
- Stretch goal (higher risk): an ECG *photo* pipeline using ecg-image-kit synthetic images, tested on real printed ECGs from Mendeley "ECG Images dataset of Cardiac Patients" (Pakistan; https://data.mendeley.com/datasets/gwbz3fsgp8/2; verify licence).

### C3. Predict second-line / new-drug TB resistance from the genome, for a TB dispensary (CRyPTIC)
**User and moment:** A phthisiatrician at a regional TB dispensary (e.g., Almaty) has a whole-genome or targeted-NGS mutation list for a new MDR-TB patient. Phenotypic drug-susceptibility testing takes weeks, and she must start a BPaLM-type regimen today.

**Evidence:**
- KZ: **33% of new and 55% of retreated TB cases are rifampicin-resistant** (WHO 2024 estimates); 3,600 MDR/RR-TB cases.
- Astana genomic study: genotype matched phenotype except for **bedaquiline**.
- The WHO catalogue 2nd ed. (2023) went from 0 to 86 bedaquiline variants, so it is still immature: https://www.who.int/publications/i/item/9789240082410

**Data:** CRyPTIC, open on EBI FTP, https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/
- `reuse/CRyPTIC_reuse_table_20240917.csv` (5.1 MB): binary phenotypes plus MICs for 13 drugs (AMI, BDQ, CFZ, DLM, EMB, ETH, INH, KAN, LEV, LZD, MXF, RIF, RFB), with quality flags.
- `reproducibility/data_tables/cryptic-analysis-group/MUTATIONS.csv.gz` (1.4 GB), `GENOMES.csv.gz` (lineage), `PREDICTIONS.csv.gz` (29 MB, catalogue-based predictions = **ready-made baseline**), `DST_MEASUREMENTS.csv.gz`.
- ~12k isolates. Citation: CRyPTIC Consortium, PLoS Biol 2022 data compendium.
- Download with `wget`; no login.

**Baseline:** WHO-catalogue / CRyPTIC `PREDICTIONS` rule; and an "any non-synonymous mutation in the drug's resistance genes" rule.

**ML:** Per-drug L1-logistic or XGBoost on gene and mutation features. **Lineage-held-out split**, to prevent learning population structure. Report AMR-standard *very major error* (missed resistance = FN) and *major error* (false resistance = FP). Subgroups by lineage, since lineage 2/Beijing dominates in Kazakhstan.

**Original because:** No high-school team will do this. It directly addresses Kazakhstan's #1 infectious-disease problem.

**Feasibility:** Medium. Data wrangling of the 1.4 GB table (use DuckDB or chunked pandas) takes ~6–8 h. Few resistant isolates for BDQ/LZD/DLM means wide CIs.

**Demo:** Paste a mutation list → per-drug traffic light plus the mutation that drove it.

**Risks:**
- Domain complexity for the team and judges.
- Less visual demo.
- No Kazakh isolates without variant calling (reads from the Almaty WGS study could be a stretch external test).

### C4. Guideline-executing LLM for hypertension follow-up in Kazakh / Russian / English, with a language-equity audit
**User and moment:** A feldsher reads a patient's home-BP log and medication list sent by WhatsApp, in Kazakh, Russian or mixed. The tool returns the next protocol step (continue / intensify / same-week GP / urgent referral) and cites the guideline node it used.

**Evidence:**
- KZ hypertension 42%, only 30.5% controlled.
- Bean 2026: LLMs fail when used directly by the public, which justifies a trained intermediary.
- CPGPrompt (JAMIA 2026) validates guideline→decision-tree→LLM evaluated on synthetic vignettes.
- Wang npj DM 2025 on LLM-driven inequity.

**Data (synthetic, allowed by the rules):**
- Code generates ~1,500 vignettes from the WHO 2021 hypertension pharmacological-treatment guideline / HEARTS protocol (https://www.who.int/publications/i/item/9789240033986), with ground-truth labels computed deterministically.
- Each vignette is rendered in EN/RU/KK (templates plus LLM paraphrase); a native speaker checks a 100-vignette sample.
- A held-out "messy" set adds code-switching, typos and colloquial units.

**Models:**
- `issai/Qwen3.5-9B-Kazakh` or `issai/LLama-3.1-KazLLM-1.0-8B` (HF gated-auto, CC-BY-NC-4.0, https://huggingface.co/issai)
- A general Qwen/Gemma model.
- Optionally the Gemini free tier.

**Baselines:** (a) zero-shot LLM without the guideline; (b) a regex/rule parser plus the decision tree.

**ML:** LLM extracts structured fields, then the decision tree is executed (CPGPrompt-style), compared with end-to-end prompting. Report missed urgent referrals (FN) and over-referrals (FP) **per language**, plus vignette age/sex, and an error taxonomy (negation, units, temporal).

**Original because:** Kazakh-language clinical LLM evaluation does not exist publicly (none on HF as of 2026-11-14). It is the format Wang publishes.

**Feasibility:** High: 7–9B models in 4-bit on a T4; ~1,500 × 3 languages × 3 systems ≈ 13k generations in ~6–8 h.

**Demo:** Live chat in Kazakh.

**Risks:**
- Synthetic-data circularity; judges may see it as an "LLM wrapper" (the brief warns about this).
- The rule parser may beat the LLM. That is an honest finding, but it weakens "AI does the main job".

### C5. Intrapartum fetal-acidaemia early warning for a rural midwife (CTU-UHB CTG)
**User and moment:** A midwife in a district maternity ward watches a CTG trace during labour and must decide whether to call the obstetrician now.

**Evidence:**
- KZ maternal mortality 10/100k (23 in 2021); infant mortality 6.8/1,000 (2024).
- "Where AI fails" angle: the INFANT RCT (Lancet 2017; older than 2023, cite as background) found computerised CTG support did not improve outcomes.

**Data:** CTU-UHB Intrapartum CTG database, PhysioNet open, ODC-By 1.0, **38 MB**: 552 recordings (~90 min each) with umbilical-artery pH, Apgar, maternal age and parity; only a few dozen are acidaemic. https://physionet.org/content/ctu-uhb-ctgdb/1.0.0/ (`wget -r -N -c -np https://physionet.org/files/ctu-uhb-ctgdb/1.0.0/`)

**Baseline:** FIGO-style features (baseline FHR, variability, decelerations) with logistic regression.

**ML:** 1D CNN on the last 30–60 min, or gradient boosting on features; nested CV.

**Original vs** the 56k-download Kaggle fetal_health tabular set.

**Feasibility:** High compute, but small n gives noisy AUCs (~0.6–0.7 in the literature).

**Demo:** Scrolling CTG with an alert.

**Risks:** Tiny positive class; weak result likely.

### C6. Child chest-sound triage with a cheap digital stethoscope (SPRSound)
**User and moment:** A village feldsher auscultates a coughing child; the tool flags wheeze or crackles to escalate.

**Evidence:**
- KZ: 3,404 under-5 deaths in 2024; respiratory causes are 10% of all deaths.
- WHO is evaluating digital stethoscopes as new screening tools (2026 call).

**Data:** SPRSound, GitHub, CC BY 4.0 (~735 MB repo): paediatric (1 month–18 years) recordings from Shanghai Children's Medical Center, with age and sex in filenames. Record labels: Normal / CAS / DAS / CAS&DAS / Poor quality; event labels: wheeze, rhonchi, stridor, crackles. https://github.com/SJTU-YONGFU-RESEARCH-GRP/SPRSound (`git clone`)

**Baseline:** MFCC + logistic regression.

**ML:** Fine-tune a pretrained audio encoder (AST, BEATs or wav2vec2).

**Fairness:** By age band and sex.

**Original:** Medium.

**Risks:** Labels are sounds, not diagnoses; single site; "poor quality" handling.

### C7. Russian-language complaint → ICD chapter / routing for a polyclinic registrar, with a Kazakh-translation robustness test (RuMedPrime)
**User and moment:** A registrar or triage nurse types the patient's complaint and the tool routes it to the right specialist queue.

**Data:** RuMedPrime: **7,625 real anonymised outpatient records** (symptoms, anamnesis, ICD-10), from https://github.com/pavel-blinov/RuMedBench (`data/raw/RuMedPrimeData.tsv`, 7.7 MB; RuMedTop3 splits included). **Licence not stated in the repo; verify.** No age or sex, so no subgroup analysis.

**Baseline:** TF-IDF + logistic regression.

**ML:** Fine-tune XLM-R / ruBERT; translate the test set to Kazakh (NLLB / ISSAI) and measure the accuracy drop; a native speaker checks 100.

**Fit:** Wang (clinical NLP).

**Risks:** Licence; no urgency label; Russian (not Kazakh) clinical source.

### C8. Smartphone anaemia check from an eyelid photo for pregnant women (Eyes-defy-anemia)
**User:** A rural midwife at an antenatal visit without a haemoglobinometer.

**Evidence:** KZ anaemia 32.3% of pregnant women.

**Data:**
- Eyes-defy-anemia: 218 subjects (Italy 123, India 95), conjunctiva photos with lab Hb, age and sex. IEEE DataPort (free account) https://ieee-dataport.org/documents/eyes-defy-anemia, reportedly CC BY 4.0; Kaggle mirror `harshwardhanfartale/eyes-defy-anemia`.
- ⚠ The Ghana CP-AnemiC Mendeley versions 1 and 2 **were removed at the author's request** (checked 2026-11-14).

**Baseline:** Colour-index (erythema index) threshold.

**ML:** CNN regression; Italy→India transfer as a skin-tone/device shift.

**Risks:** n = 218 means weak, noisy results; a phone selfie differs from the study camera. The demo is strong, but the science is thin.

### C9. Fall-risk from 3-day wearable accelerometry for older adults living alone (LTMM) — Arecibo AgeTech fit
**Data:** PhysioNet LTMM, open, ODC-By, 20.8 GB: 71 community elders (65–87 y), 3-day 3D accelerometry, faller vs non-faller. https://physionet.org/content/ltmm/1.0.0/

**Baseline:** Gait-speed / step-count rule.

**ML:** Gait features plus gradient boosting.

**Risks:** n = 71 subjects gives unstable estimates; labels come from self-reported past falls.

---

## 6. Scores (1–5) and ranking

| # | Candidate | Impact evidence | Originality | Data now | Feasibility | Demo | Judge fit | **Total /30** |
|---|---|---|---|---|---|---|---|---|
| 1 | **C1 EchoNext-Mini: hidden SHD → echo triage** | 5 | 5 | 4 | 4 | 4 | 5 | **27** |
| 2 | C4 Guideline-LLM HTN, Kazakh/Russian equity audit | 4 | 4 | 4 | 4 | 5 | 5 | **26** |
| 3 | C2 PTB-XL → CODE-15% urgent-ECG triage | 4 | 3 | 5 | 5 | 4 | 4 | **25** |
| 4 | C3 CRyPTIC MDR-TB genome resistance | 5 | 5 | 4 | 3 | 3 | 3 | **23** |
| 5 | C5 CTU-UHB intrapartum CTG | 3 | 4 | 5 | 4 | 3 | 3 | **22** |
| 5 | C6 SPRSound child chest sounds | 3 | 3 | 5 | 4 | 4 | 3 | **22** |
| 5 | C7 RuMedPrime Russian→Kazakh routing | 3 | 4 | 3 | 4 | 4 | 4 | **22** |
| 8 | C8 Eye-photo anaemia | 4 | 3 | 2 | 3 | 5 | 3 | **20** |
| 9 | C9 LTMM elder fall risk | 3 | 3 | 4 | 2 | 2 | 4 | **18** |

### Data ruled out (approval wait or unavailable, checked 2026-11-14)
| Dataset | Reason |
|---|---|
| CODA TB cough | Synapse *validated* user (ID check) plus a public intended-use statement: https://www.synapse.org/Synapse:syn31472953 |
| Zambia TB-cough | DUA on request |
| BRSET / mBRSET retina | PhysioNet *credentialed* |
| DementiaBank / ADReSS speech | Membership |
| PROCESS-2 | Controlled HF access |
| MIMIC / UK Biobank | Credentialed |
| CP-AnemiC | Withdrawn |

---

## 7. Strongest recommendation: C1, with C2 as the no-DUA fallback

1. **Evidence and locality.** It addresses Kazakhstan's top cause of death (circulatory diseases 22.3% of 2024 deaths) and a fast-rising HF burden (526k adults in records; mortality roughly tripled 2014–19). It mirrors a stated MoH 2026 "Smart ECG" heart-failure project for clinics without specialists. In a 37.6%-rural country, an echo is the scarce resource.
2. **It catches disease sooner,** literally the track brief: it finds echo-confirmed disease from a test the GP already runs.
3. **Judges' checklist built in.**
   - FN = missed SHD; FP = wasted echo slot.
   - Sex, age and race subgroups come from the data.
   - The baseline is honest and strong (tabular ECG measurements), with a published 82.0 AUROC reference.
   - Failure cases (paced rhythms, AF, borderline LVEF) arise naturally.
4. **Prasad** gets a capacity-constrained decision threshold plus calibration under prevalence shift. **Wang/Arecibo** get "verifiable" evaluation, equity analysis and an error taxonomy. Both are their stated interests.
5. **Originality:** a 2026 dataset with almost no hobbyist use, echo labels instead of ECG text labels, and the reduced-lead "what a feldsher actually owns" test.

**Required checks before committing:**
- (a) A team member can create a PhysioNet account and sign the DUA (age and terms).
- (b) Actual waveform file sizes, for Colab disk and RAM.

**If either fails, switch to C2 immediately.** C2 uses the same pipeline, user and demo with fully open data, at slightly lower originality.
