# 10 – Exhibition experience design, child–robot interaction (CRI) and prior art

Track: exhibition experience design, CRI, prior art. For: TUAI DC5/DC7 demonstrator "How does a robot see you?" (Science is Wonderful! 2027).
Written: 2026-10-01. **Updated 2026-10-02** with a second research pass (web search available again); see "Gap-fill log 2026-10-02" at the end. All prices and URLs were accessed 2026-10 unless noted otherwise.
Method note: in the first pass the web-search quota ran out partway through, and claims were checked only by fetching known primary URLs. The second pass closed most of the open items, including the now-published **Science is Wonderful! 2027 call**, which changes the throughput design (see §0 item 3 and §2.2). Anything I still could not open is marked **UNVERIFIED**. Source numbers [n] refer to the list at the end.

> **Urgent (found 2026-10-02):** the SiW 2027 researcher application deadline is **6 October 2026, 12:00 CEST**, four days from this update. Results come on 28 Oct 2026. There is a mandatory online communication workshop on 4 Nov 2026 (and a science-show workshop on 9 Nov 2026 if you present a show). The fair runs 17–19 March 2027 in Brussels, with set-up on 16 March [62]. [verifier pass 2, 2026-10-02: all dates re-confirmed on the call page. The call is addressed to "MSCA fellows and alumni" and the audience is "over 4000 pupils". TUAI DC5/DC7 are MSCA Doctoral Network fellows, so they should qualify; the page does not mention DN candidates specifically. Funding covers travel, accommodation and meals for up to 3 people and up to 4 nights, plus approved materials (giveaways excluded). Apply via https://ec.europa.eu/eusurvey/runner/Call_SiW2027 . The page does not say what stand equipment (table, power, screen) is provided.]

---

## 0. Executive summary (decision-level)

1. **Start sessions explicitly. Do not rely on automatic engagement detection.** Even good public-robot systems misjudge who wants to interact. The CMU Roboceptionist aimed 66 % of its 816 head turns at people who were just passing, and 54 % of its spoken greetings got no response. Passers-by found unwanted greetings uncomfortable [2]. Use a large "paw" start button plus a marked spot on the floor. The camera should only confirm that one frontal face is inside the interaction zone. The conservative trigger "large, frontal face close by" had a 0.18 % false-positive rate in Microsoft's field system [3].
2. **3–5 minutes is long for a single exhibit.** Mean holding time across 61 interactive science-centre exhibits was 1.6 min (range 0.5–5.6) [12]. Exploratorium "APE" exhibits, designed for prolonged engagement, reached 132 s against 51 s for other exhibits [13]. Split the experience into short chapters and offer a **90-s express path** when there is a queue.
3. **Science is Wonderful! is mostly school groups, and the 2027 call fixes the visit unit at about 15 minutes per group.** The March 2026 Brussels edition had about 4,500 young visitors over 3 days, with 150+ researchers [16]. The 2027 call says [62]:
   - "On average, groups will spend 15 minutes at your booth."
   - Groups range "from a small group to an entire school class, usually from 7 to 18-year-olds".
   - "Modular activities work best."
   - Visitors "speak mostly French and Dutch"; language assistants are provided. English is required of researchers.
   - Selection criteria include whether the proposal is "interactive".

   So **the primary design unit is a 15-min group slot, not a 4-min solo session.** Within each slot, run 2–3 rounds of a 3–4-min robot "core loop" with rotating volunteer teams of 2–4 children. The rest of the group acts as "audience scientists" who vote and predict, watching a large, abstracted display. Keep the 4-min family/small-group session and a 90-s express path as secondary modules.
4. **Speech input is the weakest link.** In a 2017 study of child speech recognition, accuracy in noise fell from 77 % with the speaker at 25 cm to 18 % at 100 cm, and to about 0 % at 90° off-axis. Spontaneous child speech was recognised only about 18 % of the time [21]. [corrected by verifier: Kennedy et al. tested 11 children aged about 5 (M = 4.9 years) with a NAO robot and 2016-era engines. The distance and angle figures come from recordings replayed to the NAO's on-board mic. The 18 % figure is Google's 2016 cloud ASR under "relaxed" scoring. Treat this as qualitative evidence for 8–14-year-olds, not as calibrated numbers. The authors also found that background noise alone mattered less than expected when the grammar was constrained.] Off-the-shelf Whisper-small reaches 24–30 % word error rate (WER) on noisy classroom child speech and can hallucinate ("the" repeated 206 times) [22]. [corrected by verifier: the NCTE/MPT test sets are whole-classroom recordings of teachers and students (grades 4–8). In MPT, five room microphones were averaged. So this is far-field mixed-speaker audio, not close-talk child speech. It shows what happens in babble; it does not predict accuracy with a close-talk bone mic.] **Recommendation:** a tethered handheld "dog-bone" microphone with push-to-talk, held at 3–10 cm. Questions should be closed (2–4 answers, also shown as icons), with a touch fallback after 2 failed attempts. Do not put a denoiser in front of Whisper by default: a Dec 2025 study found that denoising made modern ASR (including Whisper) *worse* in all 40 configurations tested [70]. Always gate the recogniser with VAD, because Whisper hallucinates on non-speech [71].
5. **Make honesty part of the script.** Children 7–9 conformed to wrong answers from a robot group: 74 % of their wrong answers matched the robots' [27]. UNICEF's 2025 guidance asks that children be told up front they are dealing with an AI, and that systems avoid encouraging anthropomorphism [31]. EU AI Act Art. 50(1) requires this disclosure from 2 Aug 2026 [32]. The robot dog should say it is a machine, give its guesses with confidence levels, and ask children to correct it.
6. **Never show people-labels from a generic classifier, and never infer sensitive or psychometric traits.** ImageNet Roulette is the cautionary example: offensive "person" labels caused a public scandal, and ImageNet later removed most of its person categories [35][36]. Biometric Mirror (psychometric traits from faces) [37] and "How Normal Am I?" (beauty, BMI, life expectancy) [38] are critical art for adults, not templates for children. AI Act Art. 5(1)(f)/(g) prohibitions apply from 2 Feb 2025 [33].
7. **Copy two privacy-by-design patterns from prior art:** process everything locally (How Normal Am I?, Teachable Machine) [38][40], and show the crowd an abstracted view (skeleton, boxes, bars), never raw video of children.
8. **Treat safety as stand operations, and keep the e-stop out of visitors' reach.** In earlier museum robots, visitors liked pressing the emergency-stop button and so stopped the robot (cited in [63]). Robot dogs are "not a toy" (the Unitree Go2 manual says not for under-14s, keep ≥2 m from crowds, risk of pinched hands at the knees) [45]. Keep the robot in a "pen" on the table, staff-handled only, with an e-stop key, rest periods between sessions and attended battery rotation. Petoi Bittle X: 7.4 Wh Li-ion pack, about 1 h runtime, 1.5 h charge, and the pack does not power the robot while charging [43][44]. [corrected by verifier: "1 hour" is the headline figure on the spec sheet. Petoi's battery page gives scenario-dependent life: standby "several hours"; coding/testing postures "a couple of hours"; stepping in place "more than an hour"; running "less than 0.5 hours". With in-place gestures only, the 40–45-min swap plan holds. Any walking demo needs swaps about every 20–25 min.] [corrected by verifier: the official Bittle X spec sheet lists only an IMU as a sensor, so there is **no camera and no general-purpose microphone stream**. It has a built-in offline voice-command module (35+ fixed commands), and Petoi's own camera module is marked discontinued. A camera for "how the robot sees you" must therefore be an external or stand-mounted camera. Bittle X starts at USD 319; spare Petoi Li-ion battery USD 51 (petoi.com, accessed 2026-10).]
9. **Children left alone with public robots sometimes mistreat them.** In a shopping mall, 19 of 185 coded child–Robovie interactions were abusive. The abusers were always children, and abuse happened more when few adults were around [26]. One staff member must always be beside the robot.
10. **Keepsake: a printed, non-personal "robot's-eye card"** (sensor icons, inferences with confidence bars, "things I cannot know"), with a QR code to a *static, generic* explanation page. Canon SELPHY CP1500 [52][76][77]:
    - 41 s per glossy postcard (56 s semi-gloss), per Canon's manual.
    - MSRP USD 179.99; USD 151.99 on Amazon on 22 Sep 2026.
    - KP-108IN ink+paper set: USD 34.99–47.99 for 108 prints, so about USD 0.32–0.44 per print.

    In a 15-min group slot, one SELPHY prints at most about 20 cards. For a whole class, use a fast label printer such as the Brother QL-800 (up to 93 labels/min, USD 124.99) [78], or print one *group* card. Do not use per-visitor QR or e-mail delivery: in Flanders 59 % of primary-school children do not own a smartphone (Apestaartjaren 2024) [80].
11. **Borrow three proven patterns from recent exhibits:**
    - a **touchable replica** outside the robot's fence (MoS Boston's Spot) [75];
    - a **"trick the robot"** moment where visitors defeat perception and watch the confidence fall (Machine Gaze workshops; MoS "try to trick it") [75][96];
    - **face-free vision tasks** (gestures, held-up objects, shadow puppets) [88].

    Prior exhibits often use face recognition with no visible privacy statement (e.g., Deutsches Museum Bonn's face-recognition "voting booth") [85]. [corrected by verifier: the Bonn "KI-Wahlkabine" is *Smile to Vote*, an artwork by Alexander Peterhaensel. It critiques AI "political physiognomy" and has also been shown at ZKM, Futurium and the European Parliament (https://alexanderpeterhaensel.com/smiletovote ; https://zkm.de/en/artwork/smile-to-vote-political-physiognomy-analytics). It is a deliberate critique, not casual use of face recognition. The point that the exhibition page carries no camera/privacy note still stands.] Our sensor toggles plus visible "forget" are a real differentiator, but "first ever" is not provable; no exact precedent was found (§6).

---

## 1. Engagement and interaction detection for public robots (a)

### 1.1 Evidence

| Source | Setting | Key quantitative findings | Implication for us |
|---|---|---|---|
| Hall's proxemics, as summarised in [2] and [5] | Human–human | Intimate 0–0.45 m; personal 0.45–1.2 m; social 1.2–3.6 m; public >3.6 m. Varies with culture, age and familiarity [2]. | Interaction spot inside the personal zone (about 0.6–1.0 m from camera/robot). Audience in the social zone (1.2–3 m). |
| Walters et al. 2006 [5] (adults, PeopleBot) | Lab | 60 % chose an approach distance in the personal/social zone. About 40 % let the robot come up to the 0.5 m safety limit. About 10 % wanted it no closer than the far social zone. | People get closer to robots than to strangers. Keep the hardware out of reach with a pen, not with distance rules. |
| Mutlu/Weiss et al., Ars Electronica 2020 [6] | Festival, industrial robot | Most visitors came up to distances that would feel threatening from a human. Spectators copied the current participant's movements. | Expect children to lean in. Spectators learn by watching, so design for them. |
| Michalowski, Šabanović & Simmons 2006 [2] (Roboceptionist, CMU) | Building lobby, laser + camera | Robot perception logged 1,500 entries to the Engaged zone and 772 to the Interacting zone. Human coders saw only 195 real "engaged" stops, while 2,458 people walked past. 66 % of 816 robot turns went to passers-by, and 51 % of those came ≥3 s too late. 54 % of greetings got no response. Directed turns were followed by interaction 26 % of the time (undirected: 10 %). Spoken address: 48 % (robot "on the phone": 15 %). Adding vision to laser cut inappropriate greetings by 69 %. 46 % of interactions involved groups. People who interacted approached at average or slower walking speed. | Use motion (head turn, tail wag) liberally and **speech conservatively**. Use direction of movement, not only position. Expect groups. |
| Bohus & Horvitz 2009 [3] (MSR receptionist) | Office lobby, camera + mic array | The conservative trigger "entered F-formation and large, close, frontal face" had **0.18 % false positives** (6/3,274 face tracks). Predicting engagement ~3 s earlier with trajectory and attention features cut false positives about 3× compared with location-only features. At a 3-s early-detection time there were still about 4 % false positives (79 cases). [corrected by verifier: that figure is for the side orientation only; after manual review the authors put the true rate at 2.9 %. In the front orientation the rate at 3 s was 7.2 %. The paper itself names a "push-to-engage button" as the model conservative detector, which supports our button-first start.] Models did not transfer between two camera orientations, so they must be learned in situ. | The cheapest robust rule is near + frontal + stable. Earlier prediction costs false triggers. Tune at the venue. |
| Bohus & Horvitz 2009, multiparty engagement [4] | Same | Engagement split into sensing (state, actions, intentions of each agent), decisions (whom to engage, when) and rendering (gaze/behaviour). Handles people joining and leaving. | Use this three-layer structure in our state machine. |
| Thrun et al., Minerva 1998 [7] | Smithsonian NMAH, 14 days | 44 km, 620 tours, >2,600 exhibit visits. Crowds blocked its sensors for up to 20 min. "People seemed to enjoy blocking the robot's path." Caricatured moods (happy → angry when blocked) cleared paths faster than its face-less predecessor Rhino. Most visitors stayed <15 min in the museum. | Simple, legible expressions work. Expect testing and blocking behaviour. |
| Shiomi et al. 2006 [8] (Robovie, Osaka science museum) | 2 months | 91,107 visitors, 11,927 wore RFID tags, 2,891 questionnaires. Most were satisfied. Free play and guidance raised interest in science. Some effects were attributed to novelty. | Identification via tags is unnecessary for us. A start button gives the same "who is the participant" signal without identity. |
| Gannon, *Mimus* [9][10] | Design Museum London 2016–17. Now permanent at Copernicus Science Centre, Warsaw | Industrial arm in an enclosure ("as if a wild animal"). 8 ceiling depth sensors cover about 45 m². It picks "the most interesting person" by position, proximity and engagement, and "gets bored" and moves on. [corrected by verifier: atonaton.com says the attributes are "proximity, age, and activity level" (age estimated from height), with weights that change daily, e.g. some days favouring children. So Mimus *does* use an age-like attribute. We should not copy that part.] | A legible attention model ("I'm looking at *you* because you are closest") doubles as an XAI lesson. Enclosure as a design element. |
| **FROG** (EU FP7, grant 288235), Karreman et al. 2015 [63][64] | Royal Alcázar, Seville; remote-controlled 4-wheeled platform with a visible stereo camera and Kinect | About 500 visitors, alone or in groups of 2–7. The tour lasted 3 min 10 s and was started 87 times but finished only 58 times (67 % kept to the end). In 78 % of coded cases most people simply walked past. Single visitors and pairs joined far more often (36.4 % of cases) than groups formed around the robot (16.1 %). Visitors "seemed not prone to join strangers" and waited for the next tour. Distance was 30 cm–3 m in 55.5 % of cases, >3 m in 20.3 % and <30 cm in 4.7 %. Visitors treated the camera lenses as eyes: they waved at them and stood in front of them. Earlier museum robots (Sage; Museum für Kommunikation Berlin) were stopped because "people liked to push the emergency stop button". | (1) The camera **is** the robot's eyes in visitors' minds, so put the stand camera where the dog's "eyes" appear to be, or say clearly "this is my eye". (2) Expect about ⅓ attrition in a 3-min linear sequence; use short chapters. (3) Strangers will not merge into one session, so run whole-group slots or explicit turns. (4) The e-stop must be **staff-side only**. |

### 1.2 What to build (engagement layer)

**Start trigger options**

| Trigger | False triggers in crowds | Child-friendliness | Privacy | Verdict |
|---|---|---|---|---|
| Automatic face/proximity | High: passers-by, spectators [2][3] | Magical, but confusing when it misfires | Camera on for everyone passing | Use only for idle "attract" behaviour (head turn, tail), never to start a session |
| Floor mat / footprint pressure | Low–medium (children jump on it) | Good ("stand on the paws") | None | Good secondary signal |
| **Large paw / bone push-button** (e.g., a 100 mm LED arcade button, USD 9.95 [93]) | Very low, but children will mash it, as they do e-stops [63]. Ignore presses during a session and debounce. | Excellent; explicit agency | None | **Primary start** |
| RFID or token card | Low | OK, but adds logistics | Possible tracking | Not needed |
| Staff-triggered (keyboard) | None | Invisible | None | **Always available as override** |

**Recommended starting parameters.** These are design values to tune on site, not values taken from the literature.

- **Interaction zone:** paw marks on the floor 0.6–1.0 m from the camera. A session starts only after the button is pressed **and** one face meets all of:
  - frontal (yaw within ±30°);
  - large enough to be within about 1.2 m;
  - stable for ≥1 s.

  To set the face-size threshold: face height in px ≈ (image width in px × 0.17 m) / (2 × d × tan(HFOV/2)). For example, 640 px wide, 70° HFOV, d = 1.2 m gives about 65 px.
- **Primary participant** = closest qualifying face inside the interaction region of interest (ROI). All other faces are *not analysed* and are shown as blurred "spectators" on screen. This is privacy by design, and it also teaches that the robot only considers the person it was told to.
- **Disengagement:**
  - no qualifying face for 8–10 s → "Are you still there? Press my paw to continue."
  - 25–30 s → polite goodbye, visible "forget" animation, reset.
- **Groups (46 % of Roboceptionist interactions [2]):** support a "team" mode. One child holds the mic, one operates the sensor toggles, others vote. Do not try to track several people at once.
- **Idle/attract behaviour:**
  - liberal head turns towards motion, using DoA from a mic array or simple motion detection;
  - occasional "sniff" animation;
  - **no speech to passers-by** [2].

---

## 2. Dwell time, throughput and queues (b)

### 2.1 Evidence

| Source | Metric | Value |
|---|---|---|
| Serrell 1998, 34 exhibitions, via [12] | Mean time in exhibition; share of exhibits stopped at; "diligent visitors" | 13 min; 29 % of exhibits; 20 % of visitors used ≥ half of exhibits |
| Sandifer 2003 [12] (Reuben H. Fleet Science Center, 61 interactive exhibits, 47 tracked visitors, 5-s engagement criterion) | Mean attracting power; mean holding time | 0.38; **1.6 min** (range 0.5–5.6 min; longest "Phone Your Image" 5.6 min). Technological novelty and open-endedness predicted longer holding. "User-centred" exhibits (visitor's own body or voice) were *not* significant. [verifier note: school groups were excluded from Sandifer's sample, and exhibits with long holding times attracted *fewer* visitors (r = −0.37) because people skipped exhibits that were already in use.] |
| Exploratorium APE Phase 2 [13] | Holding time, APE vs non-APE | **132.3 s vs 51.1 s** (p < .001). The Phase 1 interim report (2004) and the Phase 2 report both state this, per their indexed text; both PDFs return HTTP 403 to automated fetches [13]. |
| Bitgood attention–value model [14] | Attraction (stop ≥ about 5 s); holding; focus ≥ 2–3 s | Attention depends on perceived value ÷ cost. Reduce reading and waiting cost. |
| Diamond 1986, via [12] | Family visit length | About 2 h total per museum visit |
| Serrell "51 % Solution" benchmarks [68] | Thorough use of an exhibition | "Exceptionally thoroughly used" means >51 % diligent visitors (stopping at more than half the elements) and a sweep-rate index <300 ft² per minute |
| PARSEC science-experience centre, Bengaluru (arXiv 2607.13724, 2026) [66] | Median dwell, 2,816 logged sessions at 8 push-button exhibits [corrected by verifier: the paper describes *touch-enabled* exhibits logged by ESP32/RPi firmware with a 150 ms touch debounce; it does not call them push-button exhibits] | Games **170 s** (170.2); quizzes **118 s** (117.8). Escalating-challenge games produced both longer *and* denser interaction |
| Galaxy Makers, Royal Society Summer Science Exhibition 2016 [65] | Throughput of a research stand at a science fair | 3 interactive machines, 64 h open, 14,371 visitors to the exhibition. About **2,000 people used the machines** (about 31/h across 3 machines, i.e. about 10/h per machine). More than 3,000 were engaged directly. 4–6 demonstrators at a time. Keepsake: a paper "hologram" pyramid plus a code for the creation they made; **40 % (about 700) visited the website** later and 75 % of those came back |
| **Science is Wonderful! 2027 call** [62] | Visit unit at this event | "On average, groups will spend **15 minutes** at your booth"; groups range "from a small group to an entire school class, usually from 7 to 18-year-olds"; "modular activities work best" |
| Brščić et al. 2015 [26] | Abuse cases | 19 of 185 coded child–robot interactions in a mall |
| Science is Wonderful! 2026 [16] | Audience | About 4,500 young visitors, 3-day event, Brussels (March 2026); 150+ researchers from 30+ countries; primary and secondary school pupils; free |

**Interpretation:**
- At SiW the booth gets about 15 min of a group's time [62]. The question is therefore not whether one child stays 4 min, but **how to keep 5–28 children busy for 15 min with one robot.** The answer is rotating volunteer teams plus a visible audience task.
- 3–5 min is roughly 2–3× a good interactive's mean holding time. It is achievable only with a strong hook in the first 10–20 s, visible progress ("chapter 2/4"), and personal relevance. Here the visitor *is* the content, but note Sandifer found "user-centredness" alone was not significant [12].
- Spectators count: Sandifer counts "watching another visitor interact" as engagement [12], and Ars Electronica spectators copied participants [6].

### 2.2 Throughput estimates for a single-station stand

Assumptions: changeover 30–45 s. Utilisation 75 % to allow for resets, battery swaps, explanations and breaks; this is my planning assumption.

| Mode | Session | Cycle | Cycles/h (100 %) | Active participants/h at 75 %: solo / pair / team of 3 |
|---|---|---|---|---|
| Express | 1.5 min | 2.0 min | 30 | 22 / 45 / 67 |
| Short standard | 3.0 min | 3.5 min | 17 | 13 / 26 / 39 |
| Standard (recommended) | 4.0 min | 4.75 min | 12.6 | 9 / 19 / 28 |
| Long | 5.0 min | 5.75 min | 10.4 | 8 / 16 / 23 |
| Class show (whole class watches, 3 rotating drivers, class votes) | 6 min | 7 min | 8.5 | 3 drivers + about 20 spectators per show, i.e. about 150–200 children/h "reached" [verifier note: about 195/h is the 100 % figure; at the 75 % utilisation used elsewhere it is about 145–150/h] |

**Class arrival scenario.** A class of 25 doing team-of-3 standard sessions needs 9 cycles × 4.75 min ≈ 43 min. That is impossible in the **15-min average group slot** set by the SiW 2027 call [62].

**SiW group-slot model (primary mode for 2027):**

| Slot segment | Duration | Who is active | Children "hands-on" |
|---|---|---|---|
| Welcome, honesty script, "you are the scientists" | 1:30 | Whole group; FR/NL language assistant translates [62] | 0 |
| Round 1: robot core loop (camera chapter + take-a-sense-away) | 3:30 | Team A (3 children: sensor operator, bone holder, judge); audience votes with cards | 3 |
| Round 2: core loop with a different sensor set (e.g., mic only) | 3:30 | Team B; audience predicts *before* the reveal | 3 |
| Round 3 (optional, small groups) or audience "be the robot" game | 3:00 | Team C or everyone | 3 / all |
| Reveal + "forget" + group card | 2:00 | Whole group | – |
| Changeover (robot rest, wipe bone) | 1:00–1:30 | Staff | – |
| **Total** | **about 15:00 + 1:00 changeover** | | **6–9 hands-on per group; 100 % of the group watches, votes and sees the forget step** |

At one group per 16 min, a 6-h fair day gives up to about 22 slots at 100 % (about 16 at 75 % utilisation). That means about 100–140 hands-on children and 250–450 children reached per day (group sizes 15–28). Fair opening hours and the number of groups per booth are **UNVERIFIED**; ask the organisers. Galaxy Makers reached about 10 hands-on users per hour per machine with 4–6 demonstrators [65], which is the same order of magnitude.

Hence **four switchable modules**, consistent with "modular activities work best" [62]:
- **Group slot** for school groups (default at SiW);
- **Standard** for families and quiet periods;
- **Express** for a queue of individuals;
- **Class show** on a stage, if a 30-min science-show slot is requested (SiW shows have about 60 people and 15 shows over 3 days [62]).

**Queue management patterns:**
- An attract-loop screen facing the aisle, showing an *abstract* "robot's view" (skeleton or boxes only).
- A visible "next team" spot and a session timer.
- A staff host who pre-briefs the next team ("you will choose which senses the robot gets").
- A paper "sensor menu" card that waiting children fill in. This turns waiting into preparation.
- Never let more than about 2 teams queue: switch to Express or Class show instead.
- Visitors do not like joining strangers mid-session; they wait for the next run (FROG [63]). Show a visible "next run starts in 0:40" countdown instead of letting newcomers drift in.
- Museum of Science Boston runs Spot on a fixed, fenced course with a cycle of about 180 s. A **touchable replica** sits outside the fence for children who want to handle "the robot" [75]. Copy this: a spare unpowered (or 3D-printed) dog at the queue line absorbs the urge to touch.

---

## 3. Child–robot interaction design (c)

### 3.1 Evidence

| Topic | Source | Finding |
|---|---|---|
| Conformity / over-trust | Vollmer et al. 2018, *Science Robotics* [27][28] | Children 7–9: 87 % correct alone, 75 % with a robot group. **74 %** of wrong answers matched the robots. Adults resisted. Authors call for protective measures. |
| Calibrated trust | Flanagan, Georgiou, Scassellati & Kushnir 2024, *Cognition* [29] | 168 children aged 4–7 and 168 adults. Trust fell fastest when errors were intentional. Older children rejected unhelpful partners. Older children kept trust longer when a *robot* apologised for a mistake. [verifier note: "older children" here means the older part of the 4–7 sample, below our 8–14 audience. The study also found older children were *less* trusting than adults overall.] |
| Transparency about being a machine | van Straten et al. 2020, *ACM THRI* (summary via [30]) | Telling children the robot lacks human psychological capacities reduced anthropomorphism, trust, perceived animacy and similarity. |
| Robot asking questions | van Straten et al., *Computers in Human Behavior* (2×2, 293 children aged 7–10, NAO, science museum) [30b] | Robot question-asking raised trust and perceived cognitive perspective-taking. Robot self-disclosure *lowered* perceived affective perspective-taking. |
| Over-attribution in the wild | Minerva poll, n = 63 [7] | 36.9 % rated its intelligence "human", 29.5 % "dog", 25.4 % "monkey". |
| Expressive voice | Kory Westlund et al. 2017 [24] (45 children aged 4–7, Tega) | Expressive voice gave higher concentration and engagement, more target-word use (1.6 vs 1.0) and better story retention after 4–6 weeks. Liking was the same. |
| Repair when speech recognition fails | Cheng et al. 2018 [25] (14 preschoolers, 107 failed attempts) | Children persisted by repeating and changing tone. Parents moved through four phases: suggest → intervene → resign → declare it broken. |
| Repeated failures | Parreira, Neto, Rocha & Ju 2026 [23] (59 children aged 8–10) | Children adjusted prompts and tone and became more emotional. They disengaged or **sought an adult**. Errors did not hurt their perception of the robot. |
| Speech recognition design for children | Kennedy et al. 2017 [21] | Constrain answers, add touch input, place the child optimally (seat or marker), constrain the recognition grammar. Robot speech is still valuable for engagement even when recognition is poor. |
| Abuse and adult presence | Brščić et al. 2015 [26] | Abuse was always by children, more frequent where few people and no parents were present. Children ignored the robot's repeated requests to stop. |
| Policy | UNICEF *Guidance on AI and Children* v3 (2025), Requirement 5 [31] | "Clearly warn children and caregivers upfront that they are interacting with an AI." "Prevent anthropomorphizing." "Use age-appropriate language." Requirement 3: privacy by design, children's data agency. |
| Law | EU AI Act Art. 50(1) (applies from 2 Aug 2026) [32]; Art. 50(3) (inform persons exposed to emotion recognition or biometric categorisation) | Disclosure that this is an AI, unless obvious. Our design avoids emotion recognition entirely. |

### 3.2 Design rules derived from the evidence

**Honesty script (deliver in the first 20 s, in both voice and on screen):**
- "I'm a robot – a machine shaped like a dog. I don't really know you. I only *guess* from my sensors. You decide which sensors I may use. I forget everything when we finish."
- This satisfies UNICEF Requirement 5 and AI Act Art. 50(1) [31][32].

**Calibrated, not deferential:**
- Every inference gets a confidence level ("I'm *pretty sure* / *not sure*") and an evidence line ("because my camera saw…").
- End each chapter with "Was I right?" (✓/✗ buttons). This invites correction and models fallibility, which counters conformity [27].
- When the robot is wrong, it says so plainly and briefly apologises. Apology helped older children keep calibrated trust [29].
- Never use social pressure ("everyone says…") and never use persuasion.

**Zoomorphism without deception:**
- Dog behaviours (tail wag, head tilt, "sniff") are fine as *signals*.
- Explain them as signals: "I wag my tail when my camera finds a face". This makes the robot's own behaviour part of the explanation.
- Avoid claims of feelings ("I love you", "you made me sad"). Avoid self-disclosure: it lowered perceived perspective-taking in the CHB study above [30b].

**Voice:**
- Expressive, warm, clearly synthetic or robotic, not an imitation of a real person [24].
- **Pre-record or pre-synthesise every prompt** in each language. No live TTS dependency and no LLM free text to children. This keeps the robot predictable and safe.

**Question design (for ages 8–14):**
- One question per turn, ≤ 10 words, 2–4 answers always shown as large icons + words. The answer can be spoken *or* tapped [21].
- Use non-sensitive topics only: favourite animal, colour or sport; "wave at me"; "hold up something red".
- **Never ask** name, age, school, address, family, feelings, health, religion or appearance judgements.
- Ask *about the robot's guess* rather than about the child ("I think your T-shirt is blue – right?"). This keeps the focus on how the robot perceives, and the answer is a binary the system can check.

**Turn-taking:**
- Push-to-talk on the bone. The robot "listens" visibly (ears up, LED, screen waveform).
- Listen window ≤ 5 s.
- After the 1st failure: "I didn't catch that – try holding the bone closer."
- After the 2nd failure: switch to touch automatically, without blame. Children otherwise persist or look for an adult [23][25].

**Shy or silent children:**
- A full non-verbal path (buttons, gestures). Silence is a valid answer ("That's OK – you can just press a picture").
- Team mode lets a friend or parent speak.
- The robot never comments on the child's appearance, behaviour or silence.
- A staff "skip" key is available.

**Multilingual:**
- Language picker (flag + word) on the start screen. SiW 2027 is in Brussels, and visitors "will speak mostly French and Dutch". Language assistants are provided, and the team is encouraged to recruit FR/NL speakers [62]. So **FR + NL are mandatory and EN is the fallback.** PL is only for TUAI's home audience. Brief the language assistant with a one-page script, because they will voice the "honesty" intro.
- Keep the speech-recognition vocabulary small per language (answer options only). On-screen text is short and icon-led.

**Parents and teachers:**
- A printed "For grown-ups" card: what is sensed, what is inferred, what is *not* inferred, what is stored (nothing).
- Adults are invited to hold the bone or to be the "sensor operator".
- Adult presence also reduces misbehaviour [26].

---

## 4. Noise and audio capture (d)

### 4.1 Evidence

| Fact | Source |
|---|---|
| Sound pressure falls by about 6 dB per doubling of distance in a free field (less in reverberant halls). Moving a mic from 1 m to 5 cm gains about +26 dB of speech level relative to diffuse background noise. | Inverse-square law [53] |
| [verifier note: 11 children aged about 5; recordings replayed to a NAO robot's on-board mic; Nuance VoCon with a fixed number grammar; clean audio at 100 cm gave only 4 %] Child speech recognition vs distance, in noise (frontal): 25 cm 77 % → 50 cm 44 % → 75 cm 23 % → 100 cm 18 %. At 45° recognition drops sharply; at 90° it is about 0. External studio mic 84 % vs NAO on-board mic 61 % (robot fan noise). Spontaneous child speech about 18 % recognised. Authors' verdict: interactions relying *only* on speech are "still out of reach". | Kennedy et al. 2017 [21] |
| Off-the-shelf Whisper-small.en on noisy classroom child speech: WER 24.5 % (NCTE) and 30.2 % (MPT). Babble noise is the hardest case. Whisper hallucinated ("the" ×206). [corrected by verifier: whole-classroom recordings of teacher plus student speech from room mics (MPT: five mics averaged), not isolated child speech] | Classroom ASR study, arXiv 2409.14494 [22] |
| Fine-tuned Whisper on child speech (MyST) reaches about 9 % WER, but in read/clean conditions. | Kid-Whisper, AAAI/AIES [22b] |
| Lombard speech (raised voice in noise) degrades recognition even after level normalisation. | ScienceDirect (Speech Communication) [54] |
| Museums open to the public (visitors + HVAC) measured LAeq **61–66 dB(A)**, against 27–41 dB(A) empty: 25–36 dB(A) more with visitors. The recommended maximum background level for exhibition rooms is 45 dB(A). [corrected by verifier: 61–66 dB(A) is one modern art museum (Serralves, Porto) with only about 5–20 people per room; the old museum (Soares dos Reis) measured 58–62 dB(A). The 45 dB(A) ceiling is for HVAC background *without* visitors; the paper's ideal *with* visitors is ≤55 dB(A). A hall full of school classes will very likely be louder than these art-museum rooms, so 61–66 dB(A) is a floor, not an estimate.] | Carvalho, Gonçalves & Garcia, Noise-Con 2013 [69] |
| Trade-show organisers cap booth sound, e.g. "a maximum of 85 dBC with an LEQ 30 seconds", measured ≥10 ft from neighbours, with speakers pointed into the booth. | Example exhibitor rules (LDI) [73] |
| The brief assumes 70–85 dB(A) in a science-fair hall full of school classes. That is plausible given the above, but I found no direct measurement for SiW. | **UNVERIFIED.** Measure on site with a sound-level-meter app; ask SiW about amplification rules. |
| Speech enhancement in front of modern ASR: noisy original audio beat MetricGAN+-denoised audio in **all 40 configurations** (Whisper, Parakeet, Gemini Flash 2.0, Parrotlet; 1.1–46.6 points absolute semWER worse with denoising). Medical speech, Dec 2025. | Chondhekar et al., arXiv:2512.17562 [70] |
| Whisper hallucinates text on non-speech or silence; a 2025 fine-tune (Calm-Whisper) cut this by >80 %. The standard practice is a VAD gate plus rejection on `no_speech_prob` / `avg_logprob`. | arXiv:2505.12969 [71]; openai/whisper discussion #1606 |

**Tools (verified 2026-10):**

| Tool | What it is | Licence | Notes |
|---|---|---|---|
| RNNoise 0.2 (Xiph, released Apr 2024) | RNN noise suppression; SSE4.1/AVX2; models trained on public data | BSD-3-Clause | Very light on CPU [17][18] |
| DeepFilterNet (DFN3) | Deep-filtering speech enhancement; Rust real-time version + LADSPA plugin; real-time factor 0.19 single-thread on i5-8250U | MIT / Apache-2.0 | 4.8k GitHub stars. An Intel OpenVINO port exists on Hugging Face (`Intel/deepfilternet-openvino`) [19][19b] |
| Silero VAD | Voice activity detection, about 2 MB, <1 ms per 30 ms chunk on 1 CPU thread, 8/16 kHz | MIT | [20] |
| ReSpeaker XVF3800 USB 4-mic array (Seeed) | On-board AEC, AGC, DoA, VAD, dereverberation, beamforming, noise suppression; "up to 5 m" | Hardware, USD 54.90 (Seeed store, accessed 2026-10) | [46] |
| Samson Q2U | Dynamic cardioid USB/XLR handheld-style mic | Hardware: about USD 70–80 for the mic alone (e.g., Best Buy USD 79.99); about USD 99.99 for the podcast pack (retail listings, accessed 2026-10) | [47][94] |
| Vosk (alphacep/vosk-api) | Offline ASR, about 50 MB models incl. EN/FR/NL/PL, streaming, **runtime-reconfigurable vocabulary/grammar** | **Apache-2.0** (GitHub, about 15k stars) | Best fit for 2–4 closed answers: it cannot invent long text [72]. [verifier: models page, accessed 2026-10, lists vosk-model-small-nl-0.22 (39 MB, WER 22–27 % on adult benchmarks), small-fr-0.22 (41 MB, 23.95 % CV), small-pl-0.22 (50 MB), small-en-us-0.15 (40 MB), all Apache-2.0. Runtime grammar/vocabulary works only with small models ("Big models are static"). The larger Dutch Kaldi_NL models are **CC-BY-NC-SA**. https://alphacephei.com/vosk/models] |
| 100 mm LED arcade button (Adafruit #1185) | Push-to-talk / start button | Hardware, USD 9.95 | Wire to a USB HID encoder [93] |

### 4.2 Capture options compared

| Option | Speech-to-noise ratio in 75–85 dB babble | Throughput / hygiene | Child usability | Verdict |
|---|---|---|---|---|
| Robot on-board mic | Worst: distance plus servo/fan noise [21] | Good | Natural | Do **not** use for speech recognition |
| Far-field beamforming array (e.g., XVF3800) at 0.5–1 m | Medium. Beamformers struggle with diffuse babble and several children talking. DoA is useful. | Hands-free | Natural | Use for **DoA show effects** ("robot turns to the voice"), not as primary speech input |
| Shotgun mic aimed at the participant spot | Medium. Weak rejection of low frequencies and reflections indoors; must be aimed. | Hands-free | Children move off-axis (45° gives a sharp drop [21]) | Not recommended |
| Gooseneck cardioid at a "speak here" paw target, 10–20 cm | Good if the child leans in | Hands-free | Heights vary (8–14 y) | **Fallback** |
| Headset | Best | Poor: fitting time, hygiene | Intrusive | No |
| **Tethered handheld "dog bone" (dynamic/close-talk capsule + push-to-talk button), held at 3–10 cm** | Best practical, about +20–26 dB over 1 m | Wipeable; no batteries; no RF congestion | Fun prop; push-to-talk teaches "the robot only hears when you let it" | **Primary** |

**Recommended audio pipeline:**
1. Push-to-talk gate on the bone.
2. **No denoiser by default.** Denoising degraded Whisper and other modern ASR in every configuration of a 2025 study [70]. Keep RNNoise/DFN3 only for the *audience-facing* audio visualisation, or if our own A/B test on child speech in babble shows a gain. That has not been tested for child speech; it is **UNVERIFIED** here.
3. Silero VAD to gate and trim the clip. No speech frames → do not call the recogniser at all, which avoids hallucinations [71].
4. Speech recognition with a constrained answer set, choosing one of two routes and A/B testing them:
   - (a) **Vosk with a per-question grammar** of the 2–4 options in FR/NL/EN [72];
   - (b) Whisper-small, then fuzzy-match to the options, rejecting on `no_speech_prob` / `avg_logprob`.

   Reject below a confidence threshold.
5. Show "I heard: …" on screen with a confirm tap.

Record festival-like babble at 80 dB and use it for acceptance tests. The privacy-by-design point: push-to-talk means **the microphone only listens while the child presses the button**. That is itself an XAI and consent lesson.

---

## 5. Safety of small quadrupeds around children (e)

### 5.1 Evidence

| Item | Source | Fact |
|---|---|---|
| Age rating | Unitree Go2 manual [45] | "Not a toy… not intended for use by persons under the age of 14." Keep ≥2 m from crowds. "Hand may be pinched at the motion joints, such as at the knee joint." Do not lift while powered. Operate at 5–35 °C. |
| Example sub-USD 600 dog | Petoi Bittle X specs [43] | 190×153×107 mm, 269–353 g, plastic frame, coreless digital servos (max 8.4 V). Li-ion 7.4 V 1,000 mAh (7.4 Wh), about **1 h runtime**, **1.5 h charge**, 2 A typical / 5 A max. |
| Battery behaviour | Bittle X manual [44] | Pack has a protection circuit and status LED. "**The battery won't supply power during charging**", so the stock pack cannot be used tethered while charging. [verifier: also stated on https://docs.petoi.com/technical-support/battery ("The battery will NOT supply power during charging"; 5 V/1 A charger). The same page gives running life as "less than 0.5 hours" and stepping in place as "more than an hour".] |
| Overheating and pinching | Petoi docs [42] | Do not run too long (overheats electronics, shortens servo life). Pinch hazard at the arm claws. Do not force joints by hand. |
| Other sub-USD 600 options (official Hiwonder store, accessed 2026-10) | [48][95] | **MechDog** (verifier-corrected prices):<br>• Standard USD 299.99 (ESP32, no camera)<br>• Advanced 369.99 (adds an ESP32-S3 Wi-Fi vision module)<br>• Ultimate 469.99<br>• Pro Developer Kit 569.99 (vision module + WonderEcho AI voice module)<br><br>**PuppyPi Standard:** USD 589.99 (RPi 4B 4 GB) or 599.99 (RPi 5 2 GB), with an HD wide-angle head camera and an AI voice module. That **fits the ~USD 600 budget** at the official store [verifier: prices re-confirmed 2026-10 on hiwonder.com/products/puppypi.json, all variants listed as available; RPi 5 4 GB is USD 659.99. The product page advertises the AI voice module, but which kit tier includes it (Standard vs Advanced/Pro) could not be confirmed from the text, so treat it as **UNVERIFIED** for the Standard kit]; resellers charge more (RobotShop USD 678.99 for RPi 4B, 875.99 for RPi 5 8 GB). Hardware choice belongs to the hardware track. |
| Li-ion handling | University EHS guidance [49] | Never charge unattended. Use a fire-safe bag or container on a non-combustible surface. Do not charge swollen or damaged packs. Store at 20–80 % (about 50 % long term). Unplug when full. |
| Public-demo incidents | Interesting Engineering, 5 Jun 2026 [50] | A Unitree G1 *humanoid* kick hit a child in Xinjiang (not seriously hurt). An earlier G1 fall struck a spectator. Shows crowd-distance failures at demos. |
| Toy law | Toy Safety Regulation (EU) 2025/2509: published 12 Dec 2025, applies from 1 Aug 2030 [51] | Our robot is a staff-operated exhibit, not a toy placed on the market. It is not directly applicable, but it is a useful reference for small parts and battery-access thinking. Legal scope belongs to the legal track. |

### 5.2 Operating practice

**Robot pen:**
- Robot sits on a stable table, centred, inside a clear acrylic fence 10–15 cm high with rounded edges.
- Minimum about 15 cm from the fence to the robot's reach envelope.
- Table edge ≥ 40 cm from the robot.
- Movement restricted to in-place gestures (sit, head tilt, tail, paw lift, stand). **No walking routines during visitor sessions.** Walking happens only in staff demos with the pen closed.

**Hands-off:**
- Visitors interact through the bone, buttons and screen, not by touching the robot.
- Staff-only handling, robot powered down or in rest when handled.
- Sign: "I'm a machine – please don't touch my legs."

**E-stop:**
- A physical big red button on the staff side that sends "rest/relax all servos" and freezes the UI.
- **Never within visitors' reach.** Museum visitors "liked to push the emergency stop button and unintentionally stopped the robot" [63].
- Test it at every setup.

**Duty cycle:**
- Servos relaxed (lying down) during changeovers.
- A 2–3 min "nap" every about 20 min of activity.
- Check temperature by touch or IR thermometer at battery swaps.

**Battery rotation (Bittle-class, 1 h rated):**
- Swap every 40–45 min of show use, before brown-outs cause twitchy servos.
- With a 1.5 h charge you need **≥3 packs**: one in the robot, one charging, one cooling or spare.
- About 8 swaps per 6-h day.
- Charge only on the staff table, in a LiPo bag, attended, with one charger per pack. Remove packs from the venue overnight unless the venue rules allow otherwise (**UNVERIFIED**; check the venue's battery and fire rules).
- Tethered DC supply: preferred if the robot's power input allows it. For Bittle X, Petoi's battery page confirms there is **no pass-through**: the battery does not supply power while charging (5 V/1 A USB-C charging) [44][74]. Bittle X therefore runs on swapped packs only, unless the hardware track builds a regulated 7.4–8.4 V battery-eliminator lead (**UNVERIFIED**; needs a current rating of ≥5 A peak per the spec [43]).

**Cables and stand:**
- Tape all cables. Bone cable on a strain-relief hook. No cables crossing the visitor side.
- Wipe the bone between classes.

**Staffing and logging:**
- 2 people minimum: a host/explainer and a robot operator. Never leave the robot powered and unattended [26].
- Incident log: time, what happened, action taken.

---

## 6. Prior art: AI perception and AI-literacy exhibits (f)

| Exhibit / programme | What it did | What worked | What failed or is risky | Lesson for us |
|---|---|---|---|---|
| **ImageNet Roulette** (Crawford & Paglen, 2019) [34][35][36] | Face detector + classifier trained on ImageNet "person" categories labelled uploaded selfies | Made dataset bias tangible; went viral | Offensive and racist labels ("…until it called me a racist slur", *Guardian*, Sep 2019, via [36]). ImageNet "person" subtree had 2,833 subcategories [35]. Images began disappearing in Jan 2019 [35]. Filtering left 158 of 2,832 synsets, and 2,702 person categories were removed in 2021 [36]. The creators took the website offline on **27 Sep 2019**, about two weeks after its public launch. It continued as a physical installation at Fondazione Prada, Milan, and ImageNet announced removal of about 600,000 person images [83]. | **Never** show raw people-labels from a generic model. Use a closed, curated, non-evaluative label set. |
| **Biometric Mirror** (Univ. Melbourne; DIS 2019) [37] | Inferred "demographic and psychometric information" from face photos and showed speculative consequences | Started a public ethics debate | Inferring psychometric traits from a face is pseudo-scientific and, for children, harmful. It showed 14 characteristics, "from gender, age and ethnicity to attractiveness, weirdness and emotional stability", which became "more personal" the longer one stood there. Ratings came from a crowd-sourced dataset of several thousand faces rated by over 30,000 respondents. Consent was given with a hand wave. It ran at the University of Melbourne (Eastern Resource Centre) with Science Gallery Melbourne until Sep 2018 [84]. | Forbidden pattern for our audience. Our "inferences" must be observable, non-sensitive and verifiable (e.g., T-shirt colour, distance, hand raised). |
| **How Normal Am I?** (Tijmen Schep, EU H2020 SHERPA, grant 786641) [38] | Webcam judges beauty, age, gender, BMI, life expectancy and emotion, with a narrated critique | **All processing local in the browser; "No personal data is sent to our server"**; strong narration | The attributes judged are inappropriate for children | Adopt the local processing, the narration, and an EU-project framing. Drop the attributes. |
| **Gender Shades** (Buolamwini & Gebru 2018), shown in Ars Electronica *Understanding AI* [39][41] | Audited commercial gender classifiers | Error up to **34.7 %** for darker-skinned women vs **0.8 %** for lighter-skinned men | – | Reason for excluding gender, age and ethnicity inference. Good one-line XAI fact for adults. |
| **Ars Electronica Center – *Understanding AI*** (Linz) [41] | Gallery including "Computer Vision Fails", live "Keypoint Detection", "How animals and people see the world differently", StyleGAN faces | Showing *failures* and live keypoints makes perception concrete | – | Show live keypoint skeleton and boxes (non-identifying), and include a "how I get it wrong" chapter. |
| **Teachable Machine** (Google) [40] | Train image, audio and pose models in the browser (TensorFlow.js) | Instant, tangible, local training | "An experiment, not an official Google product" | In-browser/local training is a proven pattern for live demos. Apache-2.0 helper libraries. |
| **Quick, Draw!** (Google) [55] | AI guesses doodles in real time | Game framing, visible running guesses | Collected 50 M drawings (345 categories, CC BY 4.0); "may still contain inappropriate content" despite moderation | Show the guess evolving in real time. **Do not** collect visitor data. |
| **Experience AI** (Raspberry Pi Foundation + Google DeepMind) [56][91] | Free secondary-school AI lessons; "tens of thousands of educators and millions of learners across more than 180 countries". In Sep 2024 it had about 750k learners and targeted 2 M+ with a USD 10 M Google.org grant, including partners in 17 countries in Europe, the Middle East and Africa | Teacher-ready | – | Align vocabulary with school AI lessons, e.g. "data → model → prediction". Offer teachers a follow-up link. |
| **Day of AI / MIT RAISE** [57][58] | Free PreK–12 curriculum incl. how computers see, facial recognition, data and privacy. Reach: "5 M+ students" (Day of AI page) vs "2 M+ learners, 175 countries" (RAISE page); figures inconsistent | Age-graded materials | – | Borrow age-graded explanations of computer vision. |
| **AI: More than Human** (Barbican, 16 May–26 Aug 2019; touring, with Groninger Forum) [59] | Large festival-style AI show | Scale, art + science mix | Visitor-level outcomes not published (UNVERIFIED) | Competes on spectacle. We should compete on *personal* explanation. |
| **Copernicus Science Centre robots** (Warsaw) [10][92] | Ameca (GPT conversation; "curator" of the exhibition *The Future is Today*, which also has a "Digital Brain" AI section), Spot (visitors steer it), Robot Kopernik (GPT-3), RoboThespian (2010), Babyclon, Mimus. Uses face recognition, speech-to-text, GPT and TTS. | Spectacle; a robot dog in a top Polish science centre; Mimus attention model | Open-ended LLM conversation with children carries content risks (we have no outcome data) | Polish visitors have seen Spot: our distinctive feature is *transparency*, not locomotion. Avoid open-ended LLM chat. |
| **Copernicus LivingLAB** [11] | Rotating research stations with visitors | "Minors can participate… only with the consent of their guardian"; anonymous data | – | Model if we collect *any* research data (e.g., anonymous button logs). |
| **The Glass Room** (Tactical Tech) [60] | "Tech shop" exhibitions + Community Edition (30+ languages); 600k+ visitors, 73 countries | Demystification through familiar framing | – | Use a familiar metaphor (a pet "learning" you) and pair it with a privacy take-away. |
| **Minerva / Robovie / Roboceptionist / Furhat at Tekniska museet** [2][7][8][61] | Public robots | Caricatured emotions [7]. Furhat: 2 visitors + robot sort cards on a touch table; Furhat deliberately had *imperfect, randomised beliefs*, so humans had to decide whether to trust it [61]. | Perception errors and late, misdirected behaviour [2]. Crowd blocking [7]. | Use a touch table or screen as the joint-attention object. Let the robot *visibly* be uncertain. |
| **Brščić et al. 2015 (Robovie in mall)** [26] | – | – | Abuse by unattended children | Staff presence and a pen. |
| **Museum of Science Boston – *Exploring AI: Making the Invisible Visible*** (opened 27 Sep 2022) [75] | 3 dozen components: an object-recognition model to "try to trick", training-data bias interactives, Spot on a fenced obstacle course | Spot runs every day on a fixed course with a cycle of about **180 s** and is staff-operated with a controller. A **touchable replica** stands outside the course. A "Robot Roundup" show has staff driving Spot and a Unitree Go2 while answering questions | Many visitor questions are about robot *fragility*. The robot is in fact remote-controlled, which can mislead if not stated | Fence + replica pattern. "Try to trick the model" is a strong hook. **State plainly what is autonomous and what is scripted.** |
| **Deutsches Museum Bonn – *Mission KI*** [85] | 6 zones: train simple neural nets, deepfakes, RoboMob (AMECA, historical RHINO), creative AI, and a "KI-Wahlkabine" where people **vote via face recognition** | Hands-on stations instead of text; programmes for children, families and schools (workshops from upper secondary) | No privacy statement on the exhibition page about cameras or face data | [corrected by verifier: the booth is the artwork *Smile to Vote* (Alexander Peterhaensel), a deliberate critique of face-based political profiling, not casual use.] Even critical face-recognition exhibits rarely explain data handling at the point of use. Our explicit "camera off / forget" design is a differentiator; say so in the application. |
| **Technopolis Mechelen – *AI!* expo** (3 Dec 2024–31 Dec 2025) [86] | Temporary AI zone for **ages 12+**: interactive installations on simplified AI principles, benefits and dangers; a history-of-AI game | – | – | Many Flemish secondary pupils at SiW may have seen AI exhibits. Under-12s probably have not, so pitch the core loop at 8–12. |
| **Science Gallery London – *AI: Who's Looking After Me?*** (21 Jun 2023–20 Jan 2024) [87] | 13-part art/science show on AI and care; interactives such as a survey on AI doctors and "Heartificial Intelligence" (visitors' heartbeats) | Participatory, values-focused | – | Asking visitors' opinions ("would you let the robot…?") works as a low-tech audience activity. |
| **Exploratorium – *Adventures in AI*** (12 Jun–14 Sep 2025) [88] | 20 new exhibits: "Guess the Animal", a 9-ft robot hand that learns to be "lovable", generative tools. Per search-result summaries (not fetched), also an AI that identifies visitors' **shadow puppets** | Playful, game framing | – | Shadow puppets and hand gestures show computer vision **without faces**: a privacy-friendly perception task for our camera chapter. |
| **The Tech Interactive – *Dream Garden*** (Mar 2025) [89] | Immersive room reacting to movement; Google **MediaPipe** + Phi-3.5 SLMs; real-time displays explaining the algorithms | AI literacy through movement | Press release gives no privacy statement | MediaPipe pose is museum-proven; "show the algorithm live" matches our XAI aim. |
| **Five software exhibits for children** (Vahedian Movahed et al., CHI EA 2024) [90] | 5 AI/ML demos tested with **125 students aged 7–14** | Students understood that "AI and ML systems can process data from cameras (perception)" and that systems respond to their training input | – | Direct evidence that 7–14-year-olds grasp camera-based perception from short demos. |
| **Machine Gaze** (Ray LC et al., *Front. Robot. AI* 2020) and Science Gallery Dublin *Seeing* (2017) [96] | Machine Gaze: a salvaged 1980s security camera on a 3-DoF motorised base tracks faces and projects them onto a large 3D foam face. A feedback screen shows "what the camera sees". Workshops had children and adults train face detection, then **disguise themselves to "escape" detection**. *Seeing*: eye tracking, CV and drawing robots | Closest precedent to "how a machine sees you". Helped children see the machine as a separate interpreter with its own "agency", not a mirror | It projects faces publicly | Copy the **"trick the robot"** moment (hat, hand over face, turn away → watch the confidence drop). Do **not** project faces. |

**Existing "How does a robot see you?" installations.** Searches on 2026-10-02 (museum, robot-dog and AI-perception queries; EN/NL/DE/PL) found close relatives:
- Machine Gaze: camera-as-eye, face tracking, feedback screen;
- Mimus: legible attention model;
- MoS Boston *Exploring AI*: robot dog plus a "trick the model" vision demo;
- Exploratorium 2025: shadow-puppet recognition;
- Biometric Mirror / How Normal Am I?: profile built from your face, with critique.

I found **no installation combining all of**:
- a robot pet as the embodiment;
- **visitor-controlled sensor toggles**;
- an incrementally built, **non-sensitive** visitor model with per-inference evidence and confidence;
- a visible "forget" step.

The novelty claim is therefore *plausible* but still **UNVERIFIED** (absence of evidence). Frame it as "a new combination of known patterns" in the application, not "first ever".

---

## 7. Keepsakes (g)

| Option | Speed / cost | Privacy | Practicality | Verdict |
|---|---|---|---|---|
| None (on-screen only) | 0 | Best | Simple | Acceptable baseline |
| **Dye-sub photo card: Canon SELPHY CP1500** | **41 s per glossy postcard, 56 s semi-gloss** (Canon manual) [76]. Price: MSRP USD 179.99; Amazon USD 151.99 on 22 Sep 2026 [77]. KP-108IN set (108 prints) USD 34.99–47.99 → **about USD 0.32–0.44 per print** [77]. USB-C, 2.4 GHz Wi-Fi; operates 5–40 °C [76]. | Good if the card has **no photo or face** | Up to about 85 prints/h, i.e. about 20 per 15-min group slot. Carry 2 printers and 3+ KP-108IN packs per day. | **Recommended** for family/small-group sessions, or one card per *team* |
| **Label/sticker printer: Brother QL-800** | Up to **93 labels/min**; USD 124.99 on Brother USA (accessed 2026-10) [78] [verifier: 93/min is Brother's figure for *standard address labels with black text*. A graphic badge on a longer label in black/red (DK-2251) will print noticeably slower; benchmark it. Price USD 124.99 confirmed via Brother USA/Staples listings (search, 2026-10).] | Good | Monochrome (black/red). Fast enough to give *every* child in a class a sticker. Direct-thermal labels fade over years | **Recommended for school groups** ("My robot's-eye badge" sticker) |
| ESC/POS receipt printer: Epson TM-T20III | Up to 250 mm/s; about USD 180–230 (retail, accessed 2026-10) [79] | Good | Receipt-style "robot report" strip. Thermal paper in the EU must contain <0.02 % BPA by weight since 2 Jan 2020 (REACH Annex XVII, Reg. (EU) 2016/2235) [82]; buy phenol-free paper to be safe | Alternative |
| Per-visitor QR / download link / e-mail | – | **Data leaves the stand.** We become a controller for hosted personal data (retention, deletion, children's consent). Needs reliable internet. In Flanders 59 % of primary-school children have no smartphone [80]. | Adds failure modes | **Do not use** |
| Per-creation code *without* personal data (Galaxy Makers pattern) | – | Acceptable only if the linked content contains **nothing derived from the child's sensor data** | Galaxy Makers: 40 % of keepsake holders visited the website later [65] | Only for a *generic* artefact (e.g., "the robot dog's own sensor diary"), never for "how the robot saw you" |
| QR to a **static, generic** "How robots see" page (same for everyone) | Free | No personal data | Works offline at the stand. The page is hosted on TUAI's site. | **Use** on the printed card and the grown-ups card |

**Card content (non-personal):**
- which sensors the child allowed (icons);
- 3–4 robot guesses with confidence bars, and whether the child confirmed or corrected them;
- "Things I can NOT know about you" (feelings, who you are, what you think);
- a short take-away;
- TUAI/MSCA logos and a generic QR code.

No image, face crop, name or timestamp-ID.

---

## 8. Synthesis: recommended interaction flow

### 8.0 SiW group slot (default at Science is Wonderful!; target 15:00 + 1:00 changeover)

Based on the SiW 2027 rules: 15 min per group on average, groups up to a whole class aged 7–18, FR/NL language assistants, and modular activities [62].

| t (mm:ss) | Module | What happens | Audience task (everyone not at the controls) |
|---|---|---|---|
| 0:00–1:30 | Welcome + honesty | The researcher or language assistant gives the honesty script to the whole group: "This dog is a machine. Its eyes are *this* camera, its ears are *this* bone. It only guesses. It forgets everything." Show the sensor switches. | Hand out "Prediction cards" (✓/✗ and 😐/🙂 "sure / not sure") |
| 1:30–5:00 | Round 1: "What can my camera tell?" | Team A (3 volunteers) does the camera chapter: wave, raise a hand, hold a coloured card. Then **"trick the robot"**: hat on, hand over face, turn sideways, and the confidence bars drop [96]. Then camera OFF, and the robot's picture greys out. | Before each reveal, the audience predicts with cards: "Will the robot be sure?" |
| 5:00–8:30 | Round 2: "What can my ears tell?" | Team B: camera OFF, microphone ON. Closed question via the bone ("cat, dog or dinosaur?"); the robot shows "I heard… (pretty sure)". Noise-maker moment: the class claps and talks while the child answers once into the bone and once from 1 m away. The screen shows the speech-to-noise meter and the confidence. Close works; far fails. | The audience is the "noise". Afterwards they vote: "Why did the robot get confused when you were far away?" |
| 8:30–11:30 | Round 3 (if the group is ≤15) **or** "Be the robot" | Team C picks *any* sensor combination and the audience predicts the result. For large groups, run "Be the robot" instead: half the class gets blindfold or earplug cards and must guess about a classmate from one "sensor", which is the human analogue of sensor toggles. | Everyone |
| 11:30–13:30 | Reveal + "Things I can NOT know" | Group summary board (no faces): what each sensor contributed, where the robot was wrong, what it never guesses (feelings, who you are, age, etc.). | Final show of hands: "Should robots be allowed to use cameras in schools?" (opinion, not data) |
| 13:30–15:00 | Forget + keepsake | The group presses FORGET together (big button) and watches the shredder animation. One sticker per child (QL-800) or one card per team (SELPHY). | – |
| 15:00–16:00 | Changeover | Robot lies down (servo rest), bone wiped, battery check every 2–3 slots | – |

Variants:
- **Small group (2–6):** run Standard (§8.1) for each team member in turn.
- **Group of 25+ arriving while another is in progress:** start the next group on the "Be the robot" card game with the second researcher while the robot finishes. This is why the team should bring **3 people**, the maximum funded [62].

### 8.1 Standard session for families / small groups (target 4:00, plus about 0:45 changeover)

| t (mm:ss) | Chapter | Robot / screen | Visitor action | XAI / privacy element |
|---|---|---|---|---|
| idle | Attract | Robot "dozes"; head turns to motion; aisle screen loops abstract skeletons and boxes; no speech | – | Spectators see *abstract* perception only |
| 0:00–0:20 | Start + honesty | Paw press → wake animation; language flags; "I'm a robot – a machine shaped like a dog… you choose my senses… I forget everything at the end." | Press paw, choose language, step on paw marks | AI disclosure (Art. 50(1), UNICEF R5) |
| 0:20–0:40 | Sensor menu | Big physical toggle switches or on-screen toggles: 👁 camera, 👂 microphone (others off by default) | Child sets toggles (team: a "sensor operator") | Consent by design; the default is minimal |
| 0:40–1:40 | Chapter 1: What my camera sees | Live skeleton/keypoints + "person detected, about 0.8 m away (sure)", "hand raised? (sure)", "T-shirt mostly blue (not sure)"; robot head-tilt explained ("I tilt when I find a face") | Wave, raise hand, hold up a coloured card; then "trick me" (hat or hand over face) | Evidence line + confidence for every guess; ✓/✗ correction; confidence drops visibly when tricked |
| 1:40–2:40 | Chapter 2: What my ears hear | Bone glows → "Hold my bone and tell me: cat, dog or dinosaur?" (icons shown); "I heard 'dog' (pretty sure)"; second try or touch fallback | Push-to-talk answer or tap | Shows the microphone is only on while the button is pressed; shows the transcript and confidence |
| 2:40–3:20 | Chapter 3: Take a sense away | "Switch my camera OFF." Robot's picture of the child greys out and confidence bars widen: "Now I can only guess." | Flip the toggle | Core XAI: evidence → inference → uncertainty, made visible |
| 3:20–3:50 | Reveal: "How I see you" | Summary board: guesses, evidence icons, confidence, child's corrections. Panel "Things I can NOT know about you". | Confirm or correct | Limits of the AI; no sensitive inferences |
| 3:50–4:00 | Forget + card | "Press FORGET": shredder animation, all session data cleared; optional card prints | Press forget; take card | Visible deletion |
| 4:00–4:45 | Changeover | Robot lies down (servo rest); host briefs the next team | – | – |

**Express (1:30):** honesty (0:15) → camera chapter (0:35) → camera-off chapter (0:25) → forget (0:15).
**Class show (about 6 min, or extended to SiW's 30-min stage-show format):** same chapters. Three volunteer drivers (sensor operator, bone holder, judge who presses ✓/✗). The class votes "Was the robot right?" by raising hands. That vote doubles as a live demonstration of camera-based hand-raise counting, with confidence shown.

### 8.2 Session state machine (minimum)

`IDLE → (paw press ∧ qualifying face) → INTRO → SENSOR_MENU → CH1_CAMERA → CH2_MIC → CH3_REMOVE → REVEAL → FORGET → REST → IDLE`

Global transitions:
- no qualifying face 8–10 s → `PROMPT_RETURN`
- 25–30 s → `FORGET` (auto-wipe)
- staff key → `SKIP_CHAPTER` / `ABORT_AND_FORGET`
- e-stop → `ROBOT_REST` + UI freeze

Group-slot mode (§8.0) is started by a staff key, not the paw:

`GROUP_INTRO → [ROUND(team k, sensor preset k) → TEAM_HANDOVER]×2–3 → GROUP_REVEAL → GROUP_FORGET → REST`

- Each `ROUND` reuses the CH1/CH2/CH3 states with a preset sensor configuration.
- `TEAM_HANDOVER` wipes the previous team's data *before* the next team starts, so per-person data never accumulates across children.
- `GROUP_REVEAL` shows only aggregate, non-identifying results ("the robot was right 5 of 8 times; most errors happened with the camera off").

### 8.3 Design patterns (summary)

1. Explicit start, implicit attract.
2. One participant analysed, everyone else masked.
3. Speech as a bonus, touch as a guarantee.
4. Every inference has evidence, confidence and correction.
5. Remove a sensor to show its role. This counterfactual is the strongest XAI moment.
6. The robot's own behaviour is explained as sensor-triggered signals.
7. Visible forgetting.
8. Modules for each crowd state: group slot, standard, express, show.
9. Spectator screen shows abstractions only.
10. Staff host plus robot operator; robot in a pen; e-stop on the staff side; touchable replica outside the pen.
11. "Trick the robot": deliberately make perception fail (hat, hand, distance, noise) and watch the confidence drop.
12. The audience predicts before every reveal, so 20 children are active while 3 operate.

---

## 9. Recommendations for our demonstrator

0. **Apply now.** The SiW 2027 deadline is **6 Oct 2026, 12:00 CEST** [62] (form: https://ec.europa.eu/eusurvey/runner/Call_SiW2027; the call is for "MSCA fellows and alumni", so state the TUAI MSCA-DN grant and the DC positions explicitly). In the application:
   - stress that the demo is *interactive* and *modular* (both are selection-relevant [62]);
   - stress that it works in FR/NL with the provided assistants;
   - describe the privacy-by-design features (local processing, no faces shown, visible forgetting). Comparable museum exhibits do not offer these (§6).

   Plan a 3-person team, the maximum funded [62]: host/explainer, robot operator, and "audience" facilitator.
1. **Interaction model:** the **15-min group slot** (§8.0) is the default at SiW. Also provide:
   - 4-min Standard and 1.5-min Express for families and individuals;
   - an optional 6–30-min Class show for the stage.

   Staff switch modules with one keypress. Plan for about 6–9 hands-on children per group slot and about 16–22 slots per day (100–140 hands-on and 250–450 reached per day). Opening hours are **UNVERIFIED**.
2. **Start:** physical paw button + floor paw marks at 0.6–1.0 m. Camera confirms one frontal (±30° yaw), near (≤1.2 m), stable (≥1 s) face. Robot never speaks to passers-by.
3. **Perception content:** only observable, non-sensitive, checkable inferences:
   - presence and distance;
   - pose and gestures (hand raised, wave);
   - dominant clothing colour or object held up;
   - spoken answer to a closed question;
   - loudness or "talking now".

   **Exclude** age, gender, ethnicity, emotion, attractiveness, identity and personality, consistent with AI Act Art. 5(1)(f)/(g) [33] and the project brief. [verifier note on scope: Art. 5(1)(f) prohibits emotion inference only "in the areas of workplace and education institutions". Art. 5(1)(g) prohibits biometric categorisation that deduces race, political opinions, trade-union membership, religious or philosophical beliefs, sex life or sexual orientation. Age and gender inference are *not* prohibited by Art. 5. However, biometric categorisation by sensitive or protected attributes is high-risk under Annex III(1)(b), and emotion recognition is high-risk under Annex III(1)(c) and needs disclosure under Art. 50(3). So the exclusion is a sound design choice; it is not something Art. 5 alone requires. Art. 5(1)(b), which prohibits exploiting age-related vulnerabilities, also applies to a child audience.]
4. **Audio:**
   - Tethered handheld "bone" (dynamic/close-talk capsule, push-to-talk via a USB HID button, wipeable).
   - Constrained answers (2–4 options).
   - Silero VAD gate.
   - **No denoiser in front of the recogniser by default** [70].
   - A/B test Vosk grammar mode (Apache-2.0) [72] against Whisper + option matching.
   - Touch fallback after 2 failures.
   - A ReSpeaker XVF3800 (USD 54.90) only if we want DoA head-turn effects.
5. **Voice:** expressive, pre-rendered prompts in **FR/NL/EN** (plus PL for home events). No free-form LLM output to children. Give the SiW language assistant a printed script.
6. **Honesty script and "Was I right?"** after each chapter. Robot apologises briefly when wrong. No feelings claims.
7. **Displays:** participant screen shows full detail of *their* abstracted data. The aisle/audience screen shows skeletons and boxes only. **No raw video** on public screens.
8. **Data:** everything processed in RAM on the local mini-PC, no network needed. Visible "forget" step. Optionally log anonymous counters only (session count, mode, which toggles were used, ✓/✗ rates), with the organiser's agreement. Any research logging follows a LivingLAB-style guardian-consent process [11].
9. **Safety:**
   - acrylic pen on the table; no walking during sessions;
   - **staff-side** e-stop;
   - a touchable unpowered replica outside the pen [75];
   - servo rest between sessions;
   - ≥3 battery packs in rotation (Bittle-class has no pass-through charging [74]), swapped every 40–45 min;
   - attended charging in a LiPo bag;
   - 2 staff always present.
10. **Keepsake:**
    - School groups: one sticker per child from a Brother QL-800 (93 labels/min, USD 124.99) [78].
    - Families: a SELPHY CP1500 card (41 s, about USD 0.32–0.44 per print) [76][77].
    - Both carry a generic QR to a static TUAI page. No per-visitor digital delivery.
11. **Grown-ups card:** what is sensed, inferred and not inferred, and storage = none, in 4 languages.
12. **Test protocol before the event:**
    - play back 80 dB babble and measure recognition accuracy per age group with the bone at 5 cm and at 15 cm;
    - false-start rate with 10 passers-by;
    - run a mock school class of 20–25 children through the **15-min group slot**, timing each module;
    - a 6-h endurance run (battery swaps, servo temperature);
    - ask organisers (after selection, 28 Oct 2026) for opening hours, groups per booth per day, stand size, power, amplification/noise rules, Li-ion battery rules and whether the language assistant is shared between booths.

---

## 10. Pitfalls / what not to do

- **Do not auto-start or greet by voice from face or proximity detection.** It misfires on passers-by and spectators, often seconds late, and greeting people who did not intend to interact annoys them [2][3].
- **Do not run a solo-only 4–5-min experience at a school-group event.** SiW groups stay about 15 min and can be a whole class [62]; queues will collapse. Do not make a linear 4-min sequence the only path either: FROG lost about ⅓ of visitors over a 3-min tour [63].
- **Do not put the e-stop (or any "magic" button) where visitors can reach it** [63]. Debounce and ignore the start button during a session.
- **Do not put a denoiser in front of Whisper by default, and do not send silent clips to Whisper**: denoising degraded modern ASR in all 40 configurations tested [70], and Whisper hallucinates on non-speech [71].
- **Do not claim autonomy you do not have.** If any part is scripted or staff-triggered, say so. At MoS Boston, Spot "appears to be operating alone" but is staff-driven or pre-programmed [75]. In an *AI-literacy* exhibit that gap undermines the message.
- **Do not rely on the robot's on-board mic, a far-field array or a shotgun mic for speech recognition** [21]. Do not run open-vocabulary speech recognition on children's free speech, and do not show unconfirmed transcripts as fact. Whisper hallucinates in babble [22].
- **Do not ask open personal questions** (name, age, school, feelings). Do not comment on appearance or on silence.
- **Do not show raw people-labels or confidence scores from generic classifiers** (ImageNet Roulette) [35][36]. Do not infer gender, age, ethnicity, emotion, attractiveness or personality (Gender Shades disparities [39]; AI Act Art. 5 [33]; Biometric Mirror and How Normal Am I? are critiques, not templates [37][38]).
- **Do not let the robot claim feelings or friendship, or pressure children.** Children conform to robots [27], so the robot must not act as an authority.
- **Do not use free-form LLM dialogue** with children at the stand: unpredictable content, latency and network dependence.
- **Do not put live camera video of children on the aisle-facing screen.** It shows bystanders' faces and invites photography of other people's children.
- **Do not let visitors touch or lift the powered robot.** Do not let it walk near table edges. Never leave it powered and unattended [26][45]. Do not charge Li-ion packs unattended or near the public [49].
- **Do not collect e-mails or deliver per-visitor results by QR or cloud.** It needs internet and creates controller duties for children's data.
- **Do not assume the robot works for 6 h on one battery or without servo rest** [42][43].
- **Do not claim "first ever".** Claim "a new combination of known patterns" (see §6).
- **Do not miss the SiW deadline** (6 Oct 2026, 12:00 CEST) or the mandatory online communication workshop (4 Nov 2026) [62].

---

## 11. Open items / UNVERIFIED

**Resolved on 2026-10-02:**
- SiW 2027 dates, venue, deadline, group dwell, ages, languages and team size [62];
- SELPHY and KP-108IN prices (US retail) [77];
- label/receipt printer options [78][79];
- BPA rule [82];
- Bittle X pass-through (none) [74];
- Biometric Mirror specifics [84];
- ImageNet Roulette offline date [83];
- Deutsches Museum (Bonn *Mission KI*) [85];
- smartphone ownership in Flanders [80];
- the enhancement-vs-ASR question, at least for adult/medical speech [70].

**Still open:**
- SiW 2027 stand size, opening hours, groups per booth per day, power, amplification/noise rules, Li-ion battery rules, and whether a language assistant is dedicated to a booth or shared. Ask after selection.
- Actual sound level in the SiW hall (assumed 70–85 dB(A); museums with visitors measure 61–66 dB(A) [69]). Measure it.
- **EU** (EUR) prices for SELPHY/KP-108IN/QL-800; the figures above are US retail.
- Whether denoising helps or hurts **child** speech in babble with our recogniser. Needs our own A/B test; the evidence [70] is for medical adult speech.
- Whether the chosen robot can run from an external DC supply (Bittle X: not with the stock pack).
- Science Museum London AI exhibits: no current permanent AI-perception exhibit found. *AI: Who's Looking After Me?* was at **Science Gallery London** (King's College), not the Science Museum [87].
- Exploratorium shadow-puppet exhibit details (seen only in search summaries; the press release returned 403).
- The Vollmer et al. 2018 child sample size was not re-checked (science.org not fetched).
- Novelty of the full combination (§6): absence of evidence only.

---

## Sources

[1] Hall, E.T. (1966) *The Hidden Dimension*; zone values as summarised in [2] and [5].
[2] Michalowski, Šabanović, Simmons (2006) "A Spatial Model of Engagement for a Social Robot", IEEE AMC. https://publications.ri.cmu.edu/storage/publications/pub_files/pub4/michalowski_marek_piotr_2006_3/michalowski_marek_piotr_2006_3.pdf
[3] Bohus & Horvitz (2009) "Learning to Predict Engagement with a Spoken Dialog System in Open-World Settings", SIGDIAL. http://erichorvitz.com/Bohus_Horvitz_Predict_Engagement.pdf
[4] Bohus & Horvitz (2009) "Models for Multiparty Engagement in Open-World Dialog", SIGDIAL pp. 225–234. https://aclanthology.org/W09-3933/
[5] Walters et al. (2006) "Exploratory studies on social spaces between humans and a mechanical-looking robot", *Connection Science* 18(4). https://projects.laas.fr/COGNIRON/review3-open/files/RA3-Appendices/UH-2.pdf
[6] "A proxemics game between festival visitors and an industrial robot" (Ars Electronica 2020), arXiv:2105.13812. https://arxiv.org/abs/2105.13812
[7] Thrun et al. (2000) "Probabilistic Algorithms and the Interactive Museum Tour-Guide Robot Minerva", IJRR. http://robots.stanford.edu/papers/thrun.ijrr-minerva.pdf
[8] Shiomi, Kanda, Ishiguro, Hagita (2006) "Interactive Humanoid Robots for a Science Museum" (figures via listing). https://www.researchgate.net/publication/3454456_Interactive_Humanoid_Robots_for_a_Science_Museum
[9] Gannon, M. *Mimus*. https://atonaton.com/mimus
[10] Copernicus Science Centre – Robots. https://www.kopernik.org.pl/en/exhibitions/robots-exhibitions ; exhibitions index https://www.kopernik.org.pl/en/exhibitions
[11] Copernicus Science Centre – LivingLAB. https://www.kopernik.org.pl/en/exhibitions/livinglab
[12] Sandifer, C. (2003) "Technological Novelty and Open-Endedness…", *J. Res. Sci. Teaching* 40(2):121–137 (includes Serrell 1998 and Diamond 1986 summaries). https://tigerweb.towson.edu/csandife/jrst2003.pdf
[13] Exploratorium, *Going APE! Phase 2 Summative Evaluation* (132.3 s vs 51.1 s; PDF 403, figures via indexed text). https://www.exploratorium.edu/sites/default/files/pdfs/APE_Summative_Phase_2.pdf ; record: https://informalscience.org/evaluation/going-ape-active-prolonged-engagement-exploratorium-phase-2-summative-evaluation/
[14] Bitgood, S. "Exhibition Design that Provides High Value and Engages Visitor Attention" / attention–value model. https://www.aam-us.org/wp-content/uploads/2024/04/4EXHSP14Bitgood_ExhibitionDesignthatprovidesHighValues.pdf
[15] Serrell, B. "Paying More Attention to Paying Attention". https://informalscience.org/paying-more-attention-paying-attention/
[16] European Commission – Science is Wonderful! https://marie-sklodowska-curie-actions.ec.europa.eu/science-is-wonderful
[17] RNNoise releases (v0.2). https://github.com/xiph/rnnoise/releases
[18] Phoronix, "RNNoise 0.2 Released…" (BSD-3, AVX2). https://www.phoronix.com/news/RNNoise-0.2-Released
[19] DeepFilterNet (MIT/Apache-2.0, LADSPA). https://github.com/Rikorose/DeepFilterNet ; paper (RTF 0.19 on i5-8250U): https://arxiv.org/pdf/2305.08227
[19b] Intel DeepFilterNet OpenVINO port (listing only). https://huggingface.co/Intel/deepfilternet-openvino
[20] Silero VAD (MIT). https://github.com/snakers4/silero-vad
[21] Kennedy et al. (2017) "Child Speech Recognition in Human-Robot Interaction: Evaluations and Recommendations", HRI. https://academia.skadge.org/publis/kennedy2017child.pdf (DOI 10.1145/2909824.3020229)
[22] "CPT-Boosted Wav2vec2.0: Towards Noise Robust Speech Recognition for Classroom Environments", arXiv:2409.14494. https://arxiv.org/html/2409.14494v4
[22b] Kid-Whisper (AAAI/ACM AIES). https://ojs.aaai.org/index.php/AIES/article/view/31618
[23] Parreira, Neto, Rocha, Ju (2026) "Calling for Backup: How Children Navigate Successive Robot Communication Failures", arXiv:2601.00754. https://arxiv.org/abs/2601.00754
[24] Kory Westlund et al. (2017) "Flat vs. Expressive Storytelling…", *Front. Hum. Neurosci.* https://www.frontiersin.org/articles/10.3389/fnhum.2017.00295/full
[25] Cheng et al. (2018) "Why doesn't it work? Voice-driven interfaces and young children's communication repair strategies", IDC. https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3202185.3202749 (DOI 10.1145/3202185.3202749)
[26] Brščić, Kidokoro, Suehiro, Kanda (2015) "Escaping from Children's Abuse of Social Robots", HRI. https://www.irc.atr.jp/~drazen/pdf/HRI2015_Brscic.pdf
[27] Vollmer, Read, Trippas, Belpaeme (2018) "Children conform, adults resist…", *Science Robotics* 3(21). https://www.science.org/doi/10.1126/scirobotics.aat7111
[28] Technology Networks summary of [27] (87 %/75 %/74 %). https://www.technologynetworks.com/informatics/news/robots-can-influence-kids-opinions-307697
[29] Flanagan, Georgiou, Scassellati, Kushnir (2024) "School-age children are more skeptical of inaccurate robots than adults", *Cognition* 249:105814. https://pubmed.ncbi.nlm.nih.gov/38763071/
[30] van Straten et al. – transparency about the robot's lack of psychological capacities (THRI 2020; follow-up IJHCS 2023). https://www.sciencedirect.com/science/article/pii/S1071581923000721
[30b] van Straten et al. "On sharing and caring…" *Computers in Human Behavior*. https://www.sciencedirect.com/science/article/pii/S0747563221004581
[31] UNICEF Innocenti, *Guidance on AI and Children* v3 Checklist (2025). https://www.unicef.org/innocenti/media/11996/file/UNICEF-Innocenti-Guidance-on-AI-and-Children-3-Checklist-2025.pdf ; project page https://www.unicef.org/innocenti/projects/ai-for-children
[32] EU AI Act, Article 50 (applies 2 Aug 2026). https://artificialintelligenceact.eu/article/50/
[33] EU AI Act, Article 5 (applies 2 Feb 2025). https://artificialintelligenceact.eu/article/5/
[34] ImageNet Roulette (project URL; unreachable 2026-10). https://imagenet-roulette.paglen.com/
[35] Crawford & Paglen, "Excavating AI". https://excavating.ai/
[36] Wikipedia, "ImageNet" (bias, person-category removals; cites the *Guardian*, Sep 2019). https://en.wikipedia.org/wiki/ImageNet
[37] Wouters et al. (2019) "Biometric Mirror: Exploring Ethical Opinions towards Facial Analysis and Automated Decision-Making", DIS. https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3322276.3322304 (DOI 10.1145/3322276.3322304)
[38] Schep, T. *How Normal Am I?* (EU H2020 SHERPA). https://www.hownormalami.eu/
[39] Buolamwini & Gebru (2018) "Gender Shades", PMLR 81. https://proceedings.mlr.press/v81/buolamwini18a.html
[40] Teachable Machine community repo (Apache-2.0). https://github.com/googlecreativelab/teachablemachine-community
[41] Ars Electronica Center – *Understanding AI*. https://ars.electronica.art/center/en/exhibitions/understanding-ai/
[42] Petoi docs (overheating, pinch, joints). https://docs.petoi.com/getting-started-guide ; https://docs.petoi.com/extensible-modules/robot-arm
[43] Petoi Bittle X technical specifications. https://www.petoi.com/pages/bittle-x-robot-dog-with-arm-specifications
[44] Petoi Bittle X user manual – Open the box. https://bittle-x.petoi.com/2-open-the-box
[45] Unitree Go2 User Manual V1.0. https://static.generation-robots.com/media/Go2-User-Manual.pdf
[46] Seeed reSpeaker XVF3800 USB 4-Mic Array (USD 54.90). https://www.seeedstudio.com/ReSpeaker-XVF3800-USB-Mic-Array-p-6488.html
[47] Samson Q2U listings, e.g. Best Buy. https://www.bestbuy.com/site/samson-q2u-dynamic-usb-microphone/6361715.p?skuId=6361715
[48] Hiwonder MechDog / PuppyPi listings. https://www.hiwonder.com/products/mechdog ; https://www.robotshop.com/products/hiwonder-hiwonder-puppypi-quadruped-robot-with-ai-vision-powered-by-rpi-ros-open-source-robot-dog-standard-kit-with-rpi-4b-4gb
[49] University lithium-battery safety guidance, e.g. https://ehs.umich.edu/wp-content/uploads/2025/02/Lithium-Battery-Guidance.pdf ; https://www.uidaho.edu/dfa/division-operations/ehs/programs/hazmat/lithium-based-battery-safety ; https://www.cmu.edu/ehs/Laboratory-Safety/chemical-safety/documents/ehs-guideline---lithium-ion-battery-safety.pdf
[50] Interesting Engineering (5 Jun 2026) "Humanoid robot kicks child during public demo". https://interestingengineering.com/ai-robotics/viral-humanoid-robot-kicks-child-in-stomach
[51] Toy Safety Regulation (EU) 2025/2509. https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A32025R2509 ; overview https://www.eurofins.com/toys-hardlines/resources/articles/a-quick-overview-of-the-new-eu-toy-safety-regulation-eu-20252509/
[52] Digital Camera World, Canon SELPHY CP1500 review (19 Oct 2022). https://www.digitalcameraworld.com/reviews/canon-selphy-cp1500-review
[53] Sweetwater InSync, "Inverse Square Law". https://www.sweetwater.com/insync/inverse-square-law/
[54] "The impact of the Lombard effect on audio and visual speech recognition systems", *Speech Communication*. https://www.sciencedirect.com/science/article/pii/S0167639317302674
[55] Quick, Draw! dataset. https://github.com/googlecreativelab/quickdraw-dataset
[56] Experience AI. https://experience-ai.org/en/
[57] Day of AI. https://dayofai.org/
[58] MIT RAISE. https://raise.mit.edu/
[59] Barbican, *AI: More than Human*. https://www.barbican.org.uk/whats-on/2019/event/ai-more-than-human
[60] Tactical Tech, *The Glass Room*. https://theglassroom.org/
[61] KTH TMH, "The social robot Furhat at Tekniska Museet Nov. 15–23". https://www.kth.se/tmh/about-tmh/news/the-social-robot-furhat-at-tekniska-museet-nov-15-23-1.512247

*Added in the 2026-10-02 gap-fill pass:*

[62] European Commission (MSCA), "Showcase your research at Science is Wonderful! 2027" (call: 17–19 Mar 2027, Brussels; deadline 6 Oct 2026 12:00 CEST; 15 min per group; ages 7–18; FR/NL assistants; up to 3 people funded; modular activities; 30-min shows for about 60 people, 15 shows). https://marie-sklodowska-curie-actions.ec.europa.eu/node/1621 ; secondary: UKRO https://www.ukro.ac.uk/news/msca-science-is-wonderful-2027-call-for-applications/
[63] Karreman, Ludden, van Dijk, Evers (2015) "How can a tour guide robot's orientation influence visitors' orientation and formations?", AISB 2015, 4th Int. Symp. New Frontiers in HRI (FROG, EU FP7 grant 288235). https://www.cs.kent.ac.uk/events/2015/AISB2015/proceedings/hri/7-Karreman-howcana.pdf
[64] Karreman, Ludden, Evers (2015) "Visiting Cultural Heritage with a Tour Guide Robot: A User Evaluation Study in-the-Wild", ICSR 2015. https://link.springer.com/chapter/10.1007/978-3-319-25554-5_32 ; project https://www.frogrobot.eu/wordpress/category/tour-guides/
[65] Borrow & Harrison (2017) "Galaxy Makers: creating an online component to a science exhibition for re-engagement, evaluation and content legacy", arXiv:1705.04563 (Royal Society Summer Science Exhibition 2016). https://arxiv.org/abs/1705.04563
[66] "Interaction Density as a Behavioural Signature of Exhibit Type: A Minimal-Log Study from a Two-Venue Science Experience Centre", arXiv:2607.13724 (2026). https://arxiv.org/html/2607.13724
[67] (merged into [13]) Exploratorium APE Phase 1 interim summative report (2004). https://www.exploratorium.edu/sites/default/files/pdfs/APE_Summative_Phase_1.pdf (HTTP 403 to automated fetch)
[68] Serrell, "The 51% Solution Research Project" (InformalScience). https://www.informalscience.org/51-solution-research-project-meta-analysis-visitor-timeuse-museum-exhibitions
[69] Carvalho, Gonçalves & Garcia (2013) "Acoustics of Modern and Old Museums", Noise-Con 2013. https://commercial-acoustics.com/wp-content/uploads/2020/07/AcousticsofModernandOldMuseums.pdf
[70] Chondhekar et al. (2025) "When De-noising Hurts: A Systematic Study of Speech Enhancement Effects on Modern Medical ASR Systems", arXiv:2512.17562. https://arxiv.org/abs/2512.17562
[71] "Calm-Whisper: Reduce Whisper Hallucination On Non-Speech…", arXiv:2505.12969 (May 2025). https://arxiv.org/abs/2505.12969 ; openai/whisper discussion #1606 https://github.com/openai/whisper/discussions/1606
[72] Vosk API (Apache-2.0). https://github.com/alphacep/vosk-api ; https://alphacephei.com/vosk/
[73] LDI show exhibitor rules, "Noise and Sound Levels on the Expo Floor" (85 dBC LCeq 30 s). https://qtxasset.com/quartz/qcloud4/2025-08/Sound-Performaces%20(1).pdf
[74] Petoi docs – Battery (no power supplied while charging; 5 V/1 A charging). https://docs.petoi.com/technical-support/battery
[75] Museum of Science Boston – *Exploring AI: Making the Invisible Visible*. https://www.mos.org/visit/exhibits/exploring-ai-making-invisible-visible ; press release https://www.mos.org/press/press-releases/Exploring-AI-Making-the-Invisible-Visible-Exhibit-Announcement ; Boston.com (30 Sep 2025) https://www.boston.com/news/technology/2025/09/30/museum-of-science-lets-the-public-interact-with-robot-dogs-and-humanoid-robots/
[76] Canon SELPHY CP1500 user manual – Specifications. https://cam.start.canon/en/P001/manual/html/UG-07_Reference_0070.html
[77] SELPHY CP1500 price history (Amazon USD 151.99 on 22 Sep 2026; MSRP USD 179.99). https://pricehistory.app/p/canon-selphy-cp1500-wireless-compact-photo-printer-535rzy2h ; Staples USD 179.99 https://www.staples.com/canon-selphy-cp1500-wireless-color-inkjet-printer-black-5539c001/product_24545108 ; KP-108IN: Canon USA https://www.usa.canon.com/shop/p/kp-108in-color-ink-paper-set ; Best Buy https://www.bestbuy.com/product/canon-kp-108in-ink-cartridge-paper-multicolor/J7C86PFL3H
[78] Brother QL-800 (93 labels/min). https://www.brother-usa.com/p/thermal-printers-labelers/QL800
[79] Epson TM-T20III (250 mm/s). https://epson.com/For-Work/Printers/POS/TM-T20III-Thermal-Receipt-Printer/p/C31CH51A9972 ; Walmart listing https://www.walmart.com/ip/Epson-TM-T20III-Serial-USB-Pos-Receipt-Black-Printer-C31CH51001/894829131
[80] Apestaartjaren 2024 (Flanders, 5,482 pupils). Report https://assets.mediawijs.be/2024-05/apenstaartjarenrapport_2024_lr_1_3.pdf ; summaries https://www.ilikemedia.be/apenstaartjaren-2024/ and https://www.mediapuntvlaanderen.be/updates-analyse/smartphonebezit-bij-vlaamse-jongeren-11-jaar-als-kantelpunt
[81] (context only) Ofcom, *Children and Parents: Media Use and Attitudes* 2025 (UK). https://www.ofcom.org.uk/siteassets/resources/documents/research-and-data/media-literacy-research/children/childrens-media-use-and-attitudes-report-2025/childrens-media-literacy-report-2025.pdf
[82] Commission Regulation (EU) 2016/2235 (BPA ≥0.02 % w/w in thermal paper banned from 2 Jan 2020). https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A32016R2235 ; summary https://www.chemsafetypro.com/Topics/Restriction/Regulation_EU_2016_2235_Bisphenol_A_BPA_ban_thermal_paper_REACH_annex_xvii.html
[83] ImageNet Roulette offline 27 Sep 2019. Smithsonian https://www.smithsonianmag.com/smart-news/art-project-exposed-racial-biases-artificial-intelligence-system-180973207/ ; frieze https://www.frieze.com/article/how-ai-selfie-app-imagenet-roulette-took-internet-storm ; The Art Newspaper https://www.theartnewspaper.com/2019/09/23/leading-online-database-to-remove-600000-images-after-art-project-reveals-its-racist-bias
[84] Biometric Mirror: New Atlas https://newatlas.com/biometric-mirror-facial-recognition-human-bias/55711/ ; Univ. Melbourne CIS project page https://cis.unimelb.edu.au/research/hci/projects/biometric-mirror ; Science Gallery Melbourne blog (14 characteristics; now redirects) https://melbourne.sciencegallery.com/blog/this-biometric-mirror-measures-your-personality-traits-emotional-stability-and-beauty
[85] Deutsches Museum Bonn – *Mission KI*. https://www.deutsches-museum.de/bonn/ausstellung/mission-ki
[86] Technopolis Mechelen *AI!* expo (3 Dec 2024–31 Dec 2025, 12+). https://www.rtv.be/entertainment-en-ontspanning/technopolis-opent-themazone-rond-artificiele-intelligentie (403; via search summary) ; https://www.klasse.be/voordelen-aanbod/expo-ai-technopolis-mechelen-lerarenkaart/
[87] Science Gallery London, *AI: Who's Looking After Me?* (21 Jun 2023–20 Jan 2024). https://www.kcl.ac.uk/news/ai-whos-looking-after-me-science-gallery-london ; review https://www.kcl.ac.uk/news/student-review-ai-whos-looking-after-me
[88] Exploratorium *Adventures in AI* (12 Jun–14 Sep 2025). ABC7 https://abc7news.com/post/new-san-francisco-exploratorium-exhibit-adventures-ai-will-explore-world-artificial-intelligence-machine-learning/16714173/ ; press release (403) https://www.exploratorium.edu/press-office/press-releases/exploratorium-presents-adventures-ai-hands-summer-exhibition
[89] The Tech Interactive, *Dream Garden* (Mar 2025; MediaPipe + Phi-3.5). https://www.prnewswire.com/news-releases/the-tech-interactive-unveils-new-ai-powered-immersive-exhibit-302395230.html
[90] Vahedian Movahed et al. (2024) "Introducing Children to AI and ML with Five Software Exhibits", CHI EA '24 (125 students aged 7–14). https://dl.acm.org/doi/10.1145/3613905.3650991 (abstract via https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3613905.3650991)
[91] Raspberry Pi Foundation, "Experience AI expands to reach over 2 million students" (5 Sep 2024). https://www.raspberrypi.org/blog/experience-ai-expands-to-reach-over-2-million-students/
[92] Warsaw Now, Ameca at Copernicus "The Future is Today". https://en.warsawnow.pl/najbardziej-zaawansowany-robot-humanoidalny-do-zobaczenia-w-centrum-nauki-kopernik/
[93] Adafruit Massive Arcade Button with LED, 100 mm (#1185, USD 9.95). https://www.adafruit.com/product/1185
[94] Samson Q2U review/pricing 2026. https://www.thepodcasthost.com/equipment/samson-q2u-podcasting-review/ ; https://www.sweetwater.com/store/detail/Q2UPack--samson-q2u-recording-and-podcasting-pack-usb-xlr-dynamic-microphone-with-accessories
[95] Hiwonder PuppyPi (official store). https://www.hiwonder.com/products/puppypi
[96] Ray LC et al. (2020) "Machine Gaze: Self-Identification Through Play With a Computer Vision-Based Projection and Robotics System", *Front. Robot. AI*. https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2020.580835/full ; Science Gallery Dublin *Seeing* (Forbes, 30 Apr 2017) https://www.forbes.com/sites/jenniferhicks/2017/04/30/this-art-exhibit-shows-how-eyes-brains-and-robots-see-understand-and-perceive/

---

## Verification log

Independent re-check by a verifier on 2026-10-01, using fresh fetches of primary sources. Web search quota was exhausted, so claims were checked only by fetching known primary URLs or PDFs. **Verdicts:** confirmed / corrected / unverifiable.

| # | Claim in report | Verdict | Source (fetched 2026-10) / note |
|---|---|---|---|
| 1 | Science is Wonderful! 2026: Brussels, March 2026, 3 days, about 4,500 young visitors, 150+ researchers, 30+ countries | **Confirmed.** No 2027 dates, deadline or eligibility are published on the page, which only says "sign up to our newsletter". | https://marie-sklodowska-curie-actions.ec.europa.eu/science-is-wonderful |
| 2 | EU AI Act Art. 50(1) AI-interaction disclosure applies from 2 Aug 2026 | **Confirmed.** Art. 113 general date of 2 Aug 2026 is unchanged by the Digital Omnibus on AI. The Omnibus gives only a transition to 2 Dec 2026 for Art. 50(2) synthetic-content marking. | https://artificialintelligenceact.eu/article/50/ ; https://artificialintelligenceact.eu/article/113/ ; https://artificialintelligenceact.eu/ai-act-explorer/digital-omnibus/ (EUR-Lex not reachable, so this is a secondary consolidated text) |
| 3 | AI Act Art. 5(1)(f)/(g) prohibitions apply since 2 Feb 2025 | **Confirmed, scope clarified inline.** (f) is emotion inference in workplace/education institutions; (g) is biometric categorisation for race, political opinions, trade-union membership, religion/beliefs, sex life or orientation. Age and gender are not covered by Art. 5. | https://artificialintelligenceact.eu/article/5/ |
| 4 | Roboceptionist: 66 % of 816 turns at passers-by, 51 % ≥3 s late; 54 % of greetings unanswered; vision cut inappropriate greetings by 69 %; 46 % of interactions were groups; 26 %/10 % and 48 %/15 % | **Confirmed** (full text read) | Michalowski et al. 2006 PDF [2] |
| 5 | Bohus & Horvitz: 0.18 % false positives (6/3,274); about 4 % false positives (79) at 3 s early detection; no transfer between orientations | **Confirmed with nuance.** The 4 % is for the side orientation and drops to 2.9 % after manual review; the front orientation is 7.2 %. Corrected inline. | http://erichorvitz.com/Bohus_Horvitz_Predict_Engagement.pdf |
| 6 | Sandifer 2003: 61 exhibits, 47 visitors, mean holding 1.6 min (0.5–5.6), mean attracting power 0.38, user-centredness not significant | **Confirmed.** Note added: school groups were excluded from the sample. | https://tigerweb.towson.edu/csandife/jrst2003.pdf |
| 7 | Exploratorium APE 132.3 s vs 51.1 s | **Unverifiable.** The PDF returns 403 and the informalscience record has no figures; it confirms only the report (Selinda Research Associates, 2004). | informalscience.org record |
| 8 | Kennedy et al. 2017: 77→18 % with distance in noise; 0 % at 90°; studio 84 % vs NAO 61 %; spontaneous about 18 % | **Confirmed numerically, context corrected.** Participants were 11 children with mean age 4.9, using the NAO and 2016 engines; the 18 % is Google with relaxed scoring. | https://academia.skadge.org/publis/kennedy2017child.pdf |
| 9 | Whisper-small.en WER 24.5 % (NCTE) / 30.2 % (MPT); "the" ×206 hallucination | **Confirmed** (24.46 % / 30.15 %) | https://arxiv.org/html/2409.14494v4 |
| 10 | RNNoise 0.2 is the latest release; BSD-3; SSE4.1/AVX2 | **Confirmed.** 0.2 is still marked "Latest"; there has been no release in 2025–2026. | https://github.com/xiph/rnnoise/releases |
| 11 | DeepFilterNet MIT/Apache-2.0, LADSPA plugin, 4.8k stars | **Confirmed.** The RTF of 0.19 on an i5-8250U was not re-checked (paper not re-fetched). | https://github.com/Rikorose/DeepFilterNet |
| 12 | Silero VAD MIT, about 2 MB, <1 ms per 30 ms chunk, 8/16 kHz | **Confirmed** | https://github.com/snakers4/silero-vad |
| 13 | ReSpeaker XVF3800 USB 4-mic USD 54.90; AEC/AGC/DoA/VAD/beamforming; up to 5 m | **Confirmed.** In stock; USD 49.90 at 10+ units. | https://www.seeedstudio.com/ReSpeaker-XVF3800-USB-Mic-Array-p-6488.html |
| 14 | Vollmer et al. 2018: children 7–9, 87 % alone vs 75 % with robots, 74 % of errors matched robots | **Confirmed** (via Technology Networks summary; science.org not fetched) | https://www.technologynetworks.com/informatics/news/robots-can-influence-kids-opinions-307697 |
| 15 | Flanagan et al. 2024: 168 children aged 4–7 and 168 adults; apology helped older children keep trust in robots | **Confirmed.** Age caveat added inline. | Europe PMC abstract, PMID 38763071 |
| 16 | UNICEF Guidance on AI and Children v3, Requirement 5 (warn up front, prevent anthropomorphising, age-appropriate language) and Requirement 3 (privacy by design, data agency) | **Confirmed** verbatim; 10 requirements and 48 recommendations | UNICEF checklist PDF [31] |
| 17 | Brščić et al. 2015: 19 of 185 interactions abusive, always by children, more where fewer people were present | **Confirmed** | Paper PDF [26] (TLS certificate mismatch; downloaded and read) |
| 18 | Parreira et al. 2026, arXiv:2601.00754: 59 children aged 8–10; they seek adults; errors did not change their perception of the robot | **Confirmed** | https://arxiv.org/abs/2601.00754 |
| 19 | Unitree Go2 manual: not for under-14s, ≥2 m from crowds, pinching at the knee, 5–35 °C | **Confirmed** verbatim | Go2 User Manual V1.0 [45] |
| 20 | Bittle X: 269–353 g, 7.4 V 1,000 mAh (7.4 Wh), 1 h run, 1.5 h charge, battery does not supply power while charging | **Confirmed.** **Omission added:** no camera or microphone stream in the spec; offline voice-command module only; spare battery USD 51. | [43] [44]; https://www.petoi.com/collections/robots |
| 21 | Hiwonder MechDog Advanced USD 399.99 / Pro USD 599; PuppyPi USD 678.99 (over budget) | **Corrected.** Advanced is 369.99 and Pro Developer is 569.99. PuppyPi is from 589.99 (RPi 4B) or 599.99 (RPi 5 2 GB) at the official store, with camera and voice module. | https://www.hiwonder.com/products/mechdog.json ; https://www.hiwonder.com/products/puppypi.json |
| 22 | Canon SELPHY CP1500: 41 s per postcard, about USD 0.32 per print, USD 139.99–179 (Oct 2022 review) | **Confirmed** as a 2022 review figure; the current price is still unverified | https://www.digitalcameraworld.com/reviews/canon-selphy-cp1500-review |
| 23 | Toy Safety Regulation (EU) 2025/2509: published 12 Dec 2025, applies from 1 Aug 2030 | **Confirmed** (Eurofins summary; EUR-Lex not re-fetched) | Eurofins article [51] |
| 24 | ImageNet person subtree: 2,832 synsets → 158 remained; 2,702 removed in 2021 | **Confirmed** (1,593 flagged as offensive; 130 person synsets remain after 2021) | https://en.wikipedia.org/wiki/ImageNet |
| 25 | How Normal Am I?: local processing, "No personal data is sent to our server", H2020 grant 786641 | **Confirmed** | https://www.hownormalami.eu/ |
| 26 | Gender Shades: up to 34.7 % vs 0.8 % | **Confirmed** | https://proceedings.mlr.press/v81/buolamwini18a.html |
| 27 | Mimus permanent at Copernicus; 8 depth sensors; about 45 m²; "most interesting person"; "gets bored" | **Confirmed. Corrected:** the selection attributes include estimated age | https://atonaton.com/mimus |

## Omissions added by verifier

1. **Robot hardware vs concept (important for feasibility).** Petoi Bittle X has **no camera** and no raw-audio microphone path; its only listed sensor is an IMU, plus a closed, offline voice-command module. Petoi's camera module is discontinued. The "how does a robot see you" camera and microphone must therefore be **stand-mounted** (a USB webcam or depth camera plus the bone mic), with the dog as the expressive "body". That is actually good for privacy and robustness, but it should be stated honestly to visitors ("my eyes are this camera"). Two alternatives within the ~USD 600 budget do have on-board sensors:
   - **Hiwonder PuppyPi Standard** (USD 589.99 with RPi 4B, or 599.99 with RPi 5 2 GB; HD wide-angle camera plus AI voice module; ROS/ROS2);
   - **MechDog Pro Developer Kit** (USD 569.99; ESP32-S3 vision module plus WonderEcho voice module).

   Whether these expose raw camera frames or raw audio to the stand PC (versus on-board recognition only) is **UNVERIFIED** and should be checked by the hardware track. Budget about USD 51 per spare Petoi pack; ≥3 packs adds about USD 100–150.
2. **AI Act Digital Omnibus on AI: Regulation (EU) 2026/1744** (8 Jul 2026, in force 27 Jul 2026, per artificialintelligenceact.eu; not re-checked on EUR-Lex).
   - Art. 50(1) still applies from 2 Aug 2026.
   - Art. 50(2) marking gets a transition to 2 Dec 2026.
   - New Art. 5 prohibitions (non-consensual intimate imagery, CSAM generation) apply from 2 Dec 2026.
   - Annex III high-risk obligations are deferred to 2 Dec 2027.
   - The Art. 4 AI-literacy duty was reworded.

   The report cites none of this. None of it changes our design, but the legal track should cite the consolidated text.
3. **AI Act provisions relevant to a child audience that the report does not mention.**
   - Art. 5(1)(b) prohibits exploiting vulnerabilities due to age; this supports the report's "no persuasion or social pressure" rule.
   - Annex III(1)(b)/(c) makes biometric categorisation by sensitive or protected attributes, and emotion recognition, high-risk.
   - Art. 50(3) requires deployers to inform people when emotion recognition or biometric categorisation is used.

   Excluding age, gender and emotion keeps the demonstrator out of all three, which is a stronger argument than Art. 5(1)(f)/(g) alone.
4. **The abuse risk grows with session length and group size** (Brščić et al. 2015, Table 2 and model): abusive interactions averaged 238 s vs 40 s for non-abusive ones, with 4.9 vs 2.1 other children present. The modelled abuse probability for a 30-s interaction is 4.8 % with 2 children and 23 % with 4 children. Our 4-min team sessions are exactly the risky regime, which strengthens the case for the pen, constant staff presence and an adult in the team.
5. **Constrained-vocabulary offline ASR is missing from the audio pipeline.** For 2–4 closed answers, a grammar- or vocabulary-restricted recogniser fits better than open Whisper, because it cannot hallucinate long text. Vosk works offline, has about 50 MB models for EN/FR/NL/PL and supports runtime vocabulary reconfiguration (https://alphacephei.com/vosk/). [Update 2026-10-02: the licence is confirmed as **Apache-2.0** on GitHub [72]; now integrated into §4.] The report's step 4 ("match transcript to 2–4 options") should A/B a constrained recogniser against Whisper.
6. **Kennedy et al.'s own recommendation** that background noise "appears to be less of an issue than initially anticipated" with constrained grammars is omitted. The binding constraints were distance, angle and spontaneous speech, which supports the close-talk bone mic more than heavy denoising.
7. ~~**No 2027 call information exists yet.**~~ **Superseded 2026-10-02.** The SiW landing page had no 2027 details, but the separate call page [62] gives:
   - 17–19 Mar 2027 in Brussels (set-up 16 Mar);
   - deadline 6 Oct 2026, 12:00 CEST; notification 28 Oct;
   - workshops 4 and 9 Nov 2026;
   - 15 min per group; ages 7–18; FR/NL assistants; up to 3 people funded.

   Integrated into §0, §2.2, §8.0 and §9.

## Gap-fill log 2026-10-02 (second pass, web search available)

| Item (from §11 / verifier) | Result | Source |
|---|---|---|
| SiW 2027 logistics | **Found.** 17–19 Mar 2027 Brussels; deadline 6 Oct 2026 12:00 CEST; notification 28 Oct; workshops 4 and 9 Nov. Groups "spend 15 minutes at your booth"; ages 7–18; FR/NL assistants; ≤3 people funded. **Throughput model rewritten around the 15-min group slot.** | [62] |
| FROG (named in the brief, missing before) | **Added.** About 500 visitors; 87 tour starts → 58 completions; 78 % passers-by; camera seen as eyes; e-stop pressing in earlier robots | [63][64] |
| Exploratorium APE 132.3 s vs 51.1 s | **Confirmed via indexed text** of the Phase 1 and Phase 2 reports (PDFs 403) | [13] |
| Science-fair stand throughput benchmark | **Added.** Galaxy Makers: about 2,000 users over 64 h on 3 machines; 40 % keepsake re-engagement | [65] |
| Recent dwell data | **Added.** PARSEC 2026: games median 170 s, quizzes 118 s | [66] |
| Exhibition-hall noise | **Partly.** Museums with visitors 61–66 dB(A); trade-show booth caps of 85 dBC LCeq 30 s. SiW hall unmeasured | [69][73] |
| Enhancement vs Whisper | **Found (adult/medical speech).** Denoising worse in 40/40 configurations → default no denoiser | [70] |
| Whisper hallucination on non-speech | **Confirmed** → VAD gate | [71] |
| Vosk licence | **Apache-2.0 confirmed** | [72] |
| Bittle X tethered power | **No pass-through** confirmed | [74] |
| SELPHY CP1500 / KP-108IN prices | **Updated** (US retail, Sep–Oct 2026); 41 s glossy / 56 s semi-gloss per the Canon manual | [76][77] |
| Thermal/label printer | **Added.** Brother QL-800 (93 labels/min, USD 124.99); Epson TM-T20III (250 mm/s, about USD 180–230) | [78][79] |
| BPA in thermal paper | **Confirmed.** <0.02 % w/w since 2 Jan 2020 | [82] |
| Smartphone ownership (QR viability) | **Found (Flanders).** 59 % of primary pupils have no smartphone; majority ownership only from age 11 | [80] |
| ImageNet Roulette offline date | **27 Sep 2019** | [83] |
| Biometric Mirror specifics | **14 traits** incl. attractiveness, weirdness, emotional stability, aggressiveness; ratings from more than 30,000 respondents; Univ. Melbourne / Science Gallery Melbourne, 2018 | [84] |
| Deutsches Museum / Science Museum London | Deutsches Museum Bonn *Mission KI* (face-recognition voting booth, AMECA). The London AI show was **Science Gallery London**, not the Science Museum | [85][87] |
| Recent AI-perception exhibits | **Added.** MoS Boston (Spot + replica + "trick the model"), Exploratorium 2025, Tech Interactive 2025 (MediaPipe), Technopolis Mechelen 2024–25, Machine Gaze, CHI EA 2024 five-exhibit study (125 children aged 7–14) | [75][86]–[90][96] |
| "How does a robot see you" novelty | No exact match found; frame it as a new combination | §6 |

## Verification log (second independent verifier, 2026-10-02)

Fresh WebSearch/WebFetch lookups. Primary sources were preferred; full PDFs were read where possible (FROG, Galaxy Makers, Carvalho). **Verdicts:** confirmed / corrected / unverifiable.

| # | Claim | Verdict | Source / note |
|---|---|---|---|
| V1 | SiW 2027 timeline: deadline 6 Oct 2026 12:00 CEST; notification 28 Oct; workshops 4 Nov (communication) and 9 Nov (science show); fair 17–19 Mar 2027 Brussels; set-up 16 Mar | **Confirmed** | https://marie-sklodowska-curie-actions.ec.europa.eu/node/1621 |
| V2 | SiW 2027: groups spend 15 min per booth; ages 7–18; FR/NL with language assistants; up to 3 people funded; "modular activities work best"; shows 30 min, about 60 people, about 15 shows | **Confirmed.** Added: eligibility is "MSCA fellows and alumni"; "over 4000 pupils"; up to 4 nights; approved materials funded but giveaways excluded | same |
| V3 | FROG: about 500 visitors; 3 min 10 s tour; 87 starts → 58 reached the last stop; 78 % walking by; singles/pairs 36.4 % vs groups 16.1 %; distance 4.7/55.5/20.3 %; camera lenses treated as eyes; e-stop quote (Sage, Museum für Kommunikation Berlin) | **Confirmed** (full PDF). Nuance: the 78 % is "of all cases" (coded robot actions), not of individual passers-by. The robot was remote-operated. | https://www.cs.kent.ac.uk/events/2015/AISB2015/proceedings/hri/7-Karreman-howcana.pdf |
| V4 | Galaxy Makers: 3 machines, 64 h, 14,371 visitors, about 2,000 users, >3,000 engaged, 4–6 demonstrators, 40 % (about 700) visited the website, 75 % of those returned | **Confirmed** (full PDF) | https://arxiv.org/pdf/1705.04563 |
| V5 | PARSEC (arXiv 2607.13724): 2,816 sessions, 8 exhibits, median games 170 s, quizzes 118 s | **Corrected (minor).** Numbers confirmed (170.2 s / 117.8 s), but the exhibits are touch-enabled, not "push-button" | https://arxiv.org/html/2607.13724 |
| V6 | "When De-noising Hurts" (arXiv 2512.17562): 40/40 configurations worse with MetricGAN+; 4 ASR systems; 1.1–46.6 points semWER; medical speech; Dec 2025 | **Confirmed** (submitted 19 Dec 2025) | https://arxiv.org/abs/2512.17562 |
| V7 | Calm-Whisper cuts non-speech hallucination by >80 % | **Confirmed.** It is a Whisper-large-v3 head fine-tune with <0.1 % WER cost. It is not a drop-in for Whisper-small, so the VAD gate remains the practical measure. | https://arxiv.org/abs/2505.12969 |
| V8 | Whisper-small.en WER 24.46 % NCTE / 30.15 % MPT, "the" ×206, on "classroom child speech" | **Corrected.** Numbers confirmed; the data is mixed teacher and student classroom audio from room mics, not isolated child speech | https://arxiv.org/html/2409.14494v4 |
| V9 | Vosk: Apache-2.0, about 50 MB models incl. FR/NL/PL/EN, runtime vocabulary | **Confirmed with nuance.** Small NL 39 MB, FR 41 MB, PL 50 MB, EN 40 MB, all Apache-2.0. Dynamic vocabulary works on small models only. The larger NL models are CC-BY-NC-SA. 15.2k stars | https://github.com/alphacep/vosk-api ; https://alphacephei.com/vosk/models |
| V10 | Silero VAD: MIT, about 2 MB, <1 ms per 30 ms chunk, 8/16 kHz | **Confirmed** | https://github.com/snakers4/silero-vad |
| V11 | Bittle X: 7.4 V 1,000 mAh, "1 hour", 1.5 h charge, 2 A/5 A max, IMU only (no camera/mic in spec), 269–353 g | **Confirmed** | https://www.petoi.com/pages/bittle-x-robot-dog-with-arm-specifications |
| V12 | Bittle battery: no pass-through, 5 V/1 A charging | **Confirmed. Omission corrected:** the same page gives running life as "<0.5 h" and stepping in place as ">1 h" | https://docs.petoi.com/technical-support/battery |
| V13 | Bittle X from USD 319 | **Confirmed** (variants USD 319–469, petoi.com via search, 2026-10) | https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled |
| V14 | Hiwonder PuppyPi Standard USD 589.99 (RPi 4B 4 GB) / 599.99 (RPi 5 2 GB) with HD wide-angle camera | **Confirmed** (all variants available). Whether the voice module is in the Standard kit is **unverifiable** from the page text | https://www.hiwonder.com/products/puppypi.json |
| V15 | Adafruit #1185 100 mm arcade button USD 9.95 | **Confirmed** (in stock; LED up to 12 V) | https://www.adafruit.com/product/1185 |
| V16 | Canon SELPHY CP1500: 41 s glossy / 56 s semi-gloss postcard; 5–40 °C; USB-C; 2.4 GHz Wi-Fi | **Confirmed** | https://cam.start.canon/en/P001/manual/html/UG-07_Reference_0070.html |
| V17 | SELPHY MSRP USD 179.99; Amazon USD 151.99 on 22 Sep 2026 | **Confirmed** via price tracker/retail search (Best Buy USD 159.99, Micro Center USD 179.99). KP-108IN price **unverifiable** (Canon USA returned 403) | https://pricehistory.app/p/canon-selphy-cp1500-wireless-compact-photo-printer-535rzy2h |
| V18 | Brother QL-800: 93 labels/min, USD 124.99 | **Confirmed with nuance:** the speed is for standard address labels, black text (search of Brother USA and Staples; Brother page returned 403) | https://www.brother-usa.com/p/thermal-printers-labelers/QL800 |
| V19 | AI Act Art. 50(1) disclosure applies from 2 Aug 2026; Digital Omnibus = Reg. (EU) 2026/1744, adopted 8 Jul 2026, in force 27 Jul 2026; Annex III high-risk deferred to 2 Dec 2027; Art. 50(2) transition 2 Dec 2026; new Art. 5 prohibitions from 2 Dec 2026 | **Confirmed.** OJ publication was 24 Jul 2026; ELI http://data.europa.eu/eli/reg/2026/1744/oj; Annex I-linked high-risk deferred to 2 Aug 2028. EUR-Lex itself was not fetched (secondary sources only) | https://artificialintelligenceact.eu/article/50/ ; https://www.nicfab.eu/en/posts/digital-omnibus-ai-official-journal/ ; https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo |
| V20 | Carvalho et al. 2013: museums with visitors 61–66 dB(A) vs 27–41 empty; 45 dB(A) recommended max | **Corrected.** 61–66 is one museum (Serralves) with 5–20 people per room; 45 dB(A) is the HVAC-only background; the with-visitors ideal is ≤55 dB(A) | https://commercial-acoustics.com/wp-content/uploads/2020/07/AcousticsofModernandOldMuseums.pdf |
| V21 | ImageNet Roulette offline after 27 Sep 2019; ImageNet to remove about 600,000 images; Fondazione Prada *Training Humans* | **Confirmed** | https://www.theartnewspaper.com/2019/09/23/leading-online-database-to-remove-600000-images-after-art-project-reveals-its-racist-bias |
| V22 | Biometric Mirror: attractiveness, weirdness, emotional stability…; several thousand photos rated by >30,000 respondents; Univ. Melbourne until Sep 2018 | **Confirmed** (14-trait count not re-checked; New Atlas lists 6 example traits) | https://newatlas.com/biometric-mirror-facial-recognition-human-bias/55711/ |
| V23 | Deutsches Museum Bonn *Mission KI* face-recognition voting booth as "casual" use of face recognition | **Corrected.** It is *Smile to Vote*, a critical artwork by A. Peterhaensel; AMECA confirmed; no privacy note on the page confirmed | https://www.deutsches-museum.de/bonn/ausstellung/mission-ki ; https://alexanderpeterhaensel.com/smiletovote |
| V24 | MoS Boston: Spot on a 180-s course, staff-controlled, non-functional replica beside it; Unitree Go2; Robot Roundup | **Confirmed** | https://www.boston.com/news/technology/2025/09/30/museum-of-science-lets-the-public-interact-with-robot-dogs-and-humanoid-robots/ |
| V25 | Technopolis *AI!* zone 3 Dec 2024–31 Dec 2025, ages 12+ | **Confirmed** (secondary press/search) | https://www.klasse.be/voordelen-aanbod/expo-ai-technopolis-mechelen-lerarenkaart/ |
| V26 | Apestaartjaren 2024: 59 % of Flemish primary pupils have no smartphone | **Confirmed** | https://www.ilikemedia.be/apenstaartjaren-2024/ ; https://assets.mediawijs.be/2024-05/apenstaartjarenrapport_2024_lr_1_3.pdf |
| V27 | Exploratorium APE 132.3 s vs 51.1 s | **Confirmed via search index** of the 2004 Phase 1 interim report; the PDF itself was not opened | https://www.exploratorium.edu/sites/default/files/pdfs/APE_Summative_Phase_1.pdf |
| V28 | UNICEF *Guidance on AI and Children* v3 (2025) | **Confirmed** as v3.0 "updated in 2025" | https://www.unicef.org/innocenti/projects/ai-for-children |

## Omissions added by verifier (second pass)

1. **SiW eligibility and application mechanics.** The call is for "MSCA fellows and alumni". Applications go through the EUSurvey form (https://ec.europa.eu/eusurvey/runner/Call_SiW2027). Funding covers up to 3 people and up to 4 nights; materials are covered but giveaways are not. Whether the SiW budget can fund printed keepsake cards or stickers is therefore unclear (**UNVERIFIED**), so ask, or fund them from TUAI.
2. **Bittle runtime depends on the scenario.** The spec sheet says "1 h", but Petoi's battery page says running is <0.5 h. The swap plan (§5.2) holds only for in-place gestures, so do not schedule walking demos on the 40–45-min swap cycle.
3. **Vosk licensing trap for Dutch.** Only the small Dutch model (39 MB) is Apache-2.0 *and* supports runtime grammars. The more accurate Kaldi_NL models are CC-BY-NC-SA and static, so use vosk-model-small-nl-0.22 for the closed-answer grammar.
4. **Calm-Whisper targets Whisper-large-v3.** That is too heavy for low-latency CPU use on the Intel Core Ultra 7 255U at the stand (latency **UNVERIFIED** here). For Whisper-small, rely on Silero VAD plus `no_speech_prob`/`avg_logprob` rejection.
5. **Noise baseline is likely an underestimate.** The only measured museum figures (58–66 dB(A)) come from quiet art museums with 5–20 people per room, so the SiW hall will plausibly be louder. Size the acceptance test (80 dB babble) accordingly; measure on 16 Mar 2027 at set-up.
6. **Label-printer throughput.** The 93 labels/min figure is for address labels with black text. A 25-child class at roughly 2–4 s per graphic badge is still feasible within the 2-min forget/keepsake segment, but benchmark it before relying on it.
