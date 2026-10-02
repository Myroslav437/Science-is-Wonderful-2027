# 08 - Public datasets for prototyping the "How does a robot see you?" pipeline

Research track: which public datasets can we legally and ethically use to prototype and evaluate the multimodal pipeline (camera + microphone), compare camera+audio vs camera-only vs audio-only on real paired samples, and validate zero-shot visual attributes. We also need a protocol for our own small rehearsal dataset.

- Date context: all pages accessed 2026-10-01 unless noted. File sizes come from the Zenodo/OpenSLR/Hugging Face APIs on that date.
- Not legal advice. The licence readings below are an engineer's reading of primary texts. Confirm the "public proposal" uses with the Silesian University of Technology (SUT) Data Protection Officer before publishing anything.
- "UNVERIFIED" means I could not confirm the claim from a primary source in this session.

---

## 0. TL;DR (decision summary)

1. **No public dataset matches our setting.** We would need children aged 8-14, seen full-body from a low robot-dog viewpoint, talking spontaneously (in Polish) in a noisy hall, with consent to show them publicly. Nothing like this exists. Public data is only good for component benchmarking. Robot-viewpoint validation and all public-facing visuals must come from our own consented recordings (Section 5c).
2. **Cleanest paired audio-visual (AV) set: Lombard GRID** ([Zenodo 3736465](https://zenodo.org/records/3736465)).
   - Licence: **CC BY 4.0** (no NC, no SA).
   - Content: 54 talkers, 5,400 utterances, **plain vs Lombard (loud/effortful) speech**. This is real ground truth for "voice loudness/effort". It also has word alignments, and the sentences contain colour words. Front and side video.
   - Size: 1.49 GB for audio + front video + alignments.
3. **Best for richness: RAVDESS** ([Zenodo 1188976](https://zenodo.org/records/1188976)).
   - Licence: **CC BY-NC-SA 4.0**.
   - It already ships each trial as audio-video, video-only and audio-only files, which maps directly onto our sensor toggles.
   - Labels: intensity normal/strong, two fixed sentences ("Kids are talking by the door" / "Dogs are sitting by the door"), and 2 repetitions.
   - Size: Video_Speech zips of 502-596 MB per actor (13.36 GB for all 24), plus a 208.5 MB audio-only zip.
4. **Do not use the following:**
   - VoxCeleb1/2: audio, video and URLs are "no longer available" from the official site.
   - LRS3: official downloads discontinued.
   - MS-Celeb-1M, DukeMTMC, MegaFace: retracted or decommissioned.
   - LAION-Face: built on LAION-400M; LAION-5B and its derivatives were taken down in Dec 2023.
   - YouTube-ID datasets (AVSpeech, HDTF, CelebV-HQ/Text, TalkingHead-1KH).
   - Anything with race, gender, age, emotion or personality labels used as *targets*: FairFace, CelebA, PA-100K, CREMA-D demographics, Casual Conversations v2, Seamless Interaction's BFI-2 scores.
5. **Never train or demo emotion recognition**, even though RAVDESS, CREMA-D, MEAD, IEMOCAP and MELD are emotion corpora. AI Act Annex III(1)(c) lists emotion recognition as high-risk. Art. 5(1)(f) bans it in education settings, and school groups visit our stand. [corrected by verifier: Art. 5(1)(f) literally covers "the areas of workplace and education institutions" (with a medical/safety exception); a science-exhibition stand is probably not an "education institution", so this is a precautionary red line rather than a certain legal ban. Keep it as a red line anyway. Note also that the AI Act has been amended by the "Digital Omnibus on AI": the Commission AI Act Service Desk now shows new Art. 5(1)(ba)/(bb) prohibitions and gives 2 Dec 2027 as the application date for Annex III high-risk obligations ([Art. 5](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5), [Art. 113](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113)). The Art. 5 bans have applied since 2 Feb 2025.] [corrected by verifier, pass 3: the Omnibus has been formally adopted. It is Regulation (EU) 2026/1744 of 8 July 2026, published in OJ L on 24.7.2026 and in force since 27 July 2026. Annex III high-risk obligations now apply from 2 Dec 2027 and Annex I obligations from 2 Aug 2028 ([EUR-Lex ELI](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng)). Art. 5(1)(f) is unchanged.] Use the emotional variation only as nuisance variability.
6. **Do not use children's data for prototyping.** Children's speech corpora are only needed if we display ASR transcripts and want an offline WER estimate on child voices:
   - [speechocean762](https://www.openslr.org/101/): CC BY 4.0, half children.
   - [MyST](https://catalog.ldc.upenn.edu/LDC2021S05): LDC, non-commercial.
   - Never show or publish their audio.

---

## 1. Paired audio-visual human speech datasets

Legend for the "show" columns:

- **Partner** = frames or audio in an internal demo video sent to TUAI partners (non-commercial research).
- **Public** = frames or audio in a public proposal or dissemination.
- Yes / Cond. (conditionally, see notes) / No.

### 1.1 Overview table

| Dataset | Access status (2026-10) | Licence / terms | Partner | Public | Content & framing | Size | Subjects | Children | Key ethics notes | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| **RAVDESS** | Direct download, Zenodo, no registration ([record](https://zenodo.org/records/1188976)) | **CC BY-NC-SA 4.0**. Commercial licence US$9,000 (full) / 8,000 (AV-only) for businesses, 7,000/6,000 for start-ups ([fees](https://smartlaboratory.org/resources/speech-song-database-ravdess/)) | Yes (NC + attribution) | Cond. (BY-NC-SA figure licence + attribution; see 1.2) | Head + upper shoulders, white background, black T-shirts, no glasses (contacts), clean-shaven. Scripted, 2 sentences, neutral North American English. 720p H.264, 48 kHz ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0196391)) | 24.8 GB total (25.6 GB of zips) | 24 professional actors, 21-33 y | No | Paid actors gave written consent; actors whose faces appear in the paper consented to publication ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0196391)) | **Use** (offline benchmark) |
| **Lombard GRID** | Direct download, Zenodo ([record](https://zenodo.org/records/3736465)) | **CC BY 4.0** | Yes | Yes, legally cleanest (attribution). Still personal data, so minimise | Front + side face views from two Logitech C920 webcams on a **bicycle-helmet rig** (helmet and headphones visible in every frame). AKG C414 mic at 30 cm, 48 kHz / 24-bit, sound booth. Scripted GRID sentences ("place green at g 6 again"). Lombard condition = talker hears 80 dB SPL speech-shaped noise in headphones; the recorded speech stays clean ([paper](https://eprints.whiterose.ac.uk/id/eprint/131924/1/jasa-el-slash-8.pdf)) | 2.49 GB total; 1.49 GB without side view | 54 talkers (30 F / 24 M), University of Sheffield staff/students aged 18-30, native British English | No | "All participants were paid... ethics permission was obtained by following the University of Sheffield Ethics Procedure"; the paper says the corpus is released under CC BY 4.0 ([paper](https://eprints.whiterose.ac.uk/id/eprint/131924/1/jasa-el-slash-8.pdf)). Consent to *public display* specifically is not stated. The JSON metadata holds speaker gender: do not use it as a label | **Use** (primary for loudness) |
| GRID (original) | Direct download, Zenodo ([record](https://zenodo.org/records/3625687)) | **CC BY 4.0** | Yes | Yes (attribution) | Facial video; 1,000 sentences per talker; word alignments; no video for talker 21 | 16.2 GB (per-talker zips 355-492 MB; audio_25k.zip 2.61 GB; alignments 20 MB) | 34 talkers (18 M / 16 F) | No | Video file format: the Zenodo text says ".jpg videos" (UNVERIFIED, check after download) | Optional |
| CREMA-D | GitHub + Git LFS (~7.55 GB clone); GitLab mirror if the LFS quota fails; optional user form ([GitHub](https://github.com/CheyneyComputerScience/CREMA-D)) | **ODbL 1.0 + DbCL 1.0** (commercial OK, attribution and share-alike on the database) | Yes | Cond. Copyright-wise OK, but no public statement on actor consent to public display was found, so blur or avoid | Scripted, 12 sentences, 6 emotions, 4 levels (only one sentence has graded levels). FLV/MP3/WAV; resolution UNVERIFIED | 7.55 GB | 91 actors (48 M / 43 F), 20-74 y, multi-ethnic | No | Ships demographics (age, sex, race, ethnicity): never use them as targets | Optional (age-diverse adult voices) |
| VoxCeleb1/2 | **"URLs and timestamps... audio files... video files... no longer available from this website"** ([Vox1](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox1.html), [Vox2](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox2.html)) | Metadata CC BY-SA 4.0. Built without subject notification (UK GDPR Art. 14(5)(b) exemption claimed, [privacy notice](https://www.robots.ox.ac.uk/~vgg/terms/url-lists-privacy-notice.html)) | No | No | In-the-wild celebrity interviews; face tracks | n/a | 1,251 / 6,112 | Possibly | Built by face recognition for speaker identification, the opposite of our goal | **Do not use** |
| LRS2 | BBC Data Sharing Agreement, then password ([page](https://www.robots.ox.ac.uk/~vgg/data/lip_reading/lrs2.html)) | Non-commercial academic research only | No (no redistribution) | No | BBC TV sentences | 50 GB | Thousands (TV) | Possibly | Broadcast copyright | Do not use |
| LRS3 | **Discontinued**: "Downloads are no longer available from this website" ([KAIST](https://mm.kaist.ac.kr/datasets/lip_reading/)); LRS-VoxMM suggested instead | Was CC BY 4.0 (TED) | No | No | TED talks | n/a | ~5k | - | Unofficial HF "preserved mirror" exists ([HF](https://huggingface.co/datasets/TheNHz/ellipsis-lrs3-raw)); do not use withdrawn-data mirrors | **Do not use** |
| AVSpeech | CSV only: train.csv 128 MB, test.csv 9 MB (YouTube ID, start, end, face x/y) ([download](https://looking-to-listen.github.io/avspeech/download.html)) | Annotations CC BY 4.0 (Google); videos belong to uploaders | No | No | ~4,700 h, 290k YouTube videos | Self-scrape | ~unknown | Possibly | Requires YouTube scraping; dead links; no consent | Do not use |
| MEAD | Google Drive / Baidu after the terms are accepted; "download link will be sent once your request is approved" ([terms PDF](https://raw.githubusercontent.com/uniBruce/Mead/master/Terms%20of%20Use_%20Mead.pdf), [page](https://wywu.github.io/projects/MEAD/MEAD.html)) | Non-commercial research only. **"should NOT distribute, copy, reproduce, disclose... any portion... to any third party"**. Colleagues allowed only if bound by the same terms | Cond. (only partners who sign the terms) | **No** | Studio talking faces, 7 views, 8 emotions x 3 intensities | ~40 h per person per view (total GB UNVERIFIED) | 60 actors (48 released in Part0) | No | Actors under formal agreement | Avoid |
| CMU-MOSEI | Features only: "We are not allowed to share the raw videos" ([SDK](https://github.com/CMU-MultiComp-Lab/CMU-MultimodalSDK)) | SDK MIT; videos YouTube | No | No | YouTube monologues | - | ~1,000 | - | No raw video, useless for us | Do not use |
| MELD | Raw tarball at UMich ([GitHub](https://github.com/declare-lab/MELD)) | Repo GPL-3.0; clips from the *Friends* TV series (studio copyright) | No | No | 13,708 utterances, TV sitcom | UNVERIFIED | TV cast | - | Copyrighted TV | Do not use |
| IEMOCAP | Signed release form, USC SAIL ([release](https://sail.usc.edu/iemocap/iemocap_release.htm)) | **"internal research purposes only"**; no passing on without permission; no commercial use; must "consult and discuss any planned performance measures... prior to public reporting" ([licence PDF](https://sail.usc.edu/iemocap/Data_Release_Form_IEMOCAP.pdf)) | No | No | Dyadic acted sessions + mocap | ~12 h | 10 actors | No | Restrictive | Do not use |
| **AMI Meeting Corpus** | Direct per-meeting download ([download](https://groups.inf.ed.ac.uk/ami/download/)); full-size video only via drive order | **CC BY 4.0** ([licence](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml)) | Yes | Cond. (attribution; participants consented under EC-reviewed ethics, [consent page](https://groups.inf.ed.ac.uk/ami/corpus/ethicsandconsent.shtml)); minimise | Seated meeting participants, close-up + room cameras. ~2/3 scenario role-play, 1/3 natural meetings. English (many non-native) | 100 h total. Per meeting: low-size DivX AVI ~400 MB, headset mix ~30 MB; manual annotations 22 MB | Adults; meetings of 3-5 people, design focus on groups of four ([pre-announcement paper](https://infoscience.epfl.ch/bitstreams/f737e755-8723-469d-837e-038d69a61d8d/download)); ~171 meetings (145 scenario + 26 natural, secondary source, [HF card](https://huggingface.co/datasets/knkarthick/AMI)); distinct-person count UNVERIFIED | No | Consent documented | **Use** (multi-person "who is speaking") |
| AVA-ActiveSpeaker | Annotations CC BY 4.0 (Google); 160 YouTube movies, 15 min each ([download](https://sites.research.google/gr/ava/download/)) | Movie copyright with studios | No | No | Films | - | Actors | - | Copyrighted films | Avoid |
| BEAT / BEAT2 | BEAT: "Non-commercial license" ([BEAT](https://pantomatrix.github.io/BEAT/)); BEAT2 HF card says Apache-2.0, 20.3 GB ([HF](https://huggingface.co/datasets/H-Liu1997/BEAT2)). The licences conflict | Motion capture + audio + text; RGB video release UNVERIFIED (not mentioned) | n/a | n/a | 76 h mocap; EN 60 h, ZH 16 h, ES 2 h, JA 2 h | 20.3 GB (BEAT2) | 30 speakers | No | - | Not useful (no camera data) |
| Ego4D / EgoExo4D | Signed licence with each data owner, e.g. Bristol, CMU, Meta ([licence PDF](https://ego4d.github.io/pdfs/Ego4D-Licenses-Draft.pdf)) | Images may be reproduced "in a research publication"; "may not... provide access to the Database... to any third party"; no use in "any program, dataset, or product" | Cond. (publication-style only) | Cond. (research publication only, not a proposal) | First-person (wearer) view | Very large | Thousands | Possibly bystanders | De-identification details UNVERIFIED | Not useful (wrong viewpoint) |
| HDTF | YouTube URLs + crop metadata ([GitHub](https://github.com/MRzzm/HDTF)) | Metadata CC BY 4.0; repo GPL-3.0; videos belong to uploaders | No | No | 512x512 face crops from 720p/1080p YouTube | Self-scrape | ~unknown | - | Scraping; no consent | Do not use |
| CelebV-HQ | YouTube IDs + script ([GitHub](https://github.com/CelebV-HQ/CelebV-HQ)) | Non-commercial research; **"not to further copy, publish or distribute any portion"** | No | No | 35,666 clips, 15,653 identities, 83 attributes | Self-scrape | Celebrities | - | Scraped | Do not use |
| CelebV-Text | Same model ([GitHub](https://github.com/CelebV-Text/CelebV-Text)) | Same agreement as CelebV-HQ | No | No | 70,000 clips, ~279 h | Self-scrape | Celebrities | - | Scraped | Do not use |
| TalkingHead-1KH | YouTube download script ([GitHub](https://github.com/tcwang0509/TalkingHead-1KH)) | Videos stated CC BY 3.0 on YouTube; metadata/scripts MIT | Cond. | Cond. (copyright OK, but no subject consent) | 500k clips, ~80k at >512 px | Self-scrape | Many | Possibly | No consent; YouTube ToS | Avoid |
| **Seamless Interaction** (Meta, 2025) | **Ungated** HF + S3; single example ~100 MB, sample set ~1 GB, batch ~50 GB, full ~27 TB ([GitHub](https://github.com/facebookresearch/seamless_interaction), [HF](https://huggingface.co/datasets/facebook/seamless-interaction)) | **CC BY-NC 4.0** | Yes (NC + attribution) | Cond. (NC + attribution; minimise; no SA) | Dyadic face-to-face conversations (improvised by actors, naturalistic by general participants). 1080p 30 fps, 48 kHz audio, transcripts, VAD, SMPL-H body, keypoints | 4,000+ h | 4,000+ participants | No (adults, UNVERIFIED) | participants.csv holds **Big Five personality scores**: never use as targets | **Use** (1 GB sample, naturalistic robustness) |
| MultiDialog (ACL 2024) | HF audio (ungated) + video on Google Drive ([HF](https://huggingface.co/datasets/IVLLab/MultiDialog)) | HF tag only "cc", variant **UNVERIFIED** (re-checked 2026-10-02; ask jinny960812@kaist.ac.kr) | Cond. | No until the licence is clarified | Actor dyadic dialogues with emotion labels; English | ~340 h, 8,733 dialogues | Actors (count UNVERIFIED) | No | - | Skip |
| Casual Conversations v2 (Meta) | Open access, no cost, with licence ([page](https://ai.meta.com/datasets/casual-conversations-v2-dataset/)) | "Limited license": "You can evaluate models on the provided labels"; "You can only train your model on certain labels". Full text (commercial use, frame publication) UNVERIFIED. Subjects can request removal via casualconversations@meta.com | UNVERIFIED | UNVERIFIED | Paid, consenting adults talking to camera, scripted + unscripted. Self-reported age, gender, disability, physical adornments | 26,467 videos (~1 min), MP4 | 5,567 from Brazil, India, Indonesia, Mexico, Philippines, USA, Vietnam | No | Rich sensitive labels | Optional, only for fairness or robustness checks of non-sensitive outputs |

### 1.2 RAVDESS: exact files, labels, and what the authors say about images

**Files** (from the Zenodo API, record 1188976 v1.0.0, published 2018-04-05). Each Video_Speech zip holds 120 MP4s: 60 trials x 2 modalities (01 = audio-video, 02 = video-only). The audio-only WAVs (03) are in the separate Audio_Speech zip.

| File | Bytes | MB | MD5 |
|---|---:|---:|---|
| Video_Speech_Actor_01.zip | 552968353 | 553.0 | 3c8ececaf392b4a9b11b32271f4f6d01 |
| Video_Speech_Actor_02.zip | 570673024 | 570.7 | a6f40d413b2e6ef25b3a595099e59abb |
| Video_Speech_Actor_03.zip | 567824665 | 567.8 | 68fa240ddd8a3cc410c64efe5fb2b0e4 |
| Video_Speech_Actor_04.zip | 546560009 | 546.6 | 013eed832af1f7e97082aae398a00dbe |
| Video_Speech_Actor_05.zip | 562966425 | 563.0 | b00e17d61374ef6ba86fef35d50a20fb |
| Video_Speech_Actor_06.zip | 568517859 | 568.5 | 3c42877921cc08cfb5c841a0f2cb94a7 |
| Video_Speech_Actor_07.zip | 565652404 | 565.7 | bdd29bfe082f80361ec6b589845c283d |
| Video_Speech_Actor_08.zip | 562573079 | 562.6 | bed5f43d9c18e177e34d4bc1ed9b6d77 |
| Video_Speech_Actor_09.zip | 523489249 | 523.5 | 775da349c50bf915a1bbcb37379bd092 |
| Video_Speech_Actor_10.zip | 565580163 | 565.6 | 70199d1c6902f76e17df308d5c41fa01 |
| Video_Speech_Actor_11.zip | 518634370 | 518.6 | 824504aa41a8fd575e5459d5701dd378 |
| Video_Speech_Actor_12.zip | 557928718 | 557.9 | 2a1f0ddc0ca207beedee6ce2ea863ad7 |
| Video_Speech_Actor_13.zip | 501877549 | 501.9 | c5f2fd4fd77941636947620368c612b5 |
| Video_Speech_Actor_14.zip | 552484059 | 552.5 | 466d31f4cce92a14b1f4ee884bbdf7d7 |
| Video_Speech_Actor_15.zip | 525205576 | 525.2 | 4b3b9bc8473e86f884630f2506684887 |
| Video_Speech_Actor_16.zip | 562416513 | 562.4 | a63c54570ebbe6bd616d0dced5630f7e |
| Video_Speech_Actor_17.zip | 551688845 | 551.7 | 8b7ae3e5a85d2874ac8e1195e722e047 |
| Video_Speech_Actor_18.zip | 565655520 | 565.7 | fef2131ac361da182c0cb85f3d8e8a6c |
| Video_Speech_Actor_19.zip | 581121687 | 581.1 | abb97d97d8c4e88c866cee1cea9d06d6 |
| Video_Speech_Actor_20.zip | 561349264 | 561.3 | 5ddfb22770093bafebdefe8faa449f48 |
| Video_Speech_Actor_21.zip | 590292896 | 590.3 | d810cf2ff6863ef91306fc7a16d74fbb |
| Video_Speech_Actor_22.zip | 560907466 | 560.9 | fee55f72c9871401f23d4b167de3217d |
| Video_Speech_Actor_23.zip | 545177865 | 545.2 | b31e8c8904e66102e7a951694db752d6 |
| Video_Speech_Actor_24.zip | 595799165 | 595.8 | eef90e806c9179bc5b4b098d03647ae3 |
| **Sum, 24 Video_Speech zips** | **13,357,344,723** | **13,357.3 (12.44 GiB)** | |
| Audio_Speech_Actors_01-24.zip | 208468073 | 208.5 | bc696df654c87fed845eb13823edef8a |
| (related) FacialTracking_Actors_01-24.zip, [Zenodo 3255102](https://zenodo.org/records/3255102), CC BY-NC-SA 4.0 | 417163019 | 417.2 | OpenFace 2.1.0 landmarks, head pose, gaze, AUs for all 2,452 trials |

Download URL pattern: `https://zenodo.org/api/records/1188976/files/Video_Speech_Actor_01.zip/content`. Throttle the downloads. During this research Zenodo answered scripted HTML requests with "403... unusual traffic".

**Filename = 7 fields** ([Zenodo description](https://zenodo.org/records/1188976)):

| Field | Values |
|---|---|
| Modality | 01 = AV, 02 = video-only, 03 = audio-only |
| Vocal channel | 01 = speech, 02 = song |
| Emotion | 01-08 |
| Intensity | 01 = normal, 02 = strong (none for neutral) |
| Statement | 01 = "Kids are talking by the door", 02 = "Dogs are sitting by the door" |
| Repetition | 01 / 02 |
| Actor | 01-24 |

Odd/even actor number encodes male/female. Do not use this field as a label.

Per actor: 60 speech trials = neutral (2 statements x 2 reps = 4) + 7 emotions x 2 intensities x 2 statements x 2 reps (56).

**Ground truth usable without touching emotion:**

| Label | Use |
|---|---|
| Statement (kids/dogs) | Keyword or ASR ground truth |
| Repetition | Test-retest stability of inferences |
| Intensity (normal/strong) | Only a **weak proxy** for vocal loudness: confounded with emotion, and audio level normalisation is UNVERIFIED. Better: measure loudness directly (RMS/LUFS) from the 03 audio-only WAV and use that as the continuous target |
| Speech presence | Derive by VAD on the clean audio-only WAV |
| Head pose / gaze reference | From the OpenFace CSVs |
| Constant visual attributes | No glasses, black T-shirt, white background. Good **false-positive controls** for our zero-shot attribute detector |

**What the authors say about images:**
- The Zenodo page and the SMART Lab page say: cite the PLOS ONE paper ("please cite the RAVDESS if it is used in your work in any form"); personal works should link to Zenodo. The licence is CC BY-NC-SA 4.0 and commercial licences are sold ([Zenodo](https://zenodo.org/records/1188976), [SMART Lab](https://smartlaboratory.org/resources/speech-song-database-ravdess/)).
- The PLOS ONE paper states that the actors whose faces are shown "gave written informed consent... to publish these case details" ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0196391)).
- **No explicit FAQ statement about showing actor images in third-party figures or demos was found.** It is UNVERIFIED whether such guidance exists elsewhere, e.g. on the old affectivedatascience.com site, which did not respond.
- Practical reading: a partner demo video is non-commercial research use with attribution, so it is fine. A frame-plus-overlay figure in a public proposal is "Adapted Material" and must carry CC BY-NC-SA 4.0 plus attribution.
- **Action: email ravdess@gmail.com** to confirm proposal/figure use, or use our own recordings for every public visual.

### 1.3 HRI datasets (people talking to a robot)

| Dataset | Access (2026-10) | Terms | Content | Usable? |
|---|---|---|---|---|
| MuMMER (Idiap, 2020) | Zenodo **restricted**; EULA; only "permanent positions in academic or professional organizations"; no Gmail ([Zenodo](https://zenodo.org/records/3989642)) | "strictly restricted to non-commercial research" | 1 h 29 min; 33 clips; 28 participants with Pepper (quiz, chat, route guidance). Kinect v2 + D435 + Pepper camera, RGB-D; faces and IDs annotated. The distributed data is raw: unblurred and with audio ([Idiap](https://www.idiap.ch/en/scientific-research/data/mummer)). [verifier: the total volume is **3.8 TB** per Zenodo, so it is not a quick download] | Internal benchmarking only, if a permanent staff member signs. Closest to the robot viewpoint. Never show it |
| UE-HRI (Telecom Paris, 2017) | Registration + T&C; "research purpose only (not to disseminate)" ([page](https://adasp.telecom-paris.fr/resources/2017-05-18-ue-hri/)) | Research only | Spontaneous interactions with Pepper; mic array, cameras, depth, sonar, laser; ROS bags; engagement labels (participant count UNVERIFIED) | Internal only. Engagement labels are borderline affect inference |
| PInSoRo (children, 2018) | Academics only. **"[update 2024]... we can no longer distribute the full dataset"** (raw video). An anonymised no-video version is on Zenodo, 7.2 GB ([get-dataset](https://freeplay-sandbox.github.io/get-dataset)) | Academic | 120 children, 45 h+ RGB-D free play with a sandtray/robot ([site](https://freeplay-sandbox.github.io/)); age range UNVERIFIED | No video. A clear signal that children's AV data is being withdrawn |
| Vernissage (Idiap, Nao, 2013) | The HRI 2013 paper says "The dataset will be available in March 2013"; current download page and licence UNVERIFIED (Idiap data page did not resolve) ([paper](https://www.idiap.ch/~gatica/publications/Jayagopi-hri13.pdf)) | UNVERIFIED | 13 sessions, Nao as art guide + quiz master with **two** naive participants each, ~11 min per session. Nao VGA mono camera + 4 Nao mics (robot head moves), 3 external cameras, motion capture, close-talk mics. Annotations: speech utterances, transcripts, 2D head location, nodding, visual focus of attention, addressee | Good *method* reference for robot-camera perception with head motion and hall noise. Only if Idiap still distributes it, internal only |
| SHREC (2025) | Access/licence UNVERIFIED ([arXiv 2504.13898](https://arxiv.org/abs/2504.13898)) | - | ~400 real-world HRI videos, 10K+ annotations of robot social errors | Read only |
| SSUP-HRI (2024) | Access UNVERIFIED ([arXiv 2403.10994](https://arxiv.org/abs/2403.10994)) | - | ~15 h, robot trash barrels in public Astor Place NYC; 274 interactions; bystander consent UNVERIFIED | No (public-space bystanders) |
| Furhat egocentric tracking (2026) | Access UNVERIFIED ([arXiv 2606.03694](https://arxiv.org/abs/2606.03694)) | - | Robot-view multi-person tracking; face vs body ID switches | Read for method lessons (body tracking is more stable than face tracking with re-ID) |

Conclusion: no openly licensed, full-body, robot-viewpoint, consented AV dataset exists. **Self-record (Section 5c).**

---

## 2. Audio-only datasets

| Dataset | Access (2026-10) | Licence | Content | Size | Children? | Notes |
|---|---|---|---|---|---|---|
| Common Voice (Scripted Speech) | Via **Mozilla Data Collective**, account required ([cv-dataset](https://github.com/common-voice/cv-dataset), [MDC](https://mozilladatacollective.com/organization/cmfh0j9o10006ns07jq45h7xk)) | **CC0** ("All audio contributions are released under the CC-0 license", [docs](https://github.com/common-voice/cv-dataset/tree/main/datasets/scripted-speech)) | v27.0 (cut-off 2026-09-11): 295 languages, 42,593 h total, 29,295 validated h. Polish included | English 27.0 = 88.43 GB ([MDC](https://mozilladatacollective.com/organization/cmfh0j9o10006ns07jq45h7xk)); Polish size [corrected by verifier: Scripted Speech 27.0 Polish = 4.49 GB, CC0-1.0, per the same MDC page, accessed 2026-10-01] | Opt-in age bracket "teens" = "< 19" ([demographics.ts](https://github.com/common-voice/common-voice/blob/main/web/src/stores/demographics.ts)) | Use for **Polish** ASR/VAD robustness. Do not filter "teens" to build a child set. A "no re-identification" term is UNVERIFIED |
| LibriSpeech | Direct ([OpenSLR 12](https://www.openslr.org/12/)) | CC BY 4.0 | Read audiobooks, English, 16 kHz | test-clean 346 MB; full ~1,000 h | No | Clean ASR baseline |
| VCTK 0.92 | Direct ([DataShare](https://datashare.ed.ac.uk/handle/10283/3443)) | CC BY 4.0 ([licence_text](https://datashare.ed.ac.uk/bitstream/handle/10283/3443/license_text.txt)) | 110 English speakers, ~400 read sentences each, 48 kHz | 10.94 GB | No | Accent variety |
| Multilingual LibriSpeech, Polish | Direct ([OpenSLR 94](https://www.openslr.org/94/)) | CC BY 4.0 | Read Polish audiobooks | 6.2 GB flac / 1.6 GB opus | No | Polish ASR check |
| MyST | LDC ([LDC2021S05](https://catalog.ldc.upenn.edu/LDC2021S05)); fee requires login | "non-commercial projects" only; no publication **except "limited excerpts... in articles, reports"** ([agreement](https://catalog.ldc.upenn.edu/license/myst-childrens-conversational-speech-agreement.pdf)); commercial via Boulder Learning | Conversational science tutoring, ~1,371 students, grades 3-5 | ~470 h | **Yes** | Only for an offline child-ASR WER estimate |
| CSLU Kids | LDC ([LDC2007S18](https://catalog.ldc.upenn.edu/LDC2007S18)), fee | "CSLU Agreement" | 1,100 children, Kindergarten-Grade 10; prompted + spontaneous | ~8-10 min per child | **Yes** | Same as MyST |
| speechocean762 | Direct ([OpenSLR 101](https://www.openslr.org/101/)) | CC BY 4.0 | 5,000 English sentences; Mandarin-L1 speakers; "Half of the speakers are Children"; age and gender provided | 520 MB | **Yes** | Free and easiest child-voice check. Non-native English only; speaker count [corrected by verifier: 250 speakers, half of them children, i.e. ~125 children ([arXiv 2104.01378](https://arxiv.org/abs/2104.01378)); child age range still UNVERIFIED] |
| PF-STAR children | ELRA catalogue ELRA-U-S 0169 ([entry](http://universal.elra.info/product_info.php?cPath=37_39&products_id=1939); page refused connection on 2026-10-02, details from search snippet + [ISCA paper](https://www.isca-archive.org/interspeech_2005/batliner05b_interspeech.html)) | ELRA licence; price and research/commercial terms UNVERIFIED | 611 children; read/imitative native speech in British English, German, Swedish (ages 4-12); non-native English (10-11); spontaneous and *emotional* speech EN/DE (4-14) | 63 h | **Yes** | Skip. Paid, old (2005), and partly emotional speech |

**Should we use children's data at all?**

Default: no. Our pipeline needs no child-specific training. If we display ASR keywords to visitors, we need one number, "how much worse is ASR on 8-14-year-olds", to set the uncertainty display honestly. Get it as follows:
1. Benchmark first on speechocean762 (CC BY 4.0, no signature).
2. Optionally on MyST, under the LDC non-commercial agreement.
3. Never play, show or ship child audio in any demo.
4. At the exhibition, process live and store nothing.

---

## 3. Image person datasets (attribute validation)

| Dataset | Access (2026-10) | Licence | Content / labels | Show? | Ethics | Verdict |
|---|---|---|---|---|---|---|
| **Open Images V7** | Direct (AWS / official downloader) ([facts](https://storage.googleapis.com/openimages/web/factsfigures_v7.html)) | Annotations **CC BY 4.0** (Google); images "listed as having a CC BY 2.0 license", but Google says "verify the license for each image yourself" | 600 boxable classes incl. **Glasses, Sunglasses, Goggles, Hat, Sun hat, Fedora, Cowboy hat, Sombrero, Helmet, Scarf, Tie, Jacket, Coat, Shirt, Dress, Suit, Jeans, Shorts, Skirt, Backpack, Handbag, Headphones, Human face, Person** ([class list](https://storage.googleapis.com/openimages/v7/oidv7-class-descriptions-boxable.csv)). Validation-split boxes (counted 2026-10-01 from [validation-annotations-bbox.csv](https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv)): Glasses 303 boxes / 258 images; Sunglasses 184 / 134; Hat 200 / 145; Sun hat 71 / 60; Fedora 83 / 67; Cowboy hat 52 / 40; Helmet 583 / 315; Jacket 184 / 155; Shirt 95 / 84; Dress 1,288 / 710; Tie 115 / 97; Scarf 38 / 26; Person 16,753 / 7,144; Human face 5,594 / 3,124 [verifier pass 3 re-computed all of these from the CSV on 2026-10-02, and they match. Added counts: Goggles 148 / 112; **Backpack only 32 / 24; Headphones only 40 / 39**, which is too few for a reliable validation estimate, so add the train split or self-recorded data; Boy 1,095 / 579 and Girl 3,622 / 2,135, which shows how common minors are] | Cond. (CC BY 2.0 per image with attribution, after a per-image check; avoid minors) | Contains Man/Woman/Boy/Girl classes, so minors are present. Never use those classes as targets | **Use** for glasses/hat/garment-type validation |
| COCO | Direct ([terms](https://cocodataset.org/#termsofuse)) | Annotations CC BY 4.0; "COCO Consortium does not own the copyright of the images. Use of the images must abide by the Flickr Terms of Use" ([source](https://raw.githubusercontent.com/cocodataset/cocodataset.github.io/master/dataset/termsofuse.htm)). Per-image licence field incl. NC variants (UNVERIFIED list) | Person boxes, keypoints, captions; no attribute labels | Cond. (CC BY-only subset) | Children present | Use only for person detection / keypoint sanity checks |
| PETA | Dropbox/FTP ([page](http://mmlab.ie.cuhk.edu.hk/projects/PETA.html)) | "research purposes only... cannot be used commercially" | 19,000 low-res pedestrian crops (17x39 to 169x365); 8,705 persons; 61 binary + 4 multi-class attributes (incl. clothing colours); compiled from surveillance re-ID sets | No | Surveillance footage; includes gender/age attributes | Internal clothing-colour check only, if needed |
| PA-100K | Google Drive / Baidu ([GitHub](https://github.com/xh-liu/HydraPlus-Net)) | README says CC BY 4.0 | 100,000 images from "real outdoor surveillance cameras"; 26 attributes incl. gender, age, handbag, phone, upper clothing | Copyright yes, but avoid | Surveillance, no consent | Avoid |
| RAP | **rapdataset.com no longer serves the dataset**: it returns a PHP error page (2026-10-01) [corrected by verifier: on 2026-10-01 the host's TLS certificate is issued to unrelated gambling domains (e.g. 365betty-*.com), so the domain looks lapsed or hijacked. Do not visit it or download anything from it] | Agreement-based (historical) | Pedestrian attributes | No | Surveillance | Do not use |
| Market-1501 | Still linked (Google Drive / Baidu) on the lab page ([page](https://zheng-lab-anu.github.io/Project/project_reid.html)); not formally retracted (UNVERIFIED) | Research (no explicit licence found) | Re-ID: 12,936 train + 19,732 test boxes; 27 ID-level attributes added later | No | Campus CCTV-style capture; no consent procedure documented | Avoid (re-ID = identification) |
| CelebA | Direct ([page](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)) | "non-commercial research purposes only"; "agree not to further copy, publish or distribute any portion" | 202,599 images, 10,177 identities, 40 attributes (incl. Eyeglasses, Wearing_Hat, but also Attractive, Male, Young...) | **No** | Scraped celebrities; value-laden labels | Avoid. At most internal glasses/hat benchmarking |
| FairFace | Google Drive ([GitHub](https://github.com/joojs/fairface)) | CC BY 4.0 | Face crops with **race, gender, age** labels | - | Sensitive-attribute design | **Do not use** (we must not infer these) |
| LAION-Face | IDs only, then self-download of ~50M images, ~2 TB ([GitHub](https://github.com/FacePerceiver/LAION-Face)) | Inherits LAION metadata; images belong to third parties | Web-scraped faces | No | LAION took down LAION-5B "and its derivatives" on 2023-12-19 after the CSAM-link report; Re-LAION-5B released 2024-08-30 ([LAION](https://laion.ai/blog/relaion-5b/)). LAION-400M status UNVERIFIED | **Do not use** |
| MS-Celeb-1M, DukeMTMC (also Tiny Images) | Retracted ([Peng et al. 2021](https://arxiv.org/abs/2108.02922)) | - | - | No | Derivatives still circulate | **Do not use** |
| MegaFace | "being decommissioned and MegaFace data are no longer being distributed" ([site](http://megaface.cs.washington.edu/)) | - | - | No | - | **Do not use** |
| Wikimedia Commons | Per-file CC/PD | A CC licence covers only the photographer's copyright, **not the subject's personality rights**; minors require parental consent ([policy](https://commons.wikimedia.org/wiki/Commons:Photographs_of_identifiable_people)) | Any | Cond. | Check personality-rights tags | Mock-ups only |
| Pexels | [Pexels licence](https://www.pexels.com/license/) | Free use, attribution optional; "Identifiable people may not appear in a bad light"; no implied endorsement; no AI/ML clause; model releases UNVERIFIED | Stock photos | Cond. | Showing a stock person being "analysed" could be read as a bad light | UI mock-ups only, preferably without faces |
| Visual Genome | Direct ([site](https://homes.cs.washington.edu/~ranjay/visualgenome/index.html)) | Site links **CC BY 4.0** (checked 2026-10-02). This can only cover the annotations: the images are COCO/Flickr images with their own per-image licences | 108,077 images; 2.8M attributes (e.g. "red shirt"); crowd-sourced, noisy | Cond. (same as COCO) | Flickr/COCO images, minors present | Usable as a *noisy* clothing-colour label source (filter "shirt/jacket + colour" attributes on person boxes); verify a sample by hand |

**No clean public dataset with reliable, consented "clothing colour" labels exists.** Options:
- Annotate 300-500 Open Images person crops ourselves (CC BY 2.0 images, our own labels), or
- Use our self-recorded sessions with a controlled garment set.

---

## 4. Legal and ethical frame relevant to dataset choice

| Rule | Relevance |
|---|---|
| **AI Act Art. 3(39)**: "emotion recognition system" = AI "identifying or inferring emotions or intentions of natural persons on the basis of their biometric data" ([Art. 3](https://artificialintelligenceact.eu/article/3/), [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689)) | Training anything on RAVDESS/CREMA-D/MEAD emotion labels would create one |
| **Annex III(1)(b)-(c)**: biometric categorisation by sensitive attributes and **emotion recognition are high-risk** ([Annex III](https://artificialintelligenceact.eu/annex/3/)) | Keep both out of scope |
| **Art. 5(1)(f)**: emotion recognition banned in workplace and education; **Art. 5(1)(g)**: biometric categorisation by race, political opinion, etc. banned ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689)) | School-group visits make (f) a live risk [corrected by verifier: (f) applies to "workplace and education institutions" and has a medical/safety exception. An exhibition stand is probably outside the literal scope, but treat it as a red line anyway. Since the Digital Omnibus on AI, the Service Desk shows new prohibitions 5(1)(ba)/(bb) on non-consensual intimate deepfakes and CSAM generation, which are irrelevant to us] |
| **Art. 50(3)**: deployers of emotion recognition / biometric categorisation must inform the people exposed ([Art. 50](https://artificialintelligenceact.eu/article/50/)) | Avoid by design |
| **GDPR Art. 4(14)**: facial images are biometric data when specifically processed to "allow or confirm the unique identification"; **Art. 9**: special category ([Art. 4](https://gdpr-info.eu/art-4-gdpr/), [Art. 9](https://gdpr-info.eu/art-9-gdpr/)) | Do no face/speaker embeddings for identity. Session tracking should use body boxes and short-lived IDs |
| **GDPR Art. 89**: research safeguards, minimisation, pseudonymisation ([Art. 89](https://gdpr-info.eu/art-89-gdpr/)) | Applies to our self-recorded data |
| CC licences / ODbL cover copyright and database rights, **not consent or personality rights** ([Commons](https://commons.wikimedia.org/wiki/Commons:Photographs_of_identifiable_people)) | Even CC BY faces are personal data. Minimise and blur in public material unless consent for publication is documented |

---

## 5. Recommendations for our demonstrator

### (a) Minimal, legally clean set for the OFFLINE modality-ablation experiment (camera+audio vs camera-only vs audio-only on real paired samples)

**Download list (~6.2 GB; 6.6 GB with the optional tracking CSVs):**

| # | File(s) | Source | Bytes | Why |
|---|---|---|---:|---|
| 1 | lombardgrid_front.zip | [Zenodo 3736465](https://zenodo.org/records/3736465) | 837,239,327 | Front-face video, plain vs Lombard |
| 2 | lombardgrid_audio.zip | same | 652,614,041 | Paired clean audio |
| 3 | lombardgrid_alignment.zip | same | 2,532,345 | Word-level timing: speech-presence and keyword ground truth |
| 4 | lombardgrid_json.zip | same | 64,938 | Session/block metadata |
| 5 | Video_Speech_Actor_01.zip ... _08.zip | [Zenodo 1188976](https://zenodo.org/records/1188976) | 4,497,735,818 | 8 actors x 60 trials in AV (01) + video-only (02) |
| 6 | Audio_Speech_Actors_01-24.zip | same | 208,468,073 | Audio-only (03) WAVs, 48 kHz (use actors 01-08) |
| 7 (opt.) | FacialTracking_Actors_01-24.zip | [Zenodo 3255102](https://zenodo.org/records/3255102) | 417,163,019 | Reference head pose and gaze (ignore AUs) |
| 8 (opt.) | 1-2 AMI meetings: low-size AVI (~400 MB) + headset mix (~30 MB) + manual annotations (22 MB) | [AMI download](https://groups.inf.ed.ac.uk/ami/download/) | ~0.9 GB | Multi-person "who is speaking", spontaneous speech, CC BY 4.0 |
| 9 (opt.) | Seamless Interaction "sample set" | [GitHub](https://github.com/facebookresearch/seamless_interaction) | ~1 GB | Naturalistic conversation robustness (CC BY-NC 4.0) |

**Tasks and ground truth.** Report each task three ways: A-only, V-only, and A+V (late fusion).

| Task (what the robot "says" about you) | Ground truth | Expected lesson for visitors |
|---|---|---|
| "You are talking now" (frame-level speech activity) | Lombard GRID alignments; RAVDESS VAD on the clean 03 WAV | Audio wins; video (mouth motion) works without sound but fails with the face turned away |
| "You are speaking loudly / with effort" | **Lombard GRID `l` vs `p`** (primary). RAVDESS intensity 02 vs 01 (weak proxy). Measured RMS/LUFS (continuous) | Audio wins. Video gets partial cues (mouth opening, head movement) |
| "You said 'dogs' / 'kids' / a colour word" | RAVDESS statement field; GRID colour word in the utterance code (blue/green/red/white) | Camera-only is near chance: "I can't hear you, so I don't know what you said" |
| "You are wearing glasses / a black top" | RAVDESS: constant negatives/positives (no glasses, black T-shirt) | False-positive control for zero-shot vision |
| "You are wearing a hat / headphones" | Lombard GRID: constant positives (bicycle helmet rig + headphones in every frame) | Shows visitors that the camera reports what it sees, including odd things |
| Stability over time | RAVDESS repetition 01 vs 02; Lombard GRID session 1 vs 2 | Measures how inferences "settle" over seconds |

**Protocol details:**
- Use subject-disjoint splits.
- Report AUROC/F1 plus calibration (ECE, Brier), because the UI will show uncertainty.
- Add a **time-to-confident-inference** curve: seconds of input needed before the posterior passes a threshold. This directly informs the 3-5 min "gradually builds a picture" pacing.
- Run noise-robustness by mixing in exhibition-hall noise we record ourselves; third-party noise-corpus licences are UNVERIFIED. [corrected by verifier: MUSAN (music/speech/noise, ~11 GB) is CC BY 4.0 ([OpenSLR 17](https://www.openslr.org/17/)), so it is a licence-clean add-on for babble and music mixing.]
- Explicitly **exclude** emotion labels and the actor odd/even sex encoding from every model and every report table.

### (b) Image datasets for validating zero-shot visual attributes

| Attribute | Dataset |
|---|---|
| Glasses / sunglasses / hat (+ helmet, scarf, tie, jacket, dress, backpack, headphones) | **Open Images V7**. Use human-verified image-level labels plus boxes; start from the validation-split counts in Section 3. Exclude images also labelled Boy/Girl from anything shown. Keep per-image CC BY 2.0 attribution for any displayed image |
| Clothing colour (no clean labelled source) | Self-annotate 300-500 Open Images person crops with a 10-colour palette (2 annotators, report agreement), plus self-recorded data with a known garment set. Visual Genome attributes (annotations CC BY 4.0) can seed candidate crops ("red shirt", "blue jacket"), but they are crowd-sourced and noisy, so re-check by hand. PETA (research-only, low-res surveillance) is acceptable only for an internal sanity check and never for display |
| Negative controls | RAVDESS (no glasses, uniform clothing, white background) |

### (c) Protocol for a small self-recorded, controlled dataset (adult researchers, rehearsal)

**Goal:** robot-viewpoint, full-body, Polish + English, exhibition-noise data with consent for (optionally) public use. This becomes the **only** source for public visuals.

1. **Approvals.** Talk to SUT's DPO and ethics committee before recording (committee name/procedure UNVERIFIED). Do a short DPIA screening note.
   - Legal basis: consent (GDPR Art. 6(1)(a)).
   - Design out Art. 9: no face/voice identification embeddings are stored.
2. **Participants.** 8-12 consenting adult researchers/colleagues (DC5, DC7, TUAI peers).
   - No minors.
   - No recruitment pressure: supervisors don't recruit their own students without an opt-out.
   - Vary height, clothing, glasses, hats.
3. **Layered consent form**, each item opt-in and separately initialled:
   - (A) internal development use;
   - (B) sharing with named TUAI partners for research;
   - (C) use of stills/video in the public proposal and dissemination (with the right to see the material first);
   - (D) retention beyond the end of the project (default: delete by end of 2027).
   - Withdrawal at any time, with a stated deadline after which already-published material cannot be recalled.
   - Art. 13 information notice; DPO contact.
4. **Hardware.** The actual robot-dog camera and microphone, mounted at robot height, plus one reference webcam at 1.2 m and a clap/LED sync. Record 720p is enough (minimisation).
5. **Script** (~5 min per session, mirrors the exhibition flow; operator ticks a ground-truth sheet in real time):
   - (i) Approach from 3 m to 1 m, stop, turn 90 deg, step out of frame.
   - (ii) Greeting: "Cześć robocie / Hello robot".
   - (iii) Fixed phrases with keywords in PL and EN (reuse "Dogs are sitting by the door" for RAVDESS comparability, plus 2 colour words).
   - (iv) Same phrase whispered / normal / loud (ground truth = loudness condition plus a measured SPL meter reading).
   - (v) Silent mouth movement and silent gestures (camera-only cases).
   - (vi) Props: glasses on/off, cap on/off, jacket colour swap (known garment list), holding an object.
   - (vii) Two people, only one speaking.
   - (viii) Playback of recorded hall noise at ~60 and ~70 dB(A).
   - (ix) Lighting change (warm/cool).
   - (x) Sensor toggles performed by the participant on the UI.
   - Avoid names, badges and logos in frame. Neutral backdrop.
6. **Labels.** Condition timestamps from the script, a garment/props checklist, SPL readings, and VAD verified by a human. **No demographic labels.**
7. **Storage.**
   - Pseudonymous IDs (P01...); the consent forms stored separately (paper or locked).
   - Encrypted at rest. Windows 11 Home provides **Device Encryption, not full BitLocker** ([Microsoft](https://support.microsoft.com/en-us/windows/device-encryption-in-windows-cf7e2b6f-3e70-4882-9532-18633605b7df)); use it or a VeraCrypt container, or university-managed storage.
   - No upload to cloud AI APIs.
   - Access list; deletion log; retention end date.
8. **Use.** Rehearsal (end-to-end latency on the Core Ultra 7 255U), threshold calibration, robot-viewpoint domain-gap measurement against the RAVDESS/GRID numbers, and the partner demo video. Only items with consent (C) may appear in the proposal.

---

## 6. Pitfalls / what not to do

- **Do not download from unofficial mirrors** of withdrawn data (LRS3 on HF, VoxCeleb re-uploads, MS-Celeb/Duke derivatives). Peng et al. show that retracted datasets keep doing harm through derivatives ([arXiv](https://arxiv.org/abs/2108.02922)).
- **Do not scrape YouTube-ID datasets** (AVSpeech, HDTF, CelebV-HQ/Text, TalkingHead-1KH). Links are dead, the subjects never consented, and the frames cannot be shown.
- **Do not train or show emotion, gender, age, race or personality inference**, even though the labels are right there (RAVDESS/CREMA-D/MEAD emotion; CREMA-D demographics; FairFace; PA-100K; Seamless BFI-2; Casual Conversations v2). This means AI Act Annex III / Art. 5(1)(f)-(g) risk and contradicts our "no sensitive attributes" promise. Also watch VLM outputs that volunteer "a young woman", and filter them.
- **Do not treat RAVDESS intensity as true loudness.** It is emotional intensity and confounded with emotion. Use Lombard GRID or measured SPL/LUFS.
- **Do not put MEAD, CelebV, CelebA, IEMOCAP, MuMMER, UE-HRI or Ego4D frames into anything external.** Their terms forbid disclosure or limit it to research publications.
- **Do not treat a CC licence as consent.** CC BY Open Images/COCO/AMI people are still identifiable data subjects, and many Open Images/COCO images contain minors.
- **Do not over-trust benchmark numbers.** RAVDESS and GRID are frontal, studio-lit, head-and-shoulders adults at ~1.4 m (RAVDESS) or on a head-mounted camera (Lombard GRID). Our robot camera sees children from below, moving, in a noisy hall. Expect a large domain gap; measure it on self-recorded data.
- **Do not rely on GitHub LFS for CREMA-D** (bandwidth quota). Use the GitLab mirror.
- **Do not hammer Zenodo.** Scripted requests can trigger "403... unusual traffic". Throttle and resume downloads.
- **Do not record children for development.** PInSoRo stopped distributing children's video in 2024 after an ethics-policy change. Expect the same scrutiny for us.
- **Do not use English-only results to promise Polish performance.** Check ASR on Common Voice Polish / MLS Polish.

---

## 7. Sources (accessed 2026-10-01)

- RAVDESS Zenodo: https://zenodo.org/records/1188976 (API: https://zenodo.org/api/records/1188976)
- RAVDESS paper (PLOS ONE 2018): https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0196391
- RAVDESS SMART Lab page / commercial fees: https://smartlaboratory.org/resources/speech-song-database-ravdess/
- RAVDESS Facial Landmark Tracking: https://zenodo.org/records/3255102
- Lombard GRID: https://zenodo.org/records/3736465
- GRID: https://zenodo.org/records/3625687
- CREMA-D: https://github.com/CheyneyComputerScience/CREMA-D ; https://cheyneycomputerscience.github.io/CREMA-D/ ; https://gitlab.com/cs-cooper-lab/crema-d-mirror
- VoxCeleb: https://www.robots.ox.ac.uk/~vgg/data/voxceleb/ ; vox1.html ; vox2.html ; privacy notice https://www.robots.ox.ac.uk/~vgg/terms/url-lists-privacy-notice.html
- LRS2: https://www.robots.ox.ac.uk/~vgg/data/lip_reading/lrs2.html ; LRS3 (KAIST): https://mm.kaist.ac.kr/datasets/lip_reading/ ; unofficial mirror: https://huggingface.co/datasets/TheNHz/ellipsis-lrs3-raw
- AVSpeech: https://looking-to-listen.github.io/avspeech/download.html
- MEAD: https://wywu.github.io/projects/MEAD/MEAD.html ; terms https://raw.githubusercontent.com/uniBruce/Mead/master/Terms%20of%20Use_%20Mead.pdf
- CMU Multimodal SDK: https://github.com/CMU-MultiComp-Lab/CMU-MultimodalSDK
- MELD: https://github.com/declare-lab/MELD
- IEMOCAP: https://sail.usc.edu/iemocap/iemocap_release.htm ; https://sail.usc.edu/iemocap/Data_Release_Form_IEMOCAP.pdf
- AMI: https://groups.inf.ed.ac.uk/ami/corpus/ ; licence https://groups.inf.ed.ac.uk/ami/corpus/license.shtml ; consent https://groups.inf.ed.ac.uk/ami/corpus/ethicsandconsent.shtml ; download https://groups.inf.ed.ac.uk/ami/download/
- AVA: https://sites.research.google/gr/ava/download/
- BEAT: https://pantomatrix.github.io/BEAT/ ; BEAT2: https://huggingface.co/datasets/H-Liu1997/BEAT2
- Ego4D licence: https://ego4d.github.io/pdfs/Ego4D-Licenses-Draft.pdf
- HDTF: https://github.com/MRzzm/HDTF
- CelebV-HQ: https://github.com/CelebV-HQ/CelebV-HQ ; CelebV-Text: https://github.com/CelebV-Text/CelebV-Text
- TalkingHead-1KH: https://github.com/tcwang0509/TalkingHead-1KH
- Seamless Interaction: https://github.com/facebookresearch/seamless_interaction ; https://huggingface.co/datasets/facebook/seamless-interaction
- MultiDialog: https://huggingface.co/datasets/IVLLab/MultiDialog
- Casual Conversations v2: https://ai.meta.com/datasets/casual-conversations-v2-dataset/
- MuMMER: https://www.idiap.ch/en/scientific-research/data/mummer ; https://zenodo.org/records/3989642
- UE-HRI: https://adasp.telecom-paris.fr/resources/2017-05-18-ue-hri/
- PInSoRo: https://freeplay-sandbox.github.io/ ; https://freeplay-sandbox.github.io/get-dataset
- SHREC: https://arxiv.org/abs/2504.13898 ; SSUP-HRI: https://arxiv.org/abs/2403.10994 ; Furhat tracking: https://arxiv.org/abs/2606.03694
- Common Voice: https://github.com/common-voice/cv-dataset ; https://mozilladatacollective.com/organization/cmfh0j9o10006ns07jq45h7xk ; demographics https://github.com/common-voice/common-voice/blob/main/web/src/stores/demographics.ts
- LibriSpeech: https://www.openslr.org/12/ ; MLS: https://www.openslr.org/94/ ; speechocean762: https://www.openslr.org/101/
- VCTK: https://datashare.ed.ac.uk/handle/10283/3443
- MyST: https://catalog.ldc.upenn.edu/LDC2021S05 ; agreement https://catalog.ldc.upenn.edu/license/myst-childrens-conversational-speech-agreement.pdf
- CSLU Kids: https://catalog.ldc.upenn.edu/LDC2007S18
- COCO terms: https://cocodataset.org/#termsofuse (source: https://raw.githubusercontent.com/cocodataset/cocodataset.github.io/master/dataset/termsofuse.htm)
- Open Images V7: https://storage.googleapis.com/openimages/web/factsfigures_v7.html ; classes https://storage.googleapis.com/openimages/v7/oidv7-class-descriptions-boxable.csv ; val boxes https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv
- PETA: http://mmlab.ie.cuhk.edu.hk/projects/PETA.html ; PA-100K: https://github.com/xh-liu/HydraPlus-Net ; RAP: http://www.rapdataset.com/ (broken) ; Market-1501: https://zheng-lab-anu.github.io/Project/project_reid.html
- CelebA: https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html ; FairFace: https://github.com/joojs/fairface ; LAION-Face: https://github.com/FacePerceiver/LAION-Face ; Re-LAION: https://laion.ai/blog/relaion-5b/
- Retracted datasets: https://arxiv.org/abs/2108.02922 ; MegaFace: http://megaface.cs.washington.edu/
- Visual Genome: https://homes.cs.washington.edu/~ranjay/visualgenome/index.html
- Wikimedia Commons personality rights: https://commons.wikimedia.org/wiki/Commons:Photographs_of_identifiable_people ; Pexels licence: https://www.pexels.com/license/
- EU AI Act (EUR-Lex): https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689 ; Art. 3: https://artificialintelligenceact.eu/article/3/ ; Annex III: https://artificialintelligenceact.eu/annex/3/ ; Art. 50: https://artificialintelligenceact.eu/article/50/
- GDPR: https://gdpr-info.eu/art-4-gdpr/ ; https://gdpr-info.eu/art-9-gdpr/ ; https://gdpr-info.eu/art-89-gdpr/
- Windows Device Encryption: https://support.microsoft.com/en-us/windows/device-encryption-in-windows-cf7e2b6f-3e70-4882-9532-18633605b7df
- Added 2026-10-02: Lombard GRID paper https://eprints.whiterose.ac.uk/id/eprint/131924/1/jasa-el-slash-8.pdf ; Vernissage paper https://www.idiap.ch/~gatica/publications/Jayagopi-hri13.pdf ; PF-STAR https://www.isca-archive.org/interspeech_2005/batliner05b_interspeech.html ; Speech Commands https://www.tensorflow.org/datasets/catalog/speech_commands ; AMI overview https://groups.inf.ed.ac.uk/ami/corpus/overview.shtml ; MUSAN https://www.openslr.org/17/ ; AI Act Service Desk https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5

---

## Verification log

The independent verifier re-checked these claims on 2026-10-01 with fresh fetches of primary sources. Zenodo blocked direct scripted API calls (403), so Zenodo checks went through WebFetch instead.

| # | Claim | Verdict | Source |
|---|---|---|---|
| 1 | RAVDESS: CC BY-NC-SA 4.0; 24 actors (12F/12M); two statements; 7-field filename; Audio_Speech zip 208.5 MB | Confirmed | https://zenodo.org/records/1188976 |
| 2 | RAVDESS byte sizes for Video_Speech_Actor_01-08 (sum 4,497,735,818) and Audio_Speech (208,468,073) | Confirmed (Zenodo API values match exactly; the verifier recomputed the sum) | https://zenodo.org/api/records/1188976 |
| 3 | RAVDESS actors aged 21-33, black T-shirts, contacts (no glasses), clean-shaven, white background; 720p export, 48 kHz; actors shown in the paper gave written consent to publish | Confirmed | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0196391 |
| 4 | RAVDESS commercial licence US$9,000/8,000 (business), 7,000/6,000 (start-up); no guidance on actor images | Confirmed | https://smartlaboratory.org/resources/speech-song-database-ravdess/ |
| 5 | Lombard GRID: CC BY 4.0, 54 talkers (30F/24M), 5,400 utterances; front 837.2 MB, audio 652.6 MB, side 992.6 MB, alignment 2.5 MB, json 64.9 kB (core 1.49 GB; 2.49 GB with side view) | Confirmed. No consent information appears on the Zenodo page, so it stays UNVERIFIED | https://zenodo.org/records/3736465 |
| 6 | GRID original: CC BY 4.0, 34 talkers (18M/16F), 16.2 GB, no video for t21, "JPG format videos" | Confirmed | https://zenodo.org/records/3625687 |
| 7 | VoxCeleb1: URLs/timestamps and audio "no longer available from this website"; metadata CC BY-SA 4.0 | Confirmed | https://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox1.html |
| 8 | LRS3 discontinued, LRS-VoxMM suggested; LRS2 needs a BBC agreement, non-commercial academic, ~50 GB | Confirmed | https://mm.kaist.ac.kr/datasets/lip_reading/ ; https://www.robots.ox.ac.uk/~vgg/data/lip_reading/lrs2.html |
| 9 | CREMA-D: ODbL 1.0 + DbCL 1.0; 91 actors (48M/43F), 20-74 y; 7,442 clips; 12 sentences; Git LFS ~7.55 GB; GitLab mirror; demographics CSV | Confirmed | https://github.com/CheyneyComputerScience/CREMA-D |
| 10 | Seamless Interaction: CC BY-NC 4.0; ungated; 4,000+ h and 4,000+ participants; 1080p 30 fps, 48 kHz; ~1 GB sample, ~27 TB full; BFI-2 personality metadata | Confirmed (GitHub README: "Participant personality (BFI-2)") | https://github.com/facebookresearch/seamless_interaction ; https://huggingface.co/datasets/facebook/seamless-interaction |
| 11 | AMI: CC BY 4.0; low-size DivX AVI ~400 MB, headset mix 30 MB per meeting; full-size video only by drive order | Confirmed | https://groups.inf.ed.ac.uk/ami/corpus/license.shtml ; https://groups.inf.ed.ac.uk/ami/download/ |
| 12 | MEAD terms: non-commercial only; "should NOT distribute, copy, reproduce, disclose... any portion... to any third party"; colleagues only if bound | Confirmed (verifier extracted the PDF text) | https://raw.githubusercontent.com/uniBruce/Mead/master/Terms%20of%20Use_%20Mead.pdf |
| 13 | CelebA and CelebV-HQ: non-commercial, "not to further copy, publish or distribute any portion" | Confirmed | https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html ; https://github.com/CelebV-HQ/CelebV-HQ |
| 14 | Ego4D licence: images may be reproduced only in research/academic publications (or a website carrying them) | Confirmed | https://ego4d-data.org/pdfs/Ego4D-Licenses-Draft.pdf |
| 15 | MuMMER: Zenodo restricted, EULA, non-commercial, permanent-position signatories, no Gmail; 1 h 29 min, 33 clips, Pepper | Confirmed. The "28 participants" count was not visible on Zenodo and is not re-verified | https://zenodo.org/records/3989642 |
| 16 | PInSoRo: "[update 2024]... we can no longer distribute the full dataset" (Plymouth ethics policy); 7.2 GB no-video version; academics only | Confirmed | https://freeplay-sandbox.github.io/get-dataset |
| 17 | UE-HRI: "research purpose only (not to disseminate)" | Confirmed | https://adasp.telecom-paris.fr/resources/2017-05-18-ue-hri/ |
| 18 | Common Voice on Mozilla Data Collective, CC0; v27.0 with 295 languages and 42,593/29,295 h; English 88.43 GB | Confirmed. Polish size added: 4.49 GB. Whether an account is required is not explicitly stated ("Sign up" is shown), so treat it as likely | https://github.com/common-voice/cv-dataset ; https://mozilladatacollective.com/organization/cmfh0j9o10006ns07jq45h7xk |
| 19 | MLS Polish CC BY 4.0, 6.2 GB flac / 1.6 GB opus; VCTK 0.92 CC BY 4.0, 110 speakers, 10.94 GB | Confirmed | https://www.openslr.org/94/ ; https://datashare.ed.ac.uk/handle/10283/3443 |
| 20 | MyST: ~470 h, 1,371 students, grades 3-5, non-commercial; "limited excerpts... in articles, reports" | Confirmed (verifier extracted the agreement PDF text) | https://catalog.ldc.upenn.edu/LDC2021S05 |
| 21 | speechocean762: CC BY 4.0, 520 MB, half the speakers children | Confirmed. Speaker count added: 250 | https://www.openslr.org/101/ ; https://arxiv.org/abs/2104.01378 |
| 22 | Open Images: annotations CC BY 4.0, images CC BY 2.0, verify each image | Confirmed (official repo). The validation-split box counts were **not** re-computed in pass 1 [pass 3 re-computed them from the CSV, and they match exactly] | https://github.com/openimages/dataset |
| 23 | PA-100K README says CC BY 4.0; 100k surveillance images; 26 attributes incl. gender/age | Confirmed | https://github.com/xh-liu/HydraPlus-Net |
| 24 | rapdataset.com broken | Corrected/extended: the TLS certificate belongs to unrelated gambling domains, so the domain looks lapsed or hijacked | http://www.rapdataset.com/ (TLS error on fetch) |
| 25 | LAION-5B and derivatives taken down 2023-12-19; Re-LAION-5B released 2024-08-30 | Confirmed (the blog does not mention LAION-400M being taken down) | https://laion.ai/blog/relaion-5b/ |
| 26 | MegaFace decommissioned, no longer distributed | Confirmed | http://megaface.cs.washington.edu/ |
| 27 | AI Act Annex III(1)(b) biometric categorisation by sensitive attributes and (1)(c) emotion recognition are high-risk | Confirmed | https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3 |
| 28 | AI Act Art. 5(1)(f) emotion inference in workplace/education; 5(1)(g) biometric categorisation by race, political opinions etc. | Confirmed wording, with a nuance: (f) says "education institutions" and has a medical/safety exception. Digital Omnibus amendments are noted inline | https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5 |

## Omissions added by verifier

- **AI Act "Digital Omnibus on AI" amendments (2026).** The Commission's AI Act Service Desk carries "Digital Omnibus" disclaimers on Art. 5 and Art. 113.
  - It shows new prohibitions Art. 5(1)(ba) (non-consensual intimate deepfakes) and 5(1)(bb) (CSAM generation).
  - It lists **2 Dec 2027** as the date Annex III high-risk obligations apply, instead of 2 Aug 2026.
  - Our dataset choices do not change. But any legal section elsewhere in the project that cites "high-risk obligations from 2 Aug 2026" should be updated. [verifier pass 3: now confirmed in the OJ. It is Regulation (EU) 2026/1744 of 8 July 2026, OJ L 24.7.2026, in force 27 July 2026: Annex III from 2 Dec 2027, Annex I from 2 Aug 2028. https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng . Secondary sources disagree on when the new 5(1)(ba)/(bb) bans apply: nicfab.eu says 2 Dec 2026, Lewis Silkin says on entry into force. Neither affects us.]
  - Sources: https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5 ; https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113
- **Common Voice Spontaneous Speech v5.0.** 80 languages, 541 h (302 validated), on MDC. Spontaneous (non-read) speech is closer to how visitors actually talk than Scripted Speech. Check whether Polish is included (UNVERIFIED). Source: https://github.com/common-voice/cv-dataset
- **MUSAN noise/music/babble corpus.** CC BY 4.0, ~11 GB ([OpenSLR 17](https://www.openslr.org/17/)). A licence-clean source for noise-robustness mixing besides our own hall recordings, which closes the "noise-corpus licences UNVERIFIED" gap in 5(a).
- **Google Speech Commands v2.** One-second keyword clips, a natural ground truth for a "you said a keyword" demo. Dataset licence confirmed 2026-10-02 as **CC BY 4.0** on the TensorFlow Datasets catalogue; download 2.37 GiB; TFDS splits 85,511 / 10,102 / 4,890 clips. English only. https://www.tensorflow.org/datasets/catalog/speech_commands ; https://arxiv.org/abs/1804.03209
- **Practical note.** Zenodo returned HTTP 403 to plain `curl` API calls from this machine on 2026-10-01 (the report also notes this). Budget for browser-based or throttled downloads, and verify MD5 checksums against the Zenodo record.

## Continuation pass (2026-10-02)

Gaps from the first pass that were re-checked against primary sources:

| Item | Result | Source |
|---|---|---|
| Lombard GRID consent and setup | Paid University of Sheffield staff/students aged 18-30; "ethics permission was obtained by following the University of Sheffield Ethics Procedure"; CC BY 4.0 stated in the paper; helmet-mounted Logitech C920 front + side cameras; 80 dB SPL speech-shaped noise via headphones; 48 kHz / 24-bit AKG C414 at 30 cm. Consent to public display is not stated explicitly, so blur faces in public material or use our own recordings | https://eprints.whiterose.ac.uk/id/eprint/131924/1/jasa-el-slash-8.pdf |
| Vernissage | 13 sessions x ~11 min, Nao + 2 participants, Nao VGA camera + 4 mics, 3 external cameras, mocap; rich annotations (VFOA, addressee, nodding). The paper only promised availability "in March 2013"; current distribution is UNVERIFIED | https://www.idiap.ch/~gatica/publications/Jayagopi-hri13.pdf |
| PF-STAR | ELRA-U-S 0169, 63 h, 611 children aged 4-14, EN/DE/SV; ELRA price and terms UNVERIFIED (catalogue refused the connection) | http://universal.elra.info/product_info.php?cPath=37_39&products_id=1939 |
| Visual Genome | Site links CC BY 4.0 (annotations); images keep COCO/Flickr per-image licences | https://homes.cs.washington.edu/~ranjay/visualgenome/index.html |
| Speech Commands | CC BY 4.0, 2.37 GiB | https://www.tensorflow.org/datasets/catalog/speech_commands |
| Casual Conversations v2 | "Limited license"; evaluation on provided labels; training only on certain labels; 7 countries; removal requests via casualconversations@meta.com | https://ai.meta.com/datasets/casual-conversations-v2-dataset/ |
| MultiDialog | HF licence tag still just "cc"; video on Google Drive | https://huggingface.co/datasets/IVLLab/MultiDialog |
| Common Voice Spontaneous Speech v5.0 | CC0, 541 h / 302 h validated, 80 languages; Polish inclusion still UNVERIFIED | https://github.com/common-voice/cv-dataset/tree/main/datasets/spontaneous-speech |
| AMI | 100 h, English, mostly non-native speakers, ~2/3 scenario meetings; groups of 3-5 (focus on four) | https://groups.inf.ed.ac.uk/ami/corpus/overview.shtml ; https://infoscience.epfl.ch/bitstreams/f737e755-8723-469d-837e-038d69a61d8d/download |

## Verification log (pass 3, 2026-10-02)

The third independent adversarial pass re-checked these claims with fresh primary-source fetches.

| # | Claim | Verdict | Source |
|---|---|---|---|
| V1 | Lombard GRID: CC BY 4.0; 54 talkers (30F/24M); front 837.2 MB, audio 652.6 MB, alignment 2.5 MB, json 64.9 kB, side 992.6 MB | Confirmed | https://zenodo.org/records/3736465 |
| V2 | RAVDESS: CC BY-NC-SA 4.0; 24 actors; kids/dogs statements; intensity 01/02; odd = male, even = female; Actor_13 501.9 MB, Actor_24 595.8 MB, Audio_Speech 208.5 MB | Confirmed | https://zenodo.org/records/1188976 |
| V3 | RAVDESS commercial licence US$9,000/8,000 (business), 7,000/6,000 (start-up); no guidance on actor images; contact ravdess@gmail.com | Confirmed | https://smartlaboratory.org/resources/speech-song-database-ravdess/ |
| V4 | VoxCeleb2 URLs/timestamps, audio and video "no longer available from this website"; metadata CC BY-SA 4.0 | Confirmed | https://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox2.html |
| V5 | LRS3 "Downloads are no longer available from this website"; LRS-VoxMM suggested | Confirmed | https://mm.kaist.ac.kr/datasets/lip_reading/ |
| V6 | PInSoRo "[update 2024]... we can no longer distribute the full dataset" (Plymouth ethics policy); 7.2 GB anonymised no-video version; academics only | Confirmed | https://freeplay-sandbox.github.io/get-dataset |
| V7 | Seamless Interaction: CC BY-NC 4.0; ungated (S3 + HF); 4,000+ h / 4,000+ participants; 1080p; ~1 GB sample, ~27 TB full; BFI-2 personality included | Confirmed. Whether minors are included is not stated (keep UNVERIFIED) | https://github.com/facebookresearch/seamless_interaction |
| V8 | IEMOCAP: "internal research purposes only"; no passing on; no commercial use; consult on "planned performance measures... prior to public reporting" | Confirmed (verifier extracted the release-form PDF text) | https://sail.usc.edu/iemocap/Data_Release_Form_IEMOCAP.pdf |
| V9 | MuMMER: Zenodo restricted, EULA, non-commercial, permanent-position requesters; 1 h 29 min, 33 clips, Pepper | Confirmed. Added: total volume 3.8 TB | https://zenodo.org/records/3989642 |
| V10 | AI Act Art. 5(1)(f)/(g) wording; Annex III from 2 Dec 2027 after the Digital Omnibus | Confirmed and upgraded from "UNVERIFIED in OJ" to adopted: Regulation (EU) 2026/1744 of 8 July 2026, OJ L 24.7.2026, in force 27.7.2026; Annex I from 2 Aug 2028 | https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5 ; https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng ; https://www.nicfab.eu/en/posts/digital-omnibus-ai-official-journal/ |
| V11 | Open Images V7 validation counts (Glasses 303/258, Sunglasses 184/134, Hat 200/145, Helmet 583/315, Dress 1,288/710, Person 16,753/7,144, etc.) | Confirmed: re-computed from validation-annotations-bbox.csv (25.1 MB). Added: Backpack 32/24 and Headphones 40/39 are thin | https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv |
| V12 | Common Voice: v27.0 (2026-09), 295 languages, 42,593 h / 29,295 validated; Polish Scripted 27.0 = 4.49 GB, CC0-1.0; Spontaneous v5.0, 80 languages | Confirmed. **No Polish Spontaneous Speech dataset** is listed on MDC (this resolves the earlier UNVERIFIED) | https://github.com/common-voice/cv-dataset ; https://mozilladatacollective.com/organization/cmfh0j9o10006ns07jq45h7xk |
| V13 | speechocean762: CC BY 4.0, 520 MB, 250 speakers, half children | Confirmed. Child age range still not stated in the abstract | https://www.openslr.org/101/ ; https://arxiv.org/abs/2104.01378 |
| V14 | MyST LDC2021S05: ~470 h, 1,371 students, grades 3-5, custom agreement; commercial via Boulder Learning | Confirmed. Fee is behind a login | https://catalog.ldc.upenn.edu/LDC2021S05 |
| V15 | CSLU Kids LDC2007S18: 1,100 children, K-Grade 10 | Confirmed ("CSLU Agreement", non-commercial) | https://catalog.ldc.upenn.edu/LDC2007S18 |
| V16 | MLS Polish CC BY 4.0, 6.2 GB flac / 1.6 GB opus; MUSAN CC BY 4.0 ~11 GB | Confirmed | https://www.openslr.org/94/ ; https://www.openslr.org/17/ |
| V17 | Speech Commands: CC BY 4.0, 2.37 GiB, 85,511/10,102/4,890 | Size and splits confirmed on TFDS. Licence confirmed only from the arXiv paper's CC BY 4.0 link (paper-level); dataset-level CC BY 4.0 is stated in the paper body, per prior pass | https://www.tensorflow.org/datasets/catalog/speech_commands ; https://arxiv.org/abs/1804.03209 |
| V18 | AMI: CC BY 4.0 | Confirmed ("The AMI corpus and its annotations are released under the Creative Commons Attribution 4.0 license") | https://groups.inf.ed.ac.uk/ami/corpus/license.shtml |

## Omissions added by verifier (pass 3)

- **JIBO Kids Corpus (2024; Zenodo release v1.0.0).** **CC BY 4.0**, about 2.75 GB (two split archives of 1.9 GB + 851.6 MB). It has 110 children aged ~4-7 (pre-K to grade 1) talking to the JIBO **social robot** in a classroom, 21 h of sessions, 16 kHz WAV plus word-level transcripts. Audio only. It is the only openly licensed child-to-robot speech corpus found, so it is a better free child-ASR stress test than speechocean762 for "robot in a noisy room". The children are younger than our 8-14 target. Never play or show the audio. Sources: https://zenodo.org/records/19604408 ; https://github.com/balaji1312/Jibo_Kids ; https://pubs.aip.org/asa/jel/article/4/11/115201/3318582/The-JIBO-Kids-Corpus-A-speech-dataset-of-child
- **PAVSig (Scientific Data, 2025): Polish audio-visual child speech.** It has 201 children aged 4-8, recorded in Polish kindergartens and schools in 2021-2023. Video is cropped to the oral region only, and there is 15-channel audio. Access is under a Data Use Agreement on Harvard Dataverse (doi:10.7910/DVN/IHZRGB). It is a clinical (sigmatism) dataset, so it is relevant only as a Polish child-speech reference and as a **Polish precedent for guardian consent and privacy cropping**. Do not use it for training or display. Sources: https://www.nature.com/articles/s41597-025-05896-8 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12491466/
- **BIGOS V2 (NeurIPS 2024 D&B): curated Polish ASR benchmark.** It is on HF as `amu-cai/pl-asr-bigos-v2`: CC BY-SA 4.0, **gated (accept terms)**, 27.8 GB, 12 sources including Common Voice, MLS, FLEURS and CLARIN-PL. It includes a toolkit benchmarking 29 Polish ASR system/model combinations. It is a ready-made answer to the "Polish ASR performance" pitfall. The companion "PELCRA for BIGOS" (conversational Polish) is CC BY-NC-ND. No child subset. Sources: https://huggingface.co/datasets/amu-cai/pl-asr-bigos-v2 ; https://github.com/goodmike31/pl-asr-bigos-tools
- **Embody 3D (Meta Codec Avatars, Oct 2025).** It has 439 participants and 500 h of 3D motion with hand tracking, body shape, text and per-participant audio. It is a full-body multi-person dataset, but its licence terms (Meta licence agreement) are **UNVERIFIED**, and it ships tracked motion rather than plain RGB robot-view video. Low priority. Sources: https://arxiv.org/abs/2510.16258 ; https://github.com/facebookresearch/embody-3d
- **Common Voice Polish spontaneous speech does not exist** (as of v5.0 on MDC). Spontaneous-Polish robustness has to come from PELCRA (NC-ND) or our own recordings.
