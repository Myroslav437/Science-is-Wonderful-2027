# Deliverable 3: Hardware recommendation and budget

Purpose: tell TUAI partners which robot and booth hardware to buy for "How does a robot see you?", what it costs, who pays for what, and how to get it safely to Brussels.

Status 2026-10-02. Prices and specs come from `research/02-robots-linux.md` and `research/03-robots-other.md`. Those files read the vendor stores on 2026-10-01/02, and this document uses their verifier-corrected values. Anything else is marked "estimate" or "to confirm". FX (NBP table 191/A/NBP/2026, 2026-10-01): 1 USD ≈ 0.886 EUR, 1 EUR = 4.3770 PLN ([NBP EUR][nbpeur], [NBP USD][nbpusd]). The design decisions follow `docs/_brief.md`.

## Key points

- **Buy two SunFounder PiDog V2 kits and two Raspberry Pi 5 4 GB boards.** The second unit is a hot spare. PiDog is the cheapest robot that streams camera frames and raw microphone audio out of the box, and the only one cheap enough to buy a second unit as a hot spare.
- **The robot is a thin sensor node.** It captures and streams data, enforces the sensor switches and moves. All AI runs on the offline stand laptop. Nothing goes to a cloud.
- **At list prices, two units fit the USD ~600 robot budget. Landed, they do not.**
  - List: 2 kits USD 359.98 + 2 Pi 5 4 GB at ~USD 110 (derived list price) = about USD 580.
  - Landed in Poland, with 23% VAT, ~5% duty and spares, the robot line costs about €770 (≈ USD 870), before shipping.
  - If USD 600 is a landed cap: unit 1 with spares (~€425 ≈ USD 480) fits; unit 2 (~€345) comes from additional funds.
  - The rest of the booth (microphone, switch box, pen, router, signage, batteries, cables) needs about €400-800 more.
- **No laptop needs to be bought.** The dev laptop (Intel Core Ultra 7 255U, 32 GB, no NVIDIA GPU) runs the core loop on its CPU and the optional "imagination" image on its integrated GPU via OpenVINO, in 2.6 s per image (measured, brief §4). Everything running at once is still to benchmark (§5, January). A laptop with an NVIDIA GPU is optional: it should cut the image to about 1 s or less (estimate, not measured) and leave more headroom. Borrow one from SUT if possible. Buying one would add €1,200-1,500 (brief estimate).
- **Order this week if SUT procurement allows a direct card or online purchase; otherwise start the procurement request this week** (route to confirm). SunFounder ships only from China (3-14 days, plus customs). At Botland the Pi 5 4 GB is a scheduled delivery around 13 Nov 2026 (180 units expected); only the 8 GB is in stock.
- **Fallback:** Luwu XGO-lite3 (USD 599, ≈ €660-720 incl. VAT, plus shipping and duty). Gate result by 30 Nov; if PiDog fails, order the XGO on 1 Dec.
- **Privacy hardware:** a physical lens shutter, a hardware mute on the hand-held mic, and LEDs driven by the real capture state. EYES and EARS are off by default, shutter closed.
- **Safety:**
  - the robot stays on the table in a pen, with its camera raised towards child eye height;
  - it only gestures and never walks;
  - the e-stop is on the staff side;
  - spare packs are charged only on the staff side, attended, in a fire-safe bag. If the robot runs tethered, its installed pack charges in the pen: ask the organisers whether that is acceptable, or use a regulated supply into the HAT instead of the pack (§6).

---

## 1. Robot options compared

### 1A. Cost and platform

| Option | List price | What is included | Onboard computer | OS / ROS / Python | Verdict |
|---|---|---|---|---|---|
| **SunFounder PiDog V2 + Pi 5 4 GB** | Kit USD 179.99 ([store][sf]). Pi 5 4 GB 514.90 PLN ≈ €118 incl. VAT ([Botland][bl4]). **≈ €360-420 per unit incl. VAT and spares** (research/02 §4), plus ~5% duty and shipping | Kit you assemble yourself (4-6 h): 12 servos, Robot HAT V5, camera, sensors, 2×18650 pack. **No Pi, no SD card** | Our Raspberry Pi 5 (V2 supports Pi 5/4/3B+/Zero 2W) | Raspberry Pi OS, Python (`pidog`, `robot-hat`, `vilib`, GPL). No ROS | **Recommended** |
| Luwu XGO-lite3 | USD 599 ([shop][xgo]). ≈ €660-720 incl. VAT, plus shipping and duty (to confirm) | Assembled. CM5 2 GB + 32 GB microSD, arm and gripper, battery, USB-C dock | Pi CM5 | Luwu-OS, `xgolib` (Python), Blockly, ROS 2 example | Integrated alternative. Fallback only |
| Yahboom DOGZILLA-Lite CM5 | USD 639 ([store][dz]). ≈ €700-750 incl. VAT, plus duty | Assembled. Same product as XGO-lite3 (made jointly by Luwu and Yahboom) | Pi CM5 | Python/JupyterLab (default password), Blockly-style | Over budget. English-docs twin of XGO-lite3 |
| Hiwonder PuppyPi Advanced | USD 639.99 (Pi 5 2 GB) or 629.99 (Pi 4B 4 GB) ([store][pp]). ≈ €700-760 incl. VAT, plus duty | Assembled, with Pi, camera, 8.4 V charger and voice box | Pi 5 or Pi 4B | Ubuntu 22.04 + ROS 2 Humble in Docker. Humble reaches end of life on 31 May 2027 | Over budget, 480p camera, vendor "gender recognition" demo |
| MangDang Mini Pupper 2 | USD 649 pre-assembled ([store][mp2]). ≈ €620-650 (vendor states tax and clearance included) | CM4 robot. **No camera** (USD 8 add-on). LiDAR costs USD 119 extra | Pi CM4 + ESP32 | Ubuntu 22.04 + ROS 2 Humble | Not suitable |
| Freenove FNK0050 | USD 129.99 ([store][fn]) | Kit with camera. No Pi, no 18650 cells, no charger | Our Pi | Python server + PyQt client (CC BY-NC-SA 3.0) | Not suitable |
| Petoi Bittle X V2 | USD 319-399 (Alloy, pre-assembled: 399) ([Petoi][bx]) | Robot only. No camera | ESP32 (a Pi can be added over UART) | OpenCat (MIT), Arduino/C++, Python serial API | Not suitable |
| Hiwonder MechDog | USD 299.99 Standard, 369.99 Advanced ([store][md]) | Advanced adds an ESP32-S3 camera, a voice-command module, touch, light and MP3 modules ([packing list][mdw]) | ESP32 | MicroPython, Arduino, Scratch | Not suitable |
| Unitree Go2 Air (above-budget reference) | USD 1,600 without controller ([Unitree][go2]). €2,618 incl. VAT in the EU ([Reichelt][go2r]) | Assembled, ≈ 15 kg | Not open on the Air | **No official SDK on the Air** (EDU only). The unofficial WebRTC route needs a login to the vendor's cloud | Reference only |

### 1B. Sensors, audio, power

| Option | Camera (raw frames to the laptop?) | Microphone (raw audio?) | Other sensors | Speaker | Battery / runtime |
|---|---|---|---|---|---|
| **PiDog V2** | OV5647 5 MP, 65° ([docs][pdcam]). **Yes:** MJPEG at `http://<pi>:9000/mjpg` ([vilib][vilib]) | **Yes:** MEMS mic on Robot HAT V5, ALSA ([HAT V5][hat]). Also a 3-mic sound-direction module that gives the angle only, no audio ([docs][sdir]; inclusion in the current V2 kit to confirm) | Ultrasonic, dual touch, 6-DOF IMU, RGB light bar | Mono cavity speaker | 2×18650, 7.4 V 2000 mAh. 90-120 min claimed ([review][rees]). Crashes at low battery reported ([RPi mag][rpimag]) |
| XGO-lite3 | OV5647 5 MP. **Yes** (Picamera2, browser stream on `:8080`) | MEMS mic, count not stated ([wiki][xgoai]). Raw capture likely, because the twin model supports `arecord` | IMU, 2.0" screen, 4 buttons | Cavity speaker | 2500 mAh 2S. Runtime not stated. Must be charged with the robot off |
| DOGZILLA-Lite CM5 | OV5647 5 MP. **Yes** (web image transmission) | **Yes:** dual MEMS mics, `arecord` works ([docs][dzaudio]) | IMU, 2.0" screen | 2 W speaker | 18650 2500 mAh. Runtime not stated. The CM5 fan degrades voice pickup |
| PuppyPi Advanced | 480p, 130° USB camera. Yes (ROS topic `image_raw`) | **Yes:** WonderEcho Pro USB mic (`arecord`) ([docs][ppv]). The Standard kit has no mic | IMU. Ultrasonic, touch and ToF LiDAR come only with Pro | 3 W (in the voice box) | 2200 mAh LiPo, ~60 min (reseller claim) |
| Mini Pupper 2 | Not included | Built-in mic (I2S driver in the board support package) | IMU, touch, LCD face, servo feedback | Yes | 1000 mAh, ~30 min. The vendor advises restarting the AI every 15 min ([docs][mp2d]) |
| Freenove FNK0050 | Included (model not stated). Yes, over TCP port 8001 | **None** | Ultrasonic, IMU | Buzzer only | User-supplied 2×18650. **1 min forced rest after every 3 min of motion** ([docs][fnd]) |
| Bittle X V2 | **None built in.** The Petoi AI Vision Module (USD 39) gives on-module detections plus a Wi-Fi image path; resolution, fps and availability to confirm (research/03 §2.1) | **No:** fixed voice commands only ([docs][pvoice]) | IMU, back touch | Buzzer/speaker | 7.4 Wh, ~1 h. The pack does not power the robot while charging |
| MechDog | Advanced only: ESP32-S3 camera, 320×240, Wi-Fi stream (codec and fps unverified) | **No:** fixed command words only | Ultrasonic, IMU, plus touch and light sensors on Advanced. **No head joint** | MP3 module (Advanced) | 1500 mAh, ~60 min |
| Go2 Air | 1280×720, 120°. Only through the unofficial WebRTC route | **No voice function on the Air** ([docs][go2d]) | 4D LiDAR L1, IMU | No voice function | 8000 mAh, 1-2 h. 15 kg, up to 2.5 m/s |

---

## 2. Recommendation

### Buy: SunFounder PiDog V2 + Raspberry Pi 5 4 GB, two units

Why:
1. **Its sensors match the story.** The "eyes" (5 MP camera) and the "ears" (MEMS mic with raw audio) are native. Raw streams are already exposed, so the robot can stay a thin node. Our live mode server already accepts the PiDog MJPEG URL (`prototype/live/run_live.py --camera http://<pidog>:9000/mjpg`), the format PiDog's `vilib` serves. It was tested on recordings, with sensors starting OFF and the gating and "forget me" verified (brief §4), but not yet on real PiDog hardware: the November gate tests that. Distance, touch, IMU and sound direction (inclusion in the current V2 kit to confirm) give extra low-privacy cues.
2. **It is cheap enough for a hot spare.** Robustness at a 3-day fair depends more on having a second unit than on any spec difference (research/02 §4).
3. **The software is simple.** Plain Raspberry Pi OS and Python, with no ROS and no vendor cloud needed, so the image is easy to reflash and lock down. The PiDog repo switched its voice examples to offline Piper TTS in Jul 2026, the same engine we use (research/02, pass-2 omissions).
4. **It looks and acts like a dog.** It has a 3-DOF head, a tail and an RGB light bar, which gives us body language and "I'm listening / sensor off" signals.
5. **It has the highest weighted score in research/02 §5:** 4.26, against 3.88 for XGO-lite3.

What we accept:
- 4-6 h of assembly per unit;
- hobby-grade servos and HAT, with two open GitHub issues (see §5);
- audible servo noise, which is why the "ears" are a close-talk mic;
- extra battery strain from a Pi 5.

Check on delivery that the kit is **V2 with Robot HAT V5**. The V1 kit (HAT V4) has no microphone and does not support the Pi 5. Both SunFounder listings are the same SKU, CN0537D.

Pi choice:
- **Pi 5 4 GB** is enough, because the Pi only captures, streams, gates sensors and moves servos.
- The Pi 5 has **no hardware H.264 encoder**, so we stream MJPEG, which is already the plan ([RPi docs][rpicam]).
- The Raspberry Pi magazine review advised against a Pi 5 on PiDog battery power. That review tested a Pi 4 on the V1 kit, and V2 officially supports the Pi 5, but the battery strain is physical. So we will run the robot tethered and benchmark battery runtime. A **Pi 4 4 GB** is the fallback node: it has hardware H.264 and draws less power (price to confirm).
- **Stock** ([Botland][bl4], verified 2026-10-02): the 4 GB board is due around **13 Nov 2026**. To start before then, either buy one 8 GB board now (839.90 PLN ≈ €192, in stock, +€74; [Botland][bl8]) or prototype on a lab Pi 4.

### Integrated alternative: Luwu XGO-lite3 (fallback only)

- **When:** only if PiDog fails the November gate (result by 30 Nov, §5), for example because of an unstable stream, repeated HAT failures or unusable audio. Then order on 1 Dec.
- **For:** it arrives assembled, with a CM5, camera, mic, speaker and face screen, quiet servos and dual-band Wi-Fi.
- **Against:**
  - ≈ €660-720 incl. 23% VAT, plus shipping and duty (to confirm), slightly over budget;
  - weak 2.3 kg·cm servos;
  - a robot arm, which is a pinch point (keep it folded and disabled in software);
  - documentation mostly in Chinese;
  - it must be charged with the robot off, so it cannot run tethered and needs battery rotation.
- **Vendor AI must be removed.** It defaults to Alibaba Cloud LLMs with **long-term memory switched on** ([wiki][xgocloud]). We would reflash the robot, remove the vendor AI and change all default credentials.
- **Do not power it on while holding it.** The IMU calibrates at boot.
- **Other sales channels:**
  - ELECFREAKS "CM5 XGO-Lite", USD 619, if a different invoicing entity is needed ([ELECFREAKS][elf]);
  - DOGZILLA-Lite CM5, USD 639, which comes with English docs.

### Do not buy

| Do not buy | Why |
|---|---|
| PiDog **V1** (Robot HAT V4) | No microphone, no Pi 5 support |
| Freenove FNK0050 | No microphone. Forced 1-min rest after every 3 min of motion. Falls over in reviews |
| Mini Pupper 2 | No camera in the box, ~30 min battery, USD 649 |
| PuppyPi Standard | No microphone (Advanced, from USD 629.99, is needed). 480p camera. Vendor demo includes "gender recognition" |
| Yahboom DOGZILLA S1/S2 | No longer on the official store. Cannot run while charging |
| Petoi Bittle X, Hiwonder MechDog | ESP32 boards: fixed voice commands only (no raw audio). No built-in camera on Bittle (add-on image quality unverified); MechDog Advanced streams only 320×240 |
| MechDog AI, Petoi AI Head, other "XiaoZhi" AI heads | Stream children's voices to a vendor cloud by default |
| Unitree Go2 Air, or a used Go1 | USD 1,600+. No official SDK and no mic on the Air. 15 kg at up to 2.5 m/s near children. Public security flaws (CVE-2025-35027, patch status unknown; Go1 backdoor CVE-2025-2894) |
| Crowdfunded dogs (Petoi Quaddle, XGO-mini2SW) | Delivery risk against a fixed March 2027 date |
| Any vendor "AI" app (cloud LLMs, emotion or gender demos) | Conflicts with our offline, no-sensitive-attributes design and with AI Act Art. 5 (`research/09-ethics-law.md`) |

---

## 3. What the robot provides, what we add, what runs externally

| Function | Robot provides (PiDog V2) | We add | Runs externally (stand laptop, offline) |
|---|---|---|---|
| Eyes | 5 MP camera in the head | 3D-printed sliding lens shutter. The capture process on the Pi stops when EYES is off | MediaPipe face detector and pose, CLIP ViT-B/32 with Platt calibration, k-means colour naming. "Foggy lens" degradation |
| Ears | MEMS mic on HAT V5 (backup only: servo noise). The booth image never opens it for capture unless it is the declared backup. Whether it can be disabled at driver level without losing the speaker (they share the HAT's I2S bus, research/02 §2.1) is to confirm | Hand-held close-talk wireless "dog-bone" mic, with its receiver on the Pi's USB, plus a **hardware mute** on the bone (the transmitter's own mute or a switch we add; to confirm). The robot stays still while listening. Capture stops when EARS is off | Silero VAD, faster-whisper (multilingual), keyword spotting, loudness against the booth calibration. "Noisy room" babble |
| Sound direction | 3-mic module, angle only (inclusion in the current V2 kit to confirm) | Polling stops when EARS is off, because the angle is derived from audio | Head-turn cue only. Not used for any of the 6 slots |
| Distance, touch, IMU | Ultrasonic, dual touch, 6-DOF IMU | JSON publisher at 10-20 Hz on the Pi | Interaction and safety cues (for example "someone lifted me" → relax the servos). Not used for any of the 6 slots |
| Voice | Mono speaker | n/a | Piper TTS generates the speech. The Pi only plays it |
| Body language | 12 servos (3-DOF head, tail, legs), RGB light bar | Pen and pedestal. Gestures only. Staff-side e-stop | Chooses which pose or light to show and when |
| Compute | None (the kit has no Pi) | Raspberry Pi 5 4 GB and microSD. Runs only capture, streaming, sensor gating and the command API | **All AI:** perception, evidence memory, fusion, XAI, UI on the TV, optional "imagination" image (LCM-Dreamshaper v7 restyles the robot's own avatar drawing, OpenVINO on the integrated GPU; brief §1), optional printer |
| Network | Pi 5 dual-band Wi-Fi, Gigabit Ethernet | Dedicated 5 GHz travel router with no internet. Ethernet while the robot is stationary | Firewall that blocks all outbound traffic. No venue Wi-Fi |
| Controls | None | USB arcade switch box: EYES, EARS, foggy lens, noisy room, FORGET ME, language flags. Staff-side keypad: round start, skip, abort (`06_exhibition_walkthrough.md`) | Reads the switches. Sends EYES/EARS off to the Pi, which stops capture at the source and reports its real capture state back |
| Privacy state | RGB light bar (a dedicated "mic off" colour, research/02 §6) | Lens shutter and mic mute (above). LEDs in the EYES/EARS buttons and on the light bar are driven by the Pi's actual capture processes, not by the switch position. **EYES and EARS are off by default, shutter closed** | UI shows provenance, for example "no data received from camera since 12:03:15" (research/02 §6) |
| Power | 2×18650 pack, USB-C charging on the HAT | Tethered USB-C supply or pack rotation, spare packs, a way to charge spares outside the robot (§4), fire-safe bag | n/a |
| Display, keepsake | None | TV (provided by the fair). Optional offline printer, used only on request | Browser UI. Card rendering (no photo, no name, no QR code) |

External or cloud services: **none** (brief §4).

If both robots fail, a laptop webcam becomes the "eyes" and the close-talk mic plugs into the laptop's USB (`run_live.py --camera 0 --mic default`; `02_architecture.md` §6, `06_exhibition_walkthrough.md`).

---

## 4. Bill of materials and budget

Column (a) is the USD ~600 robot budget. Column (b) is reused from SUT or provided by the fair, at no cash cost. Column (c) needs additional funding. Amounts in EUR include 23% VAT. Robot-line items also include estimated duty; SunFounder shipping is listed separately. The optional printers are converted US prices (see the notes under the table).

| # | Item | Qty | Unit price (source) | (a) Robot budget | (b) Reused / provided | (c) Additional funding |
|---|---|---|---|---|---|---|
| 1 | SunFounder PiDog V2 kit | 2 | USD 179.99 ([store][sf]) | €392 (incl. 23% import VAT) | | |
| 2 | Spare servo "Metal Gear Pro" | 6 | USD 9.99 ([store][sfs]) | €65 | | |
| 3 | Customs duty and clearance on the SunFounder order | 1 | ~5% of goods (estimate, research/02 §4) | ~€20 | | |
| 4 | SunFounder shipping (DHL/UPS 3-7 days for orders over USD 400) | 1 | To confirm | to confirm | | |
| 5 | Raspberry Pi 5 4 GB | 2 | 514.90 PLN ≈ €118 incl. VAT ([Botland][bl4]) | €235 | | |
| 6 | microSD card (one is a pre-imaged spare) | 3 | ~€10 (estimate, research/02 §4) | €30 | | |
| 7 | USB-C 27 W power supply (Pi bench power and HAT charging; charger spec to confirm) | 2 | ~€13 (estimate, research/02 §4) | €26 | | |
| 8 | Spare Robot HAT V5 | 1 | To confirm (whether it is sold as a spare is unverified) | to confirm | | |
| | **Robot line subtotal** (incl. VAT, duty and spares; at list prices ≈ USD 580) | | | **~€770 + shipping** | | |
| 9 | Stand laptop: the dev laptop (Intel Core Ultra 7 255U, 32 GB, integrated GPU, no NVIDIA GPU). Measured: 250-450 ms per camera frame and 2.3 s per spoken answer on the CPU, 2.6 s per imagination image on the integrated GPU (brief §4). Caveat: while the integrated GPU generates nonstop, CPU perception slows to about a third to a half, so the image is generated once per stage (research/06 §3.1). The whole pipeline has not yet been benchmarked running at once | 1 | n/a | | €0 | |
| 10 | *Optional:* a faster laptop with an NVIDIA GPU (RTX 4060/4070 Laptop 8 GB; if buying, prefer an RTX 5070 Ti Laptop 12 GB, research/06 §11.2). Imagination about 1 s or less (estimate, not measured), more CPU headroom. If one is reused, the dev laptop becomes the cold spare. Without a second laptop, a laptop failure falls back to the unpowered "be the robot" balance game (`06_exhibition_walkthrough.md`) | 1 | €1,200-1,500 if bought (brief estimate; laptop prices are unverified in research/06) | | €0 if reused from SUT | only if bought |
| 11 | TV with HDMI, low long table, 3 chairs | 1 | Provided by the fair (research/01) | | €0 | |
| 12 | Lens shutter, bone grip, switch-box enclosure (3D printed). Plus one touchable replica dog for the front of the booth, cardboard or 3D printed (`06_exhibition_walkthrough.md`) | 2 sets | Filament only | | €0 (SUT printer) | |
| 13 | Close-talk wireless mic in the "dog-bone" grip, with a **hardware mute** on the bone (the transmitter's own mute or a switch we add; to confirm). Candidates: DJI Mic Mini, €45 (1 TX + 1 RX) or €79 (2 TX + RX) ([DJI][dji]), USB audio on the Pi to confirm; RØDE Wireless GO Gen 3 works as a USB mic ([RØDE][rode]), price to confirm. Wired fallback: Samson Q2U, ~USD 70-80 ([listing][q2u]) | 1 | €60-150 (brief) | | | €60-150 |
| 14 | USB arcade switch box (EYES, EARS, foggy lens, noisy room, FORGET ME, language flags). The EYES/EARS button LEDs show the capture state reported by the Pi. Plus a **separate staff-side e-stop** and staff keypad (round start, skip, abort) | 1 | 100 mm LED arcade button USD 9.95 ([Adafruit][ada]). Encoder, toggles: estimate | | | €40-80 (estimate) |
| 15 | Pen (clear acrylic fence 10-15 cm high) and pedestal, fixed or weighted against tipping (§6) | 1 | Estimate | | | €50-100 |
| 16 | Dedicated 5 GHz travel router and Ethernet patch cable | 1 | €40-60 (brief estimate) | | | €40-60 |
| 17 | Spare PiDog battery packs (2×18650, 7.4 V 2000 mAh). Count to be sized after the November runtime test; research/10 §5.2 uses at least 3 packs per robot for 1-h packs | 2+ | To confirm (availability unverified, research/02 §8) | | | to confirm |
| 18 | Spare-pack charging: an external 2S (7.4 V) Li-ion charger that fits the PiDog pack connector, or charge spares in the spare robot on the staff side. The pack is normally charged through the HAT's USB-C, ~2 h (research/02 §1-2) | 1 | To confirm | | | to confirm |
| 19 | LiPo fire-safe bags | 2 | Estimate | | | €15-30 |
| 20 | Signage and print: AI and privacy notice in EN/FR/NL, "please don't touch my legs", vote cards, animal picture cards, switch labels | 1 set | Estimate | | | €100-200 |
| 21 | Cables and power: power strip with 4+ sockets, extension lead, USB-C and HDMI spares, cable tape, strain-relief hook | 1 set | Estimate | | partly reused | €40-60 |
| 22 | Padded transport case (2 robots, Pis, mic) | 1 | Estimate | | | €60-120 |
| | **Additional essentials subtotal** | | | | | **~€400-800 + spare packs and charger** |
| 23 | *Optional, on request only:* Brother QL-800 label printer (monochrome black/red labels). Fast enough to print for a whole class if the group asks. No photo, no name, no QR code | 1 | USD 124.99, US list ([Brother][ql]). EU price and labels to confirm | | | ~€136 incl. VAT + labels |
| 24 | *Optional, on request only:* Canon SELPHY CP1500 card printer, 41 s per card, for a volunteer who asks. No photo, no name, no QR code; its Wi-Fi stays off. KP-108IN media USD 34.99-47.99 per 108 prints ([Canon][kp]). About 2 packs for ~130-190 cards over 3 days (our estimate) | 1 | USD 151.99-179.99, US ([price][selphy], [manual][selphym]) | | | ~€240-300 incl. VAT and media |
| 25 | *Contingency:* XGO-lite3, only if PiDog fails the November gate | 1 | USD 599 ([shop][xgo]). ≈ €660-720 incl. VAT, plus shipping and duty | | | only if triggered |

Notes on the table:
- Printer figures are US retail prices converted at 0.886 plus 23% VAT, without shipping. EU prices are to confirm (research/10 §7, §11).
- The QL-800's 93 labels/min is Brother's figure for standard black-text address labels. Graphic badges print slower, so benchmark before relying on it (research/10 §7, verifier note).
- SiW does not pay for giveaways, so card media is our cost (research/01 §1.8, research/09).

### Budget summary

| Block | Cash needed |
|---|---|
| (a) Robot line: 2 units + spares | **~USD 580 at list prices** (2 kits USD 359.98 + 2 Pi 5 4 GB at ~USD 110 derived list price, research/02 §1). **~€770 incl. VAT, duty and spares** (≈ USD 870) + shipping. research/02 §4 gives €720-840 for two units |
| (b) Reused / provided | €0 (dev laptop as the stand laptop, TV and table from the fair, SUT 3D printer) |
| (c) Additional essentials | ~€400-800 (+ spare packs and charger, to confirm) |
| (c) Optional printer | ~€135-300 incl. VAT (US prices converted) |
| (c) Optional NVIDIA GPU laptop, only if none can be reused | €1,200-1,500 (brief estimate) |
| **Total cash, no laptop bought** | **~€1,200-1,600** (+ printer if chosen) |
| **Total cash, NVIDIA laptop bought** | **~€2,400-3,100** |

**Decision for supervisors.** Is the USD ~600 robot budget a list-price or a landed (incl. VAT) figure? At list prices it buys both robots (~USD 580). Landed, the robot line is ~€770 (≈ USD 870). If USD 600 is a **hard landed cap**:
- pay for unit 1 with all spares from it (~€425 ≈ USD 480, which fits);
- pay for unit 2 (~€345) from (c).

Proposal texts copied from brief §3 ("2 units fit the USD 600 target") should carry the same qualifier: "at list prices".

Funding notes:
- The EC pays travel and accommodation for up to 3 people. It "can also help you purchase or ship any approved material", but this is not guaranteed, so do not plan around it (research/01 §1.8).
- Whether TUAI Doctoral Network funds can pay for the hardware is to confirm with the SUT project office.

---

## 5. Procurement and logistics risks

| Risk | Facts | Mitigation |
|---|---|---|
| Pi 5 stock and price | Botland: 4 GB due ~13 Nov 2026, 2 GB ~8 Jan 2027, only the 8 GB is in stock ([Botland][bl4]). Pi prices rose in Dec 2025, Feb 2026, Apr 2026 and on 1 Oct 2026 (research/02 §1) | Pre-order 2 × 4 GB now. To start immediately, buy 1 × 8 GB (+€74) or use a lab Pi 4 |
| Shipping from China | SunFounder ships only from its China warehouse. Airmail takes 7-14 working days under USD 400; DHL/UPS takes 3-7 days over USD 400 ([store][sf]). 2 kits + 6 servos = USD 419.92, so the order goes by courier. The XGO shop showed a ~10-day National Day delay in Oct 2026 | Order both kits and the servos in one order this week. Do not plan China orders after mid-January because of Chinese New Year (early Feb 2027, date to confirm) |
| Import VAT and duty | 23% Polish import VAT. The EU €150 duty exemption ended on 1 Jul 2026. Consignments above €150 now pay standard TARIC duty (0-4.7% for toys under CN 9503, classification unverified) plus clearance fees. Consignments of €150 or less pay a flat €3 per item (Reg. (EU) 2026/382, [EC][eu3]) | Budget ~5% on top of VAT. Order kits and spare servos in one consignment. Ask SUT procurement whether an EU distributor (e.g. Botland, Kamami) can supply PiDog with a VAT invoice (to confirm) |
| Hardware quality (open GitHub issues) | [#11][gh11]: a Robot HAT V5 PWM channel failed days after purchase, then a second one (opened 2026-02-09, no vendor reply). [#10][gh10]: an audio underrun crashes the robot during a sit-to-stand move and needs a power cycle (opened 2026-01-17). Both were still open on 2026-10-02 | Keep a second unit, 6 spare servos and a spare HAT (to confirm). Move servos to free PWM pins if a channel fails. Never play sound during stance changes. Keep the robot still while listening. Watchdog restart. Practise a 5-minute robot swap |
| Battery strain and runtime | Low-battery crashes. The Pi 5 is not advised on PiDog battery power (RPi magazine, Pi 4 test). 90-120 min per pack is a review claim; runtime with a Pi 5 is unmeasured (research/02 §8). Charging takes ~2 h. Whether USB-C input keeps up with the drain is unverified | Run tethered. Measure a 6-h day in November and size the spare packs and charger from it. Swap packs before they run low. Pi 4 fallback |
| Assembly time | 4 h ([raspberrytips][rtips]) to 5-6 h ([RPi mag][rpimag]) per unit. Small screws, servo zeroing | Plan 2 working days for both units, including OS image and hardening |
| Air travel with batteries | PiDog pack: 7.4 V × 2.0 Ah ≈ 14.8 Wh (our calculation), well under 100 Wh. Under IATA 2026 rules, 100-160 Wh needs operator approval and above 160 Wh must go as cargo. Spare batteries, including those of 100 Wh or less, travel in carry-on only ([IATA][iata], research/01) | No airline approval needed. Robots and all spare packs go in cabin baggage, in fire-safe bags. Confirm with the airline. Alternative: road or rail from Gliwice to Brussels |
| Wireless mic | USB-audio mode on the Pi is unverified for the DJI Mic Mini. 2.4 GHz is congested in a hall full of phones | Bench-test in November. Keep a wired close-talk fallback (research/10 prefers a tethered bone) |
| Venue | Power sockets are not in the 2027 standard kit. There are no published rules on robots or batteries (research/01) | Request at least 4 sockets in form field B9. Ask the organisers about battery and fire rules after selection (28 Oct) |

### Timeline

| When | Milestone |
|---|---|
| **Now (by 9 Oct)** | Submit the proposal (6 Oct, 12:00 CEST). Ask SUT procurement which purchase route to use. If a direct card or online purchase is allowed, order 2 × PiDog V2 + 6 servos, pre-order 2 × Pi 5 4 GB (or buy 1 × 8 GB now), and order microSD cards and power supplies. Otherwise start the procurement request this week. *Minimum option:* unit 1 + servos now, unit 2 after the 28 Oct results. We recommend ordering both now: the kits are useful for DC5/DC7 research either way, and ordering both takes the order over USD 400, so it ships by courier |
| Late Oct | Kits arrive. Assemble unit 1. **28 Oct results:** if selected, order the mic, router, switch-box parts and pen material |
| **Nov: prototype** | 4 Nov workshop. Pi 5 4 GB boards arrive around 13 Nov. **Gate by 30 Nov:** (1) stable 640×480 MJPEG to the laptop over the 5 GHz router; (2) close-talk mic works as USB audio on the Pi, and HAT mic capture works while servos move; (3) 6-h run on tethered power, and battery runtime with Pi 5 against Pi 4 (sets the spare-pack count and charger choice); (4) EYES/EARS off verifiably stops camera, mic and sound-direction capture on the Pi, the HAT mic stays closed, the hardware mic mute works, and the LEDs follow the real capture state; (5) no crash in 6 h of gestures |
| **Dec: hardware freeze** | Gate result by 30 Nov. If PiDog fails, order XGO-lite3 on 1 Dec (China shipping + customs); the freeze then moves to mid-January, before Chinese New Year shipping stops. Otherwise: assemble and image unit 2, print the shutter, bone grip and pen parts, order any remaining spares. Hardware frozen by mid-December |
| Jan | Integrate the software on the final hardware. Benchmark the whole pipeline running at once (perception, imagination, TTS, UI) on the stand laptop, and fix which laptop goes to Brussels. Produce signage. Test the printer. Confirm sockets and battery rules with the organisers. Book transport |
| **Feb: rehearsal** | Full 15-min group-module rehearsals with a class-sized group. Acceptance test against recorded 80 dB babble. 5-minute robot swap drill. Repeat the 6-h endurance run. Pack list |
| 16 Mar 2027 | Set-up in Brussels. Fair 17-19 Mar |

---

## 6. Safety at the booth

Sources: research/10 §5.2, research/09, research/02 §6-7.

**Pen and table height**
- The robot stands inside a clear acrylic pen, 10-15 cm high with rounded edges. Keep at least 15 cm between the fence and the robot's reach, and keep the robot at least 40 cm from the table edge (research/10 §5.2).
- The PiDog camera is only ~15-20 cm above its feet. research/02 §6 suggests a platform at ~70-90 cm. If the fair's "low long table" is lower, a pedestal on it raises the robot, and the pen sits on the pedestal top.
- Geometry check: 40 cm on every side plus the robot (about 24 × 14 cm per an unverified secondary source, research/02 §8) needs a surface about 1 m deep. If the table or pedestal top is shallower, the 40 cm rule must hold at least at the visitor-facing edge. The fair table's height and depth are to confirm: **measure the table first**, then build the pedestal.
- The pedestal must be fixed to the table or weighted against tipping, with a non-slip mat under the robot.
- The booth sketch (`docs/assets/booth_sketch.png`, source `booth_sketch.svg`) is schematic: it draws the table about 0.5 m deep and the pen about 0.6 × 0.34 m, which does not meet these distances. Update it once the table is measured.
- Check the framing with a 7-year-old and an 18-year-old in rehearsal.
- The volunteer stands on the mat in front of the table, out of reach of the legs.

**No walking among children**
- The robot never walks during sessions. It only gestures: sit, stand, head turn and tilt, tail, paw lift, light bar.
- It stays still while listening. This reduces servo noise and avoids the crash in issue #10.
- Relax the servos (robot lying down) at every group changeover, and give it a 2-3 min nap every ~20 min of activity. Check servo temperature at battery swaps.

**Pinch points and handling**
- The leg joints are pinch points. Small screws and hot servos are further hazards.
- Visitors interact only through the bone mic, the switches and the screen.
- Staff handle the robot only when it is powered down or resting.
- A sign says "I'm a machine, please don't touch my legs".
- One staff member is always next to the robot. In earlier studies, children left alone with public robots sometimes mistreated them.
- **E-stop:** a big red button on the staff side that relaxes all servos and freezes the UI.
  - Never put it within visitors' reach: museum visitors like pressing e-stops.
  - Test it at every set-up.
  - The visitor box has FORGET ME only. The booth sketch label "STOP / forget me" should be updated to match.

**LiPo / 18650 handling**
- Never charge unattended.
- Charge spare packs in a fire-safe bag on a non-combustible surface, on the staff side, never in the public area. Use an external charger or the spare robot (§4, row 18). The only exception is the installed pack while tethered (below), which needs the organisers' OK.
- Do not use swollen or damaged packs.
- Store packs at 20-80% charge (about 50% for long-term storage). Unplug them when full.
- Swap a pack before it runs low.
- Venue battery and fire rules are to confirm.

**Tethered power**
- Preferred setup: a USB-C supply into Robot HAT V5, so the robot runs all day without swaps. One review ran it while charging ([review][rees]). Whether that keeps up with the drain is unverified; the November gate will measure it.
- Tethering charges the installed pack in the pen, on the visitor-facing table. Ask the organisers whether that is acceptable. The alternative is a regulated supply into the HAT's 6.0-8.4 V input in place of the pack (to confirm and test).
- Tape down all cables. Put the mic receiver and any bone cable on a strain-relief hook. No cable crosses the visitor side.
- Wipe the bone between classes.

**Electrical and network**
- Use our own power strip.
- Use an isolated router, with vendor cloud services and Bluetooth disabled.
- Change all default credentials, and use a firewall that only lets the robot talk to the laptop.

---

## To confirm

- Is the USD ~600 robot budget a list-price or a landed (incl. VAT) figure?
- SunFounder shipping cost to Poland, and customs clearance time.
- Customs duty rate for the kits (CN classification).
- Spare Robot HAT V5 and spare PiDog battery pack: availability and price. An external 2S charger that fits the PiDog pack connector, and its price.
- Whether the V2 kit still ships the 3-mic sound-direction module. The product text only says "sound" sensor.
- Close-talk mic: whether the DJI Mic Mini works as USB audio on the Pi 5, and which hardware mute it offers. Price of the RØDE Wireless GO Gen 3.
- Whether the HAT V5 mic can be disabled at driver level while keeping the speaker.
- EU prices for the QL-800 and SELPHY printers and their media.
- Whether SUT can lend a laptop with an NVIDIA GPU (optional, faster imagination) or a second laptop as a cold spare. Laptop prices only matter if one must be bought.
- Pi 4 4 GB price and availability, as the fallback node.
- Height and depth of the fair's table. Number of power sockets. Venue rules for batteries (including tethered charging in the pen) and robots.
- Whether TUAI or SUT funds can pay for the hardware, the SUT procurement route (direct online purchase, or an EU distributor with a VAT invoice) and its lead time.
- Chinese New Year 2027 shipping shutdown dates.

[nbpeur]: https://api.nbp.pl/api/exchangerates/rates/a/eur/?format=json
[nbpusd]: https://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json
[sf]: https://www.sunfounder.com/products/sunfounder-pidog-robot-dog-kit-for-raspberry-pi
[sfs]: https://www.sunfounder.com/products/sunfounder-metal-gear-pro-servo-for-sunfounder-new-pidog
[hat]: https://docs.sunfounder.com/projects/robot-hat-v4/en/latest/robot_hat_v5/hardware_introduction.html
[vilib]: https://docs.sunfounder.com/projects/vilib-rpi/en/latest/py_display.html
[pdcam]: https://docs.sunfounder.com/projects/pidog/en/latest/_shared/component/cpn_camera_module.html
[sdir]: https://docs.sunfounder.com/projects/pidog/en/latest/hardware/cpn_sound_direction.html
[rpimag]: https://magazine.raspberrypi.com/articles/pidog-robot-review
[rees]: https://ctrl-alt-rees.com/2024-03-08-i-built-a-robot-dog-to-guard-my-studio-sunfounder-pidog-review.html
[rtips]: https://raspberrytips.com/sunfounder-pidog-review/
[gh10]: https://github.com/sunfounder/pidog/issues/10
[gh11]: https://github.com/sunfounder/pidog/issues/11
[bl4]: https://botland.com.pl/moduly-i-zestawy-raspberry-pi-5/23904-raspberry-pi-5-4gb-5056561803319.html
[bl8]: https://botland.com.pl/moduly-i-zestawy-raspberry-pi-5/23905-raspberry-pi-5-8gb-5056561803326.html
[rpicam]: https://www.raspberrypi.com/documentation/computers/camera_software.html
[xgo]: https://shop.xgorobot.com/products/xgo-3-world-s-first-raspberry-pi-robotic-dog-with-an-arm
[xgoai]: https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x4a000tjilgmmiah2n5
[xgocloud]: https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x44000pjilgg7vqibqq
[elf]: https://shop.elecfreaks.com/collections/xgo-robot-dog
[dz]: https://category.yahboom.net/products/dogzilla-lite
[dzaudio]: https://www.yahboom.net/public/upload/upload-html/1748594287/2.%20Record%20Audio.html
[pp]: https://www.hiwonder.com/products/puppypi
[ppv]: https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/28.ROS2_AI_Voice_Interaction_Courses.html
[mp2]: https://mangdang.store/products/mp2
[mp2d]: https://minipupperdocs.readthedocs.io/en/latest/guide/QuickStartGuide.html
[fn]: https://store.freenove.com/products/fnk0050
[fnd]: https://docs.freenove.com/projects/fnk0050/en/latest/fnk0050/codes/tutorial/4_Robot_Dog.html
[bx]: https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled
[pvoice]: https://docs.petoi.com/extensible-modules/voice-command-module
[md]: https://www.hiwonder.com/products/mechdog
[mdw]: https://wiki.hiwonder.com/projects/MechDog/en/latest/docs/1.Getting_Ready.html
[go2]: https://shop.unitree.com/products/unitree-go2
[go2r]: https://www.reichelt.com/de/en/shop/product/unitree_go2_air_-_the_robot_dog-363565
[go2d]: https://www.docs.quadruped.de/projects/go2/html/Overview_1.html
[dji]: https://store.dji.com/product/dji-mic-mini
[rode]: https://rode.com/en/microphones/wireless/wireless-go-gen-3
[q2u]: https://www.bestbuy.com/site/samson-q2u-dynamic-usb-microphone/6361715.p?skuId=6361715
[ada]: https://www.adafruit.com/product/1185
[ql]: https://www.brother-usa.com/p/thermal-printers-labelers/QL800
[selphy]: https://pricehistory.app/p/canon-selphy-cp1500-wireless-compact-photo-printer-535rzy2h
[selphym]: https://cam.start.canon/en/P001/manual/html/UG-07_Reference_0070.html
[kp]: https://www.usa.canon.com/shop/p/kp-108in-color-ink-paper-set
[eu3]: https://trade.ec.europa.eu/access-to-markets/en/news/eu-applies-eu3-customs-duty-item-low-value-e-commerce-consignments
[iata]: https://www.iata.org/contentassets/6fea26dd84d24b26a7a1fd5788561d6e/passengers_travelling_with_lithium_batteries.pdf
