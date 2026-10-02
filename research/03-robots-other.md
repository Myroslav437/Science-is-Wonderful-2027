# 03 — Robot dogs/pets: microcontroller-based kits, consumer petbots, external sensors, above-budget references

Research track for the "How does a robot see you?" demonstrator (TUAI DC5/DC7, Science is Wonderful! 2027).
Date context: research done 2026-10-01. Prices are list prices on the cited page as accessed 2026-10 unless stated otherwise; USD prices exclude VAT/shipping/customs unless stated. Anything not confirmed from a fetched source is marked **UNVERIFIED**.

> Method note: the web-search quota for this session ran out part-way through. Everything below was checked against fetched pages (official stores, docs, GitHub, CVE advisories) where possible. A broad CES 2026 / AliExpress newcomer sweep could not be completed; see "Unverified / open items".

---

## 0. Bottom line (one paragraph)

Within this track, the only platforms that fit **feasibility + robustness + budget (<= ~USD 600)** are the ESP32 kit dogs: **Petoi Bittle X V2** and **Hiwonder MechDog**. On their own, **neither gives clean raw camera and raw microphone streams to a PC**. Petoi's voice module only recognises fixed commands, and Petoi's AI vision module returns detection results, not video. MechDog's ESP32-S3 module does stream video over Wi-Fi, but at low resolution and with no raw-mic path. The robust design is: **use the robot dog as a body that moves and looks at people, mount a small streaming camera on its head (ESP32-S3), and put the "ears" (a USB mic array) at the stand**, with all inference running locally on the laptop. Consumer petbots (Loona, aibo, Vector) are closed or depend on a cloud service. They give little or no raw sensor access, so they are unsuitable. Unitree Go2 is over budget. Only the EDU version has an official SDK, and the Air has no voice/mic function. The Go2 also has unresolved public CVEs and is unsafe in a crowd of 8–14-year-olds (15 kg, up to 2.5 m/s). Keep it as an "above-budget reference" only.

---

## 1. Comparison table

| Platform | Price (accessed 2026-10) | Availability | SDK / programmability | Onboard compute | Camera → PC raw video? | Mic → PC raw audio? | Other sensors | Battery | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| **Petoi Bittle X V2** (lite/alloy, kit/pre-assembled) | USD 319 / 339 / 379 / 399 ([Maker Shed](https://www.makershed.com/products/petoi-robot-dog-bittle-x)); "from $319" ([Petoi](https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled)); EU €406.80 incl. VAT pre-assembled ([Robot-Advance](https://www.robot-advance.com/EN/art-petoi-bittle-x-v2-pre-assembled-dog-robot-5992.htm)) [corrected by verifier: the €406.80 Robot-Advance listing is the **Lite-servo** pre-assembled version, "available on request"; the Alloy version will cost more in the EU] | In stock (Maker Shed and Petoi Shopify catalogue both list all 6 variants as available, checked 2026-10-01) | Open source (MIT) OpenCatEsp32, C++/Arduino, Python serial API, block coding ([GitHub](https://github.com/PetoiCamp/OpenCatEsp32-Quadruped-Robot), [Python API](https://docs.petoi.com/apis/python-api)) | ESP32-WROOM-32D BiBoard ([spec](https://www.petoi.com/pages/bittle-x-robot-dog-with-arm-specifications)) | **No camera included.** Petoi AI Vision module = detection results on Bittle's serial link; the product page also advertises "WiFi image transmission (module as AP)" [corrected by verifier], resolution/fps UNVERIFIED. Add your own camera (§3) | **No.** Voice module = 40 fixed + 10 custom commands → serial codes ([docs](https://docs.petoi.com/extensible-modules/voice-command-module)) | 6-axis IMU, back touch, speaker; 4 Grove ports; optional sensor pack (PIR, IR distance, gesture, light, touch) | 7.4 V 1000 mAh, ~1 h, 1.5 h charge | **Best body in this track** (needs external camera/mic) |
| Petoi Bittle X V2 + Arm | USD 449 (kit) / 469 (pre-assembled) ([Maker Shed](https://www.makershed.com/products/petoi-robot-dog-bittle-x)) | In stock | as above | as above | as above (camera can sit on the arm) | No | + gripper | as above | Arm not needed; adds pinch points |
| Petoi Nybble Q (cat) | USD 435 (Lite) [corrected by verifier: Alloy-servo version USD 515] ([Petoi](https://www.petoi.com/products/petoi-nybble-q-robot-cat)) | In stock (some colours limited) | as Bittle X | ESP32 BiBoard | No camera | No (fixed voice cmds) | **Built-in ultrasonic**, IMU, 4 touch sensors, 11 DOF (2 head + tail) | ~1 h | Viable alternative if a cat is acceptable |
| Petoi Quaddle (Kickstarter) | Builder $99 / Buddy $139 / **Scout $199**, +$18 EU shipping ([CNX](https://www.cnx-software.com/2026/09/04/petoi-quaddle-a-mini-robot-dog-for-physical-ai-experimentation/)) | Ships **Dec 2026** (crowdfunded) | Blocks, Python, MicroPython, C++, ROS; Pi Zero can replace AI core | 2× ESP32-S3 (Buddy/Scout) | "AI vision (optional)", stream **UNVERIFIED** | 2 mics on Scout, raw-audio path **UNVERIFIED** | PIR, 2× IR distance, light, gesture, gyro | ~1 h (Scout) | Watch; too risky as sole platform |
| **Hiwonder MechDog** (Standard / Advanced / Ultimate / Pro Dev) | USD 299.99 / **369.99** / 469.99 / 569.99 ([Hiwonder](https://www.hiwonder.com/products/mechdog)) | In stock | Python/MicroPython, Arduino, Scratch | ESP32 | **Advanced+ includes ESP32-S3 vision module with Wi-Fi live video** (2 MP sensor, 320×240 stated, 123° FOV) | No (WonderEcho = CI1302 fixed command words, up to 300) | Ultrasonic (I2C, RGB), IMU; Advanced adds touch, light, MP3, dot matrix | 7.4 V 1500 mAh, up to ~60 min | **Runner-up**: camera stream included, metal frame, no head joint |
| Hiwonder MechDog AI (WonderLLM head) | USD 499.99 / 539.99 ([Hiwonder](https://www.hiwonder.com/products/mechdog-ai)); €687.55 / €735.55 at an EU reseller ([OpenELAB](https://openelab.io/products/hiwonder-mechdog-ai)) | In stock | as MechDog + WonderLLM (Arduino/MicroPython) | ESP32 body + ESP32-S3 head | Wi-Fi streaming stated | Mic streams Opus to a XiaoZhi server (cloud by default) | 2" touch LCD, IMU, 3-DOF arm | 1500 mAh | Over budget, depends on a cloud LLM by default. Not recommended |
| Unitree Go2 Air | USD 1,600 ex-tax/freight without controller, USD 1,850 with controller [verifier: confirmed on the official [Unitree shop](https://shop.unitree.com/products/unitree-go2), 2026-10-01] ([Robozaps](https://blog.robozaps.com/b/unitree-go2-review)); **€2,618 incl. VAT** ([Reichelt](https://www.reichelt.com/de/en/shop/product/unitree_go2_air_-_the_robot_dog-363565)) | In stock EU | **No official secondary development** ([QUADRUPED docs](https://www.docs.quadruped.de/projects/go2/html/Overview_1.html)); unofficial WebRTC | No 8-core CPU listed for Air | 1280×720 120° camera; video via unofficial WebRTC | **No voice function on Air**; WebRTC audio channel "Pro and EDU only" | 4D LiDAR L1, IMU | 8000 mAh, 1–2 h | Not suitable (budget, SDK, safety, security) |
| Unitree Go2 Pro | USD 2,800 ex-tax ([Antonrobots](https://antonrobots.com/unitree-go2-review/)) | In stock | No official SDK; unofficial WebRTC gives video + audio | 8-core CPU | Yes (unofficial) | Yes (unofficial, send/recv) | LiDAR, voice | 1–2 h | Reference only |
| Unitree Go2 EDU / EDU Plus | ≈ USD 11,190+ / 13,205+ (quote) ([Robozaps](https://blog.robozaps.com/b/unitree-go2-review)) | Quote | Official unitree_sdk2, Python/C++, ROS 2 | + Jetson-class module (40/100 TOPS per Robozaps) | Yes (official) | Yes | + foot force sensors | 15000 mAh, 2–4 h | Far above budget |
| Unitree Go1 (used) | eBay listings USD 2,300–2,500; ~USD 1,699 typical NOS ([Robozaps Go1](https://blog.robozaps.com/b/unitree-go1-review), [eBay](https://www.ebay.com/itm/267647870709)) | Discontinued ~mid-2023 | unitree_legged_sdk survives | — | — | — | — | spares scarce | **Avoid** (backdoor CVE-2025-2894, no spares) |
| Weilan AlphaDog / BabyAlpha A2 | AlphaDog from USD 5,670; BabyAlpha A2 DevQ USD 1,099 / regular 1,199 (Kickstarter 2024) ([Mikeshouts](https://mikeshouts.com/weilan-babyalpha-a2-intelligent-petbot-with-gpt-4o/), [Gadgetbyte](https://www.gadgetbytenepal.com/weilan-alphadog-ai-pet-unveiled/)) | Unclear outside China (**UNVERIFIED**) | "SDK" on DevQ (details **UNVERIFIED**) | — | — | Baidu voice / GPT-4o (cloud) | LiDAR, ToF, mmWave, mic array (per vendor claims) | — | Not suitable |
| KEYi Loona Petbot (wheeled) | USD 499 (from 529, July 2026) ([Robozaps](https://blog.robozaps.com/b/loona-robot-review)) | In stock | **Blockly only; promised SDK never shipped** | Quad A53 + 5 TOPS BPU | No developer access | No | 720p RGB + 3D ToF, 4-mic array ([KEYi](https://keyirobot.com/blogs/loona-tutorials/what-is-loona-petbot-a-complete-guide-to-smart-ai-robot-pet)) | — | Not suitable (closed, cloud GPT-4o) |
| Sony aibo ERS-1000 | USD 2,899.99 incl. 3 yr cloud, then USD 300/yr ([Robozaps](https://blog.robozaps.com/b/sony-aibo-review)) | **Japan sales ended June 2026**; US continues ([TechXplore](https://techxplore.com/news/2026-06-sony-discontinues-japan-sales-robot.html)); EU **UNVERIFIED** | Cloud REST "Web API" ([Sony](https://info.aibo.com/en-us/2019/11/20191115-21.html)) | — | Not documented in what we could fetch (**UNVERIFIED**) | No | 2 cameras, 4 mics, ToF, touch ([wiki](https://aibo.miraheze.org/wiki/ERS-1000)) | ~2 h | Not suitable |
| Anki/DDL Vector 2.0 (wheeled) | USD 249.99; voice needs subscription USD 11.99/mo or 99.99/yr ([anki.bot](https://anki.bot/products/vector-robot), [membership](https://anki.bot/pages/vector-membership)) | In stock (US store) | Python SDK via community wire-pod (MIT) | — | **Yes**: 640×360 feed (1280×720 high-res) via SDK | **No**: "Ability to access the Vector's audio stream to come" ([SDK source](https://github.com/kercre123/wirepod-vector-python-sdk)) | ToF, touch, IMU (**UNVERIFIED**) | — | Not a dog, no mic access, tiny. Not suitable |
| Hengbot Sirius | USD 1,299 ([Hengbot](https://www.hengbot.com/)) | Waitlist | "Secondary development" (no details) | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | — | — | Over budget, not shipping |
| DIY ESP32-S3 dog (SpotMicroESP32-Leika) | Self-built (BOM not stated) ([GitHub](https://github.com/runeharlyk/SpotMicroESP32-Leika)) | DIY | MIT, web UI, ESP32-S3 | ESP32-S3 | Optional OV2640/OV5640 | — | IMU, ultrasonic, gesture | — | Too much build risk for an exhibit |

Adjacent Raspberry-Pi-based dogs (likely covered in another track, listed for cross-checking): **SunFounder PiDog** USD 179.99 without Pi. It has a camera, ultrasonic, sound-direction sensor, microphone, speaker, 6-DOF IMU, touch and 12 metal-gear servos. The V2 supports Pi 3/4/5/Zero 2 W, and the library is GPL-2.0 ([SunFounder](https://www.sunfounder.com/products/pidog), [docs](https://docs.sunfounder.com/projects/pidog/en/latest/), [GitHub](https://github.com/sunfounder/pidog)). **Freenove Robot Dog Kit** USD 129.99 without Pi or 18650 cells. It has a camera and ultrasonic, and the code is CC BY-NC-SA ([store](https://store.freenove.com/products/fnk0050), [GitHub](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi)). **Hiwonder PuppyPi** USD 589.99–1,179.99 with Pi 4B/Pi 5, a 480p camera and ROS 1/2 ([Hiwonder](https://www.hiwonder.com/products/puppypi)). Because they run a Linux SBC onboard, these dogs give native raw camera and mic access. For our "raw sensors to the PC" requirement, **PiDog V2 + Pi 4/5 may beat every MCU dog in this report** and should be compared head-to-head with the Pi-track findings.

---

## 2. Platform details

### 2.1 Petoi Bittle X V2 / Bittle X V2+Arm (ESP32)
- **Variants and prices:** Construction-Lite $319, Pre-assembled-Lite $339, Construction-Alloy $379, Pre-assembled-Alloy $399, +Arm Construction $449, +Arm Pre-assembled $469 ([Maker Shed](https://www.makershed.com/products/petoi-robot-dog-bittle-x)). Petoi's own store shows "from $319" ([Petoi](https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled)). Educational volume pricing is quote-only ([Petoi educator guide](https://www.petoi.com/pages/educator-purchase-guide)). Spare Li-ion battery $51, sensor pack $44 ([accessories](https://www.petoi.com/collections/bittle-x-accessories)).
- **Hardware** ([spec page](https://www.petoi.com/pages/bittle-x-robot-dog-with-arm-specifications)):
  - Board: ESP32-WROOM-32D (520 KB SRAM, 16 MB flash). V2 uses BiBoard V1 ([guide](https://guide.petoi.com/product/bittle-x-v2)).
  - IMU: 6-axis MPU6050 or ICM42670.
  - Servos: 10 (9 active joints, 8 legs + 1 neck pan), alloy P1S or plastic P1L.
  - Size/weight: 190×153×107 mm, 269–353 g.
  - Battery: 7.4 V 1000 mAh Li-ion, ~1 h; USB 5 V 1 A charge in ~1.5 h.
  - Interfaces: Wi-Fi, Bluetooth, UART, I2C, 4 Grove ports; buzzer/speaker; back touch sensor ([guide](https://guide.petoi.com/product/bittle-x-v2)).
  - Payload ~1 lb ([Petoi](https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled)).
- **Voice module:** 40 fixed commands (EN/ZH) plus 10 custom sound clips (≤ 6 syllables). Recognition runs **on-chip and is converted to serial commands on Serial2**. There is no raw-audio API ([Petoi docs](https://docs.petoi.com/extensible-modules/voice-command-module)). The default language may be Mandarin until switched ([Learn with a Robot](https://www.learnwitharobot.com/p/exploring-the-petoi-voice-module)). → **Cannot be used as the robot's "ears" for our pipeline.** It can still serve as an offline "command channel" and is privacy-friendly, because no audio leaves the chip.
- **Petoi AI Vision Module** ($39, **sold out** on Petoi.com at access time) [corrected by verifier: Petoi's Shopify product data (`/products/petoi-ai-vision-module-for-arduino.js`, 2026-10-01) lists it as `available: true`; the "Sold out" text seen by page scrapers appears to be a template label. Confirm in the cart before ordering] ([Petoi](https://www.petoi.com/products/petoi-ai-vision-module-for-arduino)):
  - Hardware: WiseEye2 HX6538 (Cortex-M55 + Ethos-U55), Grove. Petoi's docs reference Seeed SSCMA and Grove Vision AI V2, which suggests the same platform ([Petoi docs](https://docs.petoi.com/extensible-modules/petoi-ai-vision)).
  - Inference: YOLOv8-class face/gesture/object detection runs on the module.
  - Images: the host can pull **base64 JPEG frames over the SSCMA AT protocol**, but commands are limited to 4095 bytes. That is a preview channel, not a usable video stream ([SSCMA AT protocol](https://github.com/Seeed-Studio/SSCMA-Micro/blob/main/docs/protocol/at-protocol-en_US.md)). [corrected by verifier: the 4096−1-byte limit applies to *commands* sent to the module, not to the image payload in responses. The real constraint is a small preview JPEG over UART/I2C to Bittle's ESP32. Separately, Petoi's product page advertises **"WiFi image transmission (module as AP)"**, and Petoi's docs say images can be sent over Wi-Fi when the module is paired with an ESP32-S3/C3. So a Wi-Fi image path exists; its resolution and fps are UNVERIFIED. Bench-test it against the XIAO ESP32S3 Sense before ruling it out. It would give on-module detection plus images.]
  - Mic: Grove Vision AI V2 has a PDM mic ([Seeed wiki](https://wiki.seeedstudio.com/grove_vision_ai_v2/)). Petoi firmware does not expose it (**UNVERIFIED**).
  - Petoi's older "MU" camera only outputs detection results over UART/I2C, with no video ([Petoi docs](https://docs.petoi.com/extensible-modules/mu-camera)).
- **Bittle AI Head Upgrade Kit** ($39, 2026): a drop-in head running a XiaoZhi LLM chatbot. It needs Wi-Fi, an internet connection and a **XiaoZhi account (phone number required)** ([Petoi](https://www.petoi.com/products/bittle-ai-head-upgrade-kit), via search snippet). [verifier: confirmed from the product description: "free XiaoZhi account registration (phone number required)… Requires an active internet connection and a XiaoZhi backend account". Compatible with BiBoard V1 and NyBoard V1. Listed as available, 2026-10-01.]
  - XiaoZhi firmware (MIT) streams **16 kHz mono Opus, 60 ms frames** over WebSocket/MQTT to a server. By default that is xiaozhi.me ([xiaozhi-esp32](https://github.com/78/xiaozhi-esp32), [protocol](https://github.com/78/xiaozhi-esp32/blob/main/docs/websocket.md)).
  - Self-hosting is possible with xiaozhi-esp32-server (MIT; FunASR/Sherpa local ASR, Ollama LLM, local TTS; 4 cores/8 GB recommended) ([GitHub](https://github.com/xinnan-tech/xiaozhi-esp32-server)). [corrected by verifier (2nd pass): the README gives a minimum of 2 cores/4 GB with local FunASR (2 cores/2 GB if all services are cloud APIs), and it explicitly warns that the project is "functionally incomplete and has not passed a network-security assessment, do not use in production". Devices are re-pointed to it through the OTA interface address. Treat it as a lab tool, not something to put in front of children without your own security review.]
  - → In principle this is a **raw-ish audio path from the robot's head to our laptop**, if the head can be pointed at our own server. Whether Petoi's head firmware allows a custom server URL is **UNVERIFIED**. Do not use the default cloud with children.
- **Raspberry Pi integration:** officially supported over UART. For BiBoard V1 you solder a 5-pin socket, and a 3D-printable back cover/standoff is provided; send `XS` to enable Serial2 ([Petoi docs](https://docs.petoi.com/apis/raspberry-pi-serial-port-as-an-interfac/for-biboard-v1.md)). Bittle prefers small Pis (Pi 3A+, Zero) ([FAQ](https://www.petoi.com/pages/faq)). The Python API works over USB serial or Bluetooth serial (two COM ports appear) ([Python API](https://docs.petoi.com/apis/python-api)); commands are ASCII tokens such as `ksit`, `kwkF`, `m0 30` ([serial protocol](https://docs.petoi.com/apis/serial-protocol)). Community ROS bridges exist ([bittleet_ROS](https://github.com/leetnz/bittleet_ROS)).
- **Robustness:**
  - Servos are rated for >100 h continuous walking. Servos are brushed and wear out, so plan spares (Petoi, from search snippet; exact page **UNVERIFIED**).
  - Petoi offers a 1-year limited warranty and replaceable servos; recommended age is 10+ ([FAQ](https://www.petoi.com/pages/faq)).
  - The open-source community is large: 30,000+ robots shipped, MIT licence ([OpenCatEsp32 README](https://github.com/PetoiCamp/OpenCatEsp32-Quadruped-Robot)).
- **Limitations:**
  - No camera, and no raw mic.
  - ~1 h runtime.
  - It is small (19 cm) and light, so children can grab it.
  - Plastic servos (Lite) wear faster; buy **Alloy**.

### 2.2 Petoi Nybble Q
USD 435. ESP32 BiBoard, 11 DOF (2 head joints + tail), **built-in ultrasonic "eyes"**, IMU, 4 touch sensors, voice commands, ~1 h battery, age 10+ ([Petoi](https://www.petoi.com/products/petoi-nybble-q-robot-cat)). The pan/tilt head and ultrasonic sensor make it more expressive and give one more non-camera sensor than Bittle X. The camera and mic limitations are the same. It is a cat, not a dog.

### 2.3 Petoi Quaddle (2026 newcomer)
- Kickstarter launched 2 Sep 2026. Tiers: Builder $99, Buddy $139, Scout $199; shipping $18 to the EU; delivery **expected Dec 2026** ([CNX Software](https://www.cnx-software.com/2026/09/04/petoi-quaddle-a-mini-robot-dog-for-physical-ai-experimentation/)). [verifier: confirmed. Shipping is $15 globally and $18 to the EU. CNX names the battery as a swappable BL10C (1800 mAh), giving ~1 h on Scout and 1.3–1.5 h on the other tiers. The CNX summary we fetched did not mention PIR or "2 mics", so those Scout items are UNVERIFIED.]
- Compute: ESP32-S3 motion core plus an ESP32-S3R8 "AI core" (Buddy/Scout). A Raspberry Pi Zero can replace the AI core.
- Scout sensors: 2× IR distance, 2× light, gesture, PIR, 2 mics, optional AI vision. [verifier (2nd pass): confirmed by CNX's spec table: the extension hat on **all** tiers carries 4 touchpads, 4 RGB LEDs, **2 mics**, 2 Grove sockets and a **PIR**; Buddy/Scout add 2× IR distance, 2× light and gesture. Whether the mics/camera can stream raw data to a PC is still UNVERIFIED ([CNX](https://www.cnx-software.com/2026/09/04/petoi-quaddle-a-mini-robot-dog-for-physical-ai-experimentation/)). Note the $99/$139/$199 figures are launch/early-bird pledges; Petoi's Quaddle page now shows Kickstarter $144 (Builder+) / $175 (Buddy) / $215 (Scout), MSRP $179/$219/$269 ([Petoi](https://www.petoi.com/pages/quaddle-educational-robot-kit), accessed 2026-10-02).]
- Battery: swappable phone-style BL-5C/BL-10C, 1–1.5 h. [corrected by verifier (2nd pass): CNX states a swappable **BL10C (1800 mAh)** on all models; runtime Builder 1.5 h, Buddy 1.3 h, Scout 1 h.]
- 4 servos ("MiniDoF"). Interesting because swappable batteries suit exhibitions, but crowdfunding delivery risk is high. Do not depend on it.

### 2.4 Hiwonder MechDog (ESP32) and modules
- **Kits:** Standard $299.99, **Advanced $369.99**, Ultimate $469.99, Pro Developer $569.99 ([Hiwonder](https://www.hiwonder.com/products/mechdog)).
  - Standard: robot, ultrasonic, IMU, app, Scratch/Arduino/Python.
  - Advanced adds the ESP32-S3 vision module (Wi-Fi image transmission), WonderEcho voice, MP3, dot matrix, touch and light sensors ([OpenELAB](https://openelab.io/blogs/learn/what-is-hiwonder-mechdog-open), via search snippet).
  - A different reseller page says WonderEcho is in the "Pro kit only" ([OpenELAB.com](https://openelab.com/products/hiwonder-mechdog-open-source-ai)). **Conflicting. Confirm with Hiwonder before ordering.** [corrected by verifier (2nd pass): Hiwonder's own wiki packing list puts the ESP32-S3 vision module, **WonderEcho AI voice module**, MP3 module, dot matrix, touch sensor and light sensor in the **Advanced** kit; Ultimate adds micro:bit adapters and block servos ([Hiwonder wiki, Getting Ready](https://wiki.hiwonder.com/projects/MechDog/en/latest/docs/1.Getting_Ready.html), 2026-10-02). The store page's voice section is captioned "MechDog Pro", so still confirm in writing at order time, but the official packing list supports the report's Advanced-kit description.]
- **Specs:** ESP32 controller, 8 coreless servos (8 DOF, legs only, **no neck joint**), aluminium frame, ~560 g, 214×126×138 mm, 7.4 V 1500 mAh, up to ~60 min ([Hiwonder](https://www.hiwonder.com/products/mechdog)). Reseller warranty is 12 months ([OpenELAB.com](https://openelab.com/products/hiwonder-mechdog-open-source-ai)).
- **ESP32-S3 vision module** ($19.99 standalone): 2 MP, 123° FOV. Onboard face, colour and line recognition. **"Wi-Fi video live streaming" accessible via URL**, AP or STA mode, I2C to the controller ([Hiwonder](https://www.hiwonder.com/products/esp32-s3)). Codec, resolution and fps are not specified; MechDog material says 320×240.
- **ESP32 S3-Cam module** ($12.99): 62° FOV, JPEG, Wi-Fi live feed ([Hiwonder](https://www.hiwonder.com/products/esp32-cam-ai-vision-module)).
- **Ultrasonic:** I2C, with RGB LEDs in the probe ([MechDog docs](https://docs.hiwonder.com/projects/MechDog/en/latest/docs/5.Arduino_Programming_Projects.html)).
- **WonderEcho voice:** CI1302 chip, wake word "Hello Hiwonder", up to 300 command words, offline, I2C ([same docs](https://docs.hiwonder.com/projects/MechDog/en/latest/docs/5.Arduino_Programming_Projects.html)). **Fixed command words only, no raw audio.**
- **MechDog AI** (2026, $499.99/$539.99): WonderLLM head with ESP32-S3, 2 MP camera, mic, speaker, 2" touch LCD, CI1302 wake word. LLMs (DeepSeek/Doubao/Qwen3) are reached through the XiaoZhi cloud; it also includes a 3-DOF arm ([Hiwonder](https://www.hiwonder.com/products/mechdog-ai), [CNX](https://www.cnx-software.com/2026/01/27/hiwonder-wonderllm-an-esp32-s3-smart-chat-module-with-2-inch-touch-display-2mp-camera-and-dedicated-voice-chip/)).
  - WonderLLM standalone: $39.99 ([Hiwonder](https://www.hiwonder.com/products/wonderllm)). CNX reported $29.99/$35.99 in Jan 2026.
  - "Offline firmware" with Wi-Fi video streaming is advertised (search snippet, **UNVERIFIED**).
  - Hiwonder's "1080P @ 60fps" claim for an ESP32-S3 module is a sensor-datasheet number, not a streaming rate. Do not plan on it.
- **PC control path:** USB serial/MicroPython and the BLE app are documented. A clean PC → robot command API over Wi-Fi is **UNVERIFIED**; you would probably write a small MicroPython socket server yourself.
- **Assessment:** it has more sensors in the box than Bittle, and the camera already streams. Downsides: no head DOF (cannot "look at" the visitor), heavier, and a smaller community than Petoi. A solid runner-up.

### 2.5 Unitree Go2 (Air / Pro / X / EDU) — above-budget reference
- **Prices:**
  - Air $1,600, Pro $2,800, X $4,500, EDU ≈ $11,190+, EDU Plus ≈ $13,205+ (Robozaps, July 2026, mentions mid-2026 price cuts) ([Robozaps](https://blog.robozaps.com/b/unitree-go2-review)). Pro and Air confirmed by [Antonrobots](https://antonrobots.com/unitree-go2-review/) (16 Jul 2026), which notes **$399–1,000 international freight** on top.
  - EU street price for the Air: **€2,618 incl. 19% VAT**, in stock ([Reichelt](https://www.reichelt.com/de/en/shop/product/unitree_go2_air_-_the_robot_dog-363565)). Search snippets showed €2,660.79 at RobotShop EU and €2,200 at Terra-Robotics.
- **Hardware:**
  - All versions: HD wide-angle camera (120° FOV, 1280×720 image transmission), 4D LiDAR L1, Wi-Fi 6, BT 5.2.
  - Air/Pro: 8000 mAh, 1–2 h. EDU: 15000 mAh, 2–4 h.
  - Air: 15 kg, up to 2.5 m/s, payload ~7 kg ([QUADRUPED docs](https://www.docs.quadruped.de/projects/go2/html/Overview_1.html), [Reichelt](https://www.reichelt.com/de/en/shop/product/unitree_go2_air_-_the_robot_dog-363565)).
  - **The Air has no voice function and no 8-core CPU listed. Only the EDU officially supports "Secondary Development"** ([QUADRUPED docs](https://www.docs.quadruped.de/projects/go2/html/Overview_1.html)).
- **Why the Air has no SDK:** Unitree tiers the product line. API access is reserved for the EDU to justify its price, and the Air also lacks the extra compute ([Robozaps](https://blog.robozaps.com/b/unitree-go2-review); this is the vendor's market segmentation, not a technical impossibility).
- **Community workarounds (no jailbreak):**
  - The WebRTC drivers reuse the mobile app's protocol: `unitree_webrtc_connect` (MIT, v2.2.0, 17 Aug 2026) ([GitHub](https://github.com/legion1581/unitree_webrtc_connect), [PyPI](https://pypi.org/project/unitree_webrtc_connect/)) and `go2_ros2_sdk` (BSD-2; LiDAR at 7 Hz, front camera) ([GitHub](https://github.com/abizovnuralem/go2_ros2_sdk)).
  - Video receive works on Air/Pro/EDU. **Audio send/recv is "Pro and EDU only"** ([phospho go2_webrtc_connect](https://github.com/phospho-app/go2_webrtc_connect), via search snippet). [verifier: confirmed in the phospho README: "This is supported only on Go2 Pro and Edu". The legion1581 README marks Go2 audio as "yes" without splitting by variant.]
  - Since **firmware 1.1.15 a per-device AES-128 key is required**. The tool fetches it by logging into your **Unitree cloud account with email and password** ([PyPI](https://pypi.org/project/unitree_webrtc_connect/)). Any firmware update can break the workaround.
- **Jailbreaks:** root tools such as "PawRoot" exploited a WebRTC file-upload bug that was patched in firmware 1.1.2+. Newer units have SecureBoot ([DARKNAVY, Mar 2025](https://www.darknavy.org/darknavy_insight/the_jailbroken_unitree_robot_dog/)).
- **Legal/warranty:** the WebRTC route uses the app protocol and is generally framed as interoperability. **Rooting or modifying firmware almost certainly voids support. Unitree's written warranty terms on this are UNVERIFIED.** Logging into the vendor cloud is itself a data-flow to assess under GDPR.
- **Security record (2025–2026):**
  - **UniPwn** (disclosed 20 Sep 2025): BLE Wi-Fi-config command injection gives root on Go2/B2/G1/H1 using hard-coded keys. It is wormable. CVE-2025-35027 (CVSS 7.3), plus CVE-2025-60017/60250/60251. Unpatched at disclosure ([UniPwn](https://github.com/Bin4ry/UniPwn), [GHSA](https://github.com/advisories/GHSA-27p8-m7h9-xchc)); current patch status **UNVERIFIED**.
  - The **G1** humanoid was reported sending data to servers in China every 5 min ([Interesting Engineering](https://interestingengineering.com/innovation/security-flaw-unitree-humanoids-china)).
  - On 28 Jul 2026 the US FCC added foreign-produced "advanced robotic devices" (mobile robots over 4.4 lb) to its Covered List. [corrected by verifier: the FCC fact sheet defines the category as "mobile robots, such as humanoids and quadrupeds". The "over 4.4 lb" threshold is not in the fact sheet and is UNVERIFIED (it may be in the separate National Security Determination). The fact sheet does confirm that previously authorised models and devices already bought are unaffected.] [verifier (2nd pass): the ">4.4 lb" threshold is now confirmed from a law-firm summary of the National Security Determination: covered devices are ground-mobile machines operating at a distance from a human operator, weighing **more than 4.4 lb (incl. dock)**, with a sensor, ≥200 kbps connectivity and controlling software ([Sidley, Aug 2026](https://www.sidley.com/en/insights/newsupdates/2026/08/fcc-adds-all-foreign-produced-advanced-robotic-devices-to-the-covered-list)). The rule applies to foreign-produced devices "regardless of the nationality of origin" ([FCC fact sheet](https://docs.fcc.gov/public/attachments/DOC-423682A1.pdf)). Bittle X (≈0.3 kg) and MechDog (≈0.56 kg) are under the threshold; Go2 (≈15 kg) is above it.] This blocks **new** model authorisations; Go2 was authorised earlier and remains legal ([FCC fact sheet](https://docs.fcc.gov/public/attachments/DOC-423682A1.pdf), [TechTimes](https://www.techtimes.com/articles/321890/20260728/fcc-bans-chinese-humanoid-robots-power-inverters-linked-confirmed-backdoors.htm)). This is not EU law, but it is a reputational and procurement signal for an EU-funded, child-facing stand.
- **Verdict:** a 15 kg robot moving at up to 2.5 m/s in a crowd of children needs a fenced area and a dedicated operator. The Air has no microphone path and no official API. Add the price and the security record, and it is **not suitable**. It is only useful as an "above-budget reference" in the proposal ("what a €10k+ EDU unit would add").

### 2.6 Unitree Go1 (used)
- Discontinued around mid-2023.
- Used and new-old-stock: ~$1,699 typical, eBay listings $2,300–2,500.
- Firmware frozen; official batteries ($600/$850) out of stock ([Robozaps](https://blog.robozaps.com/b/unitree-go1-review), [eBay](https://www.ebay.com/itm/267647870709)).
- **CVE-2025-2894:** the undocumented "CloudSail" tunnel (Zhexi) allowed remote takeover. The service was shut down on 29 Mar 2025, but the client and default credentials remain on the robots ([SentinelOne CVE page](https://www.sentinelone.com/vulnerability-database/cve-2025-2894/), [Robozaps](https://blog.robozaps.com/b/unitree-go1-review)).
- **Avoid.**

### 2.7 Weilan AlphaDog / BabyAlpha
- AlphaDog (C100–E400L): from $5,670 up to $27,690 ([Gadgetbyte](https://www.gadgetbytenepal.com/weilan-alphadog-ai-pet-unveiled/)).
- BabyAlpha A2 (Kickstarter, Oct 2024): headless "DevQ" developer version from $1,099, regular from $1,199. Forehead HD camera, GPT-4o (cloud), DevQ "includes SDK" ([Mikeshouts](https://mikeshouts.com/weilan-babyalpha-a2-intelligent-petbot-with-gpt-4o/)).
- Vendor claims for BabyAlpha: LiDAR, ToF, mmWave radar, mic array, Baidu voice ([Interesting Engineering](https://interestingengineering.com/innovation/charming-canine-chinese-robot-dog)).
- EU availability, SDK content and delivery record: **UNVERIFIED**. Not suitable (price, cloud, uncertain SDK).

### 2.8 KEYi Loona Petbot
- Wheeled, not a quadruped. $499 (July 2026).
- 720p RGB camera + 3D ToF, 4-mic array, quad Cortex-A53 + 5 TOPS BPU, 2.4" LCD ([KEYi](https://keyirobot.com/blogs/loona-tutorials/what-is-loona-petbot-a-complete-guide-to-smart-ai-robot-pet)).
- Conversational AI, remote access and updates need internet. GPT-4o is "free for the moment" ([Robozaps](https://blog.robozaps.com/b/loona-robot-review)).
- **The standalone SDK promised on Kickstarter never shipped. Programming is Blockly only** (Robozaps, via search snippet).
- Not suitable: no raw sensor access, and a cloud-dependent AI that we cannot audit.

### 2.9 Sony aibo ERS-1000
- Price and support: $2,899.99 including 3 years of the AI Cloud Plan, then $300/yr ([Robozaps](https://blog.robozaps.com/b/sony-aibo-review)). [verifier: not confirmed on a Sony page. TechXplore (26 Jun 2026) says the US retail price is "over $3,000" and that aibo "is not marketed anywhere else", so it is effectively **not sold in the EU**.] Sony ended Japan sales in June 2026 [corrected by verifier (2nd pass): announced June 2026; Japan sales end "once stock runs out". A search snippet (robozaps, UNVERIFIED on a Sony page) says the US store lists the base unit at $2,899.99 and the white edition at $3,199.99, sold as final sale] (US continues; support, parts and cloud maintained) ([TechXplore](https://techxplore.com/news/2026-06-sony-discontinues-japan-sales-robot.html)).
- API: a free "Web API" since 2019 (REST, owner-only). Developers can program actions, but "aibo's personality cannot be altered" ([Sony](https://info.aibo.com/en-us/2019/11/20191115-21.html), [developer page](https://us.aibo.com/developer/)). The API calls go through Sony's cloud (owner AccessToken) ([SimpleAiboWebAPI.jl](https://github.com/hsugawa8651/SimpleAiboWebAPI.jl)).
- Hardware: front camera + SLAM camera, 4 microphones, ToF, touch sensors, LTE ([aibo wiki](https://aibo.miraheze.org/wiki/ERS-1000)).
- **Raw camera/mic access through the API: not documented in anything we could fetch (UNVERIFIED, very likely absent).** Not suitable: cost, cloud, no raw sensors, EU availability unclear.

### 2.10 Anki / Digital Dream Labs Vector 2.0
- Store and price: now sold via anki.bot (© 2026 ANKI LLC / DDL), $249.99 ([anki.bot](https://anki.bot/products/vector-robot)). Voice commands need a subscription: $11.99/mo or $99.99/yr (ChatGPT), $14.99/mo or $139.99/yr (Claude) ([membership](https://anki.bot/pages/vector-membership)).
- Free path: community **wire-pod** server (MIT) restores voice on any Vector 1.0/2.0 without fees ([wire-pod](https://github.com/kercre123/wire-pod)). The extended Python SDK supports Python 3.6–3.12 ([wirepod-vector-python-sdk](https://github.com/kercre123/wirepod-vector-python-sdk)). [corrected by verifier: wire-pod is MIT, but the Python SDK is the original Anki Vector SDK under **Apache-2.0** (per its LICENSE.txt). The `anki_vector/audio.py` docstring confirms "TODO Ability to access the Vector's audio stream to come", and `camera.py` confirms 640×360 default and 1280×720 high-res.]
- Camera: the SDK gives a camera feed, 640×360 by default (1280×720 high-res; 90°×50° FOV). **Mic: the SDK source says "Ability to access the Vector's audio stream to come"** (output only).
- Not suitable as "robot dog", and it gives no raw audio. It could be a cheap secondary "toy robot" contrast exhibit (cloud subscription caveat).

### 2.11 ESP32-CAM-based DIY dogs
- The most mature open project is **SpotMicroESP32-Leika**: MIT, ESP32-S3 N8R8 recommended, 12 servos, optional OV2640/OV5640, MPU6050, HC-SR04, gesture sensor, web UI, 1,100+ commits ([GitHub](https://github.com/runeharlyk/SpotMicroESP32-Leika)).
- Cost is low in principle. For a 3–5-day public exhibit, build quality, servo burnout (MG996R-class) and debugging time make it the **least robust** option.
- Only consider it if a student project is part of the plan.

### 2.12 2025–2026 newcomers (≤ USD 800) found
- **Petoi Quaddle** (Kickstarter Sep 2026, $99–199, ships Dec 2026). See §2.3.
- **Hiwonder MechDog AI** ($499.99) and **WonderLLM** module (Jan 2026). See §2.4.
- **Petoi Bittle AI Head** ($39). See §2.1.
- **KEYi Loona** (refresh pricing 2026). See §2.8.
- Above $800: **Hengbot Sirius** $1,299, waitlist ([Hengbot](https://www.hengbot.com/)); BabyAlpha A2 $1,099+.
- Trend: almost every 2025–26 newcomer adds an **ESP32-S3 "XiaoZhi" cloud-LLM head**. These ship pointing to Chinese cloud back-ends by default, which is incompatible with privacy-by-design for children unless the device is re-pointed to a self-hosted server.

---

## 3. External sensors mounted on, or next to, a cheap robot dog

| Option | Price (accessed 2026-10) | What you get | Raw stream to PC | Latency / bandwidth notes | Fit |
|---|---|---|---|---|---|
| **Seeed XIAO ESP32S3 Sense** | USD 13.90 ([Seeed](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html)) | ESP32-S3, 8 MB PSRAM, OV2640 (OV5640 option), **built-in digital mic**, SD | MJPEG over HTTP (CameraWebServer, up to UXGA; face recognition needs ≤ CIF) ([wiki](https://wiki.seeedstudio.com/xiao_esp32s3_camera_usage/)) | 2.4 GHz only ([Espressif](https://www.espressif.com/en/products/socs/esp32-s3)). JPEG gives the best frame rates; PSRAM needed above CIF ([esp32-camera](https://github.com/espressif/esp32-camera)). **Gets very hot** in long streaming runs ([wiki](https://wiki.seeedstudio.com/xiao_esp32s3_camera_usage/)) | **Best head-cam for Bittle** (a few grams) |
| Hiwonder ESP32-S3 vision module | USD 19.99 ([Hiwonder](https://www.hiwonder.com/products/esp32-s3)) | 2 MP, 123° FOV, face/colour onboard | Wi-Fi live stream via URL | as above | Native on MechDog, possible on Bittle (Grove/I2C mount **UNVERIFIED**) |
| Raspberry Pi Zero 2 W + Camera Module 3 | USD 15 + from USD 25 (+ Zero camera cable) ([Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/), [Cam Module 3](https://www.raspberrypi.com/products/camera-module-3/)) | Linux, IMX708 12 MP, 1080p50, 75° or 120° wide, PDAF | rpicam-vid with hardware H.264, TCP/UDP/RTSP ([docs](https://www.raspberrypi.com/documentation/computers/camera_software.html)); MediaMTX for WebRTC/RTSP (MIT) ([GitHub](https://github.com/bluenviron/mediamtx)) | H.264 saves bandwidth but adds encode/jitter-buffer delay. Expect roughly 150–300 ms glass-to-glass over Wi-Fi (**estimate, measure it**). 2.4 GHz only on Zero 2 W. Drains Bittle's 1000 mAh battery faster | Officially supported on Bittle via UART ([Petoi](https://docs.petoi.com/apis/raspberry-pi-serial-port-as-an-interfac/for-biboard-v1.md)). Better image, more weight, power and boot time |
| ESP32-S3-BOX-3 | USD 49 ([Espressif](https://www.espressif.com/en/products/devkits/esp32-s3-box-3)) | Mics + speaker + LCD, ESP-SR | Audio via own firmware/XiaoZhi | — | Better as a stand-side "robot face" than on a 300 g dog |
| **Seeed ReSpeaker XVF3800 USB 4-mic array** | USD 54.90 ([Seeed](https://www.seeedstudio.com/ReSpeaker-XVF3800-USB-Mic-Array-p-6488.html)) | XMOS XVF3800: AEC, beamforming, **DoA**, VAD, noise suppression, de-reverb, 360° up to ~5 m; **USB Audio Class 2.0**; Win/macOS/Linux ([wiki](https://wiki.seeedstudio.com/respeaker_xvf3800_introduction/)) | Yes, wired USB, plug-and-play | Wired, so no network jitter. DoA lets the UI show "I heard you from the left", which works well for explanations | **Recommended "ears" at the stand** |
| Jabra Speak2 40/55-class USB speakerphone | **UNVERIFIED** (Jabra site redirect loop; typically roughly €100–200) | Beamforming mics + speaker, UC-certified | USB audio | Call-optimised DSP (AGC/noise suppression) is fine for ASR; also a speaker for robot TTS | Alternative to ReSpeaker; no DoA API |
| DJI Mic Mini (wireless lav) | €45 (1TX+1RX), €79 (2TX+RX+case) ([DJI Store](https://store.dji.com/product/dji-mic-mini)) | 2-level noise cancellation, 11.5 h TX | Receiver USB-C; works as a PC USB audio device? **UNVERIFIED** | 2.4 GHz digital. Latency not published (**UNVERIFIED**) | For a facilitator/presenter voice, not visitors |
| RØDE Wireless GO (Gen 3) | **UNVERIFIED** | Dual-channel, "near-zero latency", 260 m LOS, **works as a USB microphone with a computer** ([RØDE](https://rode.com/en/microphones/wireless/wireless-go-gen-3)) | Yes (USB) | 2.4 GHz digital | Same role as above |

**Latency rules of thumb (estimates, verify on site):**
- A wired USB webcam or mic adds the least latency and is immune to the crowded 2.4 GHz band.
- ESP32 MJPEG frames are independent, so per-frame delay is low, but fps drops sharply as resolution rises and when Wi-Fi is congested.
- H.264/WebRTC from a Pi is smoother at higher resolution but adds buffering.
- Bluetooth headset mics (HFP) are narrowband and laggy; avoid them (**UNVERIFIED** general knowledge).
- Every ESP32-S3 and Pi Zero 2 W option is **2.4 GHz-only**. At an exhibition with thousands of phones, bring a dedicated router, keep the laptop on 5 GHz/Ethernet, and fix the ESP32 to a quiet channel.

---

## 4. Suitability verdict

| Platform | Suitable? | Why |
|---|---|---|
| Petoi Bittle X V2 (Alloy, pre-assembled) | **Yes, as the body** | Within budget, mature open source (MIT), serial/BT API, neck pan to "look at" visitors, replaceable servos. Needs an external camera/mic |
| Hiwonder MechDog Advanced | **Yes (runner-up)** | Includes a streaming camera plus ultrasonic plus touch/light. Metal build. No head DOF; voice module is fixed commands only |
| Petoi Nybble Q | Conditional | Built-in ultrasonic, 2-DOF head. A cat; $435 |
| Petoi Quaddle Scout | Not yet | Crowdfunded, ships Dec 2026; re-evaluate in Q1 2027 |
| Hiwonder MechDog AI / WonderLLM / Petoi AI Head | No (as shipped) | Default cloud LLM (XiaoZhi; Chinese back-ends, phone-number account). Only acceptable if re-pointed to a self-hosted server and audited |
| PiDog V2 / Freenove / PuppyPi (Pi-based) | **Compare with the Pi track** | Native raw camera and mic on Linux; PiDog also has a sound-direction sensor |
| Unitree Go2 Air/Pro | No | €2.6k+ (Air), no official SDK, no mic on Air, 15 kg/2.5 m/s, unresolved CVEs |
| Unitree Go2 EDU | No (reference only) | ≈ $11k+ |
| Unitree Go1 used | No | Discontinued, no spares, backdoor CVE |
| Weilan, Hengbot Sirius | No | Over budget / not shipping / SDK unclear |
| Loona, aibo, Vector | No | Closed or cloud-dependent; no raw sensor access (Vector has camera only) |
| DIY ESP32-CAM dog | No (for the exhibit) | Build and robustness risk |

---

## 5. Recommendations for our demonstrator

1. **Architecture: the "body + eye on the robot, ears at the stand, brain on the laptop" split.**
   - **Body:** Petoi Bittle X V2, **Alloy, pre-assembled ($399)**. It is driven from the laptop over Bluetooth serial using the Petoi Python API, with USB as fallback. The neck servo turns the head toward the detected visitor; this is the visible "attention" cue.
   - **Eye:** XIAO ESP32S3 Sense ($13.90) fixed in Bittle's head/mouth. It streams MJPEG at VGA/QVGA over a **dedicated, offline router**, and all inference runs on the laptop. Because the camera moves with the head, "what the robot sees" equals "where it looks". That makes it very easy to explain to children.
   - **Ears:** ReSpeaker XVF3800 ($54.90) on the table, connected by USB. Use its DoA and VAD for visualisations such as "the robot heard someone, from over there", and local ASR on the laptop.
     - Do **not** rely on a robot-mounted mic: it sits next to the servos and is weak.
     - Keep the XIAO's onboard mic as an optional "robot-ear" demo channel.
   - **Extra low-privacy sensors** for the toggles: the Petoi sensor pack ($44: PIR, IR distance, gesture, light, touch) plus Bittle's IMU and back-touch. These let you show "even without camera or mic, the robot knows you're close / touching / moving it". That is strong XAI content with almost no personal data.
   - **Indicative BOM:** $399 + $14 + $55 + $44 + 2 spare batteries $102 ≈ **$614** (ex-VAT/shipping). Drop the sensor pack or one battery to reach about $520.
2. **Buy two robot bodies before the event** (second unit from the budget reserve or a later purchase). Plan battery rotation at ~1 h runtime and ~1.5 h charge, which means 3–4 batteries per robot per exhibition day. Keep a spare-servo set: servos are brushed and wear out.
3. **Fallback camera:** a wired USB webcam at the stand, labelled as "the robot's second eye", in case 2.4 GHz collapses. The UI should switch automatically and *say so* (this is itself good XAI).
4. **Runner-up path:** if the team prefers fewer custom parts, take the **Hiwonder MechDog Advanced ($369.99)**. Its ESP32-S3 camera stream and ultrasonic are integrated; add the same ReSpeaker. Confirm the kit contents (WonderEcho inclusion conflicts between sources) [verifier (2nd pass): Hiwonder's official wiki packing list includes WonderEcho in Advanced] and how to drive it from a PC over Wi-Fi/serial before buying.
5. **Before committing, run a 1-week bake-off** against the best Pi-based dog from the Pi track (PiDog V2 + Pi 5 is the obvious rival). Measure:
   - end-to-end latency (camera → detection → head-turn);
   - fps under a crowded 2.4 GHz band;
   - runtime with the camera streaming;
   - robustness to a child picking the robot up.
6. **Privacy-by-design wiring:**
   - All streams stay on a closed LAN; the laptop has no internet during the show.
   - Frames and audio are processed in RAM, never stored.
   - Nothing uses XiaoZhi or other vendor clouds.
   - Physical LED/cover cues show which sensors are on, and toggles physically gate the stream (stop the MJPEG server / mute the array), not just hide it in the UI.
7. **Use Unitree Go2 only as a slide or video**: "an €11k EDU robot has LiDAR + depth; here is what that would add", to show scientific context without the cost, safety and security exposure.

---

## 6. Pitfalls / what not to do

- **Don't assume "voice-controlled" means microphone access.** Petoi's voice module and Hiwonder's WonderEcho/CI1302 recognise fixed command words on-chip and output serial/I2C codes only.
- **Don't buy the Petoi AI Vision Module expecting a video feed.** It outputs detections; images come only as base64 JPEG over a 4 KB-limited AT protocol. It was also sold out at access time. [corrected by verifier: the 4 KB limit applies to commands, not images. The product page advertises Wi-Fi image transmission (module as AP), and the Shopify data lists it as available. Treat it as "detections plus a low-res Wi-Fi image path, quality unverified" and bench-test it rather than dismissing it.]
- **Don't plug XiaoZhi-based "AI heads" (Petoi AI Head, Hiwonder WonderLLM, MechDog AI) into their default cloud.** That streams children's voices to third-party servers (xiaozhi.me by default; Petoi's needs a phone-number account), which breaks privacy-by-design and complicates GDPR transfers. Self-host or don't use.
- **Don't buy a Go2 Air for "SDK" work.** It has no official secondary development and no voice/mic. The WebRTC workaround needs your Unitree cloud credentials since firmware 1.1.15 and can break with any OTA update.
- **Don't put a 15 kg, 2.5 m/s quadruped among 8-year-olds,** and don't connect Unitree robots to institutional networks, given UniPwn (wormable BLE root, CVE-2025-35027 et al.) and Go1's CloudSail backdoor (CVE-2025-2894).
- **Don't buy a used Go1:** discontinued, batteries unavailable, backdoor client still on the robot.
- **Don't trust ESP32 marketing numbers** ("1080P@60fps"). Real ESP32-S3 MJPEG streaming is QVGA–SVGA at modest fps, 2.4 GHz only, and boards run hot (Seeed's own burn warning).
- **Don't mount the mic on the robot** if you want reliable speech features. Servo noise and distance ruin it; a beamforming array at the stand is far better.
- **Don't rely on a single robot or battery.** ~1 h runtime and brushed-servo wear make spares mandatory. Buy Alloy servos, not Lite.
- **Don't choose closed petbots** (Loona, aibo, Vector) for an XAI exhibit. You cannot show evidence → inference chains you cannot access, and their behaviour depends on vendor clouds that may change or shut down (cf. aibo's Japan sales end).
- **Don't rely on crowdfunded hardware** (Quaddle, BabyAlpha, Sirius) for a fixed 2027 date.

---

## 7. Unverified / open items

- Petoi Bittle X V2 servo life ">100 h continuous walking": the figure is from a search snippet attributed to Petoi; the exact page was not opened.
- Whether the Petoi AI Head / Hiwonder WonderLLM firmware can be pointed at a self-hosted XiaoZhi server without reflashing.
- Hiwonder MechDog: WonderEcho in Advanced vs Pro kit (sources conflict) [verifier (2nd pass): largely resolved; the official wiki lists it in Advanced]; ESP32-S3 stream codec, resolution and fps; a documented PC-side Wi-Fi command API.
- Quaddle Scout: whether the camera and mics can stream raw data to a PC; delivery date.
- aibo Web API: camera/mic data access (very likely none); EU availability.
- Vector 2.0: microphone count and other sensors (camera verified only via SDK source).
- Unitree: current UniPwn patch status; written warranty terms on rooting; Go2 X/EDU exact EU prices.
- Prices for Jabra Speak2 and RØDE Wireless GO Gen 3 (vendor pages not fetchable); DJI Mic Mini acting as a USB audio device on a PC.
- Latency numbers in §3 are engineering estimates and must be measured.
- A complete CES 2026 / AliExpress / Amazon newcomer sweep was not finished (search quota exhausted).
- EU Radio Equipment Directive cybersecurity delegated act (2022/30) applicability to self-built Wi-Fi add-ons: for the legal track to check.

---

## 8. Sources

**Petoi**
- https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled
- https://www.makershed.com/products/petoi-robot-dog-bittle-x
- https://www.robot-advance.com/EN/art-petoi-bittle-x-v2-pre-assembled-dog-robot-5992.htm
- https://guide.petoi.com/product/bittle-x-v2
- https://www.petoi.com/pages/bittle-x-robot-dog-with-arm-specifications
- https://www.petoi.com/pages/educator-purchase-guide
- https://www.petoi.com/collections/robots
- https://www.petoi.com/collections/bittle-x-accessories
- https://www.petoi.com/collections/all/products/petoi-sensor-pack
- https://www.petoi.com/products/petoi-ai-vision-module-for-arduino
- https://www.petoi.com/products/bittle-ai-head-upgrade-kit
- https://www.petoi.com/products/petoi-nybble-q-robot-cat
- https://www.petoi.com/pages/faq
- https://docs.petoi.com/extensible-modules/voice-command-module
- https://docs.petoi.com/extensible-modules/petoi-ai-vision
- https://docs.petoi.com/extensible-modules/mu-camera
- https://docs.petoi.com/apis/python-api
- https://docs.petoi.com/apis/serial-protocol
- https://docs.petoi.com/apis/raspberry-pi-serial-port-as-an-interfac/for-biboard-v1.md
- https://github.com/PetoiCamp/OpenCatEsp32-Quadruped-Robot
- https://github.com/leetnz/bittleet_ROS
- https://www.learnwitharobot.com/p/exploring-the-petoi-voice-module
- https://www.learnwitharobot.com/p/petoi-ai-vision-module
- https://www.cnx-software.com/2026/09/04/petoi-quaddle-a-mini-robot-dog-for-physical-ai-experimentation/

**Seeed / SSCMA / XiaoZhi**
- https://wiki.seeedstudio.com/grove_vision_ai_v2/
- https://github.com/Seeed-Studio/SSCMA-Micro/blob/main/docs/protocol/at-protocol-en_US.md
- https://github.com/78/xiaozhi-esp32
- https://github.com/78/xiaozhi-esp32/blob/main/docs/websocket.md
- https://github.com/xinnan-tech/xiaozhi-esp32-server

**Hiwonder**
- https://www.hiwonder.com/products/mechdog
- https://www.hiwonder.com/products/mechdog-ai
- https://www.hiwonder.com/products/esp32-s3
- https://www.hiwonder.com/products/esp32-cam-ai-vision-module
- https://www.hiwonder.com/products/wonderllm
- https://www.hiwonder.com/products/puppypi
- https://docs.hiwonder.com/projects/MechDog/en/latest/docs/5.Arduino_Programming_Projects.html
- https://docs.hiwonder.com/projects/WonderEcho/en/latest/docs/1_Module_Introduction.html
- https://www.cnx-software.com/2026/01/27/hiwonder-wonderllm-an-esp32-s3-smart-chat-module-with-2-inch-touch-display-2mp-camera-and-dedicated-voice-chip/
- https://openelab.io/products/hiwonder-mechdog-ai
- https://openelab.io/blogs/learn/what-is-hiwonder-mechdog-open
- https://openelab.com/products/hiwonder-mechdog-open-source-ai

**Unitree, security and regulation**
- https://blog.robozaps.com/b/unitree-go2-review
- https://antonrobots.com/unitree-go2-review/
- https://www.docs.quadruped.de/projects/go2/html/Overview_1.html
- https://www.reichelt.com/de/en/shop/product/unitree_go2_air_-_the_robot_dog-363565
- https://github.com/legion1581/unitree_webrtc_connect
- https://pypi.org/project/unitree_webrtc_connect/
- https://github.com/phospho-app/go2_webrtc_connect
- https://github.com/abizovnuralem/go2_ros2_sdk
- https://www.darknavy.org/darknavy_insight/the_jailbroken_unitree_robot_dog/
- https://github.com/Bin4ry/UniPwn
- https://github.com/advisories/GHSA-27p8-m7h9-xchc
- https://interestingengineering.com/innovation/security-flaw-unitree-humanoids-china
- https://docs.fcc.gov/public/attachments/DOC-423682A1.pdf
- https://www.techtimes.com/articles/321890/20260728/fcc-bans-chinese-humanoid-robots-power-inverters-linked-confirmed-backdoors.htm
- https://blog.robozaps.com/b/unitree-go1-review
- https://www.ebay.com/itm/267647870709
- https://www.sentinelone.com/vulnerability-database/cve-2025-2894/

**Other petbots and dogs**
- https://www.gadgetbytenepal.com/weilan-alphadog-ai-pet-unveiled/
- https://mikeshouts.com/weilan-babyalpha-a2-intelligent-petbot-with-gpt-4o/
- https://interestingengineering.com/innovation/charming-canine-chinese-robot-dog
- https://blog.robozaps.com/b/loona-robot-review
- https://keyirobot.com/blogs/loona-tutorials/what-is-loona-petbot-a-complete-guide-to-smart-ai-robot-pet
- https://blog.robozaps.com/b/sony-aibo-review
- https://techxplore.com/news/2026-06-sony-discontinues-japan-sales-robot.html
- https://us.aibo.com/developer/
- https://info.aibo.com/en-us/2019/11/20191115-21.html
- https://aibo.miraheze.org/wiki/ERS-1000
- https://github.com/hsugawa8651/SimpleAiboWebAPI.jl
- https://anki.bot/products/vector-robot
- https://anki.bot/pages/vector-membership
- https://github.com/kercre123/wire-pod
- https://github.com/kercre123/wirepod-vector-python-sdk
- https://www.hengbot.com/
- https://github.com/runeharlyk/SpotMicroESP32-Leika
- https://www.sunfounder.com/products/pidog
- https://docs.sunfounder.com/projects/pidog/en/latest/
- https://github.com/sunfounder/pidog
- https://store.freenove.com/products/fnk0050
- https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi

**External sensors and streaming**
- https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html
- https://wiki.seeedstudio.com/xiao_esp32s3_camera_usage/
- https://www.espressif.com/en/products/socs/esp32-s3
- https://www.espressif.com/en/products/devkits/esp32-s3-box-3
- https://github.com/espressif/esp32-camera
- https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/
- https://www.raspberrypi.com/products/camera-module-3/
- https://www.raspberrypi.com/documentation/computers/camera_software.html
- https://github.com/bluenviron/mediamtx
- https://www.seeedstudio.com/ReSpeaker-XVF3800-USB-Mic-Array-p-6488.html
- https://wiki.seeedstudio.com/respeaker_xvf3800_introduction/
- https://store.dji.com/product/dji-mic-mini
- https://rode.com/en/microphones/wireless/wireless-go-gen-3

**Added by verifier**
- https://shop.unitree.com/products/unitree-go2
- https://category.yahboom.net/collections/dogzilla/products.json
- https://raw.githubusercontent.com/kercre123/wirepod-vector-python-sdk/master/anki_vector/audio.py

---

## Verification log

Independent re-check by a verifier on 2026-10-01. The verifier's web-search quota was exhausted, so all checks used direct fetches of primary pages, Shopify product JSON (`/products/<handle>.js`, which gives live variant prices and `available` flags), and raw GitHub files.

| # | Claim | Verdict | Source / note |
|---|---|---|---|
| 1 | Bittle X V2 prices $319/339/379/399, +Arm $449/469 | Confirmed | Maker Shed and Petoi Shopify JSON: all 6 variants priced as stated and `available: true` ([Maker Shed](https://www.makershed.com/products/petoi-robot-dog-bittle-x), [Petoi](https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled)) |
| 2 | EU €406.80 incl. VAT for pre-assembled Bittle X V2 | Corrected | That listing is the **Lite** servo version, "available on request" ([Robot-Advance](https://www.robot-advance.com/EN/art-petoi-bittle-x-v2-pre-assembled-dog-robot-5992.htm)) |
| 3 | Bittle X specs (ESP32-WROOM-32D, 6-axis IMU, 7.4 V 1000 mAh, ~1 h, 1.5 h charge, 190×153×107 mm, 269–353 g, 4 Grove) | Confirmed | [Petoi spec page](https://www.petoi.com/pages/bittle-x-robot-dog-with-arm-specifications); BiBoard V1 confirmed in [guide](https://guide.petoi.com/product/bittle-x-v2) |
| 4 | Voice module: 40 fixed (EN/ZH) + 10 custom, on-chip, serial codes on Serial2, no raw audio | Confirmed | [Petoi docs](https://docs.petoi.com/extensible-modules/voice-command-module) |
| 5 | AI Vision Module $39, sold out, images only via AT protocol capped at 4095 bytes, no video | Corrected | $39 is confirmed. Shopify lists it as available. The 4095-byte cap applies to **commands** ([SSCMA AT protocol](https://github.com/Seeed-Studio/SSCMA-Micro/blob/main/docs/protocol/at-protocol-en_US.md): "Command length ... max length is limited to 4096 - 1"). The product page advertises "WiFi image transmission (module as AP)" ([Petoi](https://www.petoi.com/products/petoi-ai-vision-module-for-arduino)) |
| 6 | Bittle AI Head $39, XiaoZhi, internet + phone-number account | Confirmed | Product description in Petoi Shopify JSON ([Petoi](https://www.petoi.com/products/bittle-ai-head-upgrade-kit)) |
| 7 | XiaoZhi firmware MIT, 16 kHz Opus 60 ms frames, default xiaozhi.me, self-host possible; xiaozhi-esp32-server MIT | Confirmed | [xiaozhi-esp32 LICENSE and docs/websocket.md](https://github.com/78/xiaozhi-esp32), [xiaozhi-esp32-server LICENSE](https://github.com/xinnan-tech/xiaozhi-esp32-server) |
| 8 | OpenCatEsp32 licence MIT | Confirmed | [LICENSE](https://github.com/PetoiCamp/OpenCatEsp32-Quadruped-Robot) |
| 9 | Pi on BiBoard V1: solder 5-pin socket, send `XS`; Python API over USB or Bluetooth serial | Confirmed | [Pi docs](https://docs.petoi.com/apis/raspberry-pi-serial-port-as-an-interfac/for-biboard-v1.md) (Pi 3/4 `/dev/ttyS0`, Pi 5 `/dev/ttyAMA0`), [Python API](https://docs.petoi.com/apis/python-api) |
| 10 | Sensor pack $44 (PIR, IR distance, gesture, light, touch); battery $51 | Confirmed | Petoi Shopify JSON `available: true`; Maker Shed add-ons ($51 battery, $44 pack) |
| 11 | MechDog $299.99 / 369.99 / 469.99 / 569.99; ~560 g, 1500 mAh, ~60 min, 8 DOF, camera 320×240 | Confirmed | [Hiwonder](https://www.hiwonder.com/products/mechdog) Shopify JSON and description. The page's voice-recognition section names "MechDog Pro", so the WonderEcho kit-inclusion conflict remains open |
| 12 | MechDog AI $499.99/$539.99; WonderLLM $39.99; ESP32-S3 vision module $19.99 | Confirmed | Hiwonder Shopify JSON ([mechdog-ai](https://www.hiwonder.com/products/mechdog-ai), [wonderllm](https://www.hiwonder.com/products/wonderllm), [esp32-s3](https://www.hiwonder.com/products/esp32-s3)) |
| 13 | Go2 Air $1,600 / Pro $2,800 / X $4,500 | Confirmed | Official [Unitree shop](https://shop.unitree.com/products/unitree-go2) JSON: Air $1,600 without controller / $1,850 with; Pro $2,800 / $3,050; X $4,500 |
| 14 | Go2 Air €2,618 incl. VAT, 15 kg, 2.5 m/s; only EDU has secondary development; Air has no voice | Confirmed | [Reichelt](https://www.reichelt.com/de/en/shop/product/unitree_go2_air_-_the_robot_dog-363565), [QUADRUPED docs](https://www.docs.quadruped.de/projects/go2/html/Overview_1.html) (Air warranty 6 months vs 12 months for Pro/EDU) |
| 15 | unitree_webrtc_connect MIT v2.2.0 (17 Aug 2026); per-device AES-128 key since Go2 fw 1.1.15 via cloud email/password; audio Pro/EDU only | Confirmed | [PyPI](https://pypi.org/project/unitree_webrtc_connect/), [README](https://github.com/legion1581/unitree_webrtc_connect) (`unitree-fetch-aes-key --email --password`), [phospho README](https://github.com/phospho-app/go2_webrtc_connect) ("supported only on Go2 Pro and Edu") |
| 16 | go2_ros2_sdk BSD-2 | Confirmed | [LICENSE](https://github.com/abizovnuralem/go2_ros2_sdk) "BSD 2-Clause" |
| 17 | UniPwn 20 Sep 2025, CVE-2025-35027 CVSS 7.3 + 60017/60250/60251, wormable, Go2/B2/G1/H1 | Confirmed | [UniPwn README](https://github.com/Bin4ry/UniPwn), [GHSA](https://github.com/advisories/GHSA-27p8-m7h9-xchc) (published 26 Sep 2025; patch status "unknown") |
| 18 | FCC Covered List, 28 Jul 2026, foreign-produced advanced robotic devices; previously authorised models stay legal | Confirmed, with a detail corrected | [FCC fact sheet](https://docs.fcc.gov/public/attachments/DOC-423682A1.pdf). The ">4.4 lb" threshold is not in the fact sheet (UNVERIFIED) |
| 19 | Sony ended aibo Japan sales June 2026, US continues | Confirmed | [TechXplore 26 Jun 2026](https://techxplore.com/news/2026-06-sony-discontinues-japan-sales-robot.html): "not marketed anywhere else"; US price "over $3,000". The $2,899.99 figure is unverifiable on a Sony page |
| 20 | Vector 2.0 $249.99; subscription $11.99/mo or $99.99/yr; SDK 640×360; audio stream "to come"; wire-pod MIT | Confirmed, licence detail corrected | [anki.bot](https://anki.bot/products/vector-robot); [SDK audio.py/camera.py](https://github.com/kercre123/wirepod-vector-python-sdk). The SDK itself is Apache-2.0; wire-pod is MIT |
| 21 | Quaddle $99/$139/$199, +$18 EU, Dec 2026 | Partly confirmed | [CNX](https://www.cnx-software.com/2026/09/04/petoi-quaddle-a-mini-robot-dog-for-physical-ai-experimentation/). PIR and "2 mics" on Scout not confirmed in the fetched text |
| 22 | XIAO ESP32S3 Sense $13.90, OV2640, digital mic, 8 MB PSRAM; "very hot" warning; face recognition ≤ CIF | Confirmed | [Seeed store](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html), [wiki](https://wiki.seeedstudio.com/xiao_esp32s3_camera_usage/) |
| 23 | ReSpeaker XVF3800 $54.90, AEC/beamforming/DoA/VAD, UAC2, ~5 m | Confirmed | [Seeed store](https://www.seeedstudio.com/ReSpeaker-XVF3800-USB-Mic-Array-p-6488.html), [wiki](https://wiki.seeedstudio.com/respeaker_xvf3800_introduction/) |
| 24 | Camera Module 3 from $25, IMX708, 1080p50; Pi Zero 2 W 2.4 GHz only | Confirmed | [Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/), [Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/). The $15 Zero 2 W price was not shown on the fetched page (UNVERIFIED) |
| 25 | PiDog $179.99 without Pi, GPL-2.0; Freenove CC BY-NC-SA | Confirmed | SunFounder Shopify catalogue; [pidog LICENSE](https://github.com/sunfounder/pidog) GPL v2; [Freenove LICENSE.txt](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi) CC BY-NC-SA 3.0 |

**Effect on recommendations:** the primary pick (Bittle X V2 Alloy pre-assembled at $399, plus XIAO ESP32S3 Sense, plus ReSpeaker XVF3800, plus sensor pack) stands; all its prices and licences are confirmed. The one material change is that the Petoi AI Vision Module ($39) should be bench-tested as a candidate head-cam, since it may offer on-module detection plus Wi-Fi images, instead of being dismissed.

## Omissions added by verifier

1. **Yahboom DOGZILLA-Lite** (Raspberry Pi-based quadruped with robotic arm, marketed with LLM vision and voice): **CM4 $619 (out of stock) / CM5 $639 (available)**, with the compute module included ([Yahboom store JSON](https://category.yahboom.net/collections/dogzilla/products.json), 2026-10-01). It is about 6% over the ~$600 target. Because it runs Linux onboard, it gives native camera access and probably mic access (mic/camera specs UNVERIFIED). It belongs in the head-to-head with PiDog V2 for the Pi track.
2. **Luwu XGO-Lite/XGO-Mini (Raspberry Pi CM4/CM5 desktop dogs with camera, mic, speaker and screen)** were not covered. The vendor site was unreachable during verification, so prices and specs are **UNVERIFIED**. Check them in the Pi track.
3. **ReSpeaker XVF3800 raw-channel firmware:** besides the processed 2-channel 48 kHz firmware, Seeed offers a **16 kHz 6-channel firmware that exposes raw microphone channels**. DoA can be read via `xvf_host` (`AEC_AZIMUTH_VALUES`) or the Python SDK (`DOA_VALUE`) ([wiki](https://wiki.seeedstudio.com/respeaker_xvf3800_introduction/)). This matters for the XAI visualisation: you can show both raw and beamformed audio.
4. **Petoi AI Vision Module as an alternative head-cam** (see correction in §2.1). Detection runs on the module, so the module can supply bounding boxes alone, with "camera images" as a separate toggle. That is a natural privacy-by-design story for the sensor toggles.
5. **Unitree Go2 Air ships without a controller in the $1,600 configuration**; the controller adds $250 ([Unitree shop](https://shop.unitree.com/products/unitree-go2)). Air warranty is 6 months against 12 months for Pro/EDU ([QUADRUPED docs](https://www.docs.quadruped.de/projects/go2/html/Overview_1.html)).
6. **EU product-law pointers for the legal track (UNVERIFIED here; EUR-Lex fetch failed):**
   - The Radio Equipment Directive delegated act (EU) 2022/30 brings in cybersecurity, privacy and fraud requirements (RED Art. 3(3)(d)(e)(f)) for internet-connected radio equipment and radio toys, and applies from 1 Aug 2025. It is relevant to self-built Wi-Fi add-ons, such as an ESP32 head-cam, that are shown to the public.
   - The Cyber Resilience Act (EU) 2024/2847 applies its reporting obligations from Sep 2026.
   - Both are relevant if the team builds and "makes available" Wi-Fi devices, and less so for a one-off research demonstrator. The legal track should confirm.
7. **Nybble Q Alloy version** costs $515, which makes it $116 dearer than Bittle X Alloy pre-assembled ($399) rather than the $36 gap the report's Lite price ($435) implied.

---

## Verification log — second independent pass (2026-10-02)

Web search was available for this pass. Prices come from live Shopify product JSON (`/products/<handle>.js`) wherever the store exposes it; licences come from the GitHub API.

| # | Claim | Verdict | Source / note |
|---|---|---|---|
| A1 | Bittle X V2: $319 / 339 / 379 / 399, +Arm $449 / 469, all in stock | Confirmed | [Petoi JSON](https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled) (all 6 variants `available: true`) |
| A2 | Robot-Advance €406.80 incl. VAT is the pre-assembled **Lite** version | Confirmed (as already corrected) | [Robot-Advance](https://www.robot-advance.com/EN/art-petoi-bittle-x-v2-pre-assembled-dog-robot-5992.htm): "9 servomotors (Lite plastic type)", "On request / shipped within 48 h" |
| A3 | Petoi AI Vision Module $39; Wi-Fi image transmission (module as AP); listed as available | Confirmed | [Petoi JSON](https://www.petoi.com/products/petoi-ai-vision-module-for-arduino) $39, available; [Petoi docs](https://docs.petoi.com/extensible-modules/petoi-ai-vision) "taking photos and transmitting images via Wi-Fi". Resolution and fps are still UNVERIFIED |
| A4 | Bittle AI Head $39, XiaoZhi cloud, phone number required, internet required | Confirmed | [Petoi product](https://www.petoi.com/products/bittle-ai-head-upgrade-kit) / JSON |
| A5 | Sensor pack $44; Nybble Q $435 Lite / $515 Alloy | Confirmed | Petoi JSON (Nybble Q White-Lite variant currently unavailable) |
| A6 | Licences: OpenCatEsp32 MIT, xiaozhi-esp32 MIT, xiaozhi-esp32-server MIT, unitree_webrtc_connect MIT, go2_ros2_sdk BSD-2, wire-pod MIT, PiDog GPL-2.0, SpotMicroESP32-Leika MIT | Confirmed | GitHub API `license.spdx_id`, 2026-10-02. All repos except the Vector SDK were active in 2026 (the Vector SDK was last pushed in Mar 2024) |
| A7 | xiaozhi-esp32-server "4 cores/8 GB recommended" | Corrected | [README](https://github.com/xinnan-tech/xiaozhi-esp32-server): 2C/4G with FunASR; README also warns "do not use in production" (no security assessment) |
| A8 | MechDog $299.99 / 369.99 / 469.99 / 569.99; 560 g, 1500 mAh, ≤60 min, 320×240 camera | Confirmed | [Hiwonder JSON](https://www.hiwonder.com/products/mechdog) |
| A9 | MechDog Advanced includes ESP32-S3 vision, WonderEcho, MP3, dot matrix, touch, light | Confirmed (conflict largely resolved) | [Hiwonder wiki packing list](https://wiki.hiwonder.com/projects/MechDog/en/latest/docs/1.Getting_Ready.html) |
| A10 | MechDog AI $499.99 / 539.99; WonderLLM $39.99; ESP32-S3 vision module $19.99 with Wi-Fi live video via URL (AP/STA), UART/I2C | Confirmed | Hiwonder JSON: [mechdog-ai](https://www.hiwonder.com/products/mechdog-ai), [wonderllm](https://www.hiwonder.com/products/wonderllm), [esp32-s3](https://www.hiwonder.com/products/esp32-s3) |
| A11 | Go2 Air $1,600 (no controller) / $1,850; Pro $2,800 / $3,050; X $4,500 | Confirmed | [Unitree shop JSON](https://shop.unitree.com/products/unitree-go2) |
| A12 | Go2 Air: no voice, no 8-core CPU, no secondary development (EDU only); ≈15 kg; 2.5 m/s; 6-month warranty | Confirmed | [QUADRUPED docs](https://www.docs.quadruped.de/projects/go2/html/Overview_1.html). Reichelt's "21.7 kg" is shipping weight |
| A13 | Go2 Air €2,618 incl. VAT, in stock (Reichelt) | Confirmed | [Reichelt](https://www.reichelt.com/de/en/shop/product/unitree_go2_air_-_the_robot_dog-363565). Ships without a controller; includes a spare 8000 mAh battery |
| A14 | unitree_webrtc_connect v2.2.0, 17 Aug 2026, MIT; per-device AES-128-GCM key since fw 1.1.15, fetched with Unitree account email/password | Confirmed | [PyPI](https://pypi.org/project/unitree_webrtc_connect/) |
| A15 | CVE-2025-35027, CVSS 7.3, Go2/B2/G1/H1, BLE Wi-Fi-config command injection as root, no patched version listed | Confirmed | [GHSA-27p8-m7h9-xchc](https://github.com/advisories/GHSA-27p8-m7h9-xchc) (published 26 Sep 2025; patched versions "unknown") |
| A16 | FCC Covered List, 28 Jul 2026, foreign-produced "advanced robotic devices"; >4.4 lb threshold; existing authorisations unaffected | Confirmed (threshold now verified) | [FCC fact sheet](https://docs.fcc.gov/public/attachments/DOC-423682A1.pdf) (date, scope, grandfathering), [Sidley](https://www.sidley.com/en/insights/newsupdates/2026/08/fcc-adds-all-foreign-produced-advanced-robotic-devices-to-the-covered-list) (>4.4 lb, ≥200 kbps, sensor) |
| A17 | Quaddle $99/$139/$199, +$18 EU shipping, Dec 2026; Scout has PIR + 2 mics | Confirmed, with notes | [CNX](https://www.cnx-software.com/2026/09/04/petoi-quaddle-a-mini-robot-dog-for-physical-ai-experimentation/): PIR + 2 mics on every tier's extension hat; battery BL10C 1800 mAh. Prices were early-bird; [Petoi page](https://www.petoi.com/pages/quaddle-educational-robot-kit) now lists $144/$175/$215 |
| A18 | aibo: Japan sales ended June 2026; US continues; $2,899.99 | Partly corrected | [TechXplore](https://techxplore.com/news/2026-06-sony-discontinues-japan-sales-robot.html): Japan sales end "once stock runs out"; US price "over $3,000"; not sold elsewhere. $2,899.99 is UNVERIFIED on a Sony page |
| A19 | Vector 2.0 $249.99; SDK audio "to come" | Confirmed | [anki.bot JSON](https://anki.bot/products/vector-robot) (Black $249.99 in stock); [audio.py](https://raw.githubusercontent.com/kercre123/wirepod-vector-python-sdk/master/anki_vector/audio.py) |
| A20 | Loona $499; SDK never shipped, Blockly only; GPT-4o "free for the moment" | Confirmed (secondary sources) | [Robozaps](https://blog.robozaps.com/b/loona-robot-review), [KEYi blog](https://keyirobot.com/blogs/insights/loona-petbot-review-2026) |
| A21 | XIAO ESP32S3 Sense $13.90 (OV2640, digital mic, 8 MB PSRAM); ReSpeaker XVF3800 $54.90 (AEC/AGC/DoA/VAD/beamforming, 360°, 5 m, USB/I2S); Pi Zero 2 W $15, 2.4 GHz only | Confirmed | [Seeed XIAO](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html), [Seeed XVF3800](https://www.seeedstudio.com/ReSpeaker-XVF3800-USB-Mic-Array-p-6488.html) (in stock; $49.90 at 10+), [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) ("$15 computer"; 2.4 GHz b/g/n) |
| A22 | PiDog $179.99 (no Pi); Freenove $129.99; PuppyPi from $589.99 | Confirmed | SunFounder JSON, [Freenove JSON](https://store.freenove.com/products/fnk0050), [Hiwonder PuppyPi JSON](https://www.hiwonder.com/products/puppypi) (Pi 4B 4 GB standard $589.99; Pi 5 2 GB $599.99) |

**Effect on recommendations:** no change to the primary pick. The prices for Bittle X V2 Alloy pre-assembled ($399), XIAO ESP32S3 Sense ($13.90), ReSpeaker XVF3800 ($54.90) and the sensor pack ($44) were all re-confirmed live on 2026-10-02. The runner-up (MechDog Advanced, $369.99) is strengthened, because the official packing list includes the camera module, WonderEcho, touch, light, MP3 and dot matrix.

## Omissions added by verifier — second pass

1. **ELECFREAKS CM4 XGO-Lite** (Raspberry Pi CM4 desktop quadruped, 12 DOF, Python/blocks): **$599**, currently **sold out** on the official ELECFREAKS store ([ELECFREAKS JSON](https://shop.elecfreaks.com/products/elecfreaks-cm4-xgo-robot-dog-kit-for-raspberry-pi), 2026-10-02). It sits exactly at the budget cap and runs Linux onboard (native camera access). Compare it in the Pi track; mic/camera specs are UNVERIFIED here.
2. **Waveshare PIPPY** (open-source Raspberry Pi bionic dog) appeared in search but was not evaluated. Price and specs are UNVERIFIED ([Waveshare](https://www.waveshare.com/pippy.htm)).
3. **FCC rule applies to new foreign-made models of any brand and nationality** (the fact sheet says "regardless of the nationality of origin"). For a later US showing, new models over 4.4 lb (e.g. Go2 successors, larger dogs) could be blocked from authorisation. Bittle X, MechDog and Quaddle are under the weight threshold. This has no EU legal effect.
4. **xiaozhi-esp32-server self-hosting caveat:** the project itself says it is not production-ready and has had no security assessment. If the XiaoZhi-head route is pursued, budget for your own security review, or avoid it, in line with the report's recommendation.
5. **PuppyPi pricing now starts at $589.99 (Pi 4B 4 GB) or $599.99 (Pi 5 2 GB)**. Only the base PuppyPi configurations fit the ~$600 cap; see the Pi track.
