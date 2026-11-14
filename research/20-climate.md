# 20 — AI + Climate track: research and candidate projects

Prepared 2026-11-14 for the Veritas AI High School Hackathon 2026, Climate track. Every claim cites a source in the reference list at the end, given as [n]. Items marked **[own check]** are data checks I ran today with curl or the Python standard library against the live APIs (log at the end).

**Bottom line:** the strongest pick is **Candidate A, a methane super-emitter watch for Mangystau oil fields**. It has the most original story with real evidence behind it: in 2023 Kazakhstan had the largest methane leak ever recorded. It also makes the most visual demo: an invisible gas becomes visible on free Sentinel-2 imagery. The fallback is **Candidate B, a next-day fire patrol map for the Abai region**. Its data needs no API key and is already verified, and it matches every item in the Climate rubric. Set a go/no-go gate at hour 10. If Kazakh Sentinel-2 L1C chips are not loading by then, switch to B.

---

## 1. Where AI works in climate and energy (2025-26), where it fails, and the gaps

### Works (operational or peer-reviewed)
| Area | Evidence |
|---|---|
| Global medium-range weather | GraphCast beat ECMWF HRES on 90% of 1,380 targets [1]. GenCast, a diffusion ensemble model, beat ECMWF ENS on 97.2% of 1,320 targets [2]. Aurora, a 1.3B-parameter foundation model from Microsoft, beat operational systems on air quality, waves, cyclone tracks and 0.1° weather [3]. |
| ML weather in operations | ECMWF AIFS Single has been operational since **25 Feb 2025**, and AIFS ENS (51 members) since **1 Jul 2025**. The open weights are on Hugging Face [4]. |
| Riverine flood forecasting | Google's LSTM, trained on many gauges, is reliable for extreme events in **ungauged** basins at a 5-day lead, about as good as GloFAS same-day forecasts. Flood Hub now covers about 150 countries [5]. |
| Satellite methane detection | CH4Net, a U-Net on Sentinel-2, detects 84% of super-emitter plumes against 24% for the classic band-ratio baseline, at a similar false-positive rate [7]. UNEP's MARS uses satellites plus AI and sent more than 3,500 alerts in 33 countries [9]. |

### Fails or is weak
- **Record-breaking extremes.** ECMWF HRES still beats GraphCast, Pangu and FuXi on record heat, cold and wind. The AI models underestimate how often records happen and by how much, and the error grows as the exceedance grows [6].
- **Near-surface wind.** IFS ENS is still more skilful than AIFS ENS for 10 m wind when checked against SYNOP observations [4]. This matters for wind-power and dust use cases.
- **Global products at local scale.** **[own check]** CAMS (via Open-Meteo) puts Almaty's mean winter PM2.5 for Dec 2023 to Feb 2024 at **25.1 µg/m³**. The US-consulate reference monitor measured **49.7 µg/m³** over the same hours (OpenAQ archive, n = 2,020 h). The model reads about **half** the real smog. **[own check]** The GloFAS v4 reanalysis cell nearest Kostanay on the Tobol gives a median annual peak of only 31 m³/s, which suggests the routing misses the main channel or reservoirs there.
- **Methane on bright or heterogeneous ground.** CH4Net precision is only 0.30. False positives come from bright surfaces and thin cloud, and false negatives from heterogeneous backgrounds. The model has never been tested outside Turkmenistan [7].

### Gaps a hackathon can use
- **Data poverty is political.** Countries with less public streamflow data have lower GDP, on a log-log scale [5]. Central Asian hydromets **sell** daily discharge data [21]. Kazakhstan's post-2024 flood system, Tasqyn, uses **no ML** and is open only to government agencies [17].
- **Alerts with no action.** About 88% of satellite methane alerts get no response; the response rate is 12% [9]. The bottleneck is triage and prioritisation, and that is a decision problem ML can help with.
- **Global reanalysis and model products are biased in Kazakh basins and cities** (own checks above). Local bias-correction and local validation are therefore real contributions.

---

## 2. Problem size: latest numbers

### Global
- 2025 was the 3rd-warmest year at **1.47 °C** above pre-industrial; 2024 was the warmest at 1.60 °C. 2023-2025 is the **first three-year period averaging more than 1.5 °C** (C3S, 14 Jan 2026) [12].
- The ten biggest emitters produced **more than 85 Mt** of fossil-fuel methane in 2025, and **Kazakhstan is one of them**. The Eurasian fossil sector emitted more than 24 Mt (IEA GMT 2026) [10].
- More than 3,500 MARS methane alerts were sent, and only 12% got a response, up from 1% the year before (UNEP, Oct 2025). Alerts that did get action led to at least 19 leaks being repaired, worth about 1,200 t CH₄ a day combined (UNEP Annual Report, Feb 2026) [9].

### Kazakhstan and Central Asia
| Problem | Numbers | Source |
|---|---|---|
| **Methane: Karaturun East blowout, Mangystau** | 9 Jun to 25 Dec 2023, 205 days. **128 ± 36 kt CH₄** from 48 high-quality plume observations, the largest leak from any documented accident. Sentinel-2 and Landsat were essential in the first weeks. The operator called it "negligible". The fine was about 500 M tenge (≈$1.1 M) per Interfax; other outlets report ≈$0.78 M. | [8], [11] |
| Methane policy | NDC target: cut fugitive methane by 42% by 2035. LDAR and MRV rules are being drafted. Penalties are "quite low" with exemptions. A Sept 2025 MoU with the Global Methane Hub, Carbon Mapper and CATF covers satellite rapid response. | [10] |
| **Spring floods 2024** | "Worst in 80 years". About **118,000** evacuated by 19 Apr. **12,908** homes flooded. More than 120,000 evacuated in total per a Feb 2026 recap. Sergeevka reservoir reached **175%** full and 11.90 m, a record since 1968. Drivers were deep snowpack, record winter soil moisture and frozen ground. | [13]–[16], [19], [20] |
| Floods, 2026 | Shoptykol dam break in Akmola region; International Charter activation 1026 on 13 Apr 2026. | [18] |
| Flood forecasting today | Tasqyn by Gharysh Sapary: 377 permanent and 44 seasonal hydroposts, flags basins up to 30 days ahead. **No AI, no published accuracy, government access only.** | [17] |
| **Wildfire: Abai region, June 2023** | Started 8 Jun 2023 in Semey Ormany. **14 forestry workers plus 1 tractor driver died.** About 60,000 ha burned. The Emergencies minister was dismissed. | [27]–[29] |
| Fires since | 2025: **609 forest fires, 62.7 k ha** on forest-fund land only, excluding steppe [30]. Oct 2024: Bayanaul fire grew to 6,000 ha in a day [31]. Steppe burned area rose about 7× from 1990 to 2000, driven by changes in grazing [32], [33]. Kazhydromet issues 5 daily fire-danger classes; classes 4-5 trigger storm warnings to MChS and akimats [34]. On 27 Jul 2026, 16 regions were under extreme fire danger [34]. | |
| **Almaty smog** | Annual PM2.5 was 5.3× the WHO limit, with a winter maximum from coal heating (2013-2018 data) [22]. A 2026 conference paper reports inversions on 65-80% of winter days and a winter mean of 68.2 µg/m³ [23]. IQAir 2024: Almaty 20.3, **Karaganda 104.8 µg/m³** [24]. The CHP-2 coal-to-gas conversion is due by **Dec 2026**, a natural experiment now under way [26]. US-embassy monitor data sharing was cut in Mar 2025 [25], but **[own check]** the OpenAQ archive still holds Almaty-8876 hourly data up to 2025-11-14. | |
| **GLOF and mudflows above Almaty** | 51 moraine lakes; **6 under constant monitoring**; draining is done largely by hand [35]. 458 debris flows on record, including **55 GLOFs (1887-2020)**, all of which became debris flows. They are linked to heat, not rain, and are moving higher and earlier in the year [36]. Lake No. 5 (Turgen) is ≈95,000 m² and 988,000 m³, surveyed by UAV on request in Jul 2024 [37]. A Talgar early-warning system launched in Aug 2026 [39]. | |
| **Grid** | Coal was **62%** of generation in 2025, and coal units average more than 50 years old. Demand grew **+16%** from 2020 to 2025 (107.3 to 124.6 TWh). Net importer since 2022. Wind was 4.4% of generation, with 2.1 GW installed by mid-2026 (Ember, 3 Nov 2026) [41]. KEGOC: renewables 6.4% in 2024 [40]. **No public hourly grid data found.** | |
| Drought and grain | 2021 drought cut wheat to ≈12 Mt [45]. 2025 set a record of 20.3 Mt wheat and 27.1 Mt grain [44]. Dry years drop yields to 8-9 c/ha. Drought was forecast in the south and west in Aug 2026 [46]. | |
| Aral dust | The Aralkum added ≈7% to Central Asian dust. **68% of its emissions happen under more than 95% cloud cover**, which satellites cannot see [42]. | |
| Caspian | Sea level reached −29.11 m in Jan 2026, below the 1978 record [43]. | |

---

## 3. "Generic answers" other teams will build (avoid)
This section is my own analysis of what an LLM gives for "AI climate hackathon idea".
1. Next-day **solar** forecast (brief case 4.3.1), often on Kaggle solar datasets.
2. Next-day **PM2.5** (brief case 4.3.2). **Every Kazakh team that picks Climate will think of Almaty smog first.**
3. **EuroSAT** land-use CNN (brief case 4.3.3) and generic deforestation maps.
4. Carbon-footprint calculator or chatbot; "meal photo to CO₂" (named in the brief).
5. Building energy prediction (ASHRAE Great Energy Predictor / BDG2).
6. Wildfire **smoke/fire image classifier**, or the US "Next Day Wildfire Spread" Kaggle set.
7. Flood prediction from the **synthetic** Kaggle Playground flood dataset.
8. Crop-yield regression on FAO country tables; Climate TRACE emitter maps.
9. Waste-sorting CNN; EV-charging optimisation; ClimateBERT greenwashing classifier.

What makes a project look different: **a Kazakh place, a named operational decision-maker, an official baseline to beat** (Kazhydromet fire classes, CAMS, GloFAS, MBMP), and a **replay of a real disaster day**.

---

## 4. Candidate projects

Score scale: 1-5. Columns are **Impact** evidence, **Orig**inality, **Data** available now, **Feas**ibility in 30 h, **Demo**-ability, **Judge** fit (one place, persistence baseline, time split, decision).

### A. Methane super-emitter watch for Mangystau oil fields (Karaturun East test case)
- **User and decision moment.** An inspector at the Mangystau regional Ecology Department, or Kazakhstan's methane rapid-response team under the Sept 2025 MoU [10], at the **Monday triage**: "Which 5 of our N oil and gas sites get a field LDAR visit this week? Is the operator's 'it's just steam' claim true?"
- **Evidence.** The largest accidental methane leak ever documented happened in Kazakhstan: 128 ± 36 kt over 205 days [8]. The operator denied it and the fine was about $1 M [8], [11]. Kazakhstan is among the top-10 fossil methane emitters and has a 42% fugitive-cut NDC [10]. 88% of satellite alerts go unanswered [9], so triage is the bottleneck.
- **Data.**
  - **CH4Net** (Vaughan et al. 2024): https://huggingface.co/datasets/av555/ch4net (doi:10.57967/hf/2117). 10,046 Sentinel-2 L1C tiles, 200×200 px, 13 bands at 10 m, from 23 Turkmen super-emitter sites, 2017-2021. 925 hand-labelled plume masks plus **precomputed MBMP baseline arrays** (`train/mbmp`, `test/mbmp`). Split: train 2017-2020, **test 2021 (time-based)**. License **CC-BY-NC-ND-4.0**. Access is **gated "auto"**: log in to HF and click accept, approval is instant **[own check]**. The tiles are numbered (`0.npy` …) and the public tree shows no site or date metadata; check the gated `quickstart.ipynb` after logging in. About 470 KB per tile, roughly 5 GB per split folder.
  - **Kazakh imagery.** Sentinel-2 **L1C**, which matches the training data:
    - Google Earth Engine `COPERNICUS/S2_HARMONIZED` (free non-commercial registration), or
    - Copernicus Data Space Ecosystem (https://dataspace.copernicus.eu, free account, Sentinel Hub Process API for small chips), or
    - Earth Search `sentinel-2-l1c`: **[own check]** 200+ items over Buzachi for Jun-Dec 2023, but the assets sit in the **requester-pays** bucket `s3://sentinel-s2-l1c` and need an AWS account.
    - Planetary Computer has only L2A, which would add a domain shift.
  - **Ground truth for Kazakhstan.** The leak window (9 Jun to 25 Dec 2023) and plume dates from Guanter et al. 2024 and its SI [8]. Images from before Jun 2023 and after Dec 2023 serve as negatives.
- **Baselines.**
  1. MBMP band-ratio threshold, already provided; the paper reports recall 0.24.
  2. **Persistence**: "the site emits at this overpass if it emitted at the previous one", run on our own dated Kazakh and Turkmen time series.
  3. Always "no plume".
- **ML.** A U-Net (segmentation_models_pytorch, ResNet-18 encoder, 13-band input) trained on 2017-2020 and tested on 2021. Scene score is the maximum plume probability. Then **out-of-region transfer** to Karaturun 2022-2024. Report detection rate inside the leak window and false alarms outside it. Optionally rank sites for inspection with a small logistic model on each site's recent detection history.
- **Originality.** **5.** CH4Net has never been tested outside Turkmenistan [7]. No high-school team will do this.
- **Feasibility.** **3.**
  - h0-3: get data access and download.
  - h3-8: train and reproduce the paper's metrics; the MBMP baseline is free.
  - h8-16: build the Kazakh L1C chip pipeline for about 150 dates. **This is the risky part.**
  - h16-24: inference, persistence baseline, failure cases.
  - h24-30: Streamlit or Gradio demo and write-up.
- **Risks.**
  - L1C access and auth.
  - Karaturun was **on fire** for much of the period; smoke and flame fall outside the training distribution. This also makes a good failure example.
  - Plumes become hard to see once emission rates fall.
  - Low precision (0.30 in the paper).
  - The ND license means you must not redistribute the modified dataset; ship code only.
  - The persistence baseline cannot run on CH4Net itself unless the gated notebook has dates.
- **Demo.** Plain RGB image (nothing visible) → model heatmap shows the plume → timeline with the leak window shaded → this week's inspection list.
- **Scores.** Impact 5 · Orig 5 · Data 4 · Feas 3 · Demo 5 · Judge 4 = **26**

### B. "Where to patrol tomorrow": next-day fire map for the Abai region (Semey Ormany)
- **User and decision moment.** The duty officer of the Semey Ormany reserve forestry or the Abai DChS, at **18:00**: "Which 20 cells (10×10 km) get patrols and aircraft on standby tomorrow? Do we close forest access?" The brief itself names "forest rangers decide where to patrol".
- **Evidence.**
  - 14-15 dead and ≈60,000 ha burned in June 2023; minister dismissed [27]–[29].
  - 609 forest fires and 62.7 k ha in 2025 [30].
  - Bayanaul, 6,000 ha in a day, Oct 2024 [31].
  - Steppe burned area rose about 7× after 1990 [32], [33].
  - **Official baseline exists:** Kazhydromet's 5-class daily fire danger [34].
- **Data (all verified today).**
  - **NASA FIRMS country CSV, no key needed** **[own check]**: `https://firms.modaps.eosdis.nasa.gov/data/country/modis/<YYYY>/modis_<YYYY>_Kazakhstan.csv` (MODIS 2000-2025, 1 km) and `.../viirs-snpp/<YYYY>/viirs-snpp_<YYYY>_Kazakhstan.csv` (VIIRS 2012-2025, 375 m). MODIS detection counts in Kazakhstan: 2015 42k, 2019 51k, 2023 15k, 2024 7k. **VIIRS shows 1,968 detections on 2023-06-08 in the Semey box versus 1-8 a day before**, so the disaster is in the data. NRT for a live demo needs a free instant MAP_KEY. NASA open data.
  - Weather: Open-Meteo archive (ERA5 from 1940, ERA5-Land from 1950; **[own check]** works, no key): https://archive-api.open-meteo.com/v1/archive. CC BY 4.0.
  - Fuel: MODIS NDVI `modis-13Q1-061` and burned area `modis-64A1-061` on Microsoft Planetary Computer (**[own check]** collections exist; free, no account). DEM: `cop-dem-glo-30`.
  - Optional physics baseline: Canadian FWI, computed from ERA5 or taken from the CEMS fire historical dataset on CDS (free account).
- **Baselines.**
  1. **Persistence**: fire in the cell today → fire tomorrow.
  2. Climatology: cell × month base rate.
  3. FWI or Nesterov-style index, as a proxy for Kazhydromet classes.
- **ML.** LightGBM on the cell-day grid (≈0.1°). Features: Tmax, minimum RH, wind, days since rain, VPD, NDVI anomaly, fire counts over the last 1/3/7 days, day of year, land cover. Train 2012-2020, validate 2021-2022, **test 2023-2025**. Metrics: **recall@top-20 cells** (patrol capacity), PR-AUC, false alarms per week. Replay **7 Jun 2023**: was the Semey Ormany cell in tomorrow's top 20?
- **Originality.** **4.** Wildfire ML is common, but Kazakh steppe with a patrol budget and a disaster replay is not.
- **Feasibility.** **5.** Everything is tabular; data loads in under an hour.
- **Risks.**
  - FIRMS detections include stubble and agricultural burning (label noise); filter with cropland masks.
  - Most ignitions (lightning or human) are unpredictable, so skill may come mostly from persistence. Report this honestly.
  - Heavy class imbalance.
- **Scores.** Impact 4 · Orig 4 · Data 5 · Feas 5 · Demo 4 · Judge 5 = **27**

### C. Almaty smog: correcting CAMS for a school "outdoor PE tomorrow?" alert
- **User and decision moment.** An Almaty school principal at 18:00 deciding whether tomorrow's PE and recess are indoors, or the parent of a child with asthma.
- **Evidence.** **[own check]** CAMS underestimates winter PM2.5 by about 2× (25.1 vs 49.7 µg/m³) [own]. Inversions on 65-80% of winter days [23]. 5.3× the WHO limit [22]. The CHP-2 gas switch by Dec 2026 is a live policy question [26].
- **Data.**
  - **OpenAQ public S3 archive, no key**: `https://openaq-data-archive.s3.amazonaws.com/records/csv.gz/locationid=8876/year=YYYY/month=MM/` holds hourly PM2.5 from **2020-04-09 to 2025-11-14** (US-consulate reference monitor) **[own check]**. Other Almaty sensors need the free OpenAQ key.
  - CAMS via Open-Meteo air-quality API: Almaty values are non-null from about Aug-Sep 2022 **[own check]**.
  - **IGRA2 radiosonde Almaty (KZM00036870)**, for inversion strength **[own check]**: https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/data-por/KZM00036870-data.txt.zip
- **Baselines.** Persistence, plus the raw CAMS forecast as the "operational" baseline.
- **ML.** Gradient boosting on CAMS + inversion + weather + calendar. Report misses and false alarms at the 35 and 55 µg/m³ thresholds.
- **Originality.** **2.** This is brief case 4.3.2 and the most likely choice for other Kazakh teams.
- **Feasibility.** 5. **Risks:** a single station; CAMS hindcast covers only 3 winters; low originality.
- **Scores.** Impact 4 · Orig 2 · Data 5 · Feas 5 · Demo 4 · Judge 5 = **25**

### D. Snowmelt flood alert for Petropavl (Ishim) and Sergeevka reservoir
- **User and decision moment.** The North Kazakhstan oblast flood HQ in March-April deciding when to evacuate low-lying Petropavl districts, raise dikes, and pre-release water from Sergeevka.
- **Evidence.** 2024 was the worst in 80 years: ≈118 k evacuated, 12.9 k homes flooded, Sergeevka at 175% [13]–[16], [19]. The 2026 dam break shows the risk is ongoing [18]. Tasqyn has no ML [17].
- **Data.**
  - Open-Meteo Flood API (GloFAS v4 reanalysis, 5 km, daily, **1984 to now**, no key; https://flood-api.open-meteo.com/v1/flood). **[own check]** The Ishim cell at 55.075 N, 69.075 E gives a 2024 peak of 1,794 m³/s (2nd since 1984, after 1997) against a median annual peak of 497 m³/s.
  - ERA5-Land snow depth, soil moisture and soil temperature from Open-Meteo, 1950 onward **[own check]**.
- **Baselines.** Persistence of discharge, plus day-of-year climatology.
- **ML.** LightGBM or LSTM at 1/3/7/10-day leads with snow and frozen-soil features. Train 1984-2014, **test 2020-2025 (includes 2024)**. Target: exceeding the 2-year return level.
- **Originality.** 4. **Feasibility.** 4.
- **Risks.**
  - **The target is model output (GloFAS), not a gauge.** Kazhydromet gauge data is sold or available only as PDFs [21], so a sharp judge can call this circular. The ERA5-Land inputs drive GloFAS too.
  - GloFAS is clearly wrong at Tobol/Kostanay **[own check]**.
- **Scores.** Impact 5 · Orig 4 · Data 3 · Feas 4 · Demo 4 · Judge 4 = **24**

### E. Moraine-lake watch above Almaty (Sentinel-2 lake-area time series)
- **User and decision moment.** A Kazselezashchita engineer in June-August deciding which lake gets this week's UAV survey or drainage crew.
- **Evidence.** 51 lakes, 6 dangerous, drained by hand [35]. 55 GLOFs since 1887, all heat-triggered [36]. Lake No. 5 holds 988,000 m³ [37]. A 2018 study lists 17 dangerous lakes in Ile Alatau [38], and remote-sensing work analysed 77 lakes [47].
- **Data.** Sentinel-2 L2A on Planetary Computer (2017 onward, 10 m, 5-day revisit), Copernicus DEM, ERA5-Land temperature.
- **Baselines.** NDWI/Otsu threshold for segmentation; persistence for lake area.
- **ML.** A small U-Net or random-forest water classifier, then a lake-area-growth regression on positive degree-days.
- **Originality.** 5. **Feasibility.** 2: cloud, shadow, snow and ice at 3,300-3,600 m; you must make labels yourself; lakes are frozen until about June.
- **Scores.** Impact 4 · Orig 5 · Data 4 · Feas 2 · Demo 4 · Judge 3 = **22**

### F. Grain-belt drought early warning (Kostanay / North Kazakhstan wheat yield in July)
- **User and decision moment.** The Food Contract Corporation or Ministry of Agriculture deciding in July on procurement and export quotas.
- **Evidence.** 2021 at ≈12 Mt against the 2025 record of 20.3 Mt [44], [45]; drought forecasts for 2026 [46].
- **Data.** stat.gov.kz oblast and district yields (xlsx; verify how far back the district level goes), MODIS NDVI (PC), ERA5-Land soil moisture.
- **Baselines.** Last year's yield, or a linear trend.
- **Risks.** Small sample (≈17 oblasts × 25 years); crop-yield regression is a generic idea.
- **Scores.** Impact 4 · Orig 2 · Data 3 · Feas 4 · Demo 3 · Judge 4 = **20**

### G. Aralkum dust-day forecast for Aralsk and Kyzylorda
- **Evidence.** Banks et al. [42]. There is **no verified ground PM station** in Aralsk, and 68% of emissions happen under cloud.
- **Data.** CAMS reanalysis (ADS account) or MERRA-2 (Earthdata login).
- **Problem.** The target would itself be a model.
- **Scores.** Impact 3 · Orig 4 · Data 2 · Feas 3 · Demo 3 · Judge 3 = **18**

### H. Caspian sea-level outlook for Aktau
- **Evidence.** −29.11 m in Jan 2026 [43].
- **Problem.** Little value for ML (smooth monthly series, few samples); the decision link is weak.
- **Scores.** Impact 3 · Orig 3 · Data 3 · Feas 4 · Demo 2 · Judge 2 = **17**

### Rejected after checking
- **Kazakh grid or wind forecasting.** The evidence is strong [41], but **no public hourly KEGOC or generation data was found**, so any target would be synthetic.
- **Generic global problems** (building energy, solar): no local edge, and the same as competitors' ideas.

---

## 5. Ranking

| Rank | Candidate | Impact | Orig | Data | Feas | Demo | Judge | Sum | Weighted* |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **A. Methane watch (Mangystau)** | 5 | 5 | 4 | 3 | 5 | 4 | 26 | **4.45** |
| 2 | **B. Fire patrol map (Abai)** | 4 | 4 | 5 | 5 | 4 | 5 | **27** | 4.40 |
| 3 | D. Snowmelt flood (Petropavl) | 5 | 4 | 3 | 4 | 4 | 4 | 24 | 4.10 |
| 4 | C. Almaty smog / CAMS correction | 4 | 2 | 5 | 5 | 4 | 5 | 25 | 4.00 |
| 5 | E. Moraine lakes (Almaty) | 4 | 5 | 4 | 2 | 4 | 3 | 22 | 3.75 |
| 6 | F. Grain drought | 4 | 2 | 3 | 4 | 3 | 4 | 20 | 3.30 |
| 7 | G. Aral dust | 3 | 4 | 2 | 3 | 3 | 3 | 18 | 3.10 |
| 8 | H. Caspian | 3 | 3 | 3 | 4 | 2 | 2 | 17 | 2.80 |

\*Weighted to match the judging rubric: Impact 0.20, Originality 0.20, Demo 0.20, Feasibility 0.15, Judge fit 0.15, Data 0.10. Finals give 30% to demo and 30% to technical depth, and Round 1 gives 20% to originality.

---

## 6. Strongest recommendation: Candidate A, with B as the hour-10 fallback

**Why A.**
1. **It is a real problem, it is current, and it is Kazakh.** The largest accidental methane leak ever documented happened in Mangystau in 2023, and the operator denied it [8]. Kazakhstan signed a satellite rapid-response MoU in Sept 2025 and is drafting LDAR rules now [10]. Worldwide, 88% of satellite alerts are ignored [9], so the decision of which site to inspect first is the real gap.
2. **It fits "measure / reduce climate impact of an energy system" exactly.** Fire and flood are hazards; methane is the energy system's own footprint.
3. **It looks nothing like the generic answers.** No LLM idea list will propose transferring a methane U-Net from Turkmenistan to Kazakhstan.
4. **It meets the rubric.**
   - The time-based split is built into the dataset (train 2017-20, test 2021).
   - There is a published baseline (MBMP, supplied in the dataset) plus persistence on dated Kazakh time series.
   - There is one small real place (Karaturun East / Buzachi).
   - There is a named decision (the weekly inspection list).
   - There are honest failure cases (fire smoke, bright salt flats, cloud).
5. **It plays to the judges.** It has the most technical depth: a 13-band segmentation model and an out-of-distribution test. It has a visual demo: a plume invisible in RGB appears in the model output. One judge works in computational rock physics, close to oil and gas. The Microsoft judges work near Aurora and the Planetary Computer.

**Go/no-go gate.** By **hour 10**, the team must have:
- CH4Net trained with test metrics close to the paper's (recall around 0.8), and
- at least 20 Karaturun L1C chips loaded through GEE or CDSE.

If either is missing, switch to **B**. All of B's data is keyless and already verified today, and it can be built in under 20 hours.

---

## Own data checks run on 2026-11-14 (reproducible)
- Open-Meteo Flood API, GloFAS reanalysis 1984-2025, scanning a 9×9 grid of cells: Ishim/Petropavl cell at 55.075 N, 69.075 E, annual-peak top years 1997 (1,802), 2024 (1,794), 2005 (1,737); median 497 m³/s. Tobol/Kostanay best cell median peak 31 m³/s (suspect). Ural/Atyrau 2024 peak 3,303 m³/s (3rd since 1984).
- OpenAQ archive, location 8876 "Almaty-8876": files run from 2020-04-09 to 2025-11-14. DJF 2023/24 hourly mean 49.7 µg/m³, maximum 247.
- Open-Meteo CAMS PM2.5 for Almaty: DJF 2023/24 mean 25.1 (max 59.6); DJF 2024/25 mean 35.7 (max 110.6). Null before about Aug 2022.
- FIRMS country CSVs for Kazakhstan download without a key (MODIS 2000-2025, VIIRS 2012-2025). VIIRS Semey box, June 2023: 1,968 detections on 06-08.
- HF `av555/ch4net`: gated "auto", CC-BY-NC-ND-4.0; folders train, val and test, each with s2, label and mbmp.
- Planetary Computer has sentinel-2-l2a, modis-13Q1-061, modis-64A1-061, cop-dem-glo-30 and sentinel-1-rtc. Earth Search has sentinel-2-l1c, in the requester-pays bucket.
- IGRA2 Almaty KZM00036870 zip returns HTTP 200 (16 MB).

## References (URL; publication date; all accessed 2026-11-14)
1. Lam et al., GraphCast, *Science* (14 Nov 2023), doi:10.1126/science.adi2336 — https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/
2. Price et al., GenCast, *Nature* 637 (2025; online 4 Dec 2024), doi:10.1038/s41586-024-08252-9 — https://ideas.repec.org/a/nat/nature/v637y2025i8044d10.1038_s41586-024-08252-9.html
3. Bodnar et al., Aurora, *Nature* 641:1180-1187 (May 2025), doi:10.1038/s41586-025-09005-y — https://ideas.repec.org/a/nat/nature/v641y2025i8065d10.1038_s41586-025-09005-y.html
4. ECMWF, "ECMWF's ensemble AI forecasts become operational" (1 Jul 2025) — https://www.ecmwf.int/en/about/media-centre/news/2025/ecmwfs-ensemble-ai-forecasts-become-operational
5. Nearing et al., *Nature* 627 (20 Mar 2024), doi:10.1038/s41586-024-07145-1 — https://www.nature.com/articles/s41586-024-07145-1 ; Google Research blog — https://research.google/blog/a-flood-forecasting-ai-model-trained-and-evaluated-globally/
6. Zhang, Fischer, Zscheischler, Engelke, "Numerical models outperform AI weather forecasts of record-breaking extremes", arXiv:2508.15724 (Aug 2025) — https://arxiv.org/abs/2508.15724 ; Carbon Brief (May 2026) — https://carbonbrief.org/traditional-models-still-outperform-ai-for-extreme-weather-forecasts
7. Vaughan et al., CH4Net, *AMT* 17:2583-2593 (3 May 2024) — https://amt.copernicus.org/articles/17/2583/2024/ ; data https://huggingface.co/datasets/av555/ch4net
8. Guanter et al., *ES&T Letters* (30 Jun 2024), doi:10.1021/acs.estlett.4c00399 ; UPV release (17 Jul 2024) — https://www.eurekalert.org/news-releases/1051624
9. UNEP, *An Eye on Methane 2025* release (Oct 2025) — https://www.unep.org/ru/novosti-i-istorii/press-reliz/bolee-kachestvennye-dannye-sposobstvuyut-deystviyam-po-sokrascheniyu ; UNEP Annual Report 2025 (Feb 2026) — https://www.unep.org/annualreport/2025
10. IEA, Global Methane Tracker 2026 — https://www.iea.org/reports/global-methane-tracker-2026/regional-insights ; https://www.iea.org/reports/global-methane-tracker-2026/policy-trends
11. Interfax, Buzachi Neft fined — https://interfax.com/newsroom/top-stories/100301/
12. Copernicus C3S, "2025 was third hottest year on record" (14 Jan 2026) — https://climate.copernicus.eu/copernicus-2025-was-third-hottest-year-record
13. ACAPS briefing note, Kazakhstan floods (23 Apr 2024) — https://www.acaps.org/fileadmin/Data_Product/Main_media/20240423_ACAPS_briefing_note_Kazakhstan_floods.pdf
14. Astana Times (Apr 2024) — https://astanatimes.com/2024/04/kazakhstan-evacuates-over-111000-people-since-beginning-of-floods/
15. Times of Central Asia (Apr 2024) — https://timesca.com/kazakhstan-struggles-to-contain-floods-worst-natural-disaster-in-80-years-president-says/
16. Times of Central Asia (19 Feb 2026) — https://timesca.com/kazakhstans-reservoirs-prepared-for-spring-flooding/
17. Orda.kz (14 May 2025), Tasqyn — https://en.orda.kz/kazakhstan-can-now-predict-floods-so-why-cant-it-prevent-them-6375
18. International Charter "Space and Major Disasters", activation 1026 (13 Apr 2026) — https://disasterscharter.org/es/activations/flood-in-kazakhstan-activation-1026-
19. Bizmedia.kz (8 Apr 2024), Sergeevka record — https://bizmedia.kz/2024-04-08-pereliv-na-vodohranilishhe-v-sko-dostig-rekorda/
20. PreventionWeb summary of the 2024 compound-event study — https://www.preventionweb.net/quick/95399
21. Marti et al., CA-discharge, *Scientific Data* (Sep 2023) — https://www.nature.com/articles/s41597-023-02474-8
22. Kerimray et al. 2020, *Aerosol Air Qual. Res.* 20:1340-1352 — https://nur.nu.edu.kz/handle/123456789/5581
23. E3S Web of Conferences EPEMR 2026, paper 01013 (four Central Asian cities, 2015-2025) — https://www.e3s-conferences.org/articles/e3sconf/pdf/2026/33/e3sconf_epemr2026_01013.pdf (conference paper; treat as secondary)
24. Times of Central Asia, IQAir 2024 rankings — https://timesca.com/kazakhstans-karaganda-among-worlds-most-polluted-cities-as-central-asia-struggles-with-air-quality/
25. NBC News (Mar 2025), US embassies end air-pollution monitoring — https://www.nbcnews.com/news/world/us-embassies-end-air-pollution-monitoring-spurred-china-others-action-rcna194825
26. 24.kz, Almaty CHP-2 fully to gas in 2026 — https://24.kz/ru/news/social/686789-almatinskuyu-tets-2-polnostyu-perevedut-na-gaz-v-2026-godu
27. Astana Times (Jun 2023) — https://astanatimes.com/2023/06/fires-in-abai-region-declared-under-control-as-president-tokayev-dismisses-minister-of-emergency-situations/
28. Meduza (1 Sep 2023) — https://meduza.io/en/feature/2023/09/01/we-didn-t-start-the-fire
29. Crisis24 (13 Jun 2023) — https://crisis24.garda.com/alerts/2023/06/kazakhstan-emergency-crews-continuing-to-respond-to-wildfire-near-semey-in-abai-region-as-of-june-13-update-1
30. Kazinform, 2025 forest fires — https://www.inform.kz/ru/bolee-600-lesnih-pozharov-proizoshlo-v-kazahstane-s-nachala-goda-f10dde
31. Tengrinews (9 Oct 2024), Bayanaul — https://en.tengrinews.kz/emergencies/large-scale-wildfire-broke-out-in-another-region-of-264432
32. Dara et al. 2020, *Ecosystems* — https://pages.cms.hu-berlin.de/baumamat/website/publication/dara_2020_ecos
33. Hankerson et al. 2025 — https://biogeo.pages.cms.hu-berlin.de/website/publication/2025-hankerson-rec/
34. 24.kz, Kazhydromet fire-danger classes — https://24.kz/ru/news/social/725403-kak-otsenivayut-uroven-pozharnoj-opasnosti-v-kazakhstane ; Zakon.kz (27 Jul 2026) — https://www.zakon.kz/obshestvo/6526098-chrezvychaynaya-pozharnaya-opasnost-grozit-srazu-16-regionam-kazakhstana.html
35. bes.media (1 Oct 2026), Almaty moraine lakes — https://bes.media/amp/shest-morennyh-ozer-v-almaty-ostayutsya-potentsialno-opasnymi-kak-gorod-zaschischayut-ot-seley/
36. Shahgedanova et al. 2024, *npj Natural Hazards* 1:49 — https://centaur.reading.ac.uk/120163/
37. CESDRR situation brief, Moraine Lake No. 5, Turgen (28 Jul 2024) — https://cesdrr.org/uploads/dev/2026/Situation-Analytical_Brief__Moraine_Lake_No._5%2C_Turgen.pdf
38. Kapitsa et al. 2018 — https://www.debrisflow.ru/wp-content/uploads/2018/10/Kapitsa_DF18.pdf
39. Devdiscourse (Aug 2026), Talgar EWS — https://www.devdiscourse.com/article/other/3966247-kazakhstan-launches-mudflow-warning-system-in-talgar-basin
40. KEGOC Annual Report 2024 — https://ar2024.kegoc.kz/en/electricity-balance.html
41. Ember, "Kazakhstan has the wind to power its demand growth" (3 Nov 2026) — https://ember-energy.org/app/uploads/2026/11/Kazakhstan-has-the-wind-to-power-its-demand-growth.pdf
42. EOS research spotlight on Banks et al. (Dec 2022) — https://eos.org/research-spotlights/when-the-aral-sea-dried-up-central-asia-became-dustier
43. Report.az (Jan 2026), Caspian record low — https://report.az/en/ecology/researcher-caspian-sea-level-hits-48-year-record-low
44. PrimeMinister.kz, 2025 harvest results — https://primeminister.kz/en/news/olzas-bektenov-ob-itogax-uborocnoi-kampanii-2025-po-poruceniiu-glavy-gosudarstva-sozdany-vse-usloviia-dlia-svoevremennogo-i-kacestvennogo-provedeniia-vesenne-polevyx-i-uborocnyx-rabot-30681
45. USDA FAS World Agricultural Production (2021) — https://esmis.nal.usda.gov/sites/default/release-files/5q47rn72z/bc387k11r/8049h557p/production.pdf
46. Dunyo.info (2026), heat and drought — https://dunyo.info/en/central_asia/zhara-i-zasuha-mogut-snizit-urozhay-pshenicy-v-kazahstane-nizhe-urovnya
47. Ile Alatau glacial-moraine lake remote-sensing study — https://czasopisma.pan.pl/Content/133147
