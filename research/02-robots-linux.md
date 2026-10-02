# 02 — Linux/SBC robot dogs at or below ~USD 600 (Raspberry Pi / CM4 / CM5 class)

*Research track for the "How does a robot see you?" demonstrator (TUAI DC5/DC7, Science is Wonderful! 2027). Date context: 2026-10-01.*

**How this was researched.** Live prices come from each vendor's official store. For SunFounder, Freenove, Hiwonder, MangDang, Yahboom, Luwu/XGO and Petoi, I read the Shopify `products.json` / `product.js` feeds on 2026-10-01. These are the same data the store page renders, so they are a primary source. Specs come from official docs and wikis, GitHub (repo activity read from the GitHub API on 2026-10-01) and a few independent reviews. FX: NBP table A, 2026-10-01: 1 EUR = 4.3770 PLN, 1 USD = 3.8762 PLN, so **1 USD ≈ 0.886 EUR** ([NBP EUR](https://api.nbp.pl/api/exchangerates/rates/a/eur/?format=json), [NBP USD](https://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json)). Polish VAT is 23% ([Your Europe](https://europa.eu/youreurope/business/taxation/vat/vat-rules-rates/index_en.htm)). Gaps:
- The session's web-search quota ran out partway through. Amazon and AliExpress block automated fetches.
- Marketplace-only newcomers (Kickstarter/AliExpress) could therefore not be swept systematically. See "Unverified".
- ESP32 dogs (Petoi Bittle X, Hiwonder MechDog) and Unitree are covered in `03-robots-other.md`. Here they appear only for contrast.

---

## 0. Bottom line

1. **Best fit: SunFounder PiDog (V2, current production) + Raspberry Pi 5 (4 GB) or Pi 4.**
   - **Cost:** USD 179.99 for the kit, Pi not included ([SunFounder](https://www.sunfounder.com/products/sunfounder-pidog-robot-dog-kit-for-raspberry-pi)). Realistic total per unit with Pi, SD card, spares and import VAT is about **€360–420 (≈ USD 410–475)**. Two units (one hot spare) still cost less than one XGO, PuppyPi or Mini Pupper.
   - **Sensors (the most distinct, explainable set of any robot here):**
     - 5 MP camera
     - MEMS microphone on the Robot HAT V5
     - 3-mic **sound-direction** sensor (direction only)
     - ultrasonic distance sensor
     - dual touch sensor
     - 6-DOF IMU
     - RGB light bar and speaker
     - very "dog-like" body (wagging tail, 3-DOF head)
   - **Raw access:** camera frames are already served as MJPEG at `http://<pi>:9000/mjpg` ([vilib docs](https://docs.sunfounder.com/projects/vilib-rpi/en/latest/py_display.html)). Raw audio comes through ALSA.
   - **Cost to us:** we must assemble it (4–6 h) and accept hobby-grade servos and electronics. There are open reports of Robot HAT V5 PWM channels failing within months [corrected by verifier: the first PWM channel failed "just a couple of days" after purchase and a second one later; issue opened 2026-02-09, still open with no vendor reply] ([GitHub #11](https://github.com/sunfounder/pidog/issues/11)) and of an audio/ALSA crash during stance changes ([#10](https://github.com/sunfounder/pidog/issues/10)).
2. **Best integrated (no assembly) alternative: Luwu XGO-lite3 (USD 599) or its Yahboom co-branded twin DOGZILLA-Lite (CM5 version, USD 639).**
   - **What's in the box:** CM5 compute module, 5 MP camera, dual MEMS mics, 2 W speaker, 2.0" face screen, battery and charger. Quiet servos, and a browser video stream on `:8080`.
   - **Price:** about USD 650–700 landed in Poland after 23% VAT, i.e. slightly over budget.
   - **Drawbacks:** weaker 2.3 kg·cm servos, a robot arm (pinch point), documentation mostly in Chinese (Luwu) or patchy English (Yahboom), and vendor AI that defaults to **Alibaba Cloud LLMs with long-term memory switched on** ([XGO wiki ch.4](https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x44000pjilgg7vqibqq)). We would not use the vendor AI at all.
3. **Hiwonder PuppyPi (Pi 5, ROS 2 Humble) is the most robust mechanics (coreless servos, aluminium).** Drawbacks:
   - It needs the **Advanced kit (USD 639.99 with Pi 5 2 GB)** to get a microphone.
   - Its camera is only **480p**, and the software runs inside Docker.
   - Hiwonder's demos include a **"gender recognition"** LLM app that we must strip out ([PuppyPi docs ch.34](https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/34.ROS2_AI_Large_Model_Courses.html)).
4. **Not recommended:**
   - **Freenove FNK0050:** no microphone, and servo protection forces a **1-min rest after every 3 min of motion** ([Freenove docs](https://docs.freenove.com/projects/fnk0050/en/latest/fnk0050/codes/tutorial/4_Robot_Dog.html)). Reviewers report it falling over.
   - **Mini Pupper 2:** USD 649 with no camera included, a ~30 min battery, and the vendor advises restarting the AI every 15 min.
   - **Mini Pupper 2 Pro:** the store page was removed (404 on 2026-10-01).
   - **Yahboom DOGZILLA S1/S2:** gone from Yahboom's official store, historically more than USD 600 without a Pi, and **it cannot run while charging**.
   - **XGO-Lite2/Mini2 (CM4):** discontinued.
5. **Architecture regardless of robot:** use the robot as a thin, honest sensor node.
   - The Pi streams camera, mic and low-rate sensor JSON over a **dedicated 5 GHz router**. All inference runs on the stand laptop.
   - Enforce sensor toggles **on the robot** (capture process stopped, plus a physical lens shutter), so "camera off" means no frame leaves the robot.
   - Keep the robot mostly stationary on a pedestal at child eye height. Run it tethered or rotate batteries.

---

## 1. Master comparison (verified data, 2026-10-01)

| Robot (current SKU) | Official price (USD) / ≈ EUR | What's included | Onboard computer | Camera | Microphone (raw audio?) | Other sensors | Battery / runtime | SW / ROS | Video to PC | Avail. / EU |
|---|---|---|---|---|---|---|---|---|---|---|
| **SunFounder PiDog (V2)** | **179.99 / €159** ([store](https://www.sunfounder.com/products/sunfounder-pidog-robot-dog-kit-for-raspberry-pi)) | Kit (assemble yourself), 12 servos, Robot HAT, camera, sensors, 7.4 V 2000 mAh 2×18650 pack ([review](https://ctrl-alt-rees.com/2024-03-08-i-built-a-robot-dog-to-guard-my-studio-sunfounder-pidog-review.html)). **No Pi, no SD card** | Your Pi 5/4/3B+/Zero 2W (V2 supports Pi 5) ([forum](https://forum.sunfounder.com/t/pidog-v1-vs-pi-dog-v2/3474)) | OV5647 5 MP, 65°, 1080p30/720p60/480p90, CSI ([docs](https://docs.sunfounder.com/projects/pidog/en/latest/_shared/component/cpn_camera_module.html)) | **Yes:** MEMS mic on Robot HAT V5 (I2S) ([HAT V5](https://docs.sunfounder.com/projects/robot-hat-v4/en/latest/robot_hat_v5/hardware_introduction.html)) + 3-mic sound-direction module (direction only, SPI) ([docs](https://docs.sunfounder.com/projects/pidog/en/latest/hardware/cpn_sound_direction.html)) | Ultrasonic, dual touch, 6-DOF IMU, 11-ch RGB light board, mono speaker ([docs](https://docs.sunfounder.com/projects/pidog/en/latest/)) | 2000 mAh 7.4 V; claimed 90–120 min (review); ~2 h charge ([RPi mag](https://magazine.raspberrypi.com/articles/pidog-robot-review)) | Python (`pidog`, `robot-hat`, `vilib`, GPL), app, no ROS | MJPEG `:9000/mjpg` (vilib/Flask) | In stock; ships to PL (airmail 7–14 d; DHL/UPS 3–7 d > $400) ([store](https://www.sunfounder.com/products/sunfounder-pidog-robot-dog-kit-for-raspberry-pi)) |
| **Luwu XGO-lite3** | **599 / €531** ([shop](https://shop.xgorobot.com/products/xgo-3-world-s-first-raspberry-pi-robotic-dog-with-an-arm)) | Assembled; CM5 2 GB + 32 GB microSD, ESP32 motion board, arm + gripper, battery, case, USB-C dock ([wiki](https://wiki.xgorobot.com/kb/zh-lite3/709b493f9c07456daa572a455b599ffc), [AI module](https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x4a000tjilgmmiah2n5)) | Raspberry Pi CM5 (BCM2712, 2.4 GHz) | 5 MP OV5647, CSI ([AI module](https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x4a000tjilgmmiah2n5)) | **Yes:** MEMS digital mic(s), dual per sister-model specs [verifier: the XGO AI-module wiki says "内置 MEMS 数字麦克风" (a built-in MEMS digital mic, count not stated). The Yahboom DOGZILLA-Lite page says "Dual MEMS digital microphones". Treat dual as UNVERIFIED for lite3.] ([mini2S](https://www.xgorobot.com/en/xgo2.html), [DOGZILLA-Lite](https://www.yahboom.net/public/upload/upload-html/1748594027/0.%20Introduction%20to%20DOGZILLA-Lite.html)) | IMU, 2.0" 320×240 IPS, 4 buttons, cavity speaker | 2500 mAh 2S; runtime not stated; USB-C 5 V charge ([wiki](https://wiki.xgorobot.com/kb/zh-lite3/709b493f9c07456daa572a455b599ffc)) | Luwu-OS, `xgolib` (PyPI 1.1.10, 2026-08-26), Blockly, "ROS 2 Lyrical" example ([PyPI](https://pypi.org/project/xgolib/), [site](https://www.xgorobot.com/en/xgo2.html)) | Browser stream `http://<ip>:8080` ([wiki ch.3](https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x3z000njilgpz0eeakw)) | In stock; ships internationally from China, "~10 days delay" notice (Oct 2026) |
| **Yahboom DOGZILLA-Lite** (Luwu × Yahboom) | **CM5: 639 / €566** (CM4: 619, sold out) ([store](https://category.yahboom.net/products/dogzilla-lite)) | Assembled, 15 DOF incl. arm | CM5 (or CM4) | OV5647 5 MP | **Yes:** dual MEMS mics; `xgoAudioRecord()`; `arecord` works ([docs](https://www.yahboom.net/public/upload/upload-html/1748594287/2.%20Record%20Audio.html)) | IMU, 2.0" IPS, 8 Ω 2 W speaker | 18650 2500 mAh; USB-C 5 V 1 A charge; 575 g ([docs](https://www.yahboom.net/public/upload/upload-html/1748594027/0.%20Introduction%20to%20DOGZILLA-Lite.html)) | Python/JupyterLab (`:8888`), Blockly-style | Web image-transmission mode ([docs](https://www.yahboom.net/public/upload/upload-html/1748593098/3.%20Web%20page%20image%20transmission%20control.html)) | In stock (CM5); FOB Shenzhen, free DHL/UPS > $499, duties paid by buyer ([policy](https://category.yahboom.net/policies/shipping-policy)) |
| **Hiwonder PuppyPi** | Standard Pi 5 2 GB **599.99** / 4 GB 659.99; **Advanced** (adds mic box) Pi 5 2 GB **639.99** / 4 GB 699.99; Pro Pi 5 2 GB 839.99 ([store JSON](https://www.hiwonder.com/products/puppypi)) | Assembled robot with camera, Pi, 8.4 V charger, card reader, balls, tags ([quick start](https://wiki.hiwonder.com/projects/PuppyPi/en/latest/docs/1.Quick_Start_Guide.html)) | Pi 5 (or Pi 4B) | "HD 130° wide-angle", **480P** ([store](https://www.hiwonder.com/products/puppypi)); USB, ROS topic `image_raw` ([docs ch.23](https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/23.ROS2_AI_Vision_and_Tracking_Course.html)) | Standard: **none**. Advanced: **WonderEcho Pro** USB-UAC mic + 3 W speaker (CI1302), raw `arecord` OK ([docs ch.28](https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/28.ROS2_AI_Voice_Interaction_Courses.html)) | IMU; Pro adds ultrasonic, touch, temp/humidity, dot matrix, TOF LiDAR ([quick start](https://wiki.hiwonder.com/projects/PuppyPi/en/latest/docs/1.Quick_Start_Guide.html)) | 7.4 V 2200 mAh LiPo; "up to ~60 min" ([reseller](https://thinkrobotics.com/products/puppypi-hiwonder-quadruped-robot-with-ai-vision)); 1.5 h charge | Ubuntu 22.04 + ROS 2 Humble (and 20.04 + Noetic) in **Docker** ([store](https://www.hiwonder.com/products/puppypi), [docs ch.3](https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/3.Remote_Tool_Installation_Connection.html)) | ROS topic; app FPV; VNC | In stock; free shipping > $499 |
| **MangDang Mini Pupper 2** | Pre-assembled **649** / legs pre-assembled 604 / upgrade kit + CM4 399 ([store JSON](https://mangdang.store/products/mp2)) | CM4-based robot. **Camera NOT included** ("security issues"); LiDAR STL-06P add-on $119 ([store](https://mangdang.store/products/mp2)) | Pi CM4 + ESP32 ([CNX](https://www.cnx-software.com/2022/10/19/mini-pupper-2-raspberry-pi-4-cm4-robot-dog-esp32-ros2-servo-feedback/)) | Optional (Pi Camera v2, OAK-D-Lite) | Built-in mic + speaker (I2S driver in BSP) ([CNX](https://www.cnx-software.com/2022/10/19/mini-pupper-2-raspberry-pi-4-cm4-robot-dog-esp32-ros2-servo-feedback/), [BSP](https://github.com/mangdangroboticsclub/mini_pupper_2_bsp)) | IMU, touch, 320×240 LCD face, servo position feedback | 1000 mAh, **~30 min**; runs on adapter ([docs](https://minipupperdocs.readthedocs.io/en/latest/guide/QuickStartGuide.html)) | Ubuntu 22.04 + ROS 2 Humble ([mini_pupper_ros](https://github.com/mangdangroboticsclub/mini_pupper_ros)) | ROS topics / web controller `:8080` | In stock; ships from Shenzhen, $20 intl incl. tax/clearance ([policy](https://mangdang.store/policies/shipping-policy)) |
| **Freenove Robot Dog FNK0050** | **129.99 / €115** ([store](https://store.freenove.com/products/fnk0050)) | Kit with camera; **no Pi, no 2×18650, no charger** | Your Pi 5/4/3B+ (Zero needs extra parts) | Camera included (model not stated) | **None** (buzzer only) | Ultrasonic, IMU (roll/pitch/yaw), LEDs, ADC battery monitor ([docs](https://docs.freenove.com/projects/fnk0050/en/latest/fnk0050/codes/tutorial/4_Robot_Dog.html)) | 2×18650 (user-supplied); **3 min motion → 1 min forced rest** | Python server, PyQt5 client, Android/iOS app; licence CC BY-NC-SA 3.0 | Custom TCP: video port 8001, commands port 5001 | In stock; ships from China, buyer pays VAT ([policy](https://store.freenove.com/policies/shipping-policy)) |
| Yahboom DOGZILLA S1/S2 | **Not on official store** (handle 404; not among the 253 products in `products.json`, 2026-10-01). Historic snippet: S1 $660 / S2 $730 without Pi (UNVERIFIED) | — | Pi 5 / Pi 4 | Wide-angle USB camera | S2: voice module | S2: LiDAR; 4.5 kg·cm 12-bit encoder bus servos ([docs](https://www.yahboom.net/public/upload/upload-html/1715680442/About%20servo.html)) | **Cannot be used while charging** ([docs](https://www.yahboom.net/public/upload/upload-html/1715679660/Precautions%20and%20battery%20safety.html)) | ROS 2 Humble ([docs](https://www.yahboom.net/study/DOGZILLA)) | — | Out of budget / unclear |
| Luwu XGO-Rider2 (wheel-legged, not a dog) | **549 / €486** ([shop](https://shop.xgorobot.com/)) | Assembled; CM5 2 GB | CM5 + ESP32 | OV5647 5 MP CSI | **Yes:** dual MEMS + 2 W speaker | IMU, 2.0" IPS, FOC hub motors ("near-whisper") | 1400 mAh, **~1 h**; 560 g ([site](https://www.xgorobot.com/en/rider.html)) | Luwu-OS, `xgolib` | Browser stream | In stock |
| Hiwonder MechDog / MechDog AI | 299.99–569.99 / 499.99–539.99 ([store JSON](https://www.hiwonder.com/collections/quadruped-robot)) | — | **ESP32, not Linux** | 320×240 (MechDog), 2 MP (AI module) | AI module mic (not raw) | — | 7.4 V 1500 mAh, ~60 min | Arduino/MicroPython/Scratch | ESP32-S3 Wi-Fi stream | See track 03 |
| Petoi Bittle X V2 | 319–469 ([Petoi JSON](https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled)) | — | **ESP32**; a Pi can be added over UART | None built in | Fixed voice commands only | IMU, touch | — | OpenCat | — | See track 03 |

Other 2025–2026 newcomers found on official stores:
- **Hiwonder MechDog AI** (listed 2026-08-25, ESP32-S3).
- **Petoi Chairo** (USD 339, ESP32, "supports Raspberry Pi integration", **not available**) ([Petoi JSON](https://www.petoi.com/products/robot-dog-chairo)).
- **Petoi Bittle AI Head** (USD 39, 2026-09-20). Cloud XiaoZhi backend; registration needs a phone number.
- **Luwu RIG-Puppy "Lulu"** (USD 99–109, 5-DOF desk pet, cloud LLM, ESP32-class; [shop](https://shop.xgorobot.com/)).
- **XGO-Duck** (biped, pre-sale ¥2,328, self-printed shell; [xgorobot.com](https://www.xgorobot.com/)).

None of these is a Linux quadruped at or below ~USD 600. **Hiwonder ROSPug** (Jetson Nano) costs USD 1,129.99 ([store JSON](https://www.hiwonder.com/collections/quadruped-robot)), which is out of budget.

**Raspberry Pi price context.** Memory-driven price increases happened in Dec 2025, Feb 2026, Apr 2026 and on 1 Oct 2026:
- Dec 2025: Pi 5 2 GB $55, 4 GB $70, 8 GB $95 ([RPi news](https://www.raspberrypi.com/news/1gb-raspberry-pi-5-now-available-at-45-and-memory-driven-price-rises/)).
- Feb 2026: +$10 / +$15 / +$30 for 2 / 4 / 8 GB ([RPi news](https://www.raspberrypi.com/news/more-memory-driven-price-rises/)).
- Apr 2026 [added by verifier, pass 2]: +$25 / +$50 / +$100 for 4 / 8 / 16 GB; 1 GB and 2 GB unchanged; CM5 2 GB +$12.50 ([RPi news, 2026-04-01](https://www.raspberrypi.com/news/a-new-3gb-raspberry-pi-4-for-83-75-and-more-memory-driven-price-increases/)). Adding the official increments gives Pi 5 list prices of about **4 GB $110 and 8 GB $175**. These are derived figures (the posts list deltas only). 16 GB $305 matches the product page.
- 1 Oct 2026: Pi 5 2 GB to **$77.50** ([RPi news](https://www.raspberrypi.com/news/price-increases-for-2gb-raspberry-pi-4-and-raspberry-pi-5/)). Pi 5 16 GB is $305 ([RPi](https://www.raspberrypi.com/products/raspberry-pi-5/)).
- Polish retail today (Botland, gross incl. VAT): **2 GB 385.90 PLN (≈ €88), 4 GB 514.90 PLN (≈ €118), 8 GB 839.90 PLN (≈ €192)** [corrected by verifier: the prices are confirmed, but on 2026-10-01 only the **8 GB is in stock** (24 h shipping). The **4 GB is a scheduled delivery around 2026-11-13** and the **2 GB around 2027-01-08** ("Dostawa zaplanowana"). Order the Pi early, or plan on the 8 GB or a Pi 4.] ([4 GB](https://botland.com.pl/moduly-i-zestawy-raspberry-pi-5/23904-raspberry-pi-5-4gb-5056561803319.html), [8 GB](https://botland.com.pl/moduly-i-zestawy-raspberry-pi-5/23905-raspberry-pi-5-8gb-5056561803326.html), [2 GB](https://botland.com.pl/moduly-i-zestawy-raspberry-pi-5/25346-raspberry-pi-5-2gb-5056561803302.html)).
- This is why kits bundled with a Pi (PuppyPi) climbed past USD 600.

---

## 2. Per-platform details

### 2.1 SunFounder PiDog (V2 = current production)

- **Versions.** **V1** has Robot HAT V4 and does **not** support Pi 5. **V2** (shipping since ~mid-2025) brings:
  - **Robot HAT V5** with an integrated MEMS microphone;
  - upgraded servos ("better gear meshing, lower current consumption, and greater power");
  - Pi 5 support.

  The metal frame is the same, so V1 owners can retrofit V2 servos ([SunFounder forum, Jul 2025–Feb 2026](https://forum.sunfounder.com/t/pidog-v1-vs-pi-dog-v2/3474)). The product title now lists "Raspberry Pi 5/4/3B+/Zero 2W" ([store JSON](https://www.sunfounder.com/products/sunfounder-pidog-robot-dog-kit-for-raspberry-pi)).
- **Price/stock.** USD 179.99, in stock (2026-10-01). Spare "Metal Gear Pro Servo for new PiDog": USD 9.99 each ([store](https://www.sunfounder.com/products/sunfounder-metal-gear-pro-servo-for-sunfounder-new-pidog)). Shipping to PL: registered airmail 7–14 working days for orders under $400, DHL/UPS 3–7 days for orders over $400 ([store](https://www.sunfounder.com/products/sunfounder-pidog-robot-dog-kit-for-raspberry-pi)).
- **Hardware.**
  - 12 servos: 2 per leg, 3 in the head, 1 tail ([summary of specs](https://mischianti.org/build-and-program-your-own-robot-dog-with-sunfounder-pidog/), secondary).
  - Aluminium alloy body, roughly 24 × 14 × 22.5 cm and ~0.95 kg (2.09 lb). Secondary source, UNVERIFIED.
  - Robot HAT V5 power input is 6.0–8.4 V; it charges the pack over USB-C and has a 2-LED battery gauge ([HAT V5](https://docs.sunfounder.com/projects/robot-hat-v4/en/latest/robot_hat_v5/hardware_introduction.html)).
  - Speaker: 2030 cavity speaker on I2S, enable/disable on GPIO12. [corrected by verifier: the speaker data line is I2S Audio OUT on GPIO21. Pass 2 confirmed the HAT V5 pin table also lists "Speaker Enable Switch" on GPIO12, so the original claim stands.]
  - Mic: MEMS, I2S on GPIO18/19/20. [verifier pass 2: confirmed. The HAT V5 pin table lists SCLK GPIO18, WS GPIO19, Audio IN GPIO20 and Audio OUT GPIO21. The PiDog docs say "The V2 Robot HAT integrates a microphone… enabling audio recording", and the V1 HAT V4 has none ([cpn_robot_hat](https://docs.sunfounder.com/projects/pidog/en/latest/hardware/cpn_robot_hat.html)).]
- **Sensors.**
  - Camera: OV5647, 2592×1944 stills, 1080p30 / 720p60 / 640×480 at 60/90 fps, 65° ([docs](https://docs.sunfounder.com/projects/pidog/en/latest/_shared/component/cpn_camera_module.html)).
  - Sound direction: TR16F064B, 3 mics, 360°, ~10° accuracy, 20° resolution. It outputs **only a 16-bit direction value over SPI**, no audio ([docs](https://docs.sunfounder.com/projects/pidog/en/latest/hardware/cpn_sound_direction.html)).
  - Ultrasonic, dual touch, 6-DOF IMU, 11-channel RGB light board ([docs index](https://docs.sunfounder.com/projects/pidog/en/latest/)).
- **Software.**
  - Python libraries `pidog`, `robot-hat` and `vilib`, all GPL ([pidog repo](https://github.com/sunfounder/pidog): 90★, last push 2026-09-15; robot-hat last push 2026-09-29; vilib last push 2026-07-30).
  - Vosk STT and TTS examples.
  - Ollama can run **on another LAN computer** (the docs explain "Expose to network") ([docs](https://docs.sunfounder.com/projects/pidog/en/latest/ai_interaction/python_local_chatbot.html)).
  - The product page now advertises cloud LLMs (ChatGPT/Gemini/Grok/Qwen, "OpenClaw"). We would not use these.
  - No ROS package. Not needed for us.
- **Streaming to the laptop.** The `vilib` web display serves `http://<pi-ip>:9000/mjpg` (Flask MJPEG) ([vilib docs](https://docs.sunfounder.com/projects/vilib-rpi/en/latest/py_display.html), [PiDog app doc](https://docs.sunfounder.com/projects/pidog/en/latest/python/py_12_app_control.html)). Audio: a standard ALSA capture device is available after `i2samp.sh`, so it can be streamed as raw PCM. The sound direction, ultrasonic, touch and IMU values can be published as JSON.
- **Power and runtime.**
  - Pack: 2×18650, 7.4 V, 2000 mAh; claimed 90–120 min ([ctrl-alt-rees](https://ctrl-alt-rees.com/2024-03-08-i-built-a-robot-dog-to-guard-my-studio-sunfounder-pidog-review.html)).
  - The Raspberry Pi magazine review saw high current draw when standing or moving, **crashes at low battery**, and **under-voltage with Pi 5** (V1 era) ([RPi mag](https://magazine.raspberrypi.com/articles/pidog-robot-review)). [corrected by verifier: the review tested with a **Pi 4** and states "Using a Raspberry Pi 5 is not recommended since its extra power requirements put too much of a strain on the battery power". It scored the kit 9/10. That advice predates V2/HAT V5, which officially supports Pi 5, but the battery strain is physical. Test Pi 5 against Pi 4 runtime on battery before committing.]
  - Charging while running worked in one review ([ctrl-alt-rees](https://ctrl-alt-rees.com/2024-03-08-i-built-a-robot-dog-to-guard-my-studio-sunfounder-pidog-review.html)). Whether USB-C input exceeds the drain while walking is UNVERIFIED.
- **Assembly and quality.**
  - Assembly takes about 4 h ([raspberrytips](https://raspberrytips.com/sunfounder-pidog-review/)) to 5–6 h ([RPi mag](https://magazine.raspberrypi.com/articles/pidog-robot-review)). Small screws; it is easy to strip plastic parts.
  - Servos must be zeroed during assembly, and the servo noise is clearly audible ([ctrl-alt-rees](https://ctrl-alt-rees.com/2024-03-08-i-built-a-robot-dog-to-guard-my-studio-sunfounder-pidog-review.html)).
  - It walks best on carpet ([same review](https://ctrl-alt-rees.com/2024-03-08-i-built-a-robot-dog-to-guard-my-studio-sunfounder-pidog-review.html)).
  - "Good balance (unlike the Freenove equivalent)" ([raspberrytips](https://raspberrytips.com/sunfounder-pidog-review/)).
- **Known open issues:**
  - **Robot HAT V5 PWM pins failing** on a V2 within months (two channels; no vendor answer) [corrected by verifier: the first channel failed "just a couple of days" after purchase and the second "recently"; the user worked around it by moving servos to free PWM pins] ([#11, Feb 2026](https://github.com/sunfounder/pidog/issues/11)).
  - **ALSA underrun → crash and disconnect** on sit-to-stand while moving ([#10, Jan 2026](https://github.com/sunfounder/pidog/issues/10)).
  - The "howl" sound effect is disturbing ([#13](https://github.com/sunfounder/pidog/issues)).
- **Our verdict.** It has the best sensor diversity and the most "dog" charisma per euro. Plan for spare servos, a spare HAT and two units.

### 2.2 Luwu Dynamics XGO family (CM5 generation) and Yahboom DOGZILLA-Lite

- **Lineup (2026).**
  - **XGO-lite3**: education model, 15 DOF incl. arm, CM5 2 GB.
  - **XGO-mini2S**: research model, 16 DOF incl. arm and turntable, CM5 4 GB.
  - **XGO-mini2SW**: wheel-legged.
  - **XGO-Rider2**: two-wheel-legged.
  - **Discontinued:** K210-based XGO-lite/XGO-mini, and CM4-based **XGO-lite2 / XGO-mini2** ([XGO wiki](https://wiki.xgorobot.com/kb/zh-lite3/709b493f9c07456daa572a455b599ffc)).
  - International shop: XGO-lite3 **USD 599**, XGO-Rider2 **USD 549**. Mini2S is not listed internationally ([shop JSON](https://shop.xgorobot.com/)).
- **DOGZILLA-Lite** "is a robot dog developed jointly by Luwu and Yahboom" ([Yahboom docs](https://www.yahboom.net/public/upload/upload-html/1748594027/0.%20Introduction%20to%20DOGZILLA-Lite.html)). Its specs match XGO-lite3: OV5647, dual MEMS mics, 8 Ω 2 W speaker, 2.0" 320×240 IPS, 2.3 kg·cm iron-core bus servos (0–300°), 2500 mAh 18650, USB-C 5 V 1 A, 575 g, 250×145×170 mm. In practice it is the same product with Yahboom's English JupyterLab tutorials (default password `yahboom` on `:8888`).
- **AI module (CM5 version)** ([wiki](https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x4a000tjilgmmiah2n5)):
  - Compute: CM5 Lite (BCM2712 4× A76 at 2.4 GHz); **CM5102000 (2 GB) in lite3/Rider2**, CM5104000 (4 GB) in mini2S. 32 GB microSD with XGO-OS.
  - Display and camera: 2.0" IPS 320×240; 5 MP camera on CSI.
  - Audio: MEMS digital mic, cavity speaker with amplifier.
  - Wireless: **dual-band 2.4/5 GHz 802.11ac**, BT 5.0.
  - Ports and controls: USB-C (USB 2.0, for a hub), micro-HDMI, UART, 4 programmable buttons.
- **Mechanics** ([wiki](https://wiki.xgorobot.com/kb/zh-lite3/709b493f9c07456daa572a455b599ffc)): lite3 has 2.3 kg·cm iron-core servos with potentiometer feedback, aluminium + ABS body, silicone legs, **610 g**, 2500 mAh 2S, USB-C charging. The vendor says it is "extremely quiet" and supports hand-guided teaching. Mini2S has 4.5 kg·cm coreless servos with magnetic encoders (0.01°), 915 g, 3800 mAh, 8.4 V 4 A DC charger.
- **Software.**
  - `xgolib` on PyPI: v1.1.10, 2026-08-26 ([PyPI](https://pypi.org/project/xgolib/)).
  - Picamera2 + OpenCV examples, and a "Luwu ROS v0.1" image with **ROS 2 Lyrical** + cv_bridge ([xgo2 page](https://www.xgorobot.com/en/xgo2.html)).
  - Code moved from `Xgorobot` (archived) to [github.com/luwudynamics](https://github.com/luwudynamics) (`xgo_doglib` 53★, `luwu_os` Apache-2.0) ([Xgorobot](https://github.com/Xgorobot)).
  - Browser streaming and control on `:8080` ([wiki ch.3](https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x3z000njilgpz0eeakw)).
- **Vendor AI (do not use at the exhibition)** ([wiki ch.4](https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x44000pjilgg7vqibqq)):
  - Wake word "Hi Luka". Everything runs on **cloud LLMs (Alibaba Cloud Bailian API key)**.
  - **Long-term memory ON by default** ("summarises your preferences… remembers your name"), web search ON by default.
  - Vision Q&A sends camera snapshots to a cloud VLM. Rider2 also advertises "emotion detection" ([Rider2](https://www.xgorobot.com/en/rider.html)).
- **Operational notes.**
  - **Never power on while hand-held:** the IMU calibrates at boot and a moving robot can oscillate uncontrollably.
  - Charge with the robot **off**. Full charge takes 1.5–2 h ([wiki](https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x3c0005jilge3has3o5)).
  - DOGZILLA-Lite: the CM5 cooling fan degrades wake-word and voice pickup; Yahboom provides a fan-noise profile step ([CM5 notes](https://www.yahboom.net/public/upload/upload-html/1762938124/CM5%20Version%20Notes%20%28Must%20Read%29.html)).
  - The preset actions include a "pee" trick. Check it is acceptable for school groups.
- **Our verdict.** It is the best "no assembly, everything included" option. It is small (~17 cm tall), so it needs a pedestal. The arm adds a pinch hazard; keep it folded and disable it in software. Landed price is roughly €650–700.

### 2.3 Hiwonder PuppyPi (Raspberry Pi 5)

- **Prices (Hiwonder store, 2026-10-01).**
  - Standard: Pi 4B 4 GB $589.99 / Pi 5 2 GB **$599.99** / 4 GB $659.99 / 8 GB $759.99 / 16 GB $879.99.
  - Advanced: +$40 (Pi 5 2 GB **$639.99**). [verifier pass 2: the cheapest Advanced variant is the **Pi 4B 4 GB at $629.99**. The others are Pi 5 4 GB $699.99, 8 GB $799.99 and 16 GB $919.99, all in stock on 2026-10-02 ([product .js](https://www.hiwonder.com/products/puppypi.js)).]
  - Pro: Pi 5 2 GB $839.99.
  - Pro Ultimate: Pi 5 2 GB $899.99 – 16 GB $1,179.99.
  - All in stock ([store JSON](https://www.hiwonder.com/products/puppypi)).
- **What each kit adds.** Advanced adds the WonderEcho Pro voice box. Pro adds a wireless handle, ultrasonic, temp/humidity sensor, touch sensor, dot-matrix display and TOF LiDAR. Ultimate adds an arm ([quick start](https://wiki.hiwonder.com/projects/PuppyPi/en/latest/docs/1.Quick_Start_Guide.html)). Older-generation owners can buy a "PuppyPi Upgrade Pack" for $99.99 ([store](https://www.hiwonder.com/products/ai-upgrade-pack)).
- **Hardware** ([store](https://www.hiwonder.com/products/puppypi)):
  - 8 DOF with HPS-0618SG coreless servos (stainless gears; 8 kg·cm per a [reseller](https://thinkrobotics.com/products/puppypi-hiwonder-quadruped-robot-with-ai-vision)).
  - Aluminium body, 226×149×190 mm, **720 g**.
  - 7.4 V 2200 mAh LiPo, charged in ~1.5 h with an 8.4 V DC charger. A voltage display is on the back; recharge below 6.8 V ([quick start](https://wiki.hiwonder.com/projects/PuppyPi/en/latest/docs/1.Quick_Start_Guide.html)).
  - Camera: "HD 130° wide angle", **480P**. Hiwonder's own 130° USB camera is a GC0308 640×480 ([camera page](https://www.hiwonder.com/products/hd-wide-angle-camera)), so a 0.3 MP sensor is likely (inference).
- **Audio.** WonderEcho Pro is a USB UAC sound card with a noise-cancelling mic and a 3 W speaker (CI1302 offline wake-word chip). `arecord` / `aplay` work, so raw audio is available ([docs ch.28](https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/28.ROS2_AI_Voice_Interaction_Courses.html)).
- **Software.**
  - Ubuntu 22.04 + ROS 2 Humble (Pi 5) or 20.04 + Noetic. All code lives in a **Docker container**. Access is over VNC (user `pi` / `raspberrypi`).
  - The default network is an **AP hotspot; the PC Wi-Fi must support 5 GHz** ([docs ch.3](https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/3.Remote_Tool_Installation_Connection.html)).
  - The camera publishes on the ROS topic `image_raw` ([docs ch.23](https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/23.ROS2_AI_Vision_and_Tracking_Course.html)).
  - GitHub [Hiwonder/PuppyPi](https://github.com/Hiwonder/PuppyPi): 17★, last push 2025-11-24, **no licence declared**.
- **Vendor AI.**
  - The LLM courses use OpenAI / OpenRouter cloud keys.
  - They include **"Embodied AI Applications in Gender Recognition"** (`vllm_gender_identification.py`) and a "watchdog" app ([docs ch.34](https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/34.ROS2_AI_Large_Model_Courses.html)). [verifier: confirmed as section 34.7 in the docs table of contents ([index](https://docs.hiwonder.com/projects/PuppyPi/en/latest/)), alongside 34.6 Robotic Watchdog. The filename `vllm_gender_identification.py` was not visible on the ch.34 landing page and is UNVERIFIED.]
  - These conflict with our "no sensitive attributes" rule and must not be deployed.
- **Our verdict.** Robust mechanics and real ROS 2, but a weak camera and only ~60 min of battery. It costs more than USD 600 once a mic is included, and Docker/VNC adds friction. Choose it only if ROS 2 is a hard scientific requirement.

### 2.4 MangDang Mini Pupper 2 / 2 Pro

- **Store (2026-10-01).** Pre-assembled **$649**; legs pre-assembled $604; upgrade kit + CM4102000 $399 ([store JSON](https://mangdang.store/products/mp2)).
  - **Camera not included** "for potential security issues"; Pi Camera v2 recommended.
  - LiDAR STL-06P $119. The controller is not included, and Bluetooth gamepads are unstable on CM4, so use the web controller ([store page](https://mangdang.store/products/mp2)).
  - Shipping: from Shenzhen, **$20 international, "includes tax fee and clearance fee"** ([policy](https://mangdang.store/policies/shipping-policy)).
- **Mini Pupper 2 Pro.** The product URL returned **404 on 2026-10-01**. Earlier search snippets showed a "Pro Maker Kit" at $799, sold out. Treat it as unavailable.
- **Specs.**
  - Compute and body: CM4 + ESP32; 12 DOF custom servos with position feedback (the Pro added velocity/torque feedback); IMU; touch; 320×240 LCD face; built-in mic + speaker; 450 g; 210×110×140 mm (CM4) ([CNX](https://www.cnx-software.com/2022/10/19/mini-pupper-2-raspberry-pi-4-cm4-robot-dog-esp32-ros2-servo-feedback/)).
  - Battery: 1000 mAh, "runs continuously for about 30 minutes"; 5 V/1 A charge, 80% in 1 h.
  - **External supply above 8.4 V will "fry all your servos".**
  - "AI function can work continuously for about 20 minutes", with a manual restart recommended every 15 min ([quick start](https://minipupperdocs.readthedocs.io/en/latest/guide/QuickStartGuide.html)).
- **Software.** Ubuntu 22.04 + ROS 2 Humble image ([mini_pupper_ros](https://github.com/mangdangroboticsclub/mini_pupper_ros): 186★, last push 2026-08-15, Apache-2.0); BSP 14★ ([bsp](https://github.com/mangdangroboticsclub/mini_pupper_2_bsp)).
- **Our verdict.** Good ROS 2 teaching robot with a cute LCD face, but over budget once a camera is added. Short runtime and stability caveats.

### 2.5 Freenove Robot Dog Kit (FNK0050)

- **Price.** $129.99, in stock ([store](https://store.freenove.com/products/fnk0050)). It needs a Pi, 2×18650 cells and a charger.
- **Hardware.** PCA9685 servo driver; ADC for battery voltage; camera, ultrasonic, IMU, LEDs and a buzzer ([docs ch.1](https://docs.freenove.com/projects/fnk0050/en/latest/fnk0050/codes/tutorial/1_Install_Python_Libraries.html), [ch.4](https://docs.freenove.com/projects/fnk0050/en/latest/fnk0050/codes/tutorial/4_Robot_Dog.html)). **No microphone.**
- **Software.** TCP server on the Pi: video on port 8001, commands on port 5001. Face recognition runs on the PC client ([ch.4](https://docs.freenove.com/projects/fnk0050/en/latest/fnk0050/codes/tutorial/4_Robot_Dog.html)). Licence CC BY-NC-SA 3.0; 145★, last push 2026-04-29, 22 open issues ([GitHub](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi)).
- **Show-stoppers for an all-day exhibition:**
  - "When the robot dog moves for 3 minutes… the robot will get into relax mode for 1 minute" ([ch.4](https://docs.freenove.com/projects/fnk0050/en/latest/fnk0050/codes/tutorial/4_Robot_Dog.html)).
  - It needs regular recalibration, a leg failed after days in one review, and USB-C charging is unreliable ([raspberrytips](https://raspberrytips.com/freenove-robot-dog-review/)).
  - It "fell over every few steps" in the comparison review ([raspberrytips PiDog](https://raspberrytips.com/sunfounder-pidog-review/)).

### 2.6 Yahboom DOGZILLA S1/S2 (and Rider-Pi)

- **Status.** S1/S2 are **no longer listed** on Yahboom's official store (2026-10-01), although the docs remain ([docs](https://www.yahboom.net/study/DOGZILLA)).
- **Hardware.** Coreless bus servos, 4.5 kg·cm, 12-bit magnetic encoder, 0–360° ([servo doc](https://www.yahboom.net/public/upload/upload-html/1715680442/About%20servo.html)).
- **Critical limitation.** "Plugging in the charger will force the output to turn off… the robot dog cannot be used at this time." Default credentials `pi/yahboom`, hotspot `DOGZILLA_WIFI/12345678` ([precautions](https://www.yahboom.net/public/upload/upload-html/1715679660/Precautions%20and%20battery%20safety.html)).
- **Rider-Pi** (CM5, $519) is Yahboom's wheel-legged robot ([store JSON](https://category.yahboom.net/products/rider-pi)). It appears to be the Rider-class platform also sold by Luwu (inference, UNVERIFIED).

### 2.7 Non-Linux contrast (details in track 03)

Hiwonder MechDog / MechDog AI (ESP32 / ESP32-S3; MechDog camera 320×240; MechDog AI has a 2 MP WonderLLM module with cloud LLMs) ([store JSON](https://www.hiwonder.com/collections/quadruped-robot)) and Petoi Bittle X V2 (ESP32; a Pi can be added over UART) ([Petoi](https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled)) give **no raw camera + raw mic path** without add-ons. Not recommended for this track.

---

## 3. What the robot provides vs. what we add vs. what runs on the laptop

| | PiDog V2 | XGO-lite3 / DOGZILLA-Lite CM5 | PuppyPi Advanced (Pi 5) | Mini Pupper 2 |
|---|---|---|---|---|
| **Robot provides** | Body, 12 servos, camera, mic (HAT V5), sound direction, ultrasonic, touch, IMU, RGB bar, speaker, battery | Everything incl. CM5, camera, mics, speaker, screen, IMU, battery, charger; arm | Pi 5, camera (480p), USB mic/speaker box, IMU, battery, charger | CM4, mic, speaker, LCD, IMU, touch, battery |
| **We must add** | Pi 5 4 GB (or Pi 4), microSD, bench PSU, spare servos (and ideally a spare HAT), optional USB mic array, physical lens shutter | Pedestal/arena, lens shutter, optional USB mic array (via USB-C hub) | Lens shutter; better camera optional; Pro sensors if wanted (+$200) | **Camera** (Pi Cam v2), possibly LiDAR |
| **Runs on robot (our code)** | Capture → stream (MJPEG/PCM/JSON), sensor-permission enforcement, motion primitives (`pidog`), LEDs/sounds | Same, using `xgolib` + Picamera2; replace vendor AI app | ROS 2 nodes in Docker, or bypass ROS with plain Python | ROS 2 / Python |
| **Runs on stand laptop** | All perception (face/pose detection, VAD/ASR, etc.), fusion, uncertainty, XAI UI, behaviour choice | Same | Same (ROS 2 DDS over Wi-Fi or a bridge) | Same |

The Intel Core Ultra 7 255U laptop needs no NVIDIA GPU for this split. The robot only encodes and streams. (Model choice and benchmarks belong to the other tracks.)

---

## 4. Total realistic cost per option (per unit, delivered to Poland)

Assumptions:
- USD→EUR 0.886 (NBP).
- Non-EU shipments: +23% import VAT on the goods. Customs duty and broker fees are not included (UNVERIFIED rates). [verifier pass 2: the EU's €150 customs-duty exemption ended on 1 July 2026. Council Regulation (EU) 2026/382 replaces it with a flat €3 per item (per CN line) on consignments of €150 or less, valid until 1 July 2028 ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ%3AL_202600382), [EC Access2Markets](https://trade.ec.europa.eu/access-to-markets/en/news/eu-applies-eu3-customs-duty-item-low-value-e-commerce-consignments)). Every robot here is above €150 (PiDog $179.99 ≈ €159), so normal TARIC duty applies plus import VAT and carrier clearance fees. That duty is 0–4.7% for toys under CN 9503, depending on classification (UNVERIFIED for these kits). Budget roughly +5% on top of VAT.]
- The Pi is bought in Poland with VAT included (Botland).
- Accessory prices marked "~" are typical retail estimates (UNVERIFIED).

| Option | Robot | Pi / compute | Battery / charger | Mic / camera extras | Spares (recommended) | **Est. total per unit** |
|---|---|---|---|---|---|---|
| **PiDog V2 + Pi 5 4 GB** | $179.99 → €159 (+VAT ≈ €196) | €118 (514.90 PLN) | Included (USB-C charging on HAT); spare pack availability UNVERIFIED | Optional ReSpeaker Lite USB 2-mic $24.90 ([Seeed](https://www.seeedstudio.com/ReSpeaker-Lite-p-5928.html)) or XVF3800 4-mic $54.90 ([Seeed](https://www.seeedstudio.com/ReSpeaker-XVF3800-USB-Mic-Array-p-6488.html)); microSD ~€10; 27 W PSU ~€13 | 4–6 servos × $9.99 (≈ €45–65 incl. VAT) | **≈ €360–420 (USD 410–475)**; 2 units ≈ €720–840 |
| PiDog V2 + Pi 5 2 GB | as above | €88 (385.90 PLN) | as above | as above | as above | ≈ €330–390 |
| **XGO-lite3** | $599 → €531 (+VAT ≈ €652) | Included (CM5 2 GB) | Included | Optional USB mic array; lens shutter | Spare mini servos $25 each ([shop](https://shop.xgorobot.com/)) | **≈ €660–720 (USD 745–810)** + shipping/duty |
| DOGZILLA-Lite CM5 | $639 → €566 (+VAT ≈ €696) | Included | Included | as above | — | ≈ €700–750 |
| PuppyPi Advanced, Pi 5 2 GB | $639.99 → €567 (+VAT ≈ €697) | Included | Included | Better camera optional (Hiwonder 160° IMX219 USB $20.99) ([store](https://www.hiwonder.com/products/hd-wide-angle-camera)) | — | ≈ €700–760 |
| Mini Pupper 2 pre-assembled | $649 + $20 shipping (vendor states tax/clearance included) → ≈ €593 | Included (CM4, implied by "pre-installed & ready to run") | Included | Pi Camera v2 ~€25 (UNVERIFIED) [corrected by verifier: MangDang's own store sells an "OV5647 Camera module" for **$8** and a "Custom Battery" for **$10** ([products.json](https://mangdang.store/products.json))] | — | ≈ €620–650 |
| Freenove + Pi 5 2 GB | $129.99 → €115 (+VAT ≈ €142) | €88 | 2×18650 + charger ~€25 (UNVERIFIED) | **USB mic required** ~€27 | — | ≈ €280–300, but **unsuitable** (duty cycle, stability, no mic) |

**Reading.** Only PiDog stays clearly under USD 600 per unit, and it is the only option where a **second unit as a hot spare** fits the budget. That matters more for robustness than any spec difference.

---

## 5. Ranking for OUR use case

Weights follow the project priorities: feasibility 0.35, robustness 0.25, educational clarity 0.20, scientific value 0.12, visual appeal 0.08. Scores 1–5 are my judgement from the evidence above.

| Rank | Platform | Feas. | Robust. | Clarity | Sci. | Visual | **Weighted** | One-line rationale |
|---|---|---|---|---|---|---|---|---|
| **1** | **SunFounder PiDog V2 + Pi 5** | 5 | 3 | 5 | 3 | 5 | **4.26** | Cheapest. It has the most distinct explainable sensors (touch, distance, sound direction, IMU, camera, mic). Raw streams are already exposed. Two units fit the budget. Hobby-grade electronics. |
| 2 | Luwu XGO-lite3 (or DOGZILLA-Lite CM5) | 4 | 4 | 4 | 3 | 4 | 3.88 | Integrated and quiet, with a face screen and no assembly. Slightly over budget after VAT, fewer non-camera sensors, cloud-first vendor software, docs mostly in Chinese (lite3). |
| 3 | Luwu XGO-Rider2 (wheel-legged, not a dog) | 4 | 3 | 4 | 3 | 4 | 3.63 | Quietest (FOC hub motors helps the mic). Self-balancing can topple when bumped, and it is not a dog. |
| 4 | Hiwonder PuppyPi Advanced (Pi 5) | 3 | 4 | 3 | 4 | 3 | 3.37 | Robust and ROS 2, but a 480p camera, more than $600, Docker friction, and problematic vendor demos. |
| 5 | MangDang Mini Pupper 2 | 3 | 3 | 3 | 4 | 4 | 3.20 | ROS 2 community and LCD eyes, but no camera included, a 30 min battery and $649. |
| 6 | Freenove FNK0050 | 3 | 2 | 3 | 2 | 3 | 2.63 | Cheap, but no mic, a 3 min/1 min duty cycle and falls. |
| — | DOGZILLA S1/S2, Mini Pupper 2 Pro, XGO-lite2/mini2 | — | — | — | — | — | n/a | Unavailable, discontinued, or over budget. |

---

## 6. Recommendations for our demonstrator

1. **Buy now (prototype):** **1× PiDog V2 + Pi 5 4 GB + 6 spare servos.** [verifier: the Pi 5 4 GB is not in stock at Botland until about 2026-11-13. Order it now, use the in-stock 8 GB (839.90 PLN), or prototype on a Pi 4. The PiDog itself ships from SunFounder's China warehouse.]
   - Build it during this month and verify three things: (a) the MJPEG stream at 640×480 to the laptop; (b) raw HAT V5 mic capture via `arecord` while servos move; (c) a whole day of runtime on battery versus on USB-C power.
   - If (b) is poor (servo noise), add a **USB mic array** (ReSpeaker Lite/XVF3800) on the robot's back. The "robot hears" story stays honest.
   - Order a **second unit** once the prototype passes. Optionally order **one XGO-lite3** as a fallback/comparison if the budget allows, but strip its cloud AI.
2. **Make the robot a thin sensor node.** On the Pi run only:
   - camera capture (Picamera2) → MJPEG/HTTP (vilib already does `:9000/mjpg`), or H.264/RTSP if latency demands;
   - mic → 16 kHz mono PCM over WebSocket/UDP;
   - ultrasonic / touch / IMU / sound direction → 10–20 Hz JSON;
   - a tiny command API for motion, LEDs and sounds.

   Everything "AI" runs on the laptop. This keeps the Pi cool, the battery alive, and the privacy story simple: frames are processed in RAM on the stand computer and never stored.
3. **Make sensor toggles real and visible.** "Camera off" must stop the capture process on the robot, and a **physical sliding lens cover** (3D-printed) gives kids a tangible signal. "Mic off" stops ALSA capture, shown by a dedicated LED colour on the RGB bar. The XAI panel can show "no data received from camera since 12:03:15". Data provenance is part of the explanation.
4. **Exploit PiDog's low-privacy sensors for XAI.** These are cheap, robust inferences children understand:
   - ultrasonic → "you are about 40 cm away";
   - sound-direction → "I heard you from the left (±10°)";
   - touch → "you patted my head";
   - IMU → "someone lifted me".

   They contrast nicely with camera/mic-based inferences and their uncertainty.
5. **Exhibition physics.**
   - Put the robot on a **pedestal or table at ~70–90 cm inside a raised-edge arena**. The PiDog/XGO camera sits only ~15–20 cm above its feet; at floor level it looks up children's noses and gets kicked.
   - Allow only short "performance" walks. Use sit, stand and head-tracking for most of the 3–5 min interaction. This reduces servo wear, noise and battery drain.
   - Run tethered (USB-C into the HAT) or rotate charged packs. Never charge unattended. LiPo/18650 packs go in a fire-safe bag between sessions.
6. **Networking.** Bring a **dedicated 5 GHz travel router** and do not rely on venue Wi-Fi. The Pi 5 and CM5 both support dual-band 802.11ac ([RPi 5](https://www.raspberrypi.com/products/raspberry-pi-5/), [XGO AI module](https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x4a000tjilgmmiah2n5)). When the robot is stationary on its pedestal, a Pi 5 can also take **Gigabit Ethernet** for zero-drop streaming.
7. **Software hygiene.**
   - Write a fresh Raspberry Pi OS image with only our services and change all default credentials (vendor images ship with `pi/yahboom`, VNC passwords, open JupyterLab, etc.).
   - Disable the vendor apps and cloud keys.
   - Firewall so the robot only talks to the stand laptop.
8. **ROS 2 is optional.** PiDog has none, and plain Python + WebSocket/ZeroMQ is more robust for a 3-day exhibition. If the researchers want ROS 2 for scientific reuse, run it on the laptop side. Ubuntu 22.04/Humble-based images (PuppyPi, Mini Pupper, DOGZILLA) are near Humble's end of life (May 2027, UNVERIFIED) [verifier pass 2: confirmed as 31 May 2027, five-year LTS ([endoflife.date](https://endoflife.date/ros-2), [ROS 2 release schedule](https://docs.ros.org/en/humble/The-ROS2-Project/Release-Schedule.html)). The exhibition runs in 2027, so it may happen on an EOL distro. That is acceptable offline, but it is another reason to keep ROS off the robot.]
9. **Procurement.** Order from official stores. PiDog orders over $400 (two units) qualify for DHL/UPS 3–7 days. Budget 23% import VAT plus possible duty and broker fees on China-shipped goods. Check whether an EU distributor (e.g. Botland, Kamami) stocks PiDog with VAT invoicing for university procurement (UNVERIFIED).

---

## 7. Pitfalls / what not to do

- **Do not run vendor "AI" stacks at the stand.** They include:
  - XGO/DOGZILLA cloud LLMs with **long-term memory on by default**;
  - Hiwonder OpenAI/OpenRouter demos and the **gender-recognition app**;
  - PiDog's ChatGPT/Gemini/Grok examples;
  - Rider2 "emotion detection".

  Inferring emotions in **education institutions** is prohibited by AI Act Art. 5(1)(f), and biometric categorisation of sensitive traits by Art. 5(1)(g) ([AI Act Art. 5](https://artificialintelligenceact.eu/article/5/), [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)). Even outside a school, these demos violate our "no sensitive attributes" design rule. [verifier: Art. 5(1)(f) and 5(1)(g) are confirmed and have applied since 2 Feb 2025. Note that 5(1)(g) lists race, political opinions, trade-union membership, religious/philosophical beliefs, sex life and sexual orientation, but **not** gender/sex as such. A gender-recognition app is therefore not per se an Art. 5 prohibition. It is still biometric categorisation: Annex III 1(b) makes it high-risk when based on sensitive or protected attributes, and Art. 50(3) imposes an information duty for emotion recognition and biometric categorisation (applies from 2 Aug 2026) ([Annex III](https://artificialintelligenceact.eu/annex/3/), [Art. 50](https://artificialintelligenceact.eu/article/50/)). Exclude it in any case.] [verifier pass 2: the letters were re-checked against the Commission's AI Act Service Desk text. 5(1)(e) is untargeted facial scraping, 5(1)(f) is emotion inference in workplace/education, and 5(1)(g) is biometric categorisation of race, political opinions, trade-union membership, religious/philosophical beliefs, sex life or sexual orientation ([AI Act Service Desk](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5)). The **Digital Omnibus on AI, Regulation (EU) 2026/1744** (signed 8 Jul 2026, in force 27 Jul 2026), moved the Annex III high-risk obligations to **2 Dec 2027** but did not move Art. 50 ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32026R1744)).]
- **Do not trust "sound sensor" to mean "microphone".** PiDog's sound-direction module returns only an angle ([docs](https://docs.sunfounder.com/projects/pidog/en/latest/hardware/cpn_sound_direction.html)). Raw audio comes from the HAT V5 MEMS mic (V2 only) or a USB mic. Buy V2 and check that the HAT says V5.
- **Do not buy PuppyPi Standard** expecting voice. The mic is only in the Advanced kit and above.
- **Do not buy Mini Pupper 2 expecting a camera.** It is not included.
- **Do not pick Freenove for all-day use.** The 3 min motion / 1 min rest limit, no mic and poor balance rule it out.
- **Do not pick DOGZILLA S1/S2.** It cannot operate while charging and is no longer on the official store.
- **Do not power on XGO/DOGZILLA-Lite while holding it**, because IMU calibration fails ([wiki](https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x3c0005jilge3has3o5)). Do not charge XGO while running.
- **Do not exceed 8.4 V** on Mini Pupper external power, or the servos die ([docs](https://minipupperdocs.readthedocs.io/en/latest/guide/QuickStartGuide.html)).
- **Do not use the onboard mic while walking** as the evidence for speech inferences. Servo and fan noise dominate (see the DOGZILLA-Lite fan-noise note, [CM5 notes](https://www.yahboom.net/public/upload/upload-html/1762938124/CM5%20Version%20Notes%20%28Must%20Read%29.html)). Use a "listening pose" where the robot is still.
- **Do not let visitors handle the robot.** Watch for leg pinch points, the XGO arm/gripper, small screws and hot servos. Do not let it walk near table edges.
- **Do not plan on a single unit.** There are open reports of HAT V5 PWM channel failures ([#11](https://github.com/sunfounder/pidog/issues/11)) and stance-change crashes ([#10](https://github.com/sunfounder/pidog/issues/10)). Carry a spare robot, spare HAT and servos, and practise a 5-minute swap.
- **Do not leave default credentials or open ports.** These include JupyterLab `:8888` (`yahboom`), VNC, the robot hotspot `12345678`, and the PuppyPi AP + VNC defaults. [verifier: the PuppyPi defaults are VNC `pi`/`raspberrypi`, AP IP 192.168.149.1 and hotspot password `hiwonder` ([docs ch.3](https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/3.Remote_Tool_Installation_Connection.html))]
- **Do not size the budget on old Raspberry Pi prices.** Pi 5 4 GB is ≈ €118 at Polish retail today, and the 2 GB went up again on 2026-10-01.

---

## 8. Unverified / open items

- PiDog V2: exact weight and size (secondary source says ~0.95 kg, 24×14×22.5 cm); real runtime with Pi 5 versus Pi 4; whether USB-C charging keeps up while idle or walking; whether the V2 kit still ships the sound-direction module (product text says "sound" sensor); availability of spare battery packs and HAT V5 as spares; any EU warehouse or DDP shipping.
- PuppyPi: camera sensor (GC0308 inferred); the "~60 min" runtime is a reseller claim; operation while charging.
- XGO-lite3: battery runtime; mic count (the AI module page says "MEMS mic"; sister models say dual); completeness of English docs; international shipping cost and duty.
- DOGZILLA S1/S2: current price and availability (historic $660 / $730 without Pi is from a search snippet).
- Mini Pupper 2: CM4 included in the "Pre-assembled Kit" (implied); the Pro is discontinued or removed (page 404).
- Raspberry Pi 5 4 GB / 8 GB official USD list price after the April 2026 increase (not published in the articles read). [verifier pass 2: derived as ≈ $110 / $175 from the official deltas; see §1.]
- Pi 5 has no hardware H.264 encoder (from memory). It matters only if we stream H.264 instead of MJPEG. [verifier pass 2: confirmed. "Raspberry Pi 5 uses software video encoders" with higher latency, though it still manages 1080p30 ([RPi camera docs](https://www.raspberrypi.com/documentation/computers/camera_software.html)). A Pi 4 has hardware H.264; on a Pi 5, prefer MJPEG.]
- ROS 2 Humble end of life in May 2027 (from memory). [verifier pass 2: confirmed, 31 May 2027.]
- Customs duty rate and HS classification for robot kits; any 2026 change to the EU €150 low-value duty exemption. [verifier pass 2: the exemption was abolished on 1 Jul 2026 (Reg. (EU) 2026/382); see §4. The exact CN code and rate are still UNVERIFIED.]
- Marketplace-only 2025–2026 newcomers on Kickstarter, AliExpress and Amazon (Amazon/AliExpress block automated access; the search quota was exhausted). Official stores of SunFounder, Freenove, Hiwonder, Yahboom, Luwu, MangDang and Petoi were fully enumerated.
- Freenove: camera model, weight and size.

---

## Sources

**SunFounder PiDog**
- Store page / product JSON (price, title, EU delivery): https://www.sunfounder.com/products/sunfounder-pidog-robot-dog-kit-for-raspberry-pi
- Spare V2 servo: https://www.sunfounder.com/products/sunfounder-metal-gear-pro-servo-for-sunfounder-new-pidog
- Forum, V1 vs V2: https://forum.sunfounder.com/t/pidog-v1-vs-pi-dog-v2/3474
- Forum, V2 + HAT V5: https://forum.sunfounder.com/t/instructions-for-updated-pidog-v2-with-robothat-v5/3676
- Docs index: https://docs.sunfounder.com/projects/pidog/en/latest/
- Robot HAT: https://docs.sunfounder.com/projects/pidog/en/latest/hardware/cpn_robot_hat.html
- Robot HAT V5 hardware: https://docs.sunfounder.com/projects/robot-hat-v4/en/latest/robot_hat_v5/hardware_introduction.html
- Sound direction sensor: https://docs.sunfounder.com/projects/pidog/en/latest/hardware/cpn_sound_direction.html
- Camera module: https://docs.sunfounder.com/projects/pidog/en/latest/_shared/component/cpn_camera_module.html
- Local LLM / Ollama on LAN: https://docs.sunfounder.com/projects/pidog/en/latest/ai_interaction/python_local_chatbot.html
- vilib web display (MJPEG :9000): https://docs.sunfounder.com/projects/vilib-rpi/en/latest/py_display.html
- App control doc: https://docs.sunfounder.com/projects/pidog/en/latest/python/py_12_app_control.html
- GitHub repos: https://github.com/sunfounder/pidog · https://github.com/sunfounder/robot-hat · https://github.com/sunfounder/vilib
- GitHub issues: https://github.com/sunfounder/pidog/issues · #10: https://github.com/sunfounder/pidog/issues/10 · #11: https://github.com/sunfounder/pidog/issues/11
- Reviews:
  - https://raspberrytips.com/sunfounder-pidog-review/
  - https://ctrl-alt-rees.com/2024-03-08-i-built-a-robot-dog-to-guard-my-studio-sunfounder-pidog-review.html
  - https://magazine.raspberrypi.com/articles/pidog-robot-review
- Secondary spec summary: https://mischianti.org/build-and-program-your-own-robot-dog-with-sunfounder-pidog/

**Freenove**
- Store / product JSON: https://store.freenove.com/products/fnk0050
- Shipping policy: https://store.freenove.com/policies/shipping-policy
- Docs ch.1: https://docs.freenove.com/projects/fnk0050/en/latest/fnk0050/codes/tutorial/1_Install_Python_Libraries.html
- Docs ch.4: https://docs.freenove.com/projects/fnk0050/en/latest/fnk0050/codes/tutorial/4_Robot_Dog.html
- GitHub: https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi (issues: https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/issues)
- Review: https://raspberrytips.com/freenove-robot-dog-review/

**Hiwonder**
- PuppyPi store / product JSON: https://www.hiwonder.com/products/puppypi
- Quadruped collection (MechDog, MechDog AI, ROSPug): https://www.hiwonder.com/collections/quadruped-robot
- Product pages:
  - AI upgrade pack: https://www.hiwonder.com/products/ai-upgrade-pack
  - Wide-angle cameras: https://www.hiwonder.com/products/hd-wide-angle-camera
  - WonderEcho: https://www.hiwonder.com/products/wonderecho
  - 6-mic array: https://www.hiwonder.com/products/far-field-microphone-array-module
  - Shipping policy: https://www.hiwonder.com/policies/shipping-policy
- PuppyPi docs: https://docs.hiwonder.com/projects/PuppyPi/en/latest/
  - Quick start: https://wiki.hiwonder.com/projects/PuppyPi/en/latest/docs/1.Quick_Start_Guide.html
  - Ch.3 Docker/VNC: https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/3.Remote_Tool_Installation_Connection.html
  - Ch.23 vision: https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/23.ROS2_AI_Vision_and_Tracking_Course.html
  - Ch.28 voice: https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/28.ROS2_AI_Voice_Interaction_Courses.html
  - Ch.34 LLM incl. gender recognition: https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/34.ROS2_AI_Large_Model_Courses.html
- GitHub: https://github.com/Hiwonder/PuppyPi
- Reseller specs: https://thinkrobotics.com/products/puppypi-hiwonder-quadruped-robot-with-ai-vision

**MangDang**
- Store / product JSON: https://mangdang.store/products/mp2 · https://mangdang.store/products.json
- Pro page (404 on 2026-10-01): https://mangdang.store/products/mini-pupper-2-pro-maker-kit-ai-quadruped-robot-educational-robot
- Shipping policy: https://mangdang.store/policies/shipping-policy
- Docs: https://minipupperdocs.readthedocs.io/en/latest/guide/QuickStartGuide.html · https://minipupperdocs.readthedocs.io/en/latest/guide/Assembly/MiniPupper2.html
- CNX: https://www.cnx-software.com/2022/10/19/mini-pupper-2-raspberry-pi-4-cm4-robot-dog-esp32-ros2-servo-feedback/
- GitHub: https://github.com/mangdangroboticsclub/mini_pupper_ros · https://github.com/mangdangroboticsclub/mini_pupper_2_bsp

**Luwu Dynamics / XGO**
- Site:
  - Home: https://www.xgorobot.com/
  - XGO-lite3: https://www.xgorobot.com/en/lite3.html
  - XGO-mini2S: https://www.xgorobot.com/en/xgo2.html
  - XGO-Rider2: https://www.xgorobot.com/en/rider.html
- Shop: https://shop.xgorobot.com/ · https://shop.xgorobot.com/products/xgo-3-world-s-first-raspberry-pi-robotic-dog-with-an-arm
- Wiki:
  - Specs / discontinued models: https://wiki.xgorobot.com/kb/zh-lite3/709b493f9c07456daa572a455b599ffc
  - AI module: https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x4a000tjilgmmiah2n5
  - Boot / charging: https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x3c0005jilge3has3o5
  - App / streaming: https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x3z000njilgpz0eeakw
  - AI chat (cloud, memory): https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x44000pjilgg7vqibqq
  - Quadruped platform: https://wiki.xgorobot.com/kb/zh-lite3/5df5e18ae5524aadbd96920abb41700c
- xgolib: https://pypi.org/project/xgolib/
- GitHub: https://github.com/luwudynamics · https://github.com/Xgorobot

**Yahboom**
- Store:
  - DOGZILLA-Lite: https://category.yahboom.net/products/dogzilla-lite
  - Rider-Pi: https://category.yahboom.net/products/rider-pi
  - Shipping policy: https://category.yahboom.net/policies/shipping-policy
  - Catalogue: https://category.yahboom.net/products.json
- DOGZILLA-Lite docs: https://www.yahboom.net/study/DOGZILLA-Lite
  - Introduction: https://www.yahboom.net/public/upload/upload-html/1748594027/0.%20Introduction%20to%20DOGZILLA-Lite.html
  - Record audio: https://www.yahboom.net/public/upload/upload-html/1748594287/2.%20Record%20Audio.html
  - Web image transmission: https://www.yahboom.net/public/upload/upload-html/1748593098/3.%20Web%20page%20image%20transmission%20control.html
  - CM5 notes: https://www.yahboom.net/public/upload/upload-html/1762938124/CM5%20Version%20Notes%20%28Must%20Read%29.html
  - Common problems: https://www.yahboom.net/public/upload/upload-html/1748594855/15.%20Analysis%20of%20common%20problems.html
- DOGZILLA S1/S2 docs: https://www.yahboom.net/study/DOGZILLA
  - Precautions: https://www.yahboom.net/public/upload/upload-html/1715679660/Precautions%20and%20battery%20safety.html
  - Servo: https://www.yahboom.net/public/upload/upload-html/1715680442/About%20servo.html

**Petoi (contrast)**
- Bittle X: https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled
- Chairo: https://www.petoi.com/products/robot-dog-chairo
- Bittle AI Head: https://www.petoi.com/products/bittle-ai-head-upgrade-kit

**Raspberry Pi, components, FX, tax, law**
- Raspberry Pi:
  - Pi 5 product page: https://www.raspberrypi.com/products/raspberry-pi-5/
  - Dec 2025 price news: https://www.raspberrypi.com/news/1gb-raspberry-pi-5-now-available-at-45-and-memory-driven-price-rises/
  - Feb 2026 price news: https://www.raspberrypi.com/news/more-memory-driven-price-rises/
  - Oct 2026 price news: https://www.raspberrypi.com/news/price-increases-for-2gb-raspberry-pi-4-and-raspberry-pi-5/
- Botland Pi 5 (PL retail):
  - 2 GB: https://botland.com.pl/moduly-i-zestawy-raspberry-pi-5/25346-raspberry-pi-5-2gb-5056561803302.html
  - 4 GB: https://botland.com.pl/moduly-i-zestawy-raspberry-pi-5/23904-raspberry-pi-5-4gb-5056561803319.html
  - 8 GB: https://botland.com.pl/moduly-i-zestawy-raspberry-pi-5/23905-raspberry-pi-5-8gb-5056561803326.html
- Seeed:
  - ReSpeaker XVF3800: https://www.seeedstudio.com/ReSpeaker-XVF3800-USB-Mic-Array-p-6488.html
  - ReSpeaker Lite: https://www.seeedstudio.com/ReSpeaker-Lite-p-5928.html
- NBP rates 2026-10-01: https://api.nbp.pl/api/exchangerates/rates/a/eur/?format=json · https://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json
- EU VAT rates (PL 23%): https://europa.eu/youreurope/business/taxation/vat/vat-rules-rates/index_en.htm
- AI Act Art. 5: https://artificialintelligenceact.eu/article/5/ · Regulation (EU) 2024/1689: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- Sibling report (ESP32 dogs, Unitree, petbots): `research/03-robots-other.md`
- Added by verifier: AI Act Annex III https://artificialintelligenceact.eu/annex/3/ · Art. 50 https://artificialintelligenceact.eu/article/50/ · MangDang catalogue https://mangdang.store/products.json · PuppyPi docs TOC https://docs.hiwonder.com/projects/PuppyPi/en/latest/

---

## Verification log

*Independent re-check by a verifier on 2026-10-01 using fresh WebFetch reads of primary sources. The web-search quota was exhausted, so only direct fetches of official pages were possible.*

| # | Claim | Verdict | Source |
|---|---|---|---|
| 1 | PiDog V2 kit costs USD 179.99, is in stock, and excludes the Pi. The title lists Pi 5/4/3B+/Zero 2W and the sensors include a microphone and a sound-direction sensor. | Confirmed | https://www.sunfounder.com/products/sunfounder-pidog-robot-dog-kit-for-raspberry-pi (.js feed + page) |
| 2 | PiDog shipping: airmail 7–14 working days under $400, DHL/UPS 3–7 days over $400. | Confirmed. All orders ship from the China warehouse; there is no EU warehouse. | same |
| 3 | Robot HAT V5 has a MEMS mic on I2S, a 2030 speaker, 6.0–8.4 V input and USB-C charging. | Confirmed. Pin detail corrected: Audio IN is GPIO20 and the speaker is on GPIO21. | https://docs.sunfounder.com/projects/robot-hat-v4/en/latest/robot_hat_v5/hardware_introduction.html |
| 4 | vilib serves MJPEG at `http://<ip>:9000/mjpg`. | Confirmed | https://docs.sunfounder.com/projects/vilib-rpi/en/latest/py_display.html |
| 5 | The sound-direction module uses a TR16F064B with 3 mics, ~10° accuracy and a 20° unit, and outputs only 16-bit direction data over SPI. | Confirmed | https://docs.sunfounder.com/projects/pidog/en/latest/hardware/cpn_sound_direction.html |
| 6 | V1 does not support Pi 5. V2 has upgraded servos and the same metal frame. | Confirmed (moderator posts, Jul 2025). The docs index says V2 has an "updated Robot HAT and servo configuration". | https://forum.sunfounder.com/t/pidog-v1-vs-pi-dog-v2/3474 ; https://docs.sunfounder.com/projects/pidog/en/latest/ |
| 7 | GitHub #11: HAT V5 PWM channels failing "within months". | Corrected. The first failure came a couple of days after purchase. Opened 2026-02-09, open, no vendor reply. | https://github.com/sunfounder/pidog/issues/11 |
| 8 | GitHub #10: an ALSA underrun crash and disconnect on sit-to-stand. | Confirmed (opened 2026-01-17, open). Recovery requires a power cycle. | https://github.com/sunfounder/pidog/issues/10 |
| 9 | Spare V2 "Metal Gear Pro" servo costs USD 9.99 each. | Confirmed | https://www.sunfounder.com/products/sunfounder-metal-gear-pro-servo-for-sunfounder-new-pidog |
| 10 | RPi magazine review: 5–6 h assembly, crashes at low battery, Pi 5 under-voltage. | Confirmed, with context added: tested on a Pi 4, says Pi 5 is "not recommended", scored 9/10. | https://magazine.raspberrypi.com/articles/pidog-robot-review |
| 11 | XGO-lite3 costs USD 599. The shop shows a ~10-day National Day shipping delay. | Confirmed | https://shop.xgorobot.com/products/xgo-3-world-s-first-raspberry-pi-robotic-dog-with-an-arm |
| 12 | XGO-lite3 specs: 610 g, 2500 mAh 2S, 2.3 kg·cm, 15 DOF. CM5102000 (2 GB) in lite3/Rider2. Dual-band 802.11ac, 32 GB microSD. lite2/mini2 (CM4) and K210 lite/mini discontinued. | Confirmed. The mic count is stated only as "MEMS digital mic", so "dual" is UNVERIFIED for lite3. | https://wiki.xgorobot.com/kb/zh-lite3/709b493f9c07456daa572a455b599ffc ; https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x4a000tjilgmmiah2n5 |
| 13 | XGO vendor AI uses Alibaba Cloud Bailian with long-term memory and web search ON by default. Wake word "Hi Luka". | Confirmed | https://wiki.xgorobot.com/kb/zh-lite3/cmsra8x44000pjilgg7vqibqq |
| 14 | XGO-Rider2: CM5 + ESP32, dual MEMS + 2 W speaker, 1400 mAh ~1 h, 560 g, "emotion detection". | Confirmed. The USD 549 price was not re-verified because shop products.json refused the connection. | https://www.xgorobot.com/en/rider.html |
| 15 | DOGZILLA-Lite: "developed jointly by Luwu and Yahboom". CM5 $639 in stock, CM4 $619 unavailable. OV5647, dual MEMS, 8 Ω 2 W, 575 g, USB-C 5 V 1 A. | Confirmed | https://category.yahboom.net/products/dogzilla-lite ; https://www.yahboom.net/public/upload/upload-html/1748594027/0.%20Introduction%20to%20DOGZILLA-Lite.html |
| 16 | DOGZILLA S1/S2 are not on the official store. | Confirmed: /products/dogzilla returns HTTP 404. | https://category.yahboom.net/products/dogzilla |
| 17 | PuppyPi prices: Std Pi5 2 GB 599.99, Adv Pi5 2 GB 639.99 / 4 GB 699.99, Pro Pi5 2 GB 839.99, Ultimate 899.99–1,179.99. All available. 480P 130° camera. | Confirmed | https://www.hiwonder.com/products/puppypi |
| 18 | PuppyPi: Docker, PC needs 5 GHz Wi-Fi. WonderEcho Pro is a USB sound card (CI1302, 3 W) and `arecord` records raw 16 kHz PCM. | Confirmed. Defaults also include hotspot password `hiwonder`. | https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/3.Remote_Tool_Installation_Connection.html ; https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/28.ROS2_AI_Voice_Interaction_Courses.html |
| 19 | The PuppyPi LLM course includes "Gender Recognition" and uses OpenAI/OpenRouter keys. | Confirmed as section 34.7 in the TOC, with OpenAI and OpenRouter key setup in 34.2. The `vllm_gender_identification.py` filename is UNVERIFIED. | https://docs.hiwonder.com/projects/PuppyPi/en/latest/ ; https://docs.hiwonder.com/projects/PuppyPi/en/latest/docs/34.ROS2_AI_Large_Model_Courses.html |
| 20 | Mini Pupper 2: $649 / $604 / $399. Camera not included "for potential security issues". LiDAR $119. ~30 min battery. AI restart every 15 min. >8.4 V fries servos. Pro not listed. | Confirmed. The Pro is absent from products.json. MangDang sells its own OV5647 camera for $8. | https://mangdang.store/products/mp2 ; https://mangdang.store/products.json ; https://minipupperdocs.readthedocs.io/en/latest/guide/QuickStartGuide.html |
| 21 | Freenove FNK0050: $129.99, excludes Pi, 18650s and charger. 3 min motion then 1 min rest. Ports 8001 (video) and 5001 (commands). CC BY-NC-SA 3.0. | Confirmed | https://store.freenove.com/products/fnk0050 ; https://docs.freenove.com/projects/fnk0050/en/latest/fnk0050/codes/tutorial/4_Robot_Dog.html ; https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi |
| 22 | Pi 5 prices: Dec 2025 $55/$70/$95. Feb 2026 +$10/+$15/+$30. 1 Oct 2026 2 GB to $77.50. 16 GB $305. | Confirmed. Posts dated 2025-12-01, 2026-02-02 and 2026-10-01; the Oct increase was +$12.50 (Pi 4 2 GB to $67.50). | raspberrypi.com news posts cited above ; https://www.raspberrypi.com/products/raspberry-pi-5/ |
| 23 | Botland prices: 2 GB 385.90, 4 GB 514.90, 8 GB 839.90 PLN gross. | Prices confirmed. Availability corrected: 4 GB arrives ~2026-11-13, 2 GB ~2027-01-08, only 8 GB in stock. | Botland URLs cited above |
| 24 | NBP 2026-10-01 rates: EUR 4.3770, USD 3.8762. | Confirmed (table 191/A/NBP/2026) | https://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json |
| 25 | AI Act Art. 5(1)(f) bans emotion inference in workplaces and education. Art. 5(1)(g) bans biometric categorisation by sensitive traits. | Confirmed (applies since 2 Feb 2025). Nuance added: gender/sex is not in the 5(1)(g) list. | https://artificialintelligenceact.eu/article/5/ |
| 26 | Hiwonder MechDog AI (ESP32-S3, listed 2026-08-25, $499.99–539.99). Petoi Chairo ($339, ESP32, unavailable). Yahboom Rider-Pi CM5 $519. | Confirmed | https://www.hiwonder.com/collections/quadruped-robot ; https://www.petoi.com/products/robot-dog-chairo ; https://category.yahboom.net/products/rider-pi |
| 27 | xgolib 1.1.10, released 2026-08-26. | Confirmed | https://pypi.org/project/xgolib/ |

**Overall:** the report is highly reliable. Nearly all prices, specs and URLs check out against primary sources. The corrections are minor:
- the timing of the PWM failures in #11;
- HAT V5 pin details;
- Pi 5 stock at Botland, which matters for procurement;
- the cheaper MangDang camera;
- the mic count on lite3;
- the legal nuance on gender recognition.

## Omissions added by verifier

1. **Pi 5 stock constraint (procurement-critical).** On 2026-10-01 Botland has the Pi 5 2 GB and 4 GB only as scheduled deliveries (4 GB ~2026-11-13, 2 GB ~2027-01-08). Only the 8 GB is in stock. Order Pis immediately, or budget the 8 GB (≈ €192) or a Pi 4.
2. **The RPi magazine reviewers (Pi 4 test) advise against a Pi 5 in PiDog on battery power.** V2 officially supports Pi 5, but runtime on battery with a Pi 5 should be benchmarked against a Pi 4. Our architecture streams only, so a Pi 4 4 GB may be sufficient and lighter on power.
3. **AI Act amendments.** artificialintelligenceact.eu now shows new Art. 5(1)(ba) (non-consensual intimate imagery) and 5(1)(bb) (CSAM) prohibitions applying from 2 Dec 2026. They are not directly relevant, but cite the consolidated text. **Art. 50(3)** applies from 2 Aug 2026: deployers must inform people exposed to emotion recognition or biometric categorisation. **Annex III 1(b)/1(c)** classes biometric categorisation by sensitive or protected attributes, and emotion recognition, as high-risk. This is another reason never to enable gender or emotion inference, even outside schools.
4. **MangDang accessories.** The official store sells an OV5647 camera module ($8), a custom battery ($10), a controller ($20) and a "Mini Pupper 2 top PCB/carry board" ($50, published 2026-10-01). No Mini Pupper 3 or 2 Pro is listed. The camera omission therefore costs only about $8, not ~€25.
5. **SunFounder ships only from China** (no EU warehouse). Budget import VAT and possible broker fees for PiDog too. The PiDog listing still dates from Dec 2023. SunFounder's robotics collection shows no new Linux quadruped for 2025–26.
6. **PuppyPi default hotspot password is `hiwonder`** (AP IP 192.168.149.1). Add it to the credential-hardening checklist.
7. Not checked because the search quota was exhausted: marketplace or Kickstarter newcomers (2025–26), and the current official USD list price of the Pi 5 4 GB after the April 2026 increase. These remain UNVERIFIED.

## Verification log — pass 2 (2026-10-02)

*A second independent verifier re-checked the claims below with fresh WebSearch/WebFetch reads of primary sources on 2026-10-02. Web search was available in this pass.*

| # | Claim | Verdict | Source |
|---|---|---|---|
| P1 | PiDog kit: USD 179.99, in stock, "RPI NOT Included", single SKU CN0537D. | Confirmed. A second listing ("PiDog AI Teaching Robots Dog", published 2026-02-25) carries the same SKU and price. Ships only from the China warehouse. | https://www.sunfounder.com/products/sunfounder-pidog-robot-dog-kit-for-raspberry-pi.js ; https://www.sunfounder.com/products/sunfounder-pidog-ai-robot-dog-kit.js |
| P2 | V2 has HAT V5 with a MEMS mic; V1 (HAT V4) has no mic and no Pi 5 support. | Confirmed: "Only the V2 Version includes a microphone". | https://docs.sunfounder.com/projects/pidog/en/latest/hardware/cpn_robot_hat.html ; https://forum.sunfounder.com/t/pidog-v1-vs-pi-dog-v2/3474 |
| P3 | HAT V5 I2S pins GPIO18/19/20, speaker enable GPIO12. | Confirmed. Pass-1 notes are softened: SCLK 18, WS 19, IN 20, OUT 21, speaker enable 12. | https://docs.sunfounder.com/projects/robot-hat-v4/en/latest/robot_hat_v5/hardware_introduction.html |
| P4 | vilib MJPEG at `http://<ip>:9000/mjpg`. | Confirmed. Resolution and fps are not documented. | https://docs.sunfounder.com/projects/vilib-rpi/en/latest/py_display.html |
| P5 | GitHub issues #10 and #11 are open with no replies. | Confirmed (0 comments each, still open on 2026-10-02). New: #16 (Jul 2026) makes **Piper TTS (local)** the default for voice examples, and #15 adds EdgeTTS (cloud). | https://api.github.com/repos/sunfounder/pidog/issues?state=all |
| P6 | Spare Metal Gear Pro servo USD 9.99. | Confirmed (SKU A0001313, in stock). | https://www.sunfounder.com/products/sunfounder-metal-gear-pro-servo-for-sunfounder-new-pidog.js |
| P7 | XGO-lite3 USD 599; XGO-Rider2 USD 549. | Confirmed, both available. Rider2 was not re-verified in pass 1; it is now confirmed. | https://shop.xgorobot.com/products.json |
| P8 | DOGZILLA-Lite CM5 $639 in stock; CM4 $619 unavailable. | Confirmed. | https://category.yahboom.net/products/dogzilla-lite.js |
| P9 | PuppyPi Advanced Pi 5 2 GB $639.99. | Confirmed. Omission corrected: an Advanced Pi 4B 4 GB variant costs $629.99. | https://www.hiwonder.com/products/puppypi.js |
| P10 | PuppyPi course includes "Gender Recognition". | Confirmed (TOC 34.7). The script filename is still UNVERIFIED. | https://docs.hiwonder.com/projects/PuppyPi/en/latest/ |
| P11 | Mini Pupper 2 $649/$604/$399; ~30 min battery; AI ~20 min, restart every 15 min; >8.4 V fries servos. | Confirmed. | https://mangdang.store/products/mp2.js ; https://minipupperdocs.readthedocs.io/en/latest/guide/QuickStartGuide.html |
| P12 | Freenove FNK0050 $129.99, no microphone. | Confirmed. | https://store.freenove.com/products/fnk0050.js |
| P13 | Pi 5 price history (Dec 2025, Feb 2026, Apr 2026, 1 Oct 2026; 16 GB $305). | Confirmed. The Apr 2026 deltas were added (+$25/+$50/+$100 for 4/8/16 GB), so 4 GB ≈ $110 and 8 GB ≈ $175 (derived). The 1 Oct post: 2 GB +$12.50 to $77.50. | https://www.raspberrypi.com/news/a-new-3gb-raspberry-pi-4-for-83-75-and-more-memory-driven-price-increases/ ; https://www.raspberrypi.com/news/more-memory-driven-price-rises/ ; https://www.raspberrypi.com/news/price-increases-for-2gb-raspberry-pi-4-and-raspberry-pi-5/ |
| P14 | Botland Pi 5 4 GB 514.90 PLN, scheduled ~2026-11-13. | Confirmed on 2026-10-02 (180 units expected). | https://botland.com.pl/moduly-i-zestawy-raspberry-pi-5/23904-raspberry-pi-5-4gb-5056561803319.html |
| P15 | AI Act Art. 5(1)(f) is emotion inference in education; 5(1)(g) is sensitive biometric categorisation. | Confirmed against the Commission Service Desk text. The Digital Omnibus (Reg. 2026/1744) defers Annex III to 2 Dec 2027; Art. 50 is unchanged. | https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5 ; https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32026R1744 |
| P16 | Pi 5 has no hardware H.264 encoder. | Confirmed: "Raspberry Pi 5 uses software video encoders." | https://www.raspberrypi.com/documentation/computers/camera_software.html |
| P17 | ROS 2 Humble EOL May 2027. | Confirmed (31 May 2027). | https://endoflife.date/ros-2 |
| P18 | EU €150 duty exemption status (listed as open). | Resolved: abolished on 1 Jul 2026 and replaced by a €3/item flat duty for consignments of €150 or less. This does not apply to these robots, which are all above €150 and pay standard duty. | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ%3AL_202600382 ; https://trade.ec.europa.eu/access-to-markets/en/news/eu-applies-eu3-customs-duty-item-low-value-e-commerce-consignments |

**Pass-2 overall:** no decision-changing errors were found. The ranking and the PiDog V2 recommendation stand. Pass 2 adds:
- the April 2026 Pi price step (a 4 GB Pi 5 now lists at about $110);
- a cheaper PuppyPi Advanced variant (Pi 4B, $629.99);
- the post-July-2026 EU customs regime;
- the AI Act Omnibus dates.

## Omissions added by verifier — pass 2

1. **Petoi Quaddle** (Kickstarter launched 2026-09-02, already funded). It is a 4-servo OpenCat desk quadruped with a "Raspberry Pi Zero socket + Arduino/ESP32", and a camera only as an optional AI-vision add-on. Prices: Builder+ $144 / Buddy $175 / Scout $215 early-bird (MSRP $179–269) ([Petoi](https://www.petoi.com/pages/quaddle-educational-robot-kit)). With 4 DOF and no integrated camera or mic it is too simple for this demo. Do not switch.
2. **XGO-mini2SW** (CM5 wheel-legged dog) ran on Kickstarter from 1 Sep to 1 Oct 2026 and raised HK$695,699 from 101 backers. The average pledge was about HK$6,888 (≈ USD 885), so it is out of budget and not yet shipping ([PledgeBox tracker](https://www.pledgebox.com/projects/xgo-mini2sw), [Kickstarter](https://www.kickstarter.com/projects/xgorobot/xgo-mini2sw)).
3. **Alternative XGO channel:** ELECFREAKS sells a "CM5 XGO-Lite Robot Dog Kit" for $619 (in stock) and a CM5 XGO-Mini for $1,299. This may help if Luwu's own shop is slow or a different invoice entity is needed ([ELECFREAKS](https://shop.elecfreaks.com/collections/xgo-robot-dog)).
4. **PiDog local TTS:** the repo switched the voice examples to **Piper TTS (offline)** by default in Jul 2026 (PR #16), with EdgeTTS (Microsoft cloud) as an option (#15). Use Piper only; keeping TTS offline fits the no-cloud privacy story ([issues](https://github.com/sunfounder/pidog/issues)).
5. **Pi 4 vs Pi 5 for streaming.** The Pi 4 has hardware H.264 encoding; the Pi 5 encodes in software with more latency ([RPi docs](https://www.raspberrypi.com/documentation/computers/camera_software.html)). The Pi 5 4 GB is also backordered at Botland and the RPi magazine review advises against a Pi 5 on PiDog battery power, so a **Pi 4 4 GB** is a serious candidate for the thin-sensor-node role. Benchmark both.
6. **EU product-compliance note.** Since 1 Aug 2025, Delegated Regulation (EU) 2022/30 has made RED Art. 3(3)(d)(e)(f) cybersecurity requirements (EN 18031) mandatory for internet-connected radio equipment placed on the EU market ([summary](https://www.schutzwerk.com/en/compliance/red/)). Vendor images with default passwords (`yahboom`, `hiwonder`, `12345678`) are exactly what EN 18031 targets. For our own non-commercial exhibit we are not "placing on the market", but this supports reflashing and hardening every unit. Check the CE/RED marking on whatever is imported (UNVERIFIED per product).
