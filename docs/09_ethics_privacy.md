# 09 - Ethics, privacy and child safety

Purpose: the legal frame, attribute register, privacy controls, notices and approval plan for "How does a robot see you?" at Science is Wonderful! 2027 (SiW), aligned with `docs/_brief.md`.

**Key points**
- Not legal advice. The SUT Data Protection Officer (DPO) signs off.
- The GDPR applies even though nothing is saved: live camera and microphone processing is processing. Lawful basis is **public task, Art. 6(1)(e)**. The opt-in switches are an ethical safeguard and an easy way to object, not the legal basis. Art. 8 does not apply. Art. 9 is avoided because we never identify anyone and never output anything that could reveal a sensitive trait.
- The AI Act's **Art. 5 (since 2 Feb 2025) and Art. 50 (since 2 Aug 2026)** bind us at the fair. The Digital Omnibus moved Annex III high-risk duties to 2 Dec 2027. With this design the exhibit is not high-risk anyway.
- The robot fills **6 child-safe slots only**. Hat detection was built and then **removed** (headwear can reveal religion). Energy and voice are **momentary readings**. Speaking speed and pitch are not labelled.
- The prototype already has the allow-list, no embeddings, keyword-only audio output, a pixelated view, an in-RAM ledger and machine-readable AI marking. Its live mode starts with both sensors off and drops a switched-off sensor's frames and sound before any model sees them. For the exhibition we still need to release the device and stop capture on the Pi when a sense is off, a lens shutter, an offline firewall, a no-write test, the forget-me button, ROI (region of interest) masking and the DPIA (data protection impact assessment).
- The optional "robot's imagination" picture restyles the robot's own avatar drawing. It never sees camera pixels, never draws a human likeness, and is labelled and machine-marked as AI-generated.
- Takeaway: **nothing by default, plus a visible "forget me"**. Optionally, an offline printed card with no photo and no name. No QR code and no email.
- Biggest open decision: the DPO's position on SUT Order 50/2024 §5(3) (guardian consent for minors' images). It decides Plan A or Plan B and must be settled in **November 2026**.
- Every booth staffer needs an SUT register check plus criminal-record information from the Polish National Criminal Register (KRK). Anyone with foreign citizenship or foreign residence in the last 20 years also needs a foreign criminal-record certificate, or a sworn statement where that country issues none (Art. 21, Polish Act of 13 May 2016). Request foreign certificates in **January 2027**. File the HR register request in **February 2027** (absolute deadline 9 Mar 2027).
- The SiW form has no ethics or data-protection field. The proposal carries the short "Privacy" paragraph in B2 (`docs/08`). The full statement in §8 is for the organisers after selection, the DPIA and the TUAI consortium.

---

## 1. Legal frame in plain language

### 1.1 GDPR (Regulation (EU) 2016/679)

| Question | Answer for our booth | Reference |
|---|---|---|
| Does the GDPR apply if we store nothing? | **Yes.** "Processing" means any operation, including collection, use and erasure. Storage is not required. The European Data Protection Board (EDPB) says even a template deleted "within the shortest possible period" is still processed. So we say "**nothing is saved**", never "no personal data" or "anonymous". | Art. 4(1),(2) [S1]; EDPB 3/2019 example 5, para. 115 [S7]; CNIL [S11]; research/09 §3.1 |
| Lawful basis | **Art. 6(1)(e) public task.** SUT is a public university, and disseminating science is one of its statutory tasks: Art. 11(1)(9) of the Polish Act of 20 July 2018 (consolidated text Dz.U. 2024 poz. 1571). Consent is weak here because of the power imbalance and the absence of parents (recital 43). Art. 6(1)(f) is in practice not available to a public body (our reading of Polish law; DPO to confirm in the Nov 2026 screening). | [S1; S15; S44]; research/09 §3.3, §16 |
| Role of the opt-in | An ethical safeguard and a practical right to object (Art. 21). Nothing is processed until the volunteer agrees, and the senses can be switched off at any time. The French regulator CNIL notes that objecting to smart cameras is usually impossible unless there is an opt-in before analysis. Signs say "you decide", not "consent". | [S1; S11]; research/09 §3.3 |
| Art. 8 (child consent, ages 16/13) | **Does not apply.** It covers information-society services provided "at a distance", which an in-person booth is not. It would come back if we delivered results online, which is one more reason for no QR code and no email. | EDPB 05/2020 paras 125-128 [S8] |
| Biometric data and Art. 9 | Art. 9 covers biometric data processed "for the purpose of uniquely identifying" someone. We do no recognition and no re-identification. A "welcome back" feature would bring in Art. 9 "from the start". **But** outputs that *reveal* religion, ethnicity or health (a headscarf label, skin tone, a wheelchair) are Art. 9 data even if inferred indirectly (CJEU C-184/20). That is why hats were removed. The AI Act's own definition of "biometric data" (Art. 3(34)) is broader, so pose and voice count there. | Art. 4(14), 9(1), rec. 51 [S1]; EDPB 3/2019 paras 74-82 [S7]; C-184/20 [S43] |
| Design principles | Minimisation and storage limitation (Art. 5(1)(c),(e)): RAM only, for one session. Privacy by design and by default (Art. 25): sensors off by default, unneeded functions deactivated. Child-friendly layered notice (Arts 12-13, rec. 58). No profiles of children (rec. 38). We do not collect extra data just to answer access requests (Art. 11). | [S1; S7 para. 129]; research/09 §3.4 |
| DPIA (Art. 35) | **Do one, short but formal.** We meet at least two criteria of the EU DPIA guidelines (WP248): vulnerable data subjects (children) and innovative technology, plus partly evaluation and monitoring. The DPIA list of the Polish Data Protection Authority (UODO) names "interactive toys" and "services and toys dedicated to children". The DPIA runs through SUT's own procedure: Order 62/2024 §16, in the RIG software ("Reed Into Green"), via the Management Control and Security Office (BKZB, BKZB@polsl.pl) and the DPO. Order 62/2024 still names the Information Security Office (BBI), which is not in SUT's organisational chart of 1 Jan 2026. Ask the DPO whether the Order was amended (**to confirm**). | [S9; S14; S16; S42; SUT org chart 2026]; research/09 §3.5, V13 |
| Research data | **None collected at SiW.** Logging, filming or questionnaires would turn outreach into research with minors (parental consent plus ethics approval). | [S20]; research/09 §5 |

### 1.2 EU AI Act (Regulation (EU) 2024/1689)

| Question | Answer for our booth | Reference |
|---|---|---|
| Are we in scope? | **Yes.** SUT is both provider and deployer ("putting into service for own use"). The research exclusions (Art. 2(6), 2(8)) do not cover a public exhibit. | Art. 3(3),(4),(11), 2(6),(8) [S2]; Art. 50 guidelines paras 21-22 [S5] |
| Art. 5(1)(f): emotion inference at work and in education | **Treated as prohibited.** The workplace limb protects workers, not visitors: the Commission's guidelines say emotion recognition of customers is not prohibited if no employees are tracked. So we do not claim a flat legal ban for visitors. Our reasons: (a) our staff and the teachers are unavoidably in frame, and "workplace" is read broadly (museums, temporary sites, volunteers) [S4 para. 254]; (b) whether a school trip to a fair counts as "education" is unsettled [S48]; (c) otherwise it is Annex III 1(c) high-risk (from 2 Dec 2027) and needs an Art. 50(3) notice now; (d) weak science [S2 rec. 44; S28] and UNICEF and UN CRC guidance against emotional analytics of children [S22; S23]. Saying "you are smiling" is not emotion recognition, but "you are happy" is. We do neither. | [S2]; prohibited-practices guidelines paras 249, 254-255 and examples after para. 254 [S4]; [S48]; research/09 §4.3, V5 |
| Art. 5(1)(g): biometric categorisation to infer race, religion and similar | **Never.** Clothes and accessories are outside "biometric categorisation" (para. 277), so clothes colour and glasses are fine under the AI Act. | [S2]; [S4] paras 271-283, 277 |
| Art. 5(1)(b): exploiting age-related vulnerability | No guilt or pressure to keep sensors on (no "I'm sad you closed my eyes"). | [S2]; ICO std 13 [S24] |
| Art. 50(1): say it is an AI | **Required.** The Commission names "robotic companion pets" as in scope. The "obvious" exception needs us to assess and demonstrate obviousness for the whole target group, including 7-year-olds, which we cannot do. (The guidelines' lifelike-pet example does not fit the visibly mechanical PiDog V2, so we do not rely on it.) For children the notice must be child-friendly, with periodic reminders. | [S2]; [S5] §3.1.1, paras 34, 40, 42; research/09 §4.5, V6 |
| Art. 50(2): mark generated images | Applies to the optional "robot's imagination" pictures: machine-readable marking that shows they are AI-generated. The Omnibus grace period (to 2 Dec 2026) covers only systems on the market before 2 Aug 2026, so it does not cover us. Benchmark: the Commission Code of Practice (finalised 10 Jun 2026). | [S2; S3b]; research/06 §9 |
| Art. 50(3): notice for emotion recognition or biometric categorisation | **Avoided by design.** It would apply to any age, gender, hair-colour or similar categorisation (rec. 16; guidelines para. 104). We do none, but the sign still says what the robot looks at and what it never guesses. | [S2]; [S5] paras 99-108 |
| Dates | Art. 5 since 2 Feb 2025 and Art. 50 since 2 Aug 2026 both apply at the fair. The **Digital Omnibus, Reg. (EU) 2026/1744** (OJ 24 Jul 2026, in force 27 Jul 2026) kept the Art. 50 date and moved Annex III high-risk duties to **2 Dec 2027** and Annex I to 2 Aug 2028. Art. 4 (AI literacy) is now a duty to "take measures", which our staff briefing covers. | [S2 Art. 113; S3; S3a-c]; research/09 §4.1 |
| High-risk? | **No, if this design is kept.** Annex III 1(a): no remote identification. 1(b): no categorisation by sensitive attributes. 1(c): no emotion recognition. 3: no grading or monitoring of pupils. The high-risk guidelines are still a draft (19 May 2026); re-check in Feb 2027. | [S6]; research/09 §4.6 |
| Enforcement | Poland: KRiBSI (Komisja Rozwoju i Bezpieczeństwa Sztucznej Inteligencji, the single AI market-surveillance authority) under the Polish AI Systems Act (fully applicable 28 Oct 2026). Belgium: BIPT (the telecoms regulator) designated by government policy; the statute had not been adopted (**to confirm**). | [S45; S46] |

### 1.3 Other rules that bind the team

| Rule | What it means | Reference |
|---|---|---|
| SUT child-protection standards (Rector's Order 50/2024) | No recording of minors for private purposes. Publishing a recorded image of a child needs the guardian's written consent. §5(3) says minors' image data are processed "on guardian consent", which conflicts with our public-task basis, so the **DPO must rule** on it (Plan A or Plan B, see §4.9). | [S40]; research/09 §3.3 |
| Staff vetting: SUT Order 37/2024 (amended by 240/2024) and Art. 21 of the Polish Act of 13 May 2016 (amended from 15 Feb 2024) | For **every** booth staffer, doctoral candidates and any non-SUT helpers included: (a) Register of Sex Offenders check, requested from HR at least 7 days before working with minors (separate forms for employees and for doctoral candidates or non-employees); (b) criminal-record information from the KRK; (c) for anyone with another citizenship or who lived in another country in the last 20 years, a criminal-record certificate from that country, or a sworn statement where it issues none. MSCA doctoral candidates usually come from abroad (mobility rule), so expect (c) to apply to both DCs. Foreign certificates can take weeks: request them in **January 2027**. Effect of the amending Act of 5 Aug 2025 on Art. 21: **to confirm** with HR. | [S41]; [MoJ FAQ]; research/09 §9 control 23, §12, V12 |
| SUT data-protection policy (Order 62/2024) | DPIA in RIG via BKZB and the DPO (§16; the Order still names BBI, see §1.1). Privacy-by-design clauses go in the robot purchase request (§17). | [S42]; research/09 V13 |
| Belgian image right (CDE Art. XI.174) | Taking and using a photo each need consent. **We do not photograph pupils.** | [S13] |

---

## 2. Attribute register (final design)

Verdicts follow research/09 §8. **ACCEPTABLE** = may be used as specified. **AVOID** = not built (legal exposure and/or harm to children, with no teaching value that justifies it). **PROHIBITED** = prohibited by law, or so close to a prohibition or to Art. 9 that we treat it as prohibited. The code register is `prototype/robotsees/config.py` (`SLOTS`, `NEVER_GUESS`).

| # | Attribute | Sensor | Verdict | Reason (source) | How we use it / safer alternative |
|---|---|---|---|---|---|
| | **Used: the 6 slots** | | | | |
| 1 | Favourite animal | EARS: word said (strong). EYES: picture card or toy shown (moderate) | ACCEPTABLE | Volunteered, specific purpose, non-sensitive. Shows "data you give" versus "data it infers" (09 §8 #16) | 12 values. A word counts only as an answer to the robot's own question |
| 2 | Favourite colour | EARS: colour word (strong). EYES: clothes colour as a weak hint (relevance 0.35) | ACCEPTABLE | Volunteered, non-sensitive (#15, #16) | 11 basic colours. The eyes' hint is shown as "a clue, not proof" |
| 3 | Clothes colour | EYES only | ACCEPTABLE | Clothes are outside biometric categorisation [S4 para. 277] (#9) | k-means in CIELAB on the upper chest, starting below the shoulders (clothes, not skin). Colour patch only. Nothing about brands, uniforms or religious dress |
| 4 | Glasses yes/no | EYES only | ACCEPTABLE (with care) | An accessory [S4 para. 277]. Eyesight would be health data (Art. 9) (#10a) | CLIP contrast prompts with Platt calibration. "Glasses help eyes; they tell me nothing else" |
| 5 | "How much is happening right now" (still / moving / very active) | EYES: body-keypoint speed. EARS: sound level | ACCEPTABLE as a momentary reading; AVOID as a trait | Trait labels like "hyper" suggest ADHD (health). Behavioural traits are a categorisation category [S2 rec. 16] (#20) | Always "right now", wiped at session end. Exhibition wording must be robot-centric (see §3) |
| 6 | "Voice right now" (quiet / normal / loud) | EARS: loudness relative to booth calibration | ACCEPTABLE | "a raised voice or whispering" is readily apparent and is not emotion recognition [S2 rec. 18] (#12) | "I hear a LOUD voice right now". Never "you are loud" or "you are angry" |
| 6a | Room noise and image quality (not about the person) | EARS: speech-to-noise ratio. EYES: brightness and sharpness | ACCEPTABLE | Ambient, not linked to a person (#22) | Only lowers evidence quality, so "noisy room" and "foggy lens" make the robot unsure instead of wrong |
| | **Built or considered, then removed or not labelled** | | | | |
| 7 | Headwear (hat, cap, headscarf) | EYES | AVOID (**removed**) | Head coverings can reveal religion (Art. 9); indirect revelation is enough (C-184/20) [S43]; misclassification risk (#10b) | Hat detector built (AUROC 0.75, brief §6), then removed from the label set. Now on the "never guess" list |
| 8 | Speaking speed | EARS | Research: ACCEPTABLE only momentary with no label (#13). **Our choice: not used** | Unfair to children who stutter and to second-language speakers (health and fairness) | Not fused, not labelled. A leftover words-per-second number in the prototype's audio log is to be removed (§3) |
| 9 | Pitch | EARS | ACCEPTABLE only as a live physics display; AVOID as a personal attribute (#14) | Pitch is a proxy for age, sex and puberty | Not computed (`perception/audio.py`). No "high/low voice" label |
| 10 | Open words, topics, transcripts | EARS | AVOID (closed vocabulary is ACCEPTABLE) (#15) | Children treat robots as able to "be trusted with secrets" [S25]. Free speech can contain Art. 9 or third-party data | Closed EN/FR/NL/DE/PL word list (`perception/lexicon.py`). Only matched words go on |
| | **Never inferred** | | | | |
| 11 | Identity: face or voice recognition, "welcome back" | EYES / EARS | PROHIBITED (by design) | Re-identification is unique identification, so Art. 9 applies "from the start" [S7 para. 82]; Belgian DPIA list item 1 [S12] (#23) | The face detector gives a head box only. No embeddings. Sessions are bounded by start and "forget me" |
| 12 | Emotion (face, voice, body), including "smile = happy" | EYES / EARS | PROHIBITED (treated as) | Art. 5(1)(f): staff and teachers in frame [S4 para. 254]; "education" unsettled [S48]; otherwise Annex III 1(c) high-risk; weak science [S2 rec. 44; S28] (#4; see §1.2) | No expression model. "Faces and voices don't reliably show feelings" |
| 13 | Ethnicity or skin tone | EYES | PROHIBITED | Art. 5(1)(g) [S4 paras 271-283]; GDPR Art. 9 (#3) | Colour is sampled on clothes below the shoulders, not on skin |
| 14 | Age | EYES / EARS | AVOID | Biometric categorisation [S2 rec. 16], so the Art. 50(3) notice would apply; error-prone [S30] (#1) | Not computed |
| 15 | Gender | EYES / EARS | AVOID | Art. 50(3); error rates up to 34.7% versus at most 0.8% across groups [S29] (#2) | Not computed, never displayed |
| 16 | Hair colour | EYES | AVOID | Named in rec. 16 and the attribute-estimation examples [S4 para. 282]; ethnicity proxy (#11) | Not computed |
| 17 | Height or body shape | EYES | AVOID | A physical characteristic [S4 para. 282]; body-image harm (#8) | Not computed. Pose keypoints are used only for motion speed |
| 18 | Health or disability (eyesight, wheelchair, cough, stutter, BMI) | EYES / EARS | PROHIBITED (treated as) | Art. 9 health data; "of key relevance" for Annex III 1(b) [S6] (#6) | Mobility aids ignored. No comment on speech fluency |
| 19 | Accent or native language | EARS | AVOID | "Language" is in rec. 16; accent is a proxy for ethnic origin (#7) | Language is **chosen with a flag button**. The prototype accepts a fixed language but by default still uses Whisper's language ID (§3) |
| 20 | Attractiveness | EYES | AVOID | No validity; fails fairness (Art. 5(1)(a)) and the best-interests test; the Biometric Mirror and How Normal Am I? lessons [S33; S34] (#5) | None |
| 21 | Personality or interaction style (shy, outgoing) | Several | AVOID | Profiling children (rec. 38); rec. 16; Art. 6(3) (#21) | None. Within a session the robot only states facts ("my ears were switched off") |
| 22 | Gaze, attention or interest | EYES | AVOID | "infer the interest and attention of students" is the Commission's example of a prohibited practice [S4 para. 255] (#24) | No attention score |

---

## 3. Privacy-by-design controls: prototype now vs exhibition to do

The prototype runs on recorded adult clips (Seamless Interaction, Lombard GRID), offline on the dev laptop. Its live mode (`prototype/live/run_live.py`: webcam or PiDog MJPEG stream plus a microphone) has been tested on recordings only. File paths are under `prototype/robotsees/` unless they start with `live/`, `experiments/` or `demo/` (under `prototype/`).

| Area | Implemented in prototype code (where) | To implement for the exhibition |
|---|---|---|
| What can be inferred | Closed vocabulary allow-list: 6 slots in `config.py` (`SLOTS`). `fusion.EvidenceMemory.add()` drops any observation whose slot or sensor is not in the register. Closed multilingual word list in `perception/lexicon.py` | Freeze the register. Any change goes through the DPO and the DPIA |
| Identity | No face or voice embeddings. The MediaPipe face detector gives a head box only, with no landmarks or identity (`perception/vision.py`). CLIP image features of the head crop are used only for the glasses score and discarded with the frame. No speaker model (`perception/audio.py`) | Code review of the final build for the DPIA: confirm that no model output persists across frames or sessions |
| Microphone content | Only matched closed-vocabulary words leave the audio path; the transcript is not exported (`session.perceive_audio`, `live/run_live.py`). No pitch | Remove `AudioResult.transcript` (kept only for the offline GRID evaluation) and the unused `words_per_second` value from the event log. Push-to-talk on the close-talk microphone |
| Prohibited models | No hat, age, gender, emotion, skin or hair models (`vision.py` "deliberately NOT computed"). The hat detector was removed | Install only the models used. Never ask a VLM or LLM to describe a person (research/09 §9 control 9) |
| Screen | Pixelated robot's-eye view: 12-px blocks, 360-480 px wide, with only the boxes the robot used (`session.robot_eye_view`) | TV shows the avatar and evidence cards. The pixelated view stays small. No raw video of children |
| Memory | Per-visitor in-RAM evidence ledger with `clear()` (`fusion.EvidenceMemory`). No images, audio, transcripts or embeddings. Live mode has a forget endpoint that resets the memory (`POST /live/forget`) | Wire this reset to the "forget me" button, with a visible wipe. Auto-wipe at each volunteer handover and on a timeout. Research suggests 25-30 s with no face [R10 §8.2] or about 60 s with nobody on the mat [09 §9]; final value **to confirm** in tests |
| Generated images | Every image gets IPTC `DigitalSourceType = trainedAlgorithmicMedia` in XMP plus an EXIF description (`render/imagination.save_marked`). The demo UI labels it "AI-generated picture" and lists the words the generator got (`demo/app.html`) | Correct the EXIF text: it still says "AI-generated image (SD-Turbo). Made only from these words", but the images now come from LCM-Dreamshaper and start from the robot's drawing. Check every output before display (a pre-rendered, human-reviewed library or a face/NSFW check), including that the mascot has no invented facial expression, which could look like emotion inference (research/06 §8, §12). LCM-Dreamshaper (MIT) needs no "Powered by Stability AI" notice; it is needed only if a Stability model such as SD-Turbo is used (research/06 §0). Generated images do not leave the booth |
| Imagination input | LCM-Dreamshaper v7 (OpenVINO int8, MIT) restyles the robot's own avatar drawing (img2img, strength 0.7, 4 steps; 2.6 s on the dev laptop's integrated GPU). The prompt uses only closed-vocabulary phrases for slots the robot believes at "guessing" or higher. The subject is a cartoon robot mascot, never a human likeness. It never sees camera pixels (`experiments/build_imagination.py`; pre-rendered for the recorded sessions, not yet in live mode). The replaced SD-Turbo text-to-image code is still in `render/imagination.py` | Keep. Add a test showing that the only image input is the avatar drawing, with no path from the camera. Leave the old SD-Turbo code out of the exhibition build |
| Sensor switches | Fusion omits a switched-off sensor's evidence (exact marginalisation, never a black frame). Live mode starts with both sensors off and drops a switched-off sensor's frames and audio before any model sees them (`live/run_live.py`). It does not yet release the device handle: the camera and microphone stay open and their data is read, then discarded | **Release the device and stop capture on the Pi** when EYES or EARS is off, so that no data reaches any process (research/09 §9 control 3). LED wired to the real capture state. Sensors off by default. Show the test to visitors |
| Physical guarantees | n/a | **Physical lens shutter** ("eyes closed") and a hardware mic mute |
| Network | Inference makes no network calls. But `vision._ensure_model` downloads model files if they are missing | **Offline**: dedicated 5 GHz booth router with no internet uplink, outbound traffic denied in the firewall, venue Wi-Fi never used. Vendor cloud, BLE and apps disabled. Packet-capture check. All model files pre-installed so auto-download fails closed |
| Storage | Live mode keeps evidence in RAM and writes nothing to disk. The dev pipeline writes pixelated frames, session JSON and imagination images for the **recorded dataset clips only** | **No-write verification**: run a file-system and network monitor during a full session and keep the log as DPIA evidence. No frames, audio, logs or crash dumps. OneDrive and screen recorders off. BitLocker on |
| Region of interest | Uses the largest face or pose only | **ROI masking**: black out everything outside the volunteer mat before inference [S7 para. 129]. Low capture resolution |
| Wording | Momentary framing in `config.py` ("right now") | Make the energy sentence robot-centric: "my eyes see a lot of movement right now", not "you are VERY ACTIVE right now" (`xai._statement`). Extend `NEVER_GUESS` and the list in the demo UI (`demo/app.html`) to the 8 items in §7 |
| Language | Live mode accepts a fixed language (`--language`). Without it, Whisper detects the language (85% English detected on short GRID sentences, brief §6) | Flag button selects the language. No language or accent inference |
| Governance | n/a | DPIA (§6), Art. 30 record, staff briefing (AI literacy and child protection), register and criminal-record checks (§1.3), counters as daily totals only if any (EDPB 02/2026 [S52]), no staff phones filming children, adult present |

---

## 4. Consent and notice for a busy fair

### 4.1 How "you decide" works in the 15-min module
1. Sign at the booth entrance (first layer, §4.2). Teacher sheet sent in advance (§4.8).
2. 0-2 min: staff give the 30-second intro (§4.3). The robot discloses it is a program (§4.4).
3. Each volunteer round: the volunteer steps onto the mat. Staff ask "May the robot use its eyes? Its ears?" and flip EYES and EARS **only after a yes**. EYES and EARS are off by default, with the shutter closed.
4. The volunteer can say "stop" or switch a sense off at any time. The robot reacts neutrally (§4.5). The group's switches (eyes off, ears off, foggy lens, noisy room) only *remove or degrade* evidence; they never switch a sense on without the volunteer's yes.
5. 14-15 min: "forget me" wipes memory visibly. A printed card is offered only on request (§5).

### 4.2 First-layer sign (A1/A2 with pictograms: camera, microphone, "not saved", stop hand)
Adapted from research/09 §10. FR and NL are **to be checked by a native speaker**.

> **EN - How does a robot see you?**
> This robot dog is a computer program (an AI system). It is not alive and has no feelings.
> Its eyes (camera) and ears (microphone) are OFF until you say yes and we switch them on.
> It only pays attention to: the colour of your clothes, glasses, how much you move, how loud your voice is, and the words you choose to tell it (favourite animal, favourite colour) or an animal picture card you show it.
> It does NOT try to recognise who you are. It does NOT guess your feelings, age, gender or where you come from.
> Nothing is recorded or saved. When you leave, the robot forgets you.
> You can switch its eyes or ears off at any time and still play. Just watching is fine too.
> Responsible: Silesian University of Technology (Poland), TUAI project. Questions: booth staff / IOD@polsl.pl

> **FR - Comment un robot te voit-il ?**
> Ce chien robot est un programme d'ordinateur (un système d'IA). Il n'est pas vivant et n'a pas de sentiments.
> Ses yeux (caméra) et ses oreilles (micro) sont ÉTEINTS tant que tu ne dis pas oui et que nous ne les allumons pas.
> Il fait seulement attention à : la couleur de tes vêtements, tes lunettes, combien tu bouges, le volume de ta voix, et les mots que tu choisis de lui dire (ton animal préféré, ta couleur préférée) ou une carte d'animal que tu lui montres.
> Il n'essaie PAS de savoir qui tu es. Il ne devine PAS tes émotions, ton âge, ton genre ni ton origine.
> Rien n'est enregistré ni sauvegardé. Quand tu pars, le robot t'oublie.
> Tu peux éteindre ses yeux ou ses oreilles à tout moment et continuer à jouer. Tu peux aussi juste regarder.
> Responsable : Université de technologie de Silésie (Pologne), projet TUAI. Questions : l'équipe du stand / IOD@polsl.pl

> **NL - Hoe ziet een robot jou?**
> Deze robothond is een computerprogramma (een AI-systeem). Hij leeft niet en heeft geen gevoelens.
> Zijn ogen (camera) en oren (microfoon) staan UIT tot jij ja zegt en wij ze aanzetten.
> Hij let alleen op: de kleur van je kleren, je bril, hoeveel je beweegt, hoe luid je stem is, en de woorden die jij hem wilt vertellen (je lievelingsdier, je lievelingskleur) of een dierenkaart die je hem laat zien.
> Hij probeert NIET te weten wie je bent. Hij raadt NIET je gevoelens, leeftijd, gender of waar je vandaan komt.
> Er wordt niets opgenomen of bewaard. Als je weggaat, vergeet de robot je.
> Je kunt zijn ogen of oren altijd uitzetten en toch verder spelen. Gewoon kijken mag ook.
> Verantwoordelijke: Silezische Technische Universiteit (Polen), project TUAI. Vragen: het standteam / IOD@polsl.pl

Second layer (A4 at the booth, plus a static page with no trackers; hosting **to confirm**). It covers the Art. 13 items: controller and DPO; purpose; legal basis (Art. 6(1)(e) GDPR with Art. 11(1)(9) of the Polish Act); data categories; no recipients or transfers; retention (RAM, deleted at session end); rights, including objecting by not starting or by stopping, and Art. 11; complaints to UODO (PL) or the Belgian Data Protection Authority, APD/GBA (BE); and an AI Act statement (an AI system, what it uses, what it never infers) [research/09 §10].

### 4.3 Staff 30-second intro (EN; the language assistant gives it in FR/NL)
"This robot dog is a computer program, an AI. It is not alive and has no feelings. Its eyes are this camera and its ears are this microphone. Both are off now. They only go on when a volunteer says yes. You tell the robot simple things, like your favourite animal, and it guesses others, like the colour of your clothes, and shows how sure it is. It never tries to find out who you are, how you feel, your age or your gender. Nothing is saved, and at the end we press 'forget me' together. You can say no and still play."

### 4.4 Robot disclosure lines (Art. 50(1) and periodic reminders [S5 paras 34, 40]; template text, Piper TTS, FR/NL versions to be checked by native speakers)
| Moment | Robot says |
|---|---|
| Start of the group | "Hi! I'm a robot dog. I'm a computer program, not a real dog. I don't know you. I can only guess from my sensors." |
| Eyes switched on | "My eyes are on. I'm using my camera now." (LED on) |
| Ears switched on | "My ears are on. I listen for animal and colour words, and how loud it is right now. Nothing you say is saved." |
| Mid-round reminder (every round) | "Remember, I'm a computer program. You can switch my eyes or ears off at any time." |
| Imagination picture shown | "An AI picture-maker turned my own drawing into this robot friend, using only my words. It never saw my camera. It is not a photo of you." |
| End of the round | "Now I forget everything about you. Watch my memory empty." |

### 4.5 Neutral reactions to "off" (no sadness, pleading or flattery [S2 Art. 5(1)(b); S24 std 13])
- Eyes off: "OK, eyes off. I'll only use what you tell me."
- Ears off: "OK, ears off. I'll only use what I see."
- Both off: "OK, everything is off. I can't learn anything new now, and that's fine."
- Volunteer stops: "OK, we stop here. I'm forgetting everything now."
- Never: "I'm sad", "please switch me back on", "I like you best", or any comment on silence or appearance.

### 4.6 No-camera mode (full experience, not a lesser one)
- For anyone who prefers it, pupils flagged by the teacher, and children without an accompanying adult. Shutter closed, EYES stays off.
- The volunteer speaks the answer into the dog-bone microphone (EARS only). Or, with no sensors at all, they point at a picture card and staff enter the answer. The input method for that case is **to confirm**: answer buttons are not yet in the switch-box design.
- The screen then shows only "data you give", which is itself the comparison the lesson needs. If no pupil wants EYES on, a staff member can stand on the mat to demonstrate the camera.
- Flagged pupils stand outside the camera's field. ROI masking (§3) keeps bystanders out of the analysis.

### 4.7 Adult present and safeguarding rules
- Camera and microphone mode only while the accompanying teacher or parent is at the booth [research/09 §10 item 5].
- At least 2 staff at the booth at all times. Never one adult alone with one child [research/09 control 22; R10 §9 item 9].
- No staff phones filming or photographing children (SUT staff code) [S40]. If we document the booth: an empty booth, staff, or the screen showing abstract output only.
- Robot stays in its pen on the table. Staff-side e-stop. Children never carry the robot. No battery charging in the public area [research/09 control 21; R10 §0 item 8].

### 4.8 Teacher information sheet (one page, EN/FR/NL, through the organisers' school pack if they agree; **to confirm** with the organisers)
1. What the 15-minute activity is and what pupils do (predict, operate switches, volunteer).
2. What the robot senses (6 slots) and what it never guesses (§7).
3. Nothing recorded, everything offline, "forget me" at the end.
4. Taking part is voluntary. No-camera mode exists, and watching is fine.
5. Please tell staff discreetly about pupils who must not be filmed (for example under protection measures). They take part without the camera and stand out of view.
6. Please stay with your group: the camera is only used while you are present.
7. Our team does not photograph pupils. EC photography follows the EC privacy statement DPR-EC-1063.1: a separate explicit consent form is used whenever participants appear in published pictures or recordings, and the EC photo booth keeps images for 7 days [research/01 §1.7]. Whether schools sign that form in advance: **to confirm** with the organisers.
8. Controller, DPO contact (IOD@polsl.pl), legal basis, rights, complaints (UODO / APD-GBA).
9. Plan B only: the consent slip (§4.9).

### 4.9 Plan B (only if the DPO requires guardian consent under Order 50/2024 §5(3))
Through the school pack, schools get a one-line slip: "My child may use the robot's camera and microphone at the TUAI booth. Nothing is recorded or saved." The teacher confirms at the booth which pupils have one. **We collect no names and no slips**; the school keeps them. Everyone else uses no-camera mode. Decide by November 2026 [research/09 §10].

---

## 5. Result delivery

| Option | What leaves the booth | Personal data? | Implications | Verdict |
|---|---|---|---|---|
| Nothing, plus a "forget me" moment | Memory only | None | Best minimisation (Art. 5(1)(c),(e)); the deletion is itself the lesson | **Default (chosen)** |
| Offline printed card, no photo, no name | Icons: senses used, slot answers with certainty words, "was I right?", "things I will never guess" | Practically non-identifying, held by the child | No storage on our side. The printer needs no network or cloud and no job memory. We pay for it (SiW does not fund giveaways [S18]) | **Optional (chosen)** |
| Group card or class poster | Aggregate only ("the robot was right 5 of 8 times") | Anonymous if coarse | Daily totals, no timestamps [S52] | Acceptable |
| QR code with the data in the URL fragment | Data inside the code | Low | The page host still sees visits and IPs. Needs a phone (59% of Flemish primary pupils have none [R10-80]). Art. 8 question returns [S8] | Not used |
| QR code to server-hosted results | Results stored online | Yes | Hosting, retention, security, processor contract, possibly Art. 8 [S8] | **Avoid** |
| Email | Email address plus result | Yes, identifying | New identifiers and retention; against minimisation | **Avoid** |
| Photo printout or AI portrait of the child | Identifiable image | Yes | Belgian image right [S13]; social-media spread; deep-fake risk (Art. 50(4)) | **Avoid** |

**Our choice:** nothing by default, plus "forget me". On request, a volunteer gets an offline-printed card with the avatar icons, certainty words, which senses were on and the "never guess" panel. The card carries no photo, face crop, name, time, ID, generated image or QR code. No email. Printer options from research/10 §7:
- Brother QL-800 label printer: USB, monochrome (black/red), USD 124.99 [R10-78]. Up to 93 labels/min is Brother's figure for black-text address labels; graphic badges print noticeably slower, so benchmark before relying on it for whole classes. Colours (clothes, favourite colour) must be printed as words.
- Canon SELPHY CP1500: colour, 41 s per glossy postcard, MSRP USD 179.99 [R10-76, R10-77]. Per-print cost unverified (the ink and paper set price could not be confirmed). It has 2.4 GHz Wi-Fi, which must stay off.

All prices are US retail. EU prices and whether either printer keeps a job memory are **to confirm** [research/10 §7, V17, V18].

---

## 6. DPIA and approvals plan

**Approach.** A short formal DPIA (10-15 pages of content) through SUT's procedure: screening under Order 62/2024 §16(2), then the DPIA in RIG via BKZB, both consulted with the DPO [S42]. The Order still names BBI, which no longer appears in the organisational chart (§1.1; **to confirm** with the DPO). We supply the content; BKZB and the DPO run it. We collect no research data. Optionally, we ask the SUT research-ethics commission for an advisory "no research data" opinion. The commission's existence is reported only by secondary sources (**to confirm**) [S49].

**Contacts (in order):** (1) DPO, IOD@polsl.pl, tel. 32 400 3077, within BKZB (BKZB@polsl.pl) [S16]: lawful basis, §5(3), screening, whether Order 62/2024 was amended. (2) The unit's local data-protection representative (LPODO). (3) HR (Dział Zasobów Osobowych): register checks, KRK information and foreign criminal-record certificates, and the effect of the 5 Aug 2025 amending Act. (4) Research-ethics commission via the research office. (5) TUAI coordinator: grant-agreement ethics deliverables (**to confirm**). (6) SiW organisers, EAC-MSCA-SIW@ec.europa.eu / schools-SIW@spectraconsortium.eu: photography, school pack, pupils with image restrictions.

**DPIA content we prepare:**
- data-flow diagram (robot sensor node, booth router, laptop RAM, models, TV, wipe) and the Art. 30 record;
- lawful-basis memo (§1.1);
- necessity and proportionality (the §2 register);
- risk register: misclassification and humiliation, bystander capture, disclosure of secrets, screen photographed by others, laptop theft, vendor telemetry, mission creep ("let's keep some clips"), peer or teacher pressure, physical safety;
- the §3 measures with test evidence (no-write and no-network logs, toggle and wipe tests);
- transparency material (§4);
- AI Act memo (§1.2);
- security assessment (BLE off, isolated network, packet capture);
- model and data provenance, with a bias check of clothes-colour and glasses detection under booth lighting and across skin tones;
- safeguarding plan;
- procurement clauses [research/09 §12].

| When | Action | Output |
|---|---|---|
| By **6 Oct 2026, 12:00 CEST** | Submit the proposal. The form has no ethics field, so privacy goes in the B2 "Privacy" paragraph (`docs/08`). No compliance claims before the DPIA ("will undergo a DPIA") | Proposal |
| Oct 2026, before buying hardware | Send privacy-by-design purchase clauses to the DPO (§17): camera/mic usable locally without vendor cloud; BLE and remote access can be disabled; no telemetry; CE-marked with a Radio Equipment Directive (RED) Declaration of Conformity [S53]. PiDog V2 kit and Raspberry Pi 5: CE/RED Declaration of Conformity, and whether the kit is marketed as a toy (then CE under the Toy Safety Directive 2009/48/EC; the new Toy Safety Regulation (EU) 2025/2509 has an unverified application date): **to confirm** with SunFounder and the Pi supplier before purchase [research/09 verifier omission 1, second-pass omission 4] | Purchase request |
| 28 Oct / 4 Nov 2026 | Results, then the mandatory online workshop | - |
| **Nov 2026** | DPIA screening with the DPO. Written position on Art. 6(1)(e) and Order 50/2024 §5(3) leads to **Plan A or Plan B**. Ask the organisers about photography, the school pack and image-restricted pupils | Screening decision, Plan A/B |
| Nov-Dec 2026 | Teacher sheet (and the Plan B slip if needed) to the organisers | School-pack text |
| Dec 2026 - Jan 2027 | Build the §3 exhibition controls. Tests on adults. Security and no-write tests. Native-speaker check of FR/NL texts. Test the notices with 3-5 colleagues' children (parental agreement, no recording). Draft the DPIA content | DPIA draft, test logs |
| **Jan 2027** | **Request foreign criminal-record certificates** (or sworn statements) for every staffer with foreign citizenship or foreign residence in the last 20 years, and KRK information for all staff (§1.3) [MoJ FAQ] | Certificates in hand by Feb |
| **Feb 2027** | Finalise the DPIA in RIG with BKZB and the DPO. Dry-run the toggle and wipe tests. Re-check the GDPR Omnibus, the final high-risk guidelines and the EDPB children's-data guidelines. **Submit register-check requests to HR** with the KRK information and foreign certificates (absolute deadline 9 Mar 2027) | Signed DPIA, HR confirmations |
| 16 Mar 2027 (set-up) | On-site checklist: router offline, firewall, shutter, LED, no-write monitor, signs up. Staff briefing (AI literacy, child protection) | Checklist |
| 17-19 Mar 2027 | Fair. Counters as daily totals only, if any | - |

---

## 7. "Things the robot will never guess, and why" (child-facing)

This replaces the 5-item `NEVER_GUESS` in `config.py` and the 6-item list in the demo UI (`demo/app.html`). Both say "guessing them is not allowed here" about feelings, which overstates the law for visitors (§1.2). FR and NL are **to be checked by a native speaker**. For ages 15-18, staff can add the rule behind each line (last column, EN only).

| # | EN: I will never guess... | EN: why | Rule behind it (15-18) |
|---|---|---|---|
| 1 | Who you are | I don't recognise faces or voices. When you leave, I forget you. | GDPR Art. 9; EDPB 3/2019 para. 82 |
| 2 | How you feel | Faces and voices don't really show what someone feels, so I never try to guess it. | AI Act Art. 5(1)(f) (at work and in schools); weak science |
| 3 | Your age or your gender | Machines often get these wrong, and it is not my business. | AI Act rec. 16, Art. 50(3); Gender Shades |
| 4 | Where you or your family come from | Skin colour, hair colour or an accent say nothing about who you are. You choose your language with a button. | AI Act Art. 5(1)(g); GDPR Art. 9 |
| 5 | Anything about your health or your body | Glasses help eyes; they tell me nothing else. I don't measure how tall you are, and I don't judge how you talk. | GDPR Art. 9 (health) |
| 6 | What you wear on your head | A cap or a headscarf can be about someone's beliefs. That is private, so I don't look at it. | GDPR Art. 9 (religion); CJEU C-184/20 |
| 7 | What kind of person you are | A few minutes of clues can't show if someone is shy, kind or brave. | GDPR rec. 38 (no profiles of children) |
| 8 | If you are paying attention or interested | Only you know what is going on in your head. | AI Act guidelines para. 255 |

**FR - Ce que je ne devinerai jamais, et pourquoi** (to be checked by a native speaker)
1. **Qui tu es.** Je ne reconnais ni les visages ni les voix. Quand tu pars, je t'oublie.
2. **Ce que tu ressens.** Un visage ou une voix ne montre pas vraiment ce qu'on ressent, alors je n'essaie jamais de le deviner.
3. **Ton âge ou ton genre.** Les machines se trompent souvent, et ça ne me regarde pas.
4. **D'où viennent toi ou ta famille.** La couleur de la peau, des cheveux ou un accent ne disent rien de qui tu es. Tu choisis ta langue avec un bouton.
5. **Ta santé ou ton corps.** Les lunettes aident les yeux, c'est tout. Je ne mesure pas ta taille et je ne juge pas ta façon de parler.
6. **Ce que tu portes sur la tête.** Une casquette ou un foulard peut être lié aux croyances de quelqu'un. C'est privé, alors je ne le regarde pas.
7. **Quel genre de personne tu es.** Quelques minutes d'indices ne montrent pas si quelqu'un est timide, gentil ou courageux.
8. **Si tu fais attention ou si ça t'intéresse.** Il n'y a que toi qui sais ce qui se passe dans ta tête.

**NL - Wat ik nooit ga raden, en waarom** (to be checked by a native speaker)
1. **Wie je bent.** Ik herken geen gezichten of stemmen. Als je weggaat, vergeet ik je.
2. **Hoe je je voelt.** Een gezicht of een stem laat niet echt zien wat iemand voelt, dus ik probeer het nooit te raden.
3. **Hoe oud je bent of je gender.** Machines vergissen zich daar vaak in, en het gaat mij niets aan.
4. **Waar jij of je familie vandaan komt.** Huidskleur, haarkleur of een accent zeggen niets over wie je bent. Je kiest je taal zelf met een knop.
5. **Je gezondheid of je lichaam.** Een bril helpt je ogen, meer niet. Ik meet niet hoe groot je bent en ik beoordeel niet hoe je praat.
6. **Wat je op je hoofd draagt.** Een pet of een hoofddoek kan met iemands geloof te maken hebben. Dat is privé, dus ik kijk er niet naar.
7. **Wat voor persoon je bent.** Een paar minuten aanwijzingen tonen niet of iemand verlegen, lief of dapper is.
8. **Of je oplet of iets interessant vindt.** Alleen jij weet wat er in je hoofd gebeurt.

---

## 8. Ethics statement (1,174 characters, checked with Python `len()`)

The SiW form has no ethics or data-protection field (research/01 §1.6: a data-protection plan and safety plan are "Not asked in the form"). In the proposal, use the condensed "Privacy" paragraph in B2 (`docs/08`). Keep this full version for the organisers after selection, the DPIA and the TUAI consortium.

> "How does a robot see you?" is privacy-protective and child-safe by design. The robot's camera and microphone stay off until a volunteer agrees to switch them on, and they can be switched off at any time; pupils can also take part without camera or microphone. All AI runs live on an offline laptop in the booth: no images, sound or transcripts are recorded, nothing leaves the booth, and a "forget me" button wipes each session. The robot only uses non-sensitive, momentary signals (clothes colour, glasses, movement, voice loudness) and words from a short list that children choose to say. It never identifies anyone and never guesses emotions, age, gender, ethnicity, health or religion; we removed a working hat detector for this reason. Explaining why is part of the lesson. The robot says in French, Dutch and English that it is a computer program, and its optional AI pictures are labelled. We do not photograph pupils. Staff follow our university's child-protection standards and will be vetted under Polish law. It is designed to comply with the GDPR, the EU AI Act (Art. 5 and Art. 50) and UNICEF guidance, and will undergo a DPIA with our Data Protection Officer.

Wording notes: "will undergo", "will be vetted" and "designed to comply with" are the honest forms before the DPIA exists. Do not write "GDPR-certified" or "AI Act-compliant certified"; no such certificate exists [research/09 §13, §15]. Do not claim the law flatly bans emotion inference for visitors (§1.2).

---

## 9. How uncertainty is communicated to children

Why it matters: children aged 7-9 conform to robots. In Vollmer et al. (2018), 74% of their wrong answers matched the robots' answers [R10-27]. So the robot must show doubt, invite correction and never act as an authority.

**Certainty words** (`config.CERTAINTY_LEVELS`). Confidence is rescaled so that a flat belief counts as 0 whatever the number of values: c = (p_max - 1/n) / (1 - 1/n), where p_max is the highest probability and n the number of possible values.

| c | Robot says | Glasses (n = 2) needs p_max of | Animal (n = 12) needs p_max of |
|---|---|---|---|
| >= 0.75 | "I'm sure ..." | 0.875 | 0.77 |
| >= 0.50 | "I think ..." | 0.75 | 0.54 |
| >= 0.25 | "I'm guessing ..." | 0.625 | 0.31 |
| < 0.25 | "I don't know yet" | below 0.625 | below 0.31 |

**Drawing.** Each avatar element is one slot. A solid line means "sure", a faded one "think", dashed "guessing", and a "?" means "don't know yet". The exact style-to-word mapping is our proposal (the brief fixes faded/dashed/"?"). A badge shows which sense found it: eye (blue `#2f7de1`) or ear (orange `#f08a24`), from `config.MODALITY_META`.

**"I don't know" states** (template sentences in `xai.py`):
- A sense is off: "I can't tell: my eyes are switched off." A missing sense is left out of the sum, so the belief falls back to "don't know" instead of being filled with a fake blank.
- A weak hint: "I only have a tiny hint that it might be BLUE - not enough to guess yet."
- Nothing yet: "I haven't noticed anything about this yet."
- Senses disagree (the "fool the robot" card trick): "My senses disagree: my eyes say CAT but my ears say DOG. For this question I trust my ears more."

**Noise makes it unsure, not wrong.** Lombard GRID, colour words: clean, 79.7% correct and 0% wrong. In babble at 0 dB, 26.6% correct, 0.5% wrong and 72.9% missed (brief §6). On screen, the "noisy room" switch turns "I'm sure" into "I don't know yet".

**Sure is not the same as right.** Glasses "I'm sure" claims were 92.8% correct on the test set, so about 1 in 14 is wrong (brief §6). The real example to show is Visitor B: the robot was "sure" her favourite colour was brown because she said "ginger brown" about her rabbit. Keyword spotting does not understand meaning.

**"Was I right?" moment.**
- After the reveal, the robot asks the volunteer slot by slot, and the group compares with its vote cards.
- When it was wrong, the robot says so plainly and briefly: "I was wrong. My ears heard 'brown', but it was about your rabbit." A short apology helped the older children in a study of 4-7-year-olds keep trust in a robot [R10-29]; this is untested with older pupils. There is no claim of feelings.
- Answers live in the session ledger and are wiped with "forget me". Only daily totals are kept, if any.

**Wording rules.** Robot-centric and momentary ("my eyes see a lot of movement right now"). Never a trait ("you are a loud person"). Never a judgement of appearance.

**Age layers** (brief §2):
- 7-10: icons and the avatar (solid, faded, dashed or "?" per element).
- 11-14: the "clue balance", i.e. how much each sense pushed the answer, and the four certainty words. The clues are exact log-odds contributions (Shapley values in this additive model).
- 15-18: adding log-odds clues, calibration (glasses ECE 0.084) and why "sure" can still be wrong, bias, and the AI Act (the rule column in §7).

---

## Sources

Research files: `research/09-ethics-law.md` (legal analysis, verifier-corrected; [S#] numbers below), `research/10-hri-prior-art.md` ([R10-#]), `research/06-generative.md`, `research/01-call-and-tuai.md` (§1.6 form fields, §1.7 EC photography), `research/02-robots-linux.md` (PiDog V2 row; no CE/RED data). Prototype: `prototype/robotsees/` (`config.py`, `fusion.py`, `xai.py`, `session.py`, `perception/vision.py`, `perception/audio.py`, `perception/lexicon.py`, `render/imagination.py`), `prototype/live/run_live.py` (live mode, source-side drop, forget endpoint), `prototype/experiments/build_imagination.py` (LCM-Dreamshaper img2img), `prototype/demo/app.html` (UI labels, never-guess list). Measurements: `docs/_brief.md` §6 and `prototype/experiments/results/`.

- [S1] GDPR: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
- [S2] AI Act: https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401689
- [S3] Reg. (EU) 2026/1744 (Digital Omnibus on AI): https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng ; [S3a] https://www.nicfab.eu/en/posts/digital-omnibus-ai-official-journal/ ; [S3b] https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo ; [S3c] https://www.regulation-ai.eu/en/changes/
- [S4] Commission guidelines on prohibited AI practices, C(2025) 5052: https://ai-act-service-desk.ec.europa.eu/sites/default/files/2025-08/guidelines_on_prohibited_artificial_intelligence_practices_established_by_regulation_eu_20241689_ai_act_english_ied3r5nwo50xggpcfmwckm3nuc_112367-1.PDF
- [S5] Commission guidelines on Art. 50 transparency, C(2026) 5054: https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems
- [S6] Draft high-risk classification guidelines (19 May 2026): https://digital-strategy.ec.europa.eu/en/library/draft-commission-guidelines-classification-high-risk-ai-systems
- [S7] EDPB Guidelines 3/2019 (video devices): https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines_201903_video_devices_en_0.pdf
- [S8] EDPB Guidelines 05/2020 (consent): https://www.edpb.europa.eu/system/files/documents/files/file1/edpb_guidelines_202005_consent_en.pdf
- [S9] WP248 rev.01 (DPIA): https://ec.europa.eu/newsroom/article29/items/611236
- [S11] CNIL, augmented cameras: https://www.cnil.fr/fr/deploiement-de-cameras-augmentees-dans-les-espaces-publics-la-cnil-publie-sa-position
- [S12] Belgian APD DPIA list: https://www.autoriteprotectiondonnees.be/publications/decision-n-01-2019-du-16-janvier-2019.pdf
- [S13] Belgian APD, image right: https://www.autoriteprotectiondonnees.be/citoyen/themes/le-droit-a-l-image
- [S14] UODO DPIA list, M.P. 2019 poz. 666: https://api.sejm.gov.pl/eli/acts/MP/2019/666/text.pdf
- [S15] Polish Higher Education Act, Art. 11(1)(9), Dz.U. 2024 poz. 1571: https://api.sejm.gov.pl/eli/acts/DU/2024/1571/text.pdf
- [S16] SUT DPO (BKZB): https://www.polsl.pl/bkzb/ochrona-danych-osobowych/
- [SUT org chart 2026] SUT organisational chart, 1 Jan 2026 (research/09 V13): https://bip.polsl.pl/wp-content/uploads/sites/4/2026/01/Struktura_organizacyjna_PS_na_dzien_1.01.2026.pdf
- [MoJ FAQ] Polish Ministry of Justice FAQ on the Act of 13 May 2016, Art. 21 checks (research/09 V12): https://www.gov.pl/web/sprawiedliwosc/pytania-do-ustawy-o-ochronie-dzieci2
- [S18] SiW 2027 call: https://ec.europa.eu/eusurvey/runner/Call_SiW2027
- [S20] EU Grants ethics self-assessment: https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/common/guidance/how-to-complete-your-ethics-self-assessment_en.pdf
- [S22] UNICEF Innocenti, Guidance on AI and Children 3.0 (Dec 2025): https://www.unicef.org/innocenti/reports/policy-guidance-ai-children
- [S23] UN CRC, General Comment No. 25 (2021): https://documents.un.org/api/symbol/access?s=CRC/C/GC/25&l=en&t=pdf
- [S24] ICO Age Appropriate Design Code: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/code-standards/
- [S25] Kahn et al. 2012: https://pubmed.ncbi.nlm.nih.gov/22369338/
- [S28] Barrett et al. 2019: https://doi.org/10.1177/1529100619832930
- [S29] Gender Shades: https://proceedings.mlr.press/v81/buolamwini18a.html
- [S30] NIST IR 8525: https://doi.org/10.6028/NIST.IR.8525
- [S33] Biometric Mirror: https://doi.org/10.1145/3322276.3322304 ; [S34] How Normal Am I?: https://www.hownormalami.eu/
- [S40] SUT Order 50/2024 (child protection): https://bip.polsl.pl/wp-content/uploads/sites/4/2024/07/M.2024.260.Z.50.pdf
- [S41] SUT Order 240/2024 amending 37/2024 (register checks): https://bip.polsl.pl/wp-content/uploads/sites/4/2024/12/M.2024.1463.Z.240.pdf
- [S42] SUT Order 62/2024 (data protection policy): https://www.polsl.pl/rr9-bbi/wp-content/uploads/sites/600/2024/04/Polityka-ochrony-danych-62.2024.pdf
- [S43] CJEU C-184/20: https://www.dpcuria.eu/case?reference=C-184/20
- [S44] SUT Statute and public-body status: https://bip.polsl.pl/wp-content/uploads/sites/4/2021/05/M.2019.135.US_.42.pdf
- [S45] Polish AI Systems Act: https://gdpr.pl/ustawa-o-systemach-sztucznej-inteligencji-weszla-w-zycie ; [S46] Belgium (secondary): https://www.regulatoryai.eu/ai-act-belgium/
- [S48] FPF on Art. 5(1)(f): https://fpf.org/blog/red-lines-under-eu-ai-act-unpacking-the-prohibition-of-emotion-recognition-in-the-workplace-and-education-institutions/
- [S49] SUT research-ethics commission (secondary): https://www.researchgate.net/publication/366550639
- [S52] EDPB Guidelines 02/2026 (anonymisation): https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202602_anonymisation_v1_en_0.pdf
- [S53] Radio Equipment Directive: https://single-market-economy.ec.europa.eu/sectors/electrical-and-electronic-engineering-industries-eei/radio-equipment-directive-red_en
- [R10-27] Vollmer et al. 2018: https://www.science.org/doi/10.1126/scirobotics.aat7111
- [R10-29] Flanagan et al. 2024: https://pubmed.ncbi.nlm.nih.gov/38763071/
- [R10-76] Canon SELPHY CP1500 manual: https://cam.start.canon/en/P001/manual/html/UG-07_Reference_0070.html ; [R10-77] prices: https://pricehistory.app/p/canon-selphy-cp1500-wireless-compact-photo-printer-535rzy2h
- [R10-78] Brother QL-800: https://www.brother-usa.com/p/thermal-printers-labelers/QL800
- [R10-80] Apestaartjaren 2024: https://assets.mediawijs.be/2024-05/apenstaartjarenrapport_2024_lr_1_3.pdf
- Code of Practice on AI-generated content (research/06 [S48]): https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content
