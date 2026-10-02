# 09 - Ethics, privacy, child safety and law for "How does a robot see you?"

Research track 09 for the TUAI (MSCA DN, GA 101168344) Science is Wonderful! 2027 demonstrator.
Prepared 2026-10-01; revised 2026-10-02 (continuation pass: resolved several UNVERIFIED items, added SUT internal rules, Polish AI Act, EDPB anonymisation guidelines). All sources accessed 2026-10-01/02 unless stated. Sources are cited as [S#] and listed at the end. Anything not confirmed against a source is marked **UNVERIFIED**.
This is a research brief, not legal advice. The SUT Data Protection Officer (IOD@polsl.pl [S16]) must sign off on the final design.

---

## 0. TL;DR (decisions)

1. **The exhibit falls under both the GDPR and the EU AI Act.** Live camera and microphone processing of identifiable visitors is processing of personal data even if nothing is saved [S1 Art. 4(1),(2); S7 example 5, para. 115; S11]. The AI Act applies because SUT will develop the system and use it itself at a public event ("putting into service for own use"). The research exclusions in Art. 2(6) and 2(8) do not cover a public outreach exhibit [S2; S4 paras 30-32; S5 para. 21].
2. **The real audience is different from what we assumed.** SiW 2027 runs on **17-19 March 2027 in Brussels**, with mostly **school groups aged 7-18**, about 4,500 pupils, roughly **15 minutes per group** at an **8 m² booth**, and visitors speaking mostly **FR/NL** [S18]. Expect many bystanders, teachers who are at work, and almost no parents.
3. **Do not infer emotion. Treat it as prohibited.** Art. 5(1)(f) bans emotion inference in "education institutions" and "workplaces". The Commission reads "workplace" broadly: it covers museums and temporary sites, whatever the person's status (staff, volunteers, and teachers accompanying pupils) [S4 paras 254-255]. [corrected by verifier: the workplace limb protects the people *working* there, not visitors. The same guidelines say a call centre tracking its *customers'* emotions "is not prohibited", and a supermarket detecting suspicious customers is not prohibited "when it is ensured that no employees are being tracked" (S4, examples after paras 254-255). Emotion inference on visiting pupils is therefore prohibited only if staff or teachers are caught by it, or if the fair counts as an "education institution" context, which is unsettled. In a crowded booth we cannot ensure that staff and teachers are excluded, so "treat it as prohibited" remains the right design decision, but do not claim in the proposal that the law flatly bans it for visitors.] Outside those areas emotion recognition is still **high-risk** (Annex III 1(c)) [S4 para. 239; S6]. Detecting a smile **as a facial movement** is allowed. Saying "you are happy" is not [S2 rec. 18; S4 para. 249].
4. **Never infer race/ethnicity or skin tone.** Art. 5(1)(g) prohibits it, and GDPR Art. 9 also applies [S2; S4 paras 271-283]. **Also avoid** age, gender, hair colour, height, accent and "personality". These count as biometric categorisation and trigger an Art. 50(3) duty to inform. They also bring bias, inaccuracy and child-harm risks, and they add little teaching value [S5 para. 104; S29; S30].
5. **Safe signals ("observe, don't judge"):** clothing colour, glasses, gestures and waving, distance, number of people, live loudness/pitch meters, words from a small fixed list (for example "favourite animal"), ambient noise. Present all of these as momentary readings, never as traits of the person.
6. **Privacy by design:** everything runs on the device and offline, in RAM only, with nothing written to disk. Sensors are off by default and started with a physical button. The camera has a physical shutter. Processing is limited to a defined interaction zone. The public screen shows an abstract figure, not raw video. No face recognition or re-identification. The robot has no vendor cloud connection [S1 Art. 25; S7 paras 126-129; S11].
7. **Lawful basis:** use GDPR Art. 6(1)(e), public task. SUT's statutory duty includes "upowszechnianie i pomnażanie osiągnięć nauki" (disseminating science) [S15 Art. 11(1)(9)]. The opt-in button is an ethical safeguard and a practical way to object, not the legal basis. Consent is weak here (power imbalance, children) [S1 rec. 43; S8]. GDPR Art. 8 does **not** apply because the exhibit is not an online service [S8 paras 127-128].
8. **Run a DPIA, done formally but short.** At least two WP248 criteria are met (children, innovative technology, evaluation, monitoring a publicly accessible space) [S9]. UODO's list gives "interactive toys" and "services and toys dedicated to children" as examples [S14]. Consult the DPO. Get a university ethics opinion if any research data at all would be collected (recommendation: collect none at SiW).
9. **Takeaway for visitors:** by default nothing. Optionally, a locally printed card with no face and no name. No email, and no QR code that points to a server.
10. **AI Act timeline (after the Digital Omnibus, Reg. (EU) 2026/1744 of 8 Jul 2026, OJ 24 Jul 2026, in force 27 Jul 2026):** Art. 5 applies since 2 Feb 2025 and Art. 50 since 2 Aug 2026, so both bind us at the fair. Annex III high-risk obligations moved to **2 Dec 2027**, after the fair [S2 Art. 113; S3; S3a; S3b; S3c].
11. **SUT's own rules add three concrete duties** that a GDPR/AI Act analysis alone would miss:
    - **Child-protection standards** (Rector's Order 50/2024). Publishing a recorded image of a child needs the guardian's written consent. Staff must not record minors for private purposes. §5(3) says minors' image data are processed "na podstawie zgody opiekunów" (on guardian consent) [S40]. This sits awkwardly with our public-task basis, so the DPO must rule on it. Plan B is in section 10.
    - **Staff verification.** Every booth staffer (doctoral candidates included) must be checked in the Polish Register of Sex Offenders. The HR request goes in **at least 7 days** before the person works with minors (Order 37/2024 as amended by 240/2024) [S41]. [corrected by verifier: the register check is not the only duty. Art. 21 of the Polish Act of 13 May 2016 (as amended from 15 Feb 2024) also requires criminal-record information from the Polish KRK. Anyone who holds another citizenship, or who has lived in another country in the last 20 years, must also obtain a criminal-record certificate from that country, or make a sworn statement where that country does not issue one (Ministry of Justice FAQ: https://www.gov.pl/web/sprawiedliwosc/pytania-do-ustawy-o-ochronie-dzieci2). MSCA doctoral candidates are usually non-Polish because of the mobility rule, so foreign certificates can take weeks. Start in Jan 2027, not 7 days before. A further amending Act of 5 Aug 2025 exists; its effect on Art. 21 is **UNVERIFIED**, so check with HR.]
    - **Internal DPIA procedure.** It runs in the "RIG" software with the Information Security Office (BBI) and the DPO. [corrected by verifier: SUT's organisational chart as of 1 Jan 2026 lists no BBI. The DPO now sits in the "Biuro Kontroli Zarządczej i Bezpieczeństwa" (BKZB, BKZB@polsl.pl). Route the DPIA through BKZB/IOD, and ask whether Order 62/2024 has been amended (**UNVERIFIED**).] Privacy-by-design requirements must be written into procurement specs, which covers buying the robot (Order 62/2024 §§16-17) [S42].

---

## 1. Facts about the event that drive the analysis

| Fact | Value | Source |
|---|---|---|
| Event | Science is Wonderful! 2027, MSCA science fair, Brussels | [S18] |
| Dates | Set-up 16 Mar 2027; fair 17 Mar (9-13h), 18-19 Mar (9-15h). The form's timeline section says "16-19 March 2026", which looks like a typo | [S18] |
| Proposal deadline / results | 6 Oct 2026 / 28 Oct 2026; communication workshop 4 Nov 2026 | [S18] |
| Audience | "thousands of primary and secondary school pupils", about 4,500 per year, ages "7 to 18"; groups "from a small group of friends to an entire school class"; "on average, groups will spend 15 minutes at your booth" | [S18] |
| 2026 edition | Maison de la Poste, Tour & Taxis, Brussels; "open to everyone"; schools and groups of 10+ must register | [S19] |
| Booth | 8 m² (4x2 m), low table, TV + HDMI, Wi-Fi, standard lighting | [S18] |
| Language | Visitors "mostly French and Dutch"; language assistants on site | [S18] |
| Giveaways | "we cannot pay for 'goodies' or giveaways"; teams may bring their own materials | [S18] |
| Controller | Silesian University of Technology (SUT), coordinator of TUAI, GA 101168344; DPO: IOD@polsl.pl, tel. 32 400 3077 | [S16; S17] |

**Implications.** (i) Most visitors come as pupils on a school trip. Teachers are present and at work, and parents mostly are not. (ii) A whole class crowds a small booth, so the camera will capture many non-participants. (iii) There are about 15 minutes per group, so the 3-5 minute single-visitor flow has to become a group demo plus 1-3 hands-on participants. (iv) All notices must be in FR/NL/EN with pictograms.

---

## 2. Legal map at a glance

| Instrument / provision | Applies? | What it means for us | Applies from |
|---|---|---|---|
| GDPR Art. 4(1),(2): personal data, processing | Yes | Live video and audio of identifiable people is processing even without storage | 25 May 2018 [S1] |
| GDPR Art. 9: special categories (biometric only when processed "for the purpose of uniquely identifying") | Avoidable | No face recognition or re-identification, so biometric data stays outside Art. 9. Never infer ethnicity, health or religion | [S1; S7 paras 74-82] |
| GDPR Art. 6: lawful basis | Yes | Art. 6(1)(e) public task (SUT), plus an ethical opt-in | [S1; S15] |
| GDPR Art. 8: child consent for ISS | No (on site) | Only relevant if we deliver results through an online service | [S8 paras 127-128] |
| GDPR Arts 5(1)(c),(e), 12-13, 25 | Yes | Minimisation, no retention, child-friendly layered notice, privacy by design and by default | [S1] |
| GDPR Art. 35: DPIA | Strongly advised (likely required) | At least two WP248 criteria; UODO list criterion 10 | [S9; S14] |
| AI Act Art. 5(1)(f): emotion inference at work or in education | Risk | Do not build it | 2 Feb 2025 [S2 Art. 113(a)] |
| AI Act Art. 5(1)(g): biometric categorisation for race etc. | Risk | Never infer race/ethnicity | 2 Feb 2025 |
| AI Act Art. 50(1): tell people they are interacting with AI | Yes (the robot is an AI interacting with people; "robotic companion pets" are listed as in scope) | Child-friendly disclosure plus reminders | 2 Aug 2026 [S2; S5 paras 34, 40] |
| AI Act Art. 50(3): notice for emotion recognition / biometric categorisation | Only if we categorise from biometric data | Avoid it by design, but post the notice anyway | 2 Aug 2026 [S5 paras 99-108] |
| AI Act Art. 50(2)/(4): synthetic content marking / deep fakes | Only if we generate images or audio | Avoid generative portraits | 2 Aug 2026; grace to 2 Dec 2026 only for systems on the market before 2 Aug 2026 [S3a; S3b] |
| AI Act Annex III: high-risk | No (argued in section 4.6) | Document the reasoning | 2 Dec 2027 for Annex III (Omnibus) [S3a-c] |
| Belgian image right (Code de droit économique Art. XI.174) | Yes for any photos or video of visitors | Do not photograph children | [S13] |
| Polish AI Systems Act (ustawa o systemach sztucznej inteligencji) | Yes for SUT as a Polish provider | Creates KRiBSI as Poland's single AI market-surveillance authority. It adds no new substantive duties | Published 27 Jul 2026; main part in force 11 Aug 2026; full application 28 Oct 2026 [S45] |
| Belgian AI Act authority | Yes at the fair | BIPT/IBPT is designated by government policy; as of mid-2026 the statute was not yet adopted (**UNVERIFIED**, secondary sources only) | [S46] |
| SUT Child-protection standards (Order 50/2024; based on Art. 22c of the Polish child-protection Act) | Yes (binds SUT staff) | No recording for private purposes; guardian's written consent to publish a child's image; crowd exception; group framing | 21 Mar 2024 [S40] |
| SUT staff verification (Order 37/2024 as amended by 240/2024) | Yes | Register check for every booth staffer, requested from HR at least 7 days in advance | 9 Dec 2024 amendment [S41] |
| SUT Data protection policy (Order 62/2024) | Yes | DPIA in RIG via BBI plus DPO; privacy by design in procurement specs | In force 1 May 2024 [S42] |

---

## 3. GDPR analysis

### 3.1 Transient, in-memory processing is still processing
- "Personal data" is information relating to an identified or identifiable person, including by reference to "factors specific to the physical, physiological, genetic, mental, economic, cultural or social identity" [S1 Art. 4(1)]. "Processing" means "any operation ... whether or not by automated means", including collection, use, consultation and erasure [S1 Art. 4(2)]. Storage is not required.
- EDPB, example 5: temporary biometric templates "constitute biometric data", and a system "would be unlawful if it captures visitors or passers-by who have not consented ... **even if their template is deleted within the shortest possible period**" [S7, example after para. 82].
- EDPB treats **live monitoring** as processing that needs transparency. If no recording is announced, people "should be able to trust that there is solely a live monitoring" [S7 para. 115].
- CNIL describes augmented cameras that "captent automatiquement l'image ... la traitent souvent instantanément" as personal-data processing. Its recommended safeguards are lower definition, frugal data use, local processing, near-immediate deletion of source images, and anonymous outputs such as counting [S11].
- **Conclusion:** "we don't store anything" lowers risk a great deal, but it does **not** take us outside the GDPR.

### 3.2 Biometric data and Art. 9
- GDPR Art. 4(14) defines biometric data as data "resulting from specific technical processing ... which allow or confirm the unique identification". Art. 9(1) prohibits processing "biometric data for the purpose of uniquely identifying a natural person" [S1; S39]. Recital 51: photographs are biometric data "only when processed through a specific technical means allowing the unique identification" [S1].
- EDPB three-part test: nature of the data, specific technical processing, and **purpose of unique identification** [S7 paras 74-76]. "When the purpose of the processing is ... to distinguish one category of people from another but not to uniquely identify anyone the processing does not fall under Article 9". Example: age/gender-targeted advertising without templates is outside Art. 9 [S7 para. 80, example 4].
- **Trap:** if the system "detect[s] a data subject re-entering the area", the purpose "would then be to uniquely identify a natural person" and Art. 9 applies "from the start" [S7 para. 82]. So no "welcome back!" feature, and no face embeddings.
- The definitions differ. The AI Act's "biometric data" (Art. 3(34)) leaves out the unique-identification element, so it is much broader than the GDPR's [S2; S4 fn. 160]. Pose, voice and facial features are "biometric data" for AI Act purposes even when the GDPR does not treat them as Art. 9 data.
- Inferences that **reveal** ethnicity, health or religion (for example from skin tone, a wheelchair or a headscarf) would be Art. 9 data under the "revealing" wording of Art. 9(1) [S1]. The CJEU confirmed this broad reading in **C-184/20 *OT*** (1 Aug 2022). "Revealing" covers data that disclose sensitive information indirectly, through deduction or cross-referencing (paras 122-127, paraphrased from the dpcuria summary). The Court held that a narrow reading would undermine the effectiveness of Art. 9 protection [S43]. So a model that only *outputs* "headscarf" or "dark skin" is already processing Art. 9 data, even if nobody intends to infer religion or ethnicity.

### 3.3 Lawful basis (Art. 6) for a university outreach event

| Basis | Fit | Notes |
|---|---|---|
| (a) Consent | Poor | Recital 43 says consent is not valid where there is "a clear imbalance ... in particular where the controller is a public authority" [S1]. Pupils in a school group, with teacher and peer pressure, cannot easily give consent that is "freely given". Parental consent is impractical (parents are absent). Art. 8 (the 16/13 age threshold) only applies to information-society services, i.e. services provided "at a distance", which an in-person booth is not [S8 paras 125-128]. |
| (e) Public task | **Recommended** | SUT "jest publiczną uczelnią akademicką" (Statute §1(1)) [S44]. Its "basic tasks" include "upowszechnianie i pomnażanie osiągnięć nauki i kultury" [S15 Art. 11(1)(9)], which satisfies Art. 6(3)'s requirement for a basis in Member State law. **Wording confirmed unchanged in the current consolidated text, Dz.U. 2024 poz. 1571** [S15]. The processing must be *necessary* and proportionate, hence minimisation. |
| (f) Legitimate interests | **Not available** (in practice) | Not available to "public authorities in the performance of their tasks" [S1 Art. 6(1) last subpara.]. Public universities are units of the public finance sector (Public Finance Act Art. 9(11), consolidated Dz.U. 2025 poz. 1483). Polish law treats such units as "organy i podmioty publiczne" for GDPR Art. 37(1)(a) (Polish Data Protection Act Art. 9(1), Dz.U. 2019 poz. 1781) [S44]. That strongly suggests SUT is a public body acting within its tasks, so (f) is out. The DPO should confirm (the Art. 37 classification is our inference applied to Art. 6). If (f) were ever used, the balancing test must give special weight "where the data subject is a child" [S1 Art. 6(1)(f)]. |

**Tension with SUT's internal child-protection standards (resolve with the DPO before the proposal is final).** Order 50/2024, §5(3), states: "Dane osobowe małoletnich są przetwarzane w celu realizacji obowiązków prawnych lub na podstawie zgody opiekunów małoletniego (wizerunek)", meaning minors' data are processed for legal obligations or, for images, on the guardians' consent [S40]. Read literally, any camera processing of a child's image would need guardian consent. Two arguments go the other way:
- the image-specific rules (§6) are about **publishing a recorded** ("utrwalony") image, and our design records and publishes nothing;
- the Art. 6(1)(e) public-task basis is set by law, which an internal order cannot narrow for legal purposes.

Still, an internal rule binds the staff. Ask the DPO for a written position. If the DPO requires guardian consent, use **Plan B** (section 10): camera mode only for groups whose teacher confirms the school holds parental consent for this activity; everyone else gets the full no-camera mode.

**How the opt-in fits.** Under (e), visitors have a right to object (Art. 21). The design makes objecting effortless: nothing is processed until the child presses "start", and a "stop / forget me" button works at any time. CNIL notes that objection is usually impossible with augmented cameras unless there is an opt-in before analysis [S11]. That is what we provide. On signs, avoid the word "consent". Use "you decide whether the robot can see/hear you".

### 3.4 Principles that shape the design
- **Minimisation** (Art. 5(1)(c)): "adequate, relevant and limited to what is necessary" [S1]. Every signal needs a teaching reason (see the attribute table in section 8).
- **Storage limitation** (Art. 5(1)(e)): keep data identifiable "for no longer than is necessary" [S1]. Here that means RAM, for the duration of the session.
- **Privacy by design and by default** (Art. 25): measures "such as pseudonymisation ... data minimisation"; by default only the data needed for each purpose [S1]. EDPB adds "Functions provided, but not necessary, must be deactivated" and recommends "masking or scrambling areas that are not relevant" [S7 para. 129].
- **Children** (recital 38): "Children merit specific protection". This applies "in particular" to "creating personality or user profiles" [S1]. That argues against "interaction style" or "personality" inferences.
- **Transparency** (Art. 12(1), recital 58): information "addressed specifically to a child" must use language "that the child can easily understand"; recital 58 also allows "visualisation" [S1]. Art. 13 information is given at the time of collection, in layers (warning sign first, then full notice) [S7 paras 112-115].
- **Art. 11** (processing that does not require identification): we do not have to collect extra data just to answer access requests [S1]. Say so in the second-layer notice.
- **Art. 22 / profiling:** the exhibit makes no decisions with legal or similarly significant effects. Still, avoid anything that looks like a "profile" (recital 71 defines profiling as evaluating "personal preferences or interests, reliability or behaviour") [S1].

### 3.5 Is a DPIA needed? Effectively yes, so do one
- Art. 35(1) requires a DPIA where processing, "in particular using new technologies", is "likely to result in a high risk" [S1; S39].
- WP248 criteria (endorsed by the EDPB): "a processing meeting two criteria would require a DPIA" "in most cases" [S9].

| WP248 criterion [S9] | Met? |
|---|---|
| 1 Evaluation or scoring (incl. profiling) | Partly: "building a representation of you" |
| 3 Systematic monitoring of a publicly accessible area | Partly: a camera at a public fair. Reduced by the opt-in zone |
| 7 Vulnerable data subjects: "Vulnerable data subjects may include children" | **Yes** |
| 8 "Innovative use or applying new technological or organisational solutions" | **Yes**: AI plus a robot plus camera and microphone |
| 4, 5, 6, 9 (sensitive data, large scale, matching, preventing rights) | No, by design |

- **UODO list** (M.P. 2019 poz. 666), which applies to SUT as a Polish controller: "co do zasady" two or more criteria require a DPIA. Criterion 10 (innovative technology) gives examples including "Zabawki interaktywne", "Usługi i zabawki dedykowane dzieciom" and devices with "głośnik, mikrofon, kamera" [S14]. Note: the speaker/microphone/camera example covers devices with "oprogramowanie i system łączności umożliwiające przekazywanie danych poprzez sieci telekomunikacyjne". An offline set-up therefore weakens that one example, but "interactive toys" and "services and toys dedicated to children" still apply.
- **Belgian APD list** (Decision SG 01/2019): item 1 covers biometric data for unique identification in places accessible to the public, and item 8 covers large-scale systematic observation of behaviour. Neither is triggered if we stay small and avoid identification [S12]. The Belgian APD calls facial recognition high-risk and says a DPIA is required for it [S13, facial recognition page].
- ICO Children's Code, standard 2, also requires a DPIA for services likely to be used by children (UK law, used here as good practice) [S24].
- **SUT's internal procedure** (Data protection policy, Order 62/2024, §16) [S42]:
  - §16(1): a DPIA is required before a "nowy rodzaj przetwarzania – w szczególności z użyciem nowych technologii" that is likely to be high-risk.
  - §16(2): a 12-item screening list. Item 1 is evaluation or behavioural analysis, item 3 systematic monitoring of public places "wykorzystujące elementy rozpoznawania cech", item 10 "innowacyjne rozwiązania technologiczne".
  - §16(3): the DPIA "odbywa się z wykorzystaniem oprogramowania RIG", carried out by the Information Security Office (BBI) together with the person responsible for the new processing.
  - §16(4): both the screening decision and the DPIA itself are consulted with the DPO.

  So the DCs do not write a stand-alone DPIA in a vacuum. They supply the content (data flow, risk register, measures) to BBI and the DPO, who run it in RIG. [corrected by verifier: "RIG" is defined in the Policy as "Reed Into Green" software. BBI no longer appears in the 1 Jan 2026 organisational chart. The data-protection function and DPO are under BKZB (https://www.polsl.pl/bkzb/ochrona-danych-osobowych/), so contact BKZB/IOD.]

### 3.6 Photos and video at the event (people, not the AI)
- Belgian image right (Code de droit économique Art. XI.174): taking **and** using an image of a person requires that person's consent, given separately for each. "La jurisprudence admet de plus en plus souvent qu'un mineur disposant de la capacité de discernement donne lui-même son consentement"; before that, both parents must agree. People who appear only incidentally, or in crowds where no one is singled out, are exceptions [S13].
- SiW organisers: we found no published SiW rules on filming pupils [S18; S19] (**UNVERIFIED** whether schools sign photo consents). Ask EAC-MSCA-SIW@ec.europa.eu / schools-SIW@spectraconsortium.eu [S18; S19].
- **Polish guidance (applies to SUT as controller, and to anything SUT publishes).** The UODO-backed guide *Wizerunek dziecka w internecie. Publikować czy nie?* (Fundacja Orange with UODO as content partner, Warsaw, June 2024) [S47] says:
  - The crowd exception (Copyright Act Art. 81) covers an image that is only "szczegół takiej całości, jak zgromadzenie, krajobraz, impreza publiczna", where the photo shows the event, the participants are not the dominant element, and there is no close-up of one person or a small group.
  - **But** "jeżeli uwidocznioną na zdjęciu osobę można zidentyfikować, wizerunek będzie stanowił daną osobową", so the GDPR still applies even when no image-right consent is needed.
  - Recommended alternatives: images without identifying features, showing the *results* of children's activities (e.g. drawings), and covering faces with graphic stickers or blur **before** upload, in an editing tool rather than the platform's own tools.
- **SUT standards (Order 50/2024)** [S40]:
  - §6(1): publishing a child's image recorded in any form "wymaga pisemnej zgody opiekuna dziecka", and it is good practice to also get the child's consent.
  - §6(3): the crowd/public-event exception.
  - §7: do not caption with names; photos should show what the child is doing, "w grupie, a nie jako pojedynczą osobę".
  - §9: no media recording of children without written guardian consent.
  - The staff code bans recording minors "na potrzeby prywatne".
- **Rule for the team:** no photos or videos of identifiable children for dissemination. Document the booth empty, show staff, or film the robot's screen showing abstract output only. If the SiW organisers' photographers shoot at our booth, that is presumably their processing under the Commission's own notice (**UNVERIFIED**: no SiW photo policy found on the 2026 or 2027 pages [S18; S19]), but our staff must not ask children to pose for it.

---

## 4. EU AI Act (Regulation (EU) 2024/1689)

### 4.1 Timeline after the Digital Omnibus on AI
- Original Art. 113: general application 2 Aug 2026; Chapters I-II (incl. Art. 5) from **2 Feb 2025**; Art. 6(1) from 2 Aug 2027 [S2].
- **Regulation (EU) 2026/1744** of 8 Jul 2026 ("Digital Omnibus on AI") was published in OJ L on 24 Jul 2026 and entered into force on **27 Jul 2026**, the third day after publication [S3; S3a; S3b; S3c]. Its main changes:
  - Annex III high-risk obligations ("Sections 1, 2 and 3 of Chapter III") move to **2 Dec 2027**, and Annex I to **2 Aug 2028** [S3].
  - Machine-readable marking under Art. 50(2) for generative systems placed on the market **before** 2 Aug 2026 gets until **2 Dec 2026**. Systems placed on the market later must comply immediately [S3a; S3b].
  - The rest of Art. 50 applies from **2 Aug 2026**, unchanged (the Omnibus only touched Art. 50(7)) [S3; S3c].
  - Art. 4 (AI literacy) becomes a duty of means. The OJ text reads "Providers and deployers of AI systems shall take measures to support the development of AI literacy of their staff and other persons dealing with the operation and use of AI systems on their behalf" [S3].
  - New Art. 5(1)(ba) and (bb) ban AI that generates non-consensual intimate imagery of identifiable persons and child sexual abuse material. They apply from **2 Dec 2026** according to three consistent secondary sources [S3a; S3b; S3c]. A model summary of the OJ text suggested they apply immediately, but we could not see the Art. 113 wording ourselves. Either way, they bind us at the fair and point the same way: never run generative image models on photos of children.
  - **Verification note:** the OJ text was reachable through the ELI link in this pass, but only partly (title, date, entry into force, Art. 4 and Art. 113 Annex dates were confirmed). The full Art. 113 text was cut off.
- **At SiW (17-19 Mar 2027):** Art. 5 and Art. 50 apply. Annex III obligations do not apply yet, but avoiding high-risk features matters anyway: they bring ethics problems, and any reuse after Dec 2027 would be caught.
- **National enforcement.** In Poland, the *ustawa o systemach sztucznej inteligencji* (published 27 Jul 2026, main part in force 11 Aug 2026, full application 28 Oct 2026) sets up **KRiBSI** (Komisja Rozwoju i Bezpieczeństwa Sztucznej Inteligencji) as the single market-surveillance authority, cooperating with UODO [S45]. [verifier: confirmed. The act of 3 Jul 2026 is Dz.U. 2026 poz. 1003 (https://www.infor.pl/akt-prawny/DZU.2026.208.0001003,metryka,ustawa-o-systemach-sztucznej-inteligencji.html). Inspections, fines and proceedings start on 28 Oct 2026.] In Belgium, BIPT is the designated lead authority by government decision; secondary sources say the implementing law was not yet adopted in mid-2026 (**UNVERIFIED**) [S46].
- **GDPR "Digital Omnibus" (COM(2025) 837, procedure 2025/0360(COD))** is still at first reading in the EP committees (ITRE/LIBE): draft report 22 Jun 2026, amendments 27 Jul 2026, no adoption. The current GDPR text applies and will very likely still apply in March 2027. Re-check in Feb 2027 (https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2025/0360(COD)).

### 4.2 Are we in scope? Yes
- SUT develops the system and uses it under its own name, so it is the **provider**. It also uses it, so it is the **deployer** [S2 Art. 3(3),(4)]. "Putting into service" includes supply "for own use in the Union for its intended purpose" [S2 Art. 3(11)].
- Art. 2(6) excludes systems "specifically developed and put into service for the **sole purpose** of scientific research and development". A public outreach exhibit is not "sole purpose" research. The Art. 50 guidelines add: "if those systems are put into service ... for other purposes than for the sole purpose of scientific research ... the relevant transparency obligations ... would still need to be complied with" [S5 para. 21].
- Art. 2(8) covers R&D "prior to ... being placed on the market or put into service". It does not cover real-world use, and "Testing in real world conditions ... is not covered by that exclusion" [S4 para. 32; S5 para. 22].
- Art. 2(12) (open-source licences) does not exempt systems that fall under Art. 5 or 50 [S2].

### 4.3 Art. 5(1)(f): emotion recognition at work and in education. Do not build it
- The text prohibits AI systems "to infer emotions of a natural person in the areas of workplace and education institutions, except ... for medical or safety reasons" [S2].
- "Emotion recognition system": emotions or intentions inferred "on the basis of their biometric data" [S2 Art. 3(39)]. Recital 18 lists "happiness, sadness, anger, surprise, disgust, embarrassment, excitement, shame, contempt, satisfaction and amusement" [S2]. The list is "not exhaustive", and calling an emotion an "attitude" does not get around the ban [S4 paras 247-248].
- **Education institutions:** the term is "broad", covers public and private institutions, and has "no limitation as regards the types or ages of pupils". Institutions are "normally accredited". Example: emotion recognition "to infer the interest and attention of students is prohibited" [S4 para. 255]. Whether a school trip to an external fair is "in the area of" education institutions is not settled. The Future of Privacy Forum's analysis of the Guidelines (Dushi, 24 Mar 2026) notes the Guidelines interpret both contexts "broadly" but "do not clarify whether this extends to temporary locations (museums, fairs) or off-campus educational activities" [S48]. No authority found either way (**UNVERIFIED**). SUT itself is an education institution. Even without this point, the workplace limb covers the booth, so the conclusion stands.
- **Workplace:** "any specific physical or virtual space where natural persons engage in tasks ... spanning from ... publicly accessible spaces like shops, stadiums or museums ... as well as temporary or mobile work sites ... independent from the status as an employee, contractor, trainee, volunteer" [S4 para. 254]. The booth is the workplace of our staff and of the accompanying teachers. [corrected by verifier: this limb protects workers, not customers or visitors. The Guidelines' own examples: a call centre tracking "customers emotions, such as anger or impatience, is not prohibited by Article 5(1)(f)", and supermarket cameras for customers are not prohibited "when it is ensured that no employees are being tracked" (S4, examples following para. 254). So the workplace limb catches our booth only because staff and teachers would be in frame. That cannot be reliably prevented at a crowded booth, so the precautionary "do not build it" conclusion stands. The legal basis for it is the risk of capturing workers plus the unsettled education-institution question, not a general ban on visitor emotion recognition. Outside Art. 5, emotion recognition of visitors would still be Annex III 1(c) high-risk (from 2 Dec 2027) and trigger the Art. 50(3) notice now.]
- Outside those areas, emotion recognition is **high-risk** under Annex III 1(c) [S4 paras 239, 266]. The draft high-risk guidelines give as examples a gaming system that infers players' "excitement, anger, frustration, amusement" and a mood-monitoring smartwatch, where "It is not relevant whether the emotion recognition results are disclosed solely to the specific user" [S6 §3.1.4].
- **What is allowed:** "The observation that a person is smiling is not emotion recognition", whereas "Concluding that a person is happy is emotion recognition" [S4 para. 249; S6 §3.1.4]. Recital 18 also excludes "the mere detection of readily apparent expressions, gestures or movements" and voice features "such as a raised voice or whispering" unless they are used to infer emotions [S2].
- **Science and policy:** recital 44 records "serious concerns about the scientific basis", including "limited reliability, the lack of specificity and the limited generalisability" [S2]. Barrett et al. (2019) review the evidence against reading emotion from facial movements [S28]. The EDPB/EDPS called emotion inference "highly undesirable" and said it "should be prohibited" [S10 para. 35]. UNICEF 3.0 says practices relying on "emotional analytics" should be prohibited from engaging with children [S22]. CRC General Comment 25 flags "emotional analytics or inference" and automated inferences "about a child's inner state" [S23 para. 62].

### 4.4 Art. 5(1)(g): prohibited biometric categorisation
- The text prohibits systems "that categorise individually natural persons based on their biometric data to deduce or infer their race, political opinions, trade union membership, religious or philosophical beliefs, sex life or sexual orientation" [S2].
- Five conditions must all be met [S4 para. 273]. Individual categorisation includes "'Attribute Estimation' ... 'age, gender, ethnicity' ... face, height, or skin, eye and hair colour" [S4 para. 282].
- **Outside "biometric categorisation" altogether:** "categorisation according to clothes or accessories, such as scarfs or crosses" [S4 para. 277]. So clothing colour is fine under the AI Act. Head coverings and religious symbols remain a GDPR Art. 9 "revealing" risk.
- **Biometric categorisation that is not prohibited** still triggers Art. 50(3). Recital 16 lists categories "such as sex, age, hair colour, eye colour, tattoos, behavioural or personality traits, language" [S2].

### 4.5 Art. 50: transparency (applies at the fair)
- **50(1), interaction with AI:** the provider must design the system so that people "are informed that they are interacting with an AI system, unless this is obvious" [S2]. The Commission lists "(humanoid) robots/cobots, AI companions; robotic companion pets" as in scope [S5 §3.1.1]. In §3.2.1 the guidelines also list, among examples that do **not** meet the obviousness exception, "An AI-powered robotic companion pet, looking highly similar to its natural equivalent and designed to mimic typical human-pet interaction". That is very close to a robot dog, so an explicit AI disclosure is required. [corrected by verifier: the Guidelines' example is specifically a pet "looking highly similar to its natural equivalent". A visibly mechanical quadruped (e.g. a Unitree- or Petoi-style robot) is not that example. However, the exception only applies if the provider can "assess and demonstrate" obviousness to the average member of the target group, including children (para. 42), and with 7-year-olds we cannot. So the conclusion holds: disclose explicitly. The basis is para. 42 plus paras 34 and 40, not the companion-pet example alone.] Where children may interact, notifications "must be child-friendly, age-appropriate, easy-to-understand and easily accessible to all children" [S5 para. 34]. In riskier contexts, including those with children, "periodic reminders and context-aware disclosures are likely to be necessary" [S5 para. 40]. To rely on the "obvious" exception, the provider must "assess and demonstrate" that it applies [S5 para. 42]. Do not rely on it with 7-year-olds.
- **50(3), emotion recognition / biometric categorisation:** deployers "shall inform the natural persons exposed" [S2]. This applies to "any biometric categorisation systems (e.g. age or gender classification ...) regardless of whether they fall ... in the scope of high-risk" [S5 para. 104], and to "all natural persons exposed ... including children" [S5 para. 106]. Signs, standardised icons or spoken notices are acceptable. The Commission's own example is "A visible notice at each possible entrance to an exhibition room ... that visitors' facial images are captured ... to assign them to a specific age group" [S5 para. 107]. The notice is due "at the latest at the time of the first interaction or exposure" [S2 Art. 50(5); S5 para. 108], and Art. 50(5) adds "applicable accessibility requirements" [S2].
- **50(2)/(4), synthetic content:** if we generate a portrait or avatar with a generative model, outputs must be "marked in a machine-readable format and detectable as artificially generated" [S2]. A photorealistic generated image of a real child could also be a "deep fake" (Art. 3(60)) [S2]. **Design choice:** draw any avatar procedurally (rule-based), with no generative model.
- **Penalties:** breaching Art. 5 can cost up to EUR 35M or 7% of turnover; breaching Art. 50 up to EUR 15M or 3% (Art. 99(3)-(4)) [S2]. Member States decide how far fines apply to public bodies (Art. 99(8)) [S2].

### 4.6 Is the exhibit high-risk under Annex III? No, if we follow this design

| Annex III point [S2] | Our design | Verdict |
|---|---|---|
| 1(a) Remote biometric identification | No identification, no reference database, no re-identification | Not applicable |
| 1(b) Biometric categorisation "according to sensitive or protected attributes" | Draft Commission guidelines: "sensitive" means GDPR Art. 9(1) attributes, of which "ethnic origin, genetic data, and data concerning health" are "of key relevance". Age and gender inference is "not high-risk" [S6 paras 169-170 and examples]. We infer none of these | Not applicable |
| 1(c) Emotion recognition | Excluded by design. Smile detection only as a movement, with no emotion label [S6] | Not applicable |
| 3(a)-(d) Education: admission, evaluating learning outcomes, assessing level, proctoring | No evaluation, grading or monitoring of pupils | Not applicable |
| Art. 6(1) / Annex I (safety component of a product, e.g. a toy) | The AI is not a safety component of the robot. Annex I obligations apply from 2 Aug 2028 anyway [S3a] | Not applicable |

Note: the high-risk guidelines are still a **draft**. They were published 19 May 2026, and the consultation closed **23 Jul 2026** after the original 23 Jun deadline was extended. We found no final version as of 2 Oct 2026. Jones Day (June 2026) says the final guidelines are "expected before the AI Act's high-risk obligations enter into force", i.e. before 2 Dec 2027 [S6; S6a]. Re-check before the DPIA is finalised.
Under Art. 6(3), an Annex III system that "performs profiling of natural persons" is always high-risk [S2]. Building a trait "profile" of a child would push the system toward Annex III if any Annex III category were in play. That is one more reason to avoid it.

### 4.7 Art. 5(1)(a)/(b): manipulation and exploiting age-related vulnerability
Art. 5(1)(b) prohibits AI that "exploits any of the vulnerabilities ... due to their age" and materially distorts behaviour in a way that causes significant harm [S2]. The risk at our exhibit is low, but the design must not use guilt or pressure to keep sensors on (for example "I'm sad you closed my eyes"). ICO standard 13 makes the same point: "Do not use nudge techniques to ... weaken or turn off their privacy protections" [S24].

---

## 5. MSCA / Horizon Europe ethics and SiW rules

- **EU Grants ethics self-assessment (v2.0, 13 Jul 2021)** [S20]. For *research* with children, "consent must be obtained from the parents/legally authorised representative ... Whenever possible, the assent of the participants should be obtained ... Dissent should be respected". Researchers must "maintain an active relationship with their legal guardians and/or carers". The **AI section** asks how users will be informed about "their interaction with an AI system", "the abilities, limitations, risks and benefits", "the logic", and about "measures taken to avoid bias", with a risk assessment covering "development, deployment and post-deployment phases" [S20 §8].
- **Ethics by Design and Ethics of Use Approaches for AI** (v1.0, 25 Nov 2021, expert panel, "does not constitute official EU guidance"): people must not be "deceived, manipulated, objectified or dehumanized" [S21].
- **Outreach versus research.** The exhibit is *outreach*. As soon as we log interactions, film, or ask questions to evaluate XAI comprehension, it becomes **research with minors**: parental consent, child assent and ethics approval are needed, which is not feasible at SiW. **Recommendation:** collect no research data at SiW, only anonymous aggregate counters.
- **TUAI grant agreement:** check whether Annex 1 contains ethics requirements or deliverables covering dissemination activities with minors (**UNVERIFIED**; the public site gives no detail [S17]).
- **SUT research-ethics body.** Secondary sources report that SUT set up a "Komisja ds. etyki badań naukowych przeprowadzonych z udziałem ludzi" on 28 Jun 2021, after a Rector's ethics commission of 22 Apr 2021 [S49]. We could not find its current rules or application form on polsl.pl (**UNVERIFIED**: ask the TUAI coordinator or the research office). Use it only for an advisory "no research data collected" opinion, or for a full review if any evaluation study with children is planned later.
- **Polish child-protection law and SUT orders** bind the DCs as SUT staff or doctoral candidates: the standards [S40] and the register check [S41]. A booth for school groups is very likely "działalność związana z ... edukacją ... małoletnich", which is what triggers the register check. We saw no territorial limit in the parts of the orders we read. Both points are our reading, so confirm them with SUT HR (Dział Zasobów Osobowych).
- **SiW participant rules:** the 2027 call form contains no rules on filming, children's data or safety [S18]. The organisers' consent covers applicants' data only. Ask the organisers before the event (see section 10).

---

## 6. Child-focused guidance and child-robot interaction research

| Source | Key point | Design implication |
|---|---|---|
| **UNICEF Guidance on AI and Children 3.0** (Dec 2025; 10 requirements, up from 9 in v2.0 of 2021) [S22] | Requirements include safety, "data and privacy", non-discrimination, "transparency, explainability and accountability for children", best interests, inclusion, and skilling children. "There should not be 'invisible' data processing". Data should be kept "for the shortest period feasible". "**prevent anthropomorphizing** the tools ... teach children to develop accurate mental models of AI systems as data-driven applications rather than sentient machines". No emotional analytics with children | The robot says plainly that it is a program without feelings. Show the data pipeline. Nothing is retained |
| **UN CRC General Comment 25** (CRC/C/GC/25, 2 Mar 2021) [S23] | Para. 62 covers emotional analytics and inference "about a child's inner state". Para. 68: "biometric data, can uniquely identify a child". Para. 69: interference must "uphold the principle of data minimization". Para. 70: "privacy-by-design". Para. 71: consent from the child or a parent depending on "evolving capacity" | No emotion inference, no identification, minimisation, privacy by design |
| **ICO Age Appropriate Design Code** (UK; good practice only) [S24] | Standard 1: best interests. 4: transparency "suited to the age of the child". 7: "'high privacy' by default". 8: minimisation "in which a child is actively and knowingly engaged". 12: profiling "off" by default. 13: no nudges. 14: connected toys and devices | Sensors off by default; profiling off; no nudging |
| **Kahn et al. 2012** (n = 90 children aged 9, 12 and 15; Robovie) [S25] | Most children "believed that Robovie had mental states (e.g., was intelligent and had feelings) and was a social being (e.g., could be a friend, offer comfort, and **be trusted with secrets**)". Younger children did so more than 15-year-olds | Expect children to tell the robot things. Microphone: closed vocabulary only, never store or display free speech |
| **van Straten et al. 2020** (review of 86 studies) [S26] | Robot "responsiveness and role, as well as strategic and emotional interaction" increase children's closeness to the robot | Keep the interaction short and factual. Avoid emotional bonding scripts |
| **Sharkey and Sharkey 2010**, "The crying shame of robot nannies", Interaction Studies 11(2):161-190 [S27] | The abstract raises "human rights, privacy, robot use of restraint, **deception of children** and accountability", and says "the most pressing ethical issues ... concern the consequences for the psychological and emotional wellbeing of children", set against the literature on attachment disorders (abstract verified via Crossref) | Do not fake emotions or invite attachment. Use the robot as a sensor platform, not a friend |

Note: the robot "dog" is zoomorphic and built to invite anthropomorphism. Turn that into the lesson: "It looks like a dog, but it sees you as numbers. Here is what those numbers are."

---

## 7. Lessons from controversial projects

| Project | What it did | What went wrong | Lesson for us |
|---|---|---|---|
| **ImageNet Roulette** (Crawford and Paglen, 2019) [S31] | Classified uploaded selfies using a model trained only on ImageNet's "person" categories. The essay notes it "does not store the photos" | Returned offensive labels drawn from the dataset ("Bad Person", "Loser" and similar). This exposed 2,833 person subcategories and led to ImageNet removing person images [S31]. Yang et al. found 1,593 of 2,832 person synsets "potentially offensive" (600,040 images) and only 158 of the rest "visual" [S32] | Labels are value judgements. A closed, harmless vocabulary is essential. Never label people with character words |
| **Biometric Mirror** (Univ. Melbourne / Science Gallery Melbourne, 2018; Wouters et al., DIS 2019) [S33] | Showed gender, age and ethnicity, plus "aggressiveness, weirdness, emotional stability, attractiveness, happiness, responsibility, kindness", learned from "an open data set of thousands of facial images and crowd-sourced evaluations". It then picked one trait and asked the visitor to imagine it "being shared with someone, like your insurer or future employer" [S33a; S33b] | Deliberately provocative: it showed people unfounded trait inferences derived from other people's subjective ratings | A provocation design does not suit 7-year-olds. If we want to show bad inferences, demonstrate them on synthetic or cartoon faces, never on the visitor |
| **How Normal Am I?** (Tijmen Schep; EU H2020 SHERPA, GA 786641) [S34] | Estimated beauty, age, BMI, life expectancy, emotion and gender in the browser. "No personal data is sent to our server in any way" | Good privacy engineering (local processing), but the outputs (beauty, BMI, life expectancy) are harmful for children | Copy its **local-only architecture**, not its outputs |
| **Microsoft how-old.net** (launched at Build, late Apr 2015) | Age and gender guessing from uploaded photos; "over 35,000 users" within hours [S50] | Became famous for wrong guesses. Microsoft said "No we don't store photos ... The photos are discarded from memory once we guess", while the site's boilerplate Terms granted Microsoft "permission to use your Submission in connection with the operation of their Internet businesses" (Global News, 5 May 2015) [S51] | **Our privacy promise must match every document and vendor term**, not just the code. Age and gender guesses are error-prone. NIST IR 8525 (May 2024): accuracy depends on "algorithm, sex, image quality, region-of-birth, age"; border-crossing webcam photos were hardest for four of six algorithms [S30] |
| **Gender classifiers** (Gender Shades) [S29] | Commercial gender classification | Error rates "up to 34.7%" for darker-skinned females versus at most 0.8% for lighter-skinned males | Gender inference would systematically misgender some children |
| **Emotion-recognition products** | "Read" emotions from faces and voices | Weak science [S28]; regulators' opposition [S10]; now banned at work and in education [S2] | Explain why the robot does not do this. That is the teaching moment |

---

## 8. Deliverable (a): candidate attributes and verdicts

Legend: **ACCEPTABLE** = may be used as specified. **AVOID** = do not build: legal exposure (Art. 50(3), GDPR fairness) and/or harm to children, with no teaching value that justifies it. **PROHIBITED** = prohibited by law, or so close to a prohibition or Art. 9 that we treat it as prohibited.

| # | Attribute | Sensor | Verdict | Reason (with source) | How to use it / safe alternative |
|---|---|---|---|---|---|
| 1 | Age estimate | Camera / microphone | **AVOID** | Age is a biometric categorisation category [S2 rec. 16]. It triggers the Art. 50(3) notice [S5 para. 104]. It is not prohibited, and per the draft guidelines not high-risk [S6]. Accuracy varies by "sex, image quality, region-of-birth, age", and webcam images are hardest [S30]. Being judged "younger" stings at age 11-14 | Explain on a slide using a synthetic face: "some AIs guess age, and they are often wrong" |
| 2 | Gender | Camera / microphone | **AVOID** | Biometric categorisation of sex [S2 rec. 16]; Art. 50(3) [S5]. Error disparity of 34.7% vs 0.8% [S29]. Misgendering harm; binary labels. Recital 38 on profiling children [S1] | None. Never display it |
| 3 | Ethnicity / skin tone | Camera | **PROHIBITED** | Inferring race through biometric categorisation is banned by Art. 5(1)(g) [S2; S4 paras 271-283]. GDPR Art. 9 covers data "revealing racial or ethnic origin" [S1]. Ethnic origin is "of key relevance" under Annex III 1(b) [S6 para. 169] | Never compute. Also block it as a VLM output token |
| 4 | Emotion (face / voice / body) | Camera / microphone | **PROHIBITED** (treated as) | Art. 5(1)(f) at work and in education; the workplace includes museums, temporary sites and volunteers [S4 paras 254-255] [corrected by verifier: the ban covers visitors only where staff or teachers are also tracked; see section 4.3]. Elsewhere it is high-risk [S4 para. 266]. Weak science [S2 rec. 44; S28]. Opposed by EDPB/EDPS, UNICEF and the CRC [S10; S22; S23] | **ACCEPTABLE only:** "smile detected" as a mouth movement, with the explicit caption "I can't know how you feel" [S4 para. 249] |
| 5 | Attractiveness | Camera | **AVOID** (never) | No validity. Harmful to self-image. Fails GDPR fairness (Art. 5(1)(a)) and the best-interests test [S1; S22]. The lesson of Biometric Mirror and How Normal Am I [S33; S34] | None |
| 6 | Health / disability (glasses as eyesight, wheelchair, cough, stutter, BMI) | Camera / microphone | **PROHIBITED** (treated as) | GDPR Art. 9 "data concerning health" [S1]. Health is "of key relevance" for Annex III 1(b) [S6] | The system must ignore mobility aids. No comments on speech fluency |
| 7 | Accent / native language | Microphone | **AVOID** | "Language" is a biometric categorisation category [S2 rec. 16]. Accent is a proxy for ethnic origin (Art. 9 and Art. 5(1)(g) risk) [S1; S2]. Most visitors speak FR or NL | Let the child **choose** a language by pressing a flag button |
| 8 | Height | Camera | **AVOID** | A physical characteristic, so biometric categorisation and an Art. 50(3) notice [S2; S4 para. 282]. Body-image sensitivity; poor monocular accuracy | Use only "distance to robot" (#18) |
| 9 | Clothing colour | Camera | **ACCEPTABLE** | "excludes categorisation according to clothes or accessories" [S4 para. 277]. Low sensitivity; robust (dominant colour of the torso area) | Report only the dominant colour, as a colour patch. Nothing on brands, uniforms or religious dress |
| 10a | Accessories: glasses | Camera | **ACCEPTABLE** (with care) | An accessory, outside biometric categorisation [S4 para. 277]. Draw no eyesight or health conclusion | "I see glasses" (70% sure) |
| 10b | Accessories: hat / headwear | Camera | **AVOID** | Headscarves, kippahs and turbans can reveal religion (GDPR Art. 9) [S1]. Indirect revelation is enough (C-184/20) [S43]. High risk of misclassification | Remove the class from the model's label set |
| 11 | Hair colour | Camera | **AVOID** | Named in recital 16 and in the attribute-estimation examples [S2; S4 para. 282], so Art. 50(3) applies. Ethnicity proxy; dyed hair; lighting | Drop it. If the team insists: post the notice and show uncertainty |
| 12 | Voice loudness | Microphone | **ACCEPTABLE** | A "raised voice or whispering" is a readily apparent characteristic, not emotion recognition, provided no emotion is inferred [S2 rec. 18] | Live meter ("the microphone hears 70 dB now"). Never "you are loud/angry" |
| 13 | Speaking speed | Microphone | **ACCEPTABLE** (momentary, no label) | Low sensitivity, but stuttering and second-language speakers create a health/fairness risk [S1 Art. 9] | Frame it from the robot's side: "I needed 3 s to understand". No "slow/fast talker" |
| 14 | Pitch | Microphone | **ACCEPTABLE** as a live physics display; **AVOID** as a personal attribute | Voice is behavioural biometric data [S4 para. 251]. Pitch is a proxy for age, sex and puberty, which is sensitive for teenagers | Live spectrogram or "sound-wave" demo; no "high/low voice" label |
| 15 | Words spoken / topics | Microphone | **ACCEPTABLE** for a closed vocabulary; **AVOID** for open topic inference | Children treat robots as able to "be trusted with secrets" [S25]. Free speech may contain special-category or third-party data [S1 Art. 9] | Keyword spotting for game prompts. Transcripts in RAM only and never shown in full |
| 16 | Favourite animal (said) | Microphone / button | **ACCEPTABLE** (best case) | Volunteered, for a specific purpose, non-sensitive. It shows the difference between "data you give" and "data it infers" | Keep in RAM for the session. Can go on the printed card |
| 17 | Gestures / waving | Camera | **ACCEPTABLE** | Detecting "readily apparent ... gestures" is not emotion recognition [S2 rec. 18; S4 para. 249]. The gesture is a deliberate input | On-device pose estimation; keypoints never stored |
| 18 | Distance | Camera / depth | **ACCEPTABLE** | Non-sensitive, framed from the robot's side, also useful for safety | "You are 1.2 m away" |
| 19 | Number of people | Camera | **ACCEPTABLE** | Counting without identification is an anonymous output CNIL cites as a safeguard [S11] | Triggers "group mode". Only within the interaction zone |
| 20 | Energy / movement | Camera | **ACCEPTABLE** as momentary motion; **AVOID** as a trait | Labels such as "hyper" suggest ADHD (health). "Behavioural or personality traits" are a categorisation category [S2 rec. 16] | "The camera sees a lot of movement right now" |
| 21 | Interaction style (shy, outgoing, ...) | Several | **AVOID** | Personality or behaviour profiling of children [S1 rec. 38]; biometric categorisation [S2 rec. 16]; edges toward profiling under Art. 6(3) [S2] | Factual log only: "you waved 3 times and switched the camera off once" |
| 22 | Environment noise | Microphone | **ACCEPTABLE** | Ambient, not linked to a person | Explains why the robot misunderstands at a noisy fair |
| 23 | Face identity / "welcome back" | Camera | **PROHIBITED** (by design) | Re-identification is unique identification, so Art. 9 applies [S7 para. 82]. It also matches item 1 of the Belgian DPIA list [S12] | Sessions are bounded by start/stop buttons. No embeddings |
| 24 | Gaze / attention / interest | Camera | **AVOID** | "infer the interest and attention of students" is the Commission's example of a prohibited practice [S4 para. 255] | Robot head-tracking for show only, with no attention score |

---

## 9. Deliverable (b): privacy-by-design architecture controls

**Sensing**
1. **Off by default.** Camera and microphone stay closed until a physical button is pressed [S1 Art. 25(2); S24 std 7].
2. **Physical guarantees a child can see:** a lens shutter or flap closes when the camera is off ("the robot's eyes are closed"), a hardware mute is used for the microphone, and an LED is wired to the actual capture state.
3. **Honest toggles.** The software toggle must release the device handle, so no frames reach any process. Test this, and run the test in front of visitors as part of the demo.
4. **Region of interest.** Crop to a marked floor zone (a 1-2 m mat) and black out everything else **before** inference [S7 para. 129: "masking or scrambling areas that are not relevant"].
5. **Frugal capture.** Low resolution (for example 320x240 for detection) and a low frame rate [S11].

**Processing**
6. **All inference on the device** (the exhibition laptop or mini-PC). No cloud vision, speech or LLM APIs. These would transfer children's images to third parties, with their own retention and possible international transfers.
7. **Offline booth.** Do not use the venue Wi-Fi [S18]. Deny all outbound traffic in the firewall. The robot sits on an isolated link to the laptop.
8. **Closed-set models only:** person detector, pose, colour histogram, a glasses classifier, a keyword spotter. **No** face recognition or face-embedding models.
9. **No open-ended "describe this person" prompts to a VLM.** VLMs readily output age, gender, ethnicity and emotion, which would put us into Art. 50(3) or Art. 5(1)(g) territory by accident. If a VLM is used for objects, filter its outputs through an allow-list.
10. **Attribute allow-list enforced in code.** The inference layer can only emit fields from the section 8 register. Anything else is dropped, and its occurrence is counted for QA.
11. **Session-scoped state.** No cross-session linking and no re-identification [S7 para. 82]. Raw frames and audio live in ring buffers of 2 s or less. Derived features are wiped at session end, after a timeout (for example 60 s with nobody on the mat), or on "Forget me", which plays a visible wipe animation as part of the lesson.

**Storage**
12. **Nothing persisted.** No frames, audio, transcripts or keypoints on disk. No debug dumps. Check crash-dump settings. Disable cloud sync (OneDrive) and screen recorders. Enable full-disk encryption (BitLocker) as defence in depth.
13. **Anonymous aggregate counters only**, for example the share of sessions with the camera on. **Aggregate per fair day (or per half-day), never per session, and with no timestamps.** EDPB Guidelines 02/2026 on anonymisation (adopted for consultation 7 Jul 2026) say aggregates can still relate to individuals when "additional processing" reveals the link (para. 17). They test anonymity by three criteria: "No Record Isolation, No Linkage and No Inference" [S52]. A 09:03 entry saying "1 session, camera off", combined with what the staff saw, would single out a child. Coarse daily totals pass all three tests and can go on the class poster.
14. **Verification.** Before the fair, run a file-system and network monitor during a full session to show that nothing is written or sent. Keep the log as DPIA evidence.

**Display**
15. **The public screen shows an abstract representation** (silhouette or skeleton, colour patches, icons), not raw video. This stops bystanders photographing children off the screen. If a raw view is educationally essential, show it small, facing the participant, at low resolution, with automatic blur outside the zone.
16. **Show evidence and uncertainty.** "Sensor, evidence, inference (confidence)", a **"Things I will NOT guess about you, and why"** panel, and a "Was I right? Yes/No" button that teaches error and human oversight.
17. **No judging words.** Only neutral, robot-centric phrasing.

**Robot and security**
18. **Assume the robot vendor's cloud is hostile.** Documented cases:
    - Unitree Go1 had an undocumented "CloudSail" remote-control backdoor (CVE-2025-2894, published 28 Mar 2025) [S35].
    - "UniPwn" is a BLE root exploit for Unitree Go2/G1/H1/B2 with hard-coded keys. It was disclosed on 20 Sep 2025 and reported unfixed at disclosure [S36]. [corrected by verifier: it is tracked as CVE-2025-35027 (BLE Wi-Fi configuration command injection, CVSS 7.3, GitHub advisory published 26 Sep 2025, "Patched versions: Unknown"), together with CVE-2025-60017, -60250 and -60251. According to the researchers, Unitree said a fix would "require full system iteration taking quarters or years" (https://github.com/advisories/GHSA-27p8-m7h9-xchc ; https://github.com/Bin4ry/UniPwn). Treat any Go2-family robot as vulnerable unless the vendor documents a fix.]
    - The Unitree G1 sent telemetry to remote IPs "every 300 seconds" [S37].

    Measures: disable BLE and vendor apps, never pair with the vendor cloud, and prefer a robot whose camera stream can be kept local or an **external USB camera wired to the laptop**. Check with packet capture.
19. **Deactivate functions that are not needed** (cloud, remote view, recording, zoom) [S7 para. 129].
20. **Procurement.**
    - Buy an EU-market, CE-marked robot whose Declaration of Conformity covers the Radio Equipment Directive. The RED cybersecurity and privacy requirements (Art. 3(3)(d),(e),(f), Delegated Reg. (EU) 2022/30) apply from 1 Aug 2025 [S53].
    - Ask the vendor about vulnerability handling (the Cyber Resilience Act's reporting duties apply from 11 Sep 2026) [S54].
    - SUT Order 62/2024 §17 requires privacy-by-design requirements to be written into the procurement specification and consulted with the DPO [S42]. Put "camera/microphone usable locally without vendor cloud; BLE/remote access can be disabled; no telemetry" into the purchase request.
21. **Physical safety.** A powered quadruped among 7-year-olds brings risks of pinch points, falls or jumps, and LiPo battery charging at the venue. Keep it in a stationary "stand/sit" mode on a low platform or behind a low barrier. Give a staffer a hand-held emergency stop. Never let children carry or hold the robot. Add these to the DPIA risk register and the safeguarding plan. (Product safety for the device itself falls under the General Product Safety Regulation (EU) 2023/988; we did not verify its specific provisions.)

**Organisation**
22. A staff script and briefing to meet the Art. 4 AI-literacy measures [S3]. No staff phones filming children (SUT staff code: no recording of minors "na potrzeby prywatne" [S40]). Never one adult alone with one child.
23. **Register check for every booth staffer**, including doctoral candidates and any non-SUT helpers. Submit the request to SUT HR (Dział Zasobów Osobowych) **at least 7 days** before the fair (Order 37/2024 §4 as amended by Order 240/2024; separate request forms for employees and for doctoral candidates or non-employees) [S41]. [corrected by verifier: also collect KRK information and, for anyone with foreign citizenship or foreign residence in the last 20 years, foreign criminal-record certificates or sworn statements (Art. 21 of the 2016 Act; MoJ FAQ https://www.gov.pl/web/sprawiedliwosc/pytania-do-ustawy-o-ochronie-dzieci2). Allow weeks for foreign certificates.] Brief all staff on SUT's child-protection standards [S40].
24. Records of processing (Art. 30, kept by the SUT DPO from information supplied by project managers [S42 §3]), the DPIA (Art. 35), DPO sign-off, and a breach procedure (72 h notification under Art. 33; internally, report to the DPO, who prepares the report for the Rector [S42]) [S1].
25. Tune models on adults, synthetic data or public datasets. **Do not collect children's data to train or tune** without parental consent and ethics approval [S20].

---

## 10. Deliverable (c): consent and notice for a busy fair

**Legal framing.** The legal basis is public task (Art. 6(1)(e)). The **opt-in button** is an ethical assent mechanism and an easy right to object. It also satisfies the Art. 50(1)/(3) notices [S1; S5]. Respect dissent: "Dissent should be respected" [S20].

**Before the fair**
- Send a **one-page teacher information sheet** (EN/FR/NL) through the SiW organisers' school pack, if they agree. It should cover what the exhibit does, that nothing is recorded, how a pupil can take part without the camera, and a request that **teachers tell staff about pupils who must not be filmed** (for example children under protection measures). Those pupils use no-camera mode.
- Ask the organisers whether schools collect photo or filming consents, and what their rules are for researchers' own photos.

**At the booth (each group, about 15 minutes)**
1. **First-layer sign** at the booth entrance, A1 or A2, with pictograms (camera, microphone, "not saved", stop hand) and three languages [S7 paras 112-115; S5 para. 107].
2. **Thirty-second group introduction by staff:** "This robot runs an AI program. It is not alive and has no feelings. Its camera and microphone switch on only when you press the green button. Nothing is saved, and when you leave it forgets you. You can say no and still play."
3. **Per participant:** step onto the mat, then press green ("let it see me") and/or blue ("let it hear me"). Toggles are visible. The red **STOP / Forget me** button is always available. The session ends automatically when the child leaves the mat or after N minutes.
4. **No-camera mode** gives the full experience: the child answers with buttons or picture cards, and the robot builds its picture only from "data you give". This also teaches the comparison between what is said and what is seen.
5. **Adult present.** Camera and microphone mode only while the accompanying teacher or parent is at the booth. Children without an adult get no-camera mode.
6. **Robot reminders in the middle of the session** (child-specific, per [S5 para. 40]), for example "Remember, I'm a computer program. I'm using my camera now. Press red to stop."
7. **Neutral reactions to "off":** "OK, camera off. I'll only use what you tell me." No sadness, no pleading [S2 Art. 5(1)(b); S24 std 13].
8. **Accessibility:** large type, pictograms, the notice also spoken by the robot, the screen at wheelchair height [S2 Art. 50(5)].

**Plan B, if the SUT DPO requires guardian consent for camera processing** (see the tension with Order 50/2024 §5(3) in section 3.3):
- Schools register for SiW in advance [S19]. Through the organisers' school pack, send the teacher sheet with a **one-line consent slip** covering this booth: "My child may use the robot's camera and microphone at the TUAI booth. Nothing is recorded or saved."
- At the booth, the teacher confirms which pupils have a slip. The booth itself collects **no names and no slips**; the school keeps them. That avoids creating new records on our side.
- Pupils without a slip, and groups that did not take part, get the **full no-camera mode**. Because no-camera mode is a complete experience (button and picture-card input, "data you give" versus "data it sees" comparison), nobody is excluded.
- This costs some throughput but keeps the exhibit viable whichever way the DPO rules. Decide by **November 2026** so the school pack text can go out in time (ask the organisers for their schedule).

**Sign text (first layer; translations to be checked by native speakers)**

> **EN - How does a robot see you?**
> The robot's camera and microphone are OFF until you press the green button.
> It looks at things like the colour of your clothes, how far away you are and your waves. It does NOT try to recognise who you are, and does NOT guess your feelings, age, gender or where you come from.
> Nothing is recorded or saved. When you leave, the robot forgets you.
> You can switch the camera or microphone off at any time, and the game still works.
> Not sure? Just watch, or ask us!
> Responsible: Silesian University of Technology (Poland), TUAI project, an AI system. Questions: staff at the booth / IOD@polsl.pl. More info: ask for the info sheet.

> **FR - Comment un robot te voit-il ?**
> La caméra et le micro du robot sont ÉTEINTS tant que tu n'appuies pas sur le bouton vert.
> Il regarde par exemple la couleur de tes vêtements, ta distance et tes gestes. Il n'essaie PAS de savoir qui tu es et ne devine PAS tes émotions, ton âge, ton genre ni ton origine.
> Rien n'est enregistré ni sauvegardé. Quand tu pars, le robot t'oublie.
> Tu peux éteindre la caméra ou le micro à tout moment : le jeu continue.
> Tu hésites ? Regarde simplement, ou pose-nous une question !
> Responsable : Université de technologie de Silésie (Pologne), projet TUAI, un système d'IA. Contact : IOD@polsl.pl.

> **NL - Hoe ziet een robot jou?**
> De camera en microfoon van de robot staan UIT tot jij op de groene knop drukt.
> Hij kijkt bijvoorbeeld naar de kleur van je kleren, hoe ver je staat en of je zwaait. Hij probeert NIET te weten wie je bent en raadt NIET je gevoelens, leeftijd, gender of waar je vandaan komt.
> Er wordt niets opgenomen of bewaard. Als je weggaat, vergeet de robot je.
> Je kunt de camera of microfoon altijd uitzetten: het spel werkt nog steeds.
> Twijfel je? Kijk gewoon mee of vraag het ons!
> Verantwoordelijke: Silezische Technische Universiteit (Polen), project TUAI, een AI-systeem. Contact: IOD@polsl.pl.

**Second layer** (A4 sheet at the booth plus a static web page with no trackers). It covers the Art. 13 items:
- controller and DPO contact [S16];
- purpose (public science communication);
- legal basis (Art. 6(1)(e) GDPR with Art. 11(1)(9) of the Polish Act of 20 July 2018 [S15]);
- data categories (live video and audio; derived non-sensitive features, listed);
- no recipients and no transfers;
- retention (RAM only, deleted at session end; anonymous counters only);
- rights, including objection by not starting or by pressing STOP, and Art. 11 [S1];
- the right to complain to UODO (PL) or the APD/GBA (BE);
- an AI Act statement (an AI system; which simple categories it uses; what it never infers) [S5 paras 105-107].

---

## 11. Deliverable (d): result delivery options

| Option | What leaves the booth | Personal data? | Privacy / legal implications | Verdict |
|---|---|---|---|---|
| **Nothing, plus a "Forget me" ceremony** | Memory only | None | Best minimisation [S1 Art. 5(1)(c),(e)]; the deletion is itself the lesson | **Default** |
| **Locally printed card** (USB thermal printer, offline) | Icons: sensors used, clothing colour patch, favourite animal, "what I guessed and how sure", "what I could NOT know". No face, no name | Practically non-identifying, held by the child | No storage on our side. Use a printer with no network or cloud and no job memory. We pay for it (SiW will not fund giveaways [S18]) | **Recommended optional** |
| **Class poster / aggregate infographic** | Counts (for example "62% kept the camera off") | Anonymous aggregates | Not personal data if coarse; good for teaching | **Acceptable** |
| **QR code with the data in the URL fragment**, opening a static page | The data sits in the code; the page decodes it in the browser | Low | "The fragment is not sent to the server" [S38], but the page host still sees visits and IPs. Needs a phone (many pupils have none or may not use one), and the child may share it. If treated as an online service, the Art. 8 question returns [S8] | Possible, but adds little over paper |
| **QR code pointing to server-hosted results** | Results stored online | Yes | Requires hosting, retention, security, a processor contract, possibly an ISS under Art. 8 with 16/13 thresholds [S8]; and children's data online | **Avoid** |
| **Email** | Child's or parent's email address and the result | Yes, directly identifying | New identifiers, retention, consent needed; contrary to minimisation | **Avoid** |
| **Photo printout / AI-generated portrait** | An identifiable image of the child | Yes | Belgian image right [S13]; spread on social media; if generative, Art. 50(2)/(4) labelling [S2] | **Avoid** |

---

## 12. Deliverable (e): DPIA and ethics approval

**Recommendation.** Do a **formal but short DPIA** (10-15 pages of content) through SUT's own procedure: screening under §16(2) of Order 62/2024, then the DPIA in the RIG software with BBI, with both steps consulted with the DPO [S42]. SUT reportedly has a "Komisja ds. etyki badań naukowych przeprowadzonych z udziałem ludzi" (2021) [S49]. Request an **advisory opinion** from it stating that the exhibit collects no research data. A full ethics approval is needed only if any research data on children is collected. We recommend collecting none at SiW.

**Who to contact at SUT (in this order):**
1. The DPO, IOD@polsl.pl, tel. 32 400 3077 [S16]: lawful basis, the §5(3) question, DPIA screening.
2. The unit's local data-protection representative (LPODO) [S42].
3. HR (Dział Zasobów Osobowych): register checks [S41].
4. The research-ethics commission, through the research office: advisory opinion.
5. The TUAI coordinator: grant-agreement ethics deliverables.

**Prepare:**
1. A data-flow diagram (sensor, RAM buffers, models, display, wipe) and the Art. 30 record.
2. A lawful-basis memo: Art. 6(1)(e) plus Art. 11(1)(9) of the Polish Act [S15], why consent is not used [S1 rec. 43], and why Art. 8 does not apply [S8].
3. Necessity and proportionality: the section 8 table, with a teaching reason per signal and the "never infer" list.
4. A risk register covering at least these risks: misclassification and humiliation; bystander capture; disclosure of secrets [S25]; screen photographed by others; laptop theft; vendor telemetry [S35-S37]; mission creep ("let's save some clips"); teacher or peer pressure to take part.
5. The section 9 measures, with test evidence (no-write and no-network logs, toggle tests).
6. Transparency material: signs in three languages, robot script, teacher sheet, second-layer notice. **Test them with 3-5 children of colleagues, with parental agreement and no recording.**
7. An AI Act memo:
   - Art. 2 scope (not excluded) [S4; S5];
   - an Art. 5 screen (no emotion inference, no race inference) [S4];
   - Art. 50(1)/(3) compliance [S5];
   - Annex III non-applicability (section 4.6) [S6];
   - the Omnibus dates [S3];
   - Art. 4 AI-literacy measures for staff.
8. A security assessment of the robot and laptop: firmware, BLE off, isolated network, packet capture.
9. Model and data provenance: licences, no training on children's data, a bias check on the clothing-colour and glasses detectors under fair lighting and across skin tones.
10. Safeguarding: staff conduct under SUT's standards [S40], adult present, incident escalation, register checks [S41], and how to stop the robot physically (e-stop, platform, battery handling).
11. Coordination with the SiW organisers (photography, the school pack, pupils with image restrictions, the Plan B consent slip if needed).
12. The procurement specification for the robot and any camera, with privacy-by-design clauses consulted with the DPO (§17 of Order 62/2024) [S42].

**Timeline:**
- **6 Oct 2026:** submit the proposal with the ethics statement.
- **Now, before buying hardware:** send the procurement privacy clauses to the DPO (§17).
- **After 28 Oct 2026** (results): DPIA screening with the DPO in November, including a written position on lawful basis and §5(3). Decide between Plan A and Plan B.
- **Nov-Dec 2026:** if Plan B applies, deliver the consent-slip text to the organisers for the school pack.
- **Dec 2026 - Jan 2027:** prototype tests on adults; finalise the notices and translations; draft the DPIA content.
- **Feb 2027:** finalise the DPIA in RIG with BBI and the DPO; dry-run the toggle and wipe tests; re-check the GDPR Omnibus and the final high-risk guidelines.
- **By 9 Mar 2027 at the latest** (7 days before set-up on 16 Mar): register-check requests for all booth staff submitted to HR. Better to file them in February. [corrected by verifier: request foreign criminal-record certificates for non-Polish staff in **January 2027**, because of the lead times.]
- **17-19 Mar 2027:** the fair.

---

## 13. Deliverable (f): ethics statement (for the proposal)

> *"How does a robot see you?" is designed to be privacy-protective and child-safe from the start. The robot's camera and microphone stay off until a visitor chooses to switch them on, and they can be switched off at any time; a version of the activity without camera or microphone gives the same learning experience. All processing happens live on a local, offline computer: no images, sound or transcripts are recorded, nothing leaves the booth, and everything is wiped when the visitor leaves. The robot only uses simple, non-sensitive signals such as clothing colour, distance, gestures and words the child chooses to say. It never tries to identify anyone and never guesses emotions, age, gender, ethnicity, health or personality. Explaining why AI should not make such guesses is part of what visitors learn. The robot tells visitors in child-friendly French, Dutch and English that it is an AI program without feelings. We do not photograph pupils. All booth staff are trained in and bound by our university's child-protection standards and have been vetted under Polish child-protection law. The design follows the GDPR, the EU AI Act (including the Article 5 prohibitions and the Article 50 transparency duties), UNICEF's Guidance on AI and Children, and our university's data-protection procedures, including a data protection impact assessment reviewed by the Data Protection Officer of the Silesian University of Technology.*

(Wording note: write "reviewed" or "will be reviewed" to match the actual status on 6 Oct 2026. At submission the DPIA will not yet exist, so the honest form is "will undergo a data protection impact assessment ...".)

---

## 14. Recommendations for our demonstrator (in priority order)

1. **Freeze the attribute register now** (section 8). The allowed signals are #9, #10a, #12-#19 and #22, all framed as momentary. Hard-block #1-#8, #10b, #11, #21, #23 and #24. Put the register in the proposal; it also improves feasibility and robustness.
2. **Make "what I will NOT guess, and why" a headline feature.** To show bad inferences, use **pre-rendered** examples on synthetic or cartoon faces, never a live system run on the child, a teacher or a researcher. Live emotion inference on staff would be emotion recognition in a workplace [S4 para. 254].
3. **Architecture:** on-device, offline, RAM only, physical shutter and mute, a defined zone, an abstract display, no face models, an output allow-list, no vendor cloud (section 9).
4. **Notice and assent:** a green start button and red stop button, no-camera mode, three-language pictogram signs, robot disclosure plus reminders, a teacher sheet through the organisers (section 10).
5. **Takeaway:** none by default; optionally an offline printed card with no face or name (section 11).
6. **Governance:** a DPIA and DPO consultation (IOD@polsl.pl) by February 2027; an AI Act memo; an advisory opinion from the SUT ethics body if one exists; no research data collection at SiW.
7. **Robot choice:** prefer hardware whose camera can be used locally without a vendor app or cloud, or mount an external USB camera; keep BLE off.
8. **Plan for groups:** one to three hands-on participants plus a narrated group view. Bystanders stay outside the processed zone.
9. **Language:** FR/NL/EN chosen with buttons, not detected from accent.
10. **Contact the organisers early** about photography rules, school information, and pupils with image restrictions.
11. **Clear SUT internal rules early:** a DPO position on the lawful basis and the §5(3) consent wording (decides Plan A or Plan B); procurement privacy clauses (§17); register checks for all staff at least 7 days ahead; a staff briefing on the child-protection standards [S40-S42].
12. **Physical safety:** a stationary robot on a platform or behind a barrier, a staff-held e-stop, and no battery charging in the public area.
13. **Counters:** daily totals only, no timestamps [S52].

## 15. Pitfalls / what not to do

- Do not claim "no personal data" or "anonymous". Say "**nothing is saved**". Live processing is still processing [S1; S7].
- Do not use cloud vision, speech or LLM APIs, and do not connect the robot or laptop to venue Wi-Fi.
- Do not ask a VLM or LLM to "describe the person". You will get age, gender, ethnicity and emotion words.
- Do not use face embeddings to "remember" or "welcome back" visitors. That is unique identification under Art. 9 [S7 para. 82].
- Do not say "you look happy, sad or excited", even from a smile [S4 para. 249].
- Do not show raw video of children's faces on the booth TV.
- Do not keep "a few clips for debugging or training", and do not collect children's data to tune models.
- Do not photograph or film identifiable pupils for dissemination [S13].
- Do not let the robot pressure, guilt or flatter ("I'm sad", "I like you best") [S2 Art. 5(1)(b); S24 std 13; S22].
- Do not let the robot claim feelings or life, against UNICEF's guidance on anthropomorphising [S22].
- Do not label traits: "shy", "loud", "hyper", "tall", "slow talker".
- Do not run a "mini study" (questionnaires, logging, video) without ethics approval and parental consent [S20].
- Do not collect email addresses or names, and do not use server-backed QR results.
- Do not generate photorealistic AI portraits of children [S2 Art. 50(2),(4)].
- Do not trust the robot vendor's defaults (backdoors, BLE exploits, telemetry) [S35; S36; S37].
- Do not assume accuracy at a noisy, crowded fair. Design visible, educational failure modes.
- Do not write "GDPR-certified" or "AI Act-compliant certified". No such certificate exists for this. Say "designed to comply with".
- Do not let notices, vendor terms and the code say different things (the how-old.net lesson [S51]). If the robot vendor's app or terms allow data upload, do not use that app.
- Do not assume a GDPR analysis covers SUT's internal rules. The child-protection standards and register checks apply on their own terms [S40; S41].
- Do not log per-session events with timestamps, even "anonymously" [S52].
- Do not have a model output "headscarf", "skin tone" or "wheelchair" labels, even without intending to infer religion, ethnicity or health. Under C-184/20, indirect revelation is enough for Art. 9 [S43].
- Do not let children handle the robot or stand within reach of moving legs. Do not charge LiPo batteries at the booth.

---

## 16. Unverified items (to check)

**Still open:**
- The full Art. 113 wording of Reg. (EU) 2026/1744. The OJ was only partly readable, so the start date of new Art. 5(1)(ba)/(bb) rests on secondary sources (2 Dec 2026). This is irrelevant to our design.
- The final Commission high-risk guidelines (draft only; final expected before 2 Dec 2027).
- Whether a school trip to an external fair is "in the area of education institutions" under Art. 5(1)(f). The workplace limb covers us anyway.
- Whether SUT counts as a "public authority" for Art. 6(1) last subparagraph. There is strong statutory indication that it does (see section 3.3), but the DPO must confirm.
- **The DPO's position on SUT Order 50/2024 §5(3)** (guardian consent for minors' image data) versus public task. This decides Plan A or Plan B.
- SiW organiser rules on photography and pupils' image consents. None are published on the 2026 or 2027 pages, so ask the organisers.
- SUT's research-ethics commission: current rules and form (existence reported only by secondary sources). The TUAI grant agreement's ethics deliverables.
- Belgian AI Act implementing law and the formal designation of BIPT.
- Whether the robot vendor has patched UniPwn (BLE) since Sep 2025.
- EDPB Guidelines on children's data: announced and "currently" in preparation (EDPB, 28 Jan 2026) but not adopted as far as we found [S55]. Re-check before the DPIA is finalised.

**Resolved in the 2026-10-02 pass:** Art. 8 thresholds (Belgium 13, Poland 16 [S56]; not relevant on site); CJEU C-184/20 [S43] and C-212/13 *Ryneš* (para. 22: "the image of a person recorded by a camera constitutes personal data ... inasmuch as it makes it possible to identify the person concerned", 11 Dec 2014 [S57]); UODO-backed guidance on children's images and the Art. 81 crowd exception [S47]; Art. 11(1)(9) in the consolidated text [S15]; the Biometric Mirror trait list [S33a; S33b]; how-old.net facts [S50; S51]; the Sharkey and Sharkey abstract [S27]; the OJ title, date and entry into force of the Omnibus [S3]; the GDPR Omnibus status (still in committee).

---

## Sources

- [S1] GDPR, Regulation (EU) 2016/679, EUR-Lex: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679 (PDF text extracted: https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0679)
- [S2] AI Act, Regulation (EU) 2024/1689, OJ L 12.7.2024: https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401689 (ELI http://data.europa.eu/eli/reg/2024/1689/oj)
- [S3] Regulation (EU) 2026/1744 of 8 July 2026 (Digital Omnibus on AI), OJ L, 2026/1744, 24.7.2026, ELI: https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng (partly read 2026-10-02)
- [S3a] nicfab, "Digital Omnibus on AI: Regulation (EU) 2026/1744 Is Published in the Official Journal": https://www.nicfab.eu/en/posts/digital-omnibus-ai-official-journal/ (OJ link: https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202601744, not fetchable)
- [S3b] Lewis Silkin, "The Digital Omnibus on AI enters into force today" (27 Jul 2026): https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo
- [S3c] regulation-ai.eu, "Regulation (EU) 2024/1689 as amended in 2026": https://www.regulation-ai.eu/en/changes/
- [S4] European Commission, Guidelines on prohibited AI practices, C(2025) 5052 final, 29.7.2025 (content first published 4 Feb 2025): https://ai-act-service-desk.ec.europa.eu/sites/default/files/2025-08/guidelines_on_prohibited_artificial_intelligence_practices_established_by_regulation_eu_20241689_ai_act_english_ied3r5nwo50xggpcfmwckm3nuc_112367-1.PDF
- [S5] European Commission, Guidelines on the transparency obligations under Article 50 AI Act, C(2026) 5054 final, 20.7.2026: https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems (PDF: https://ec.europa.eu/newsroom/dae/redirection/document/131215)
- [S6] European Commission, Draft guidelines on the classification of high-risk AI systems (19 May 2026), Annex III document: https://digital-strategy.ec.europa.eu/en/library/draft-commission-guidelines-classification-high-risk-ai-systems (PDF: https://ec.europa.eu/newsroom/dae/redirection/document/128561); consultation: https://digital-strategy.ec.europa.eu/en/consultations/targeted-consultation-draft-guidelines-classification-high-risk-artificial-intelligence-systems
- [S6a] Jones Day, "Draft EU Guidelines Clarify When AI Systems Are High-Risk Under the AI Act" (June 2026): https://www.jonesday.com/en/insights/2026/06/draft-eu-guidelines-clarify-when-ai-systems-are-highrisk-under-the-ai-act
- [S7] EDPB Guidelines 3/2019 on processing of personal data through video devices, v2.0 (adopted 29 Jan 2020): https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines_201903_video_devices_en_0.pdf
- [S8] EDPB Guidelines 05/2020 on consent, v1.1 (4 May 2020): https://www.edpb.europa.eu/system/files/documents/files/file1/edpb_guidelines_202005_consent_en.pdf
- [S9] Article 29 WP, Guidelines on DPIA, WP248 rev.01: https://ec.europa.eu/newsroom/article29/items/611236 (PDF: https://ec.europa.eu/newsroom/just/document.cfm?doc_id=47711)
- [S10] EDPB-EDPS Joint Opinion 5/2021 on the AI Act proposal (18 Jun 2021): https://www.edpb.europa.eu/system/files/documents/2021-06/edpb-edps_joint_opinion_ai_regulation_en.pdf
- [S11] CNIL, "Caméras dites intelligentes ou augmentées dans les espaces publics", position (July 2022): https://www.cnil.fr/fr/deploiement-de-cameras-augmentees-dans-les-espaces-publics-la-cnil-publie-sa-position (PDF: https://www.cnil.fr/sites/cnil/files/atoms/files/cameras-intelligentes-augmentees_position_cnil.pdf)
- [S12] Belgian Data Protection Authority, Décision SG 01/2019 (DPIA list): https://www.autoriteprotectiondonnees.be/publications/decision-n-01-2019-du-16-janvier-2019.pdf
- [S13] Belgian Data Protection Authority, "Le droit à l'image" (principes; quelques cas particuliers; reconnaissance faciale): https://www.autoriteprotectiondonnees.be/citoyen/themes/le-droit-a-l-image ; https://www.autoriteprotectiondonnees.be/citoyen/themes/le-droit-a-l-image/principes ; https://www.autoriteprotectiondonnees.be/citoyen/themes/le-droit-a-l-image/quelques-cas-particuliers ; https://www.autoriteprotectiondonnees.be/citoyen/themes/le-droit-a-l-image/reconnaissance-faciale-et-le-droit-a-l-image-
- [S14] Komunikat Prezesa UODO z 17 czerwca 2019 (wykaz operacji wymagających oceny skutków), M.P. 2019 poz. 666: https://api.sejm.gov.pl/eli/acts/MP/2019/666/text.pdf
- [S15] Ustawa z 20 lipca 2018 r. Prawo o szkolnictwie wyższym i nauce, Dz.U. 2018 poz. 1668, Art. 11: https://api.sejm.gov.pl/eli/acts/DU/2018/1668/text.pdf ; latest consolidated text Dz.U. 2024 poz. 1571 (Art. 11(1)(9) unchanged): https://api.sejm.gov.pl/eli/acts/DU/2024/1571/text.pdf
- [S16] SUT Data Protection Officer page: https://www.polsl.pl/bkzb/ochrona-danych-osobowych/
- [S17] TUAI project website: https://tuai.aei.polsl.pl/
- [S18] SiW 2027 call for projects (EUSurvey form): https://ec.europa.eu/eusurvey/runner/Call_SiW2027
- [S19] MSCA, Science is Wonderful! pages (2026 edition): https://marie-sklodowska-curie-actions.ec.europa.eu/science-is-wonderful/about-the-event ; https://marie-sklodowska-curie-actions.ec.europa.eu/science-is-wonderful/registration
- [S20] EU Grants, How to complete your ethics self-assessment, v2.0 (13 Jul 2021): https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/common/guidance/how-to-complete-your-ethics-self-assessment_en.pdf
- [S21] Ethics by Design and Ethics of Use Approaches for AI, v1.0 (25 Nov 2021): https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/guidance/ethics-by-design-and-ethics-of-use-approaches-for-artificial-intelligence_he_en.pdf
- [S22] UNICEF Innocenti, Guidance on AI and Children 3.0 (Dec 2025): https://www.unicef.org/innocenti/reports/policy-guidance-ai-children (PDF: https://www.unicef.org/innocenti/media/11991/file/UNICEF-Innocenti-Guidance-on-AI-and-Children-3-2025.pdf ; v2.0 2021: https://www.unicef.org/innocenti/media/1341/file/UNICEF-Global-Insight-policy-guidance-AI-children-2.0-2021.pdf)
- [S23] UN CRC, General Comment No. 25 (2021), CRC/C/GC/25: https://documents.un.org/api/symbol/access?s=CRC/C/GC/25&l=en&t=pdf
- [S24] ICO, Age Appropriate Design Code, standards: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/code-standards/
- [S25] Kahn P.H. et al. (2012), "Robovie, you'll have to go into the closet now", Developmental Psychology 48(2):303-314: https://pubmed.ncbi.nlm.nih.gov/22369338/ (doi:10.1037/a0027033)
- [S26] van Straten C.L., Peter J., Kühne R. (2020), Child-Robot Relationship Formation: A Narrative Review, Int J Soc Robotics: https://doi.org/10.1007/s12369-019-00569-0
- [S27] Sharkey N., Sharkey A. (2010), The crying shame of robot nannies: an ethical appraisal, Interaction Studies 11(2):161-190: https://doi.org/10.1075/is.11.2.01sha (abstract via Crossref: https://api.crossref.org/works/10.1075/is.11.2.01sha ; OA PDF: http://www.lucs.lu.se/wp-content/uploads/2013/04/kke13_the_crying_shame_of_robot_nannies.pdf)
- [S28] Barrett L.F. et al. (2019), Emotional Expressions Reconsidered, Psychological Science in the Public Interest: https://doi.org/10.1177/1529100619832930
- [S29] Buolamwini J., Gebru T. (2018), Gender Shades, PMLR 81: https://proceedings.mlr.press/v81/buolamwini18a.html
- [S30] NIST IR 8525 (2024), Face Analysis Technology Evaluation: Age Estimation and Verification: https://doi.org/10.6028/NIST.IR.8525
- [S31] Crawford K., Paglen T. (2019), Excavating AI: https://excavating.ai/
- [S32] Yang K. et al. (2020), Towards Fairer Datasets (FAT* 2020): https://arxiv.org/abs/1912.07726
- [S33] Wouters N. et al. (2019), Biometric Mirror, DIS '19: https://doi.org/10.1145/3322276.3322304 (OA: http://hdl.handle.net/11343/224240)
- [S33a] Wouters N., Vetere F., "AI scans your data to assess your character - but Biometric Mirror asks: what if it is wrong?", The Conversation, 23 Jul 2018: https://theconversation.com/ai-scans-your-data-to-assess-your-character-but-biometric-mirror-asks-what-if-it-is-wrong-100328
- [S33b] New Atlas, "Biometric Mirror starkly demonstrates how facial recognition systems amplify human bias", 1 Aug 2018: https://newatlas.com/biometric-mirror-facial-recognition-human-bias/55711/
- [S34] Schep T., How Normal Am I? (SHERPA, H2020 GA 786641): https://www.hownormalami.eu/
- [S35] CVE-2025-2894, Unitree Go1 backdoor (published 28 Mar 2025): https://www.cve.org/CVERecord?id=CVE-2025-2894
- [S36] UniPwn, Unitree BLE vulnerability (disclosed 20 Sep 2025): https://github.com/Bin4ry/UniPwn
- [S37] Mayoral-Vilches V. et al. (2025), Cybersecurity AI: Humanoid Robots as Attack Vectors: https://arxiv.org/abs/2509.14139
- [S38] MDN, URI fragment: https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment
- [S39] gdpr-info.eu (reproduction of GDPR Arts 4, 8, 9, 35, used for quick quotes; authoritative text is [S1]): https://gdpr-info.eu/art-9-gdpr/
- [S40] SUT Rector's Order No. 50/2024 of 21 Mar 2024 on Standards of protection of minors from harm (Monitor Prawny PŚ 2024 poz. 260): https://bip.polsl.pl/wp-content/uploads/sites/4/2024/07/M.2024.260.Z.50.pdf ; overview page: https://bip.polsl.pl/ochrona-maloletnich/
- [S41] SUT Rector's Order No. 240/2024 of 9 Dec 2024 amending Order No. 37/2024 of 23 Feb 2024 on the procedure for verifying persons in contact with minors (Monitor Prawny PŚ 2024 poz. 1463): https://bip.polsl.pl/wp-content/uploads/sites/4/2024/12/M.2024.1463.Z.240.pdf
- [S42] SUT Rector's Order No. 62/2024 of 8 Apr 2024, Data protection policy (in force 1 May 2024), §§3, 16, 17: https://www.polsl.pl/rr9-bbi/wp-content/uploads/sites/600/2024/04/Polityka-ochrony-danych-62.2024.pdf
- [S43] CJEU, C-184/20 *OT v Vyriausioji tarnybinės etikos komisija*, 1 Aug 2022 (summary with paragraph references): https://www.dpcuria.eu/case?reference=C-184/20 ; commentary: https://www.insideprivacy.com/eu-data-protection/special-category-data-by-inference-cjeu-significantly-expands-the-scope-of-article-9-gdpr/
- [S44] SUT Statute §1(1) ("publiczną uczelnią akademicką"): https://bip.polsl.pl/wp-content/uploads/sites/4/2021/05/M.2019.135.US_.42.pdf ; Public Finance Act Art. 9(11), consolidated Dz.U. 2025 poz. 1483: https://api.sejm.gov.pl/eli/acts/DU/2025/1483/text.pdf ; Polish Data Protection Act Art. 9, Dz.U. 2019 poz. 1781: https://api.sejm.gov.pl/eli/acts/DU/2019/1781/text.pdf
- [S45] Polish Act on AI systems (published 27 Jul 2026; in force 11 Aug 2026; full application 28 Oct 2026; KRiBSI): https://gdpr.pl/ustawa-o-systemach-sztucznej-inteligencji-weszla-w-zycie ; Sejm procedure: https://www.sejm.gov.pl/Sejm10.nsf/PrzebiegProc.xsp?nr=2443
- [S46] Belgium AI Act authorities (secondary): https://www.regulatoryai.eu/ai-act-belgium/ ; https://cms.law/en/int/expert-guides/ai-regulation-scanner/belgium
- [S47] Fundacja Orange with UODO as content partner, *Wizerunek dziecka w internecie. Publikować czy nie?* (Warsaw, June 2024), hosted by UODO: https://uodo.gov.pl/pl/file/4958
- [S48] Future of Privacy Forum (D. Dushi), "Red Lines under EU AI Act: Unpacking the prohibition of emotion recognition in the workplace and education institutions", 24 Mar 2026: https://fpf.org/blog/red-lines-under-eu-ai-act-unpacking-the-prohibition-of-emotion-recognition-in-the-workplace-and-education-institutions/
- [S49] SUT research-ethics commission, existence and date reported in: "Aspekty normatywne i aktualna sytuacja komisji etyki badań naukowych z udziałem ludzi na polskich uczelniach technicznych" (2022): https://www.researchgate.net/publication/366550639 (secondary; not confirmed on polsl.pl)
- [S50] TechXplore, "Microsoft age-estimate tool unleashed real-time virality", 1 May 2015: https://techxplore.com/news/2015-05-microsoft-age-estimate-tool-unleashed-real-time.html
- [S51] Global News, "Microsoft assures users its age-guessing app does not keep photos", 5 May 2015: https://globalnews.ca/news/1980578/microsoft-assures-users-its-age-guessing-app-does-not-keep-your-photos/
- [S52] EDPB Guidelines 02/2026 on Anonymisation, v1.0, adopted for public consultation 7 Jul 2026: https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202602_anonymisation_v1_en_0.pdf
- [S53] European Commission, Radio Equipment Directive page (Delegated Reg. (EU) 2022/30 applicable from 1 Aug 2025): https://single-market-economy.ec.europa.eu/sectors/electrical-and-electronic-engineering-industries-eei/radio-equipment-directive-red_en
- [S54] European Commission, Cyber Resilience Act summary: https://digital-strategy.ec.europa.eu/en/policies/cra-summary
- [S55] EDPB, "Data Protection Day 2026: keeping children's personal data safe online", 28 Jan 2026: https://www.edpb.europa.eu/news/news/2026/data-protection-day-2026-keeping-childrens-personal-data-safe-online_en
- [S56] euCONSENT, "Digital Age of Consent under the GDPR" (member-state table): https://euconsent.eu/digital-age-of-consent-under-the-gdpr/
- [S57] CJEU, C-212/13 *Ryneš*, 11 Dec 2014 (summary with paragraph references): https://www.dpcuria.eu/case?reference=C-212/13

---

## Verification log

Independent re-check by a verifier on 2026-10-01. Primary documents were downloaded and their text extracted (pdftotext) wherever possible.

| # | Claim | Verdict | Source used |
|---|---|---|---|
| 1 | SiW 2027: set-up 16 Mar 12-19h; fair 17 Mar 9-13h, 18-19 Mar 9-15h; ~4,500 pupils, ages 7-18, 15 min per group; 8 m² (4x2 m) booth with low table, TV + HDMI, Wi-Fi; visitors "mostly French and Dutch"; no funding for goodies; timeline row says "16-19 March 2026" (typo) | Confirmed | EUSurvey PDF export of the call form: https://ec.europa.eu/eusurvey/pdf/survey/1137942?lang=EN (form https://ec.europa.eu/eusurvey/runner/Call_SiW2027) |
| 2 | Deadline 6 Oct 2026; results 28 Oct 2026; communication workshop 4 Nov 2026 | Confirmed. Also: show workshop 9 Nov; final booth title due 23 Nov 2026 | same |
| 3 | Reg. (EU) 2026/1744 published 24 Jul 2026, in force 27 Jul 2026; Annex III to 2 Dec 2027, Annex I to 2 Aug 2028; Art. 50(2) grace to 2 Dec 2026 only for systems on the market before 2 Aug 2026; rest of Art. 50 from 2 Aug 2026; Art. 4 becomes a duty of means | Confirmed (secondary sources only; OJ text not retrievable) | https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo ; https://www.nicfab.eu/en/posts/digital-omnibus-ai-official-journal/ ; https://www.regulation-ai.eu/en/changes/ |
| 4 | "Sources disagree" on new Art. 5 prohibitions | **Corrected**: all three sources agree that points (ba)/(bb) (intimate imagery / CSAM generation) apply from 2 Dec 2026 | same three |
| 5 | Art. 50 guidelines are C(2026) 5054 final, 20 Jul 2026; paras 21-22 (research exclusions do not cover other uses or real-world testing); para 34 "child-friendly"; para 40 "periodic reminders" for children; "robotic companion pets" in scope; para 104 "any biometric categorisation systems (e.g. age or gender classification"; para 106 "including children"; para 107 exhibition-room entrance notice | Confirmed verbatim | https://ec.europa.eu/newsroom/dae/redirection/document/131215 |
| 6 | Prohibited-practices guidelines C(2025) 5052 final, 29.7.2025: paras 30-32 (R&D exclusion); 249 (smiling vs happy); 254 (workplace incl. museums, temporary sites, volunteers); 255 (no age limit; "interest and attention of students"); 266 (high-risk elsewhere); 277 (clothes/accessories excluded); 282 ("Attribute Estimation ... age, gender, ethnicity") | Confirmed verbatim | https://ai-act-service-desk.ec.europa.eu/sites/default/files/2025-08/guidelines_on_prohibited_artificial_intelligence_practices_established_by_regulation_eu_20241689_ai_act_english_ied3r5nwo50xggpcfmwckm3nuc_112367-1.PDF |
| 7 | EDPB Guidelines 3/2019: para 80 + example 4 (category distinction is outside Art. 9); para 82 (re-entering the area means Art. 9 "from the start"); example 5 ("even if their template is deleted within the shortest possible period"); para 129 ("Functions provided, but not necessary, must be deactivated") | Confirmed verbatim | https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines_201903_video_devices_en_0.pdf |
| 8 | EDPB Guidelines 05/2020 paras 125-128: Art. 8 applies only to ISS, which are services "at a distance" | Confirmed | https://www.edpb.europa.eu/system/files/documents/files/file1/edpb_guidelines_202005_consent_en.pdf |
| 9 | Polish Act of 20 Jul 2018, Art. 11(1)(9): "upowszechnianie i pomnażanie osiągnięć nauki i kultury" | Confirmed (original Dz.U. 2018 poz. 1668 text; current consolidated text not checked) | https://api.sejm.gov.pl/eli/acts/DU/2018/1668/text.pdf |
| 10 | UODO list M.P. 2019 poz. 666: two criteria "co do zasady"; criterion 10 examples "Zabawki interaktywne", "Usługi i zabawki dedykowane dzieciom", devices with "głośnik, mikrofon, kamera" | Confirmed, with a nuance added inline (that example concerns devices that transmit over telecom networks) | https://api.sejm.gov.pl/eli/acts/MP/2019/666/text.pdf |
| 11 | Draft high-risk guidelines (19 May 2026): Annex III 1(b) "sensitive" means GDPR Art. 9(1) attributes; ethnic origin, genetic data and health "of key relevance"; age/gender "not high-risk"; smartwatch mood monitor is high-risk even if results go "solely to the specific user" | Confirmed verbatim. **Corrected**: consultation closed 23 Jul 2026 (extended); still a draft | https://ec.europa.eu/newsroom/dae/redirection/document/128561 ; https://digital-strategy.ec.europa.eu/en/consultations/targeted-consultation-draft-guidelines-classification-high-risk-artificial-intelligence-systems |
| 12 | AI Act recital 16 categories (sex, age, hair colour, eye colour, tattoos, behavioural or personality traits, language ...) | Confirmed | https://artificialintelligenceact.eu/recital/16/ |
| 13 | Art. 99(3) EUR 35M / 7%; 99(4) EUR 15M / 3%; 99(8) Member States decide on fines for public bodies | Confirmed | https://artificialintelligenceact.eu/article/99/ |
| 14 | CVE-2025-2894, Unitree Go1 "CloudSail" backdoor, published 28 Mar 2025 | Confirmed | https://cveawg.mitre.org/api/cve/CVE-2025-2894 |
| 15 | UniPwn: BLE root exploit (command injection in the BLE Wi-Fi configuration) for Go2/G1/H1/B2, disclosed 20 Sep 2025, unpatched at disclosure | Confirmed. Whether Unitree has since patched it: UNVERIFIED | https://github.com/Bin4ry/UniPwn |
| 16 | arXiv 2509.14139: G1 exfiltrates telemetry "every 300 seconds" | Confirmed (Mayoral-Vilches, Makris, Finisterre; submitted 17 Sep 2025) | https://arxiv.org/abs/2509.14139 |
| 17 | Gender Shades: up to 34.7% error for darker-skinned females vs at most 0.8% for lighter-skinned males | Confirmed | https://proceedings.mlr.press/v81/buolamwini18a.html |
| 18 | Yang et al. 2020: 1,593 of 2,832 person synsets unsafe; 600,040 images; 158 visual | Confirmed | https://arxiv.org/pdf/1912.07726 |
| 19 | NIST IR 8525 quote; "webcam images are hardest" | Quote confirmed (May 2024). **Corrected**: webcam (border) photos were hardest for 4 of 6 algorithms | https://doi.org/10.6028/NIST.IR.8525 |
| 20 | Kahn et al. 2012: n = 90 (ages 9, 12, 15); "be trusted with secrets"; 15-year-olds less so | Confirmed | PubMed 22369338 via NCBI E-utilities |
| 21 | UNICEF Guidance on AI and Children 3.0, Dec 2025, 10 requirements; "prevent anthropomorphizing"; "invisible" data processing; "shortest period feasible"; emotional analytics prohibited from engaging with children | Confirmed (the emotional-analytics sentence sits in the context of commercial profiling, quoting GC 25) | https://www.unicef.org/innocenti/reports/policy-guidance-ai-children ; PDF https://www.unicef.org/innocenti/media/11991/file/UNICEF-Innocenti-Guidance-on-AI-and-Children-3-2025.pdf |
| 22 | SUT DPO: IOD@polsl.pl, tel. 32 400 3077 | Confirmed | https://www.polsl.pl/bkzb/ochrona-danych-osobowych/ |
| 23 | Belgian image right, CDE Art. XI.174: separate consent for taking and using; minors with discernment can increasingly consent | Confirmed (the "both parents" and crowd-exception details were not on the "principes" page checked; they may be on the sub-pages cited in S13) | https://www.autoriteprotectiondonnees.be/citoyen/themes/le-droit-a-l-image/principes |
| 24 | Status of the GDPR Digital Omnibus | **Resolved** (was UNVERIFIED): COM(2025) 837, 2025/0360(COD), EP committee stage, not adopted | https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2025/0360(COD) |
| 25 | CJEU C-184/20 *OT* ("revealing" read broadly) | **Resolved 2026-10-02**: 1 Aug 2022; indirect disclosure through deduction or cross-referencing falls under Art. 9(1) (paras 122-127) | https://www.dpcuria.eu/case?reference=C-184/20 |

**Continuation pass, 2026-10-02**

| # | Claim | Verdict | Source used |
|---|---|---|---|
| 26 | Omnibus: Reg. (EU) 2026/1744 of 8 Jul 2026, OJ L 24.7.2026, in force on the third day; Annex III to 2 Dec 2027, Annex I to 2 Aug 2028; new Art. 4 wording | Confirmed from the OJ (ELI page, partly readable) | https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng |
| 27 | Start date of Art. 5(1)(ba)/(bb) | Secondary sources: 2 Dec 2026 (cypheron, nicfab, Lewis Silkin). A model summary of the OJ said "immediately", but the Art. 113 text was cut off. Kept as secondary | https://cypheron.cz/en/resources/ai-act/omnibus-2026 |
| 28 | Art. 11(1)(9) of the Higher Education Act unchanged in the consolidated text | Confirmed (Dz.U. 2024 poz. 1571, the latest consolidated text listed by the Sejm ELI API) | https://api.sejm.gov.pl/eli/acts/DU/2024/1571/text.pdf |
| 29 | SUT is a public university; public universities are public finance sector units; such units are "organy i podmioty publiczne" for Art. 37 | Confirmed (Statute §1(1); UFP Art. 9(11); UODO Act Art. 9(1)) | [S44] |
| 30 | SUT child-protection standards: §5(3) consent wording; §6 written guardian consent to publish; crowd exception; §7 group framing; §9 media; no private recording | Confirmed verbatim (Order 50/2024) | [S40] |
| 31 | Register check requested at least 7 days before admitting a person (incl. doctoral candidates) to activity with minors | Confirmed (Order 240/2024 amending 37/2024, §4) | [S41] |
| 32 | SUT DPIA procedure: §16 screening list, RIG software, BBI, DPO consultation; §17 privacy by design in procurement specs | Confirmed verbatim (Order 62/2024) | [S42] |
| 33 | UODO-backed guide on children's images (June 2024): crowd exception; identifiable image remains personal data; alternatives | Confirmed verbatim | [S47] |
| 34 | EDPB Guidelines 02/2026 on anonymisation (7 Jul 2026, consultation version): three criteria; aggregates can relate to individuals (para. 17; example 17) | Confirmed verbatim | [S52] |
| 35 | Polish AI Systems Act: published 27 Jul 2026; in force 11 Aug 2026; full application 28 Oct 2026; KRiBSI | Confirmed (secondary, Polish legal press) | [S45] |
| 36 | Biometric Mirror traits; how-old.net (35,000 users; "discarded from memory" vs Terms); Sharkey and Sharkey abstract; C-212/13 para. 22 | Confirmed | [S33a; S33b; S50; S51; S27; S57] |
| 37 | EDPB children's-data guidelines | Not adopted as far as found (in preparation per EDPB, 28 Jan 2026) | [S55] |

## Omissions added by verifier

(Items 1, 2 and 5 were folded into section 9, controls 20-21, and section 14 in the 2026-10-02 pass. Items 3 and 4 are in sections 4.5 and 4.1.)

1. **Radio Equipment Directive cybersecurity rules are in force.** Delegated Regulation (EU) 2022/30 applies from **1 Aug 2025**. It brings in essential requirements Art. 3(3)(d),(e),(f) (network protection, **personal data and privacy protection**, fraud) for internet-connected radio equipment, which covers Wi-Fi/BLE robots (https://single-market-economy.ec.europa.eu/sectors/electrical-and-electronic-engineering-industries-eei/radio-equipment-directive-red_en). Procurement: buy a robot that is CE-marked for the EU market, with a Declaration of Conformity naming RED. A grey-market or direct-import robot without this is both a compliance and a security red flag, and that matters given CVE-2025-2894 and UniPwn.
2. **Cyber Resilience Act (Reg. (EU) 2024/2847):** in force 10 Dec 2024. Vulnerability-reporting duties for manufacturers have applied since **11 Sep 2026**; full application is **11 Dec 2027** (https://digital-strategy.ec.europa.eu/en/policies/cra-summary). It does not bind SUT at the fair. It is useful when choosing a vendor: ask whether the vendor has a CRA vulnerability-handling and reporting process.
3. **The Art. 50 guidelines name a robot pet that resembles the real animal** as not "obvious" AI (§3.2.1). An explicit, repeated AI disclosure is therefore legally required, not just good practice (added inline in section 4.5).
4. **New AI Act Art. 5(1)(ba)/(bb)** (non-consensual intimate imagery and CSAM generation), applying from 2 Dec 2026, as added by the Omnibus. This is one more reason never to use generative image models on photos of children, even internally.
5. **Physical child safety is barely covered.** The report deals with data, but a powered quadruped among 7-year-olds raises its own risks: pinch points in the leg joints, falls or jumps, LiPo battery handling and charging at the venue, and a reliable emergency stop. The General Product Safety Regulation (EU) 2023/988 applies to the vendor's product (not separately verified here). Recommendation (verifier's design advice): keep the robot in a stationary or "sit/stand" mode inside a low barrier or on a raised platform, with a staff-held e-stop or remote, and add physical-safety items to the DPIA risk register and the safeguarding plan.
6. **SiW call details relevant to the ethics plan** (from the call PDF): only MSCA fellows or alumni may be lead applicants; the Commission covers up to 3 team members for up to 4 nights; booths must be staffed at all times; a new evaluation criterion requires a 120-second video of the researcher (not of children). The call says "we will allow pupils of all ages to come to your booth", which supports planning for 7-year-olds.
7. **Polish Act consolidated text:** Art. 11(1)(9) was checked only in the original 2018 promulgation. The DPO should cite the current consolidated text (tekst jednolity) in the lawful-basis memo.

---

## Verification log (second pass)

Second independent adversarial pass, 2026-10-02. Primary documents were re-downloaded and text-extracted (pdftotext) where possible. Inline fixes are marked "[corrected by verifier: ...]".

| # | Claim | Verdict | Source used |
|---|---|---|---|
| V1 | SiW 2027: set-up 16 Mar; fair 17 Mar 9-13h, 18-19 Mar 9-15h; ~4,500 pupils aged 7-18; ~15 min per group; 8 m² (4x2 m) booth, low table, TV + HDMI, Wi-Fi; visitors "mostly French and Dutch"; no money for goodies; only MSCA fellows/alumni as lead; deadline 6 Oct 2026, results 28 Oct 2026, workshop 4 Nov 2026; timeline typo "16-19 March 2026" | Confirmed (call PDF re-extracted) | https://ec.europa.eu/eusurvey/pdf/survey/1137942?lang=EN |
| V2 | Reg. (EU) 2026/1744 of 8 Jul 2026, OJ 24 Jul 2026, in force on third day (27 Jul 2026); Annex III to 2 Dec 2027, Annex I to 2 Aug 2028; new Art. 4 wording ("take measures to support") | Confirmed | https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng ; https://www.hunton.com/privacy-and-cybersecurity-law-blog/eu-digital-omnibus-on-ai-enters-into-force |
| V3 | New Art. 5(1)(ba)/(bb) apply from 2 Dec 2026 | Confirmed (secondary, quoting amended Art. 113); an automated summary of the OJ again said "from entry into force", so it is still not read verbatim. Irrelevant to the design | https://artificialintelligenceact.eu/ai-act-explorer/digital-omnibus/ |
| V4 | Prohibited-practices Guidelines C(2025) 5052: para. 249 smiling vs happy; para. 254 workplace incl. museums, temporary sites, any status; para. 255 "interest and attention of students"; para. 277 clothes/accessories excluded | Confirmed verbatim | S4 PDF |
| V5 | "Workplace limb covers the booth, so emotion inference on visitors is prohibited" | **Corrected**: the Guidelines say customer emotion recognition is not prohibited (call-centre and supermarket examples) unless employees are tracked. The precautionary conclusion stands, but the reason is narrower | S4 PDF, examples after para. 254 |
| V6 | Art. 50 Guidelines C(2026) 5054 (20 Jul 2026): "robotic companion pets" in scope; para. 34 child-friendly; para. 40 periodic reminders for children; para. 42 "assess and demonstrate"; para. 104 "any biometric categorisation systems (e.g. age or gender classification"; §3.2.1 lifelike robot pet not obvious | Confirmed verbatim. **Nuance added**: the example concerns a pet "looking highly similar to its natural equivalent" | https://ec.europa.eu/newsroom/dae/redirection/document/131215 |
| V7 | EDPB 3/2019 para. 82 (re-entering the area means Art. 9 "from the start"); example 5 ("even if their template is deleted within the shortest possible period"); para. 129 | Confirmed verbatim | S7 PDF |
| V8 | CJEU C-184/20 *OT*, 1 Aug 2022: "revealing" covers indirect disclosure "following an intellectual operation involving deduction or cross-referencing" (paras 120-128) | Confirmed | https://www.dpcuria.eu/case?reference=C-184/20 |
| V9 | Higher Education Act Art. 11(1)(9) "upowszechnianie i pomnażanie osiągnięć nauki i kultury"; Dz.U. 2024 poz. 1571 is the latest consolidated text | Confirmed (Sejm ELI API lists 2024/1571 as current, status "obowiązujący"; no 2025/2026 consolidated text) | https://api.sejm.gov.pl/eli/acts/DU/2018/1668/references ; https://api.sejm.gov.pl/eli/acts/DU/2024/1571/text.pdf |
| V10 | Public Finance Act Art. 9 pt 11 "uczelnie publiczne"; consolidated Dz.U. 2025 poz. 1483 | Confirmed (obwieszczenie of 26 Sep 2025, published 28 Oct 2025) | https://api.sejm.gov.pl/eli/acts/DU/2025/1483/text.pdf |
| V11 | SUT Order 50/2024 §5(3) "na podstawie zgody opiekunów małoletniego (wizerunek)"; §6(1) written guardian consent to publish a recorded image; §6(3) crowd exception | Confirmed verbatim. The child-facing summary on BIP also says staff may not "bez zgody Twoich rodziców lub opiekunów robić Ci zdjęć, nagrywać filmów" | https://bip.polsl.pl/wp-content/uploads/sites/4/2024/07/M.2024.260.Z.50.pdf ; https://bip.polsl.pl/ochrona-maloletnich/ |
| V12 | Order 240/2024 (9 Dec 2024) amending 37/2024: register request to HR at least 7 days before; separate form for doctoral candidates and non-employees | Confirmed verbatim. **Omission corrected**: Art. 21 also requires KRK and foreign criminal records | https://bip.polsl.pl/wp-content/uploads/sites/4/2024/12/M.2024.1463.Z.240.pdf ; https://www.gov.pl/web/sprawiedliwosc/pytania-do-ustawy-o-ochronie-dzieci2 |
| V13 | Order 62/2024 §16(1)-(4): DPIA in RIG ("Reed Into Green"), by BBI with the project owner, consulted with the DPO; §17(3)-(4): privacy-by-design requirements in procurement specs, consulted with the DPO | Confirmed verbatim. **Corrected**: BBI does not appear in SUT's 1 Jan 2026 org chart; the DPO sits in BKZB | S42 PDF; https://bip.polsl.pl/wp-content/uploads/sites/4/2026/01/Struktura_organizacyjna_PS_na_dzien_1.01.2026.pdf ; https://www.polsl.pl/bkzb/lpodo/ |
| V14 | SUT DPO contact: IOD@polsl.pl, tel. 32 400 3077 | Confirmed (also BKZB@polsl.pl; ul. Akademicka 2A, Gliwice) | https://www.polsl.pl/bkzb/ochrona-danych-osobowych/ |
| V15 | UODO list M.P. 2019 poz. 666: "co do zasady" two criteria; "Zabawki interaktywne", "Usługi i zabawki dedykowane dzieciom" | Confirmed | https://api.sejm.gov.pl/eli/acts/MP/2019/666/text.pdf |
| V16 | EDPB Guidelines 02/2026 on anonymisation, adopted 7 Jul 2026 for consultation; No Record Isolation / No Linkage / No Inference; para. 17 on aggregates | Confirmed verbatim | S52 PDF |
| V17 | Polish AI Systems Act: adopted 3 Jul 2026, published 27 Jul 2026, main part in force 11 Aug 2026, enforcement provisions 28 Oct 2026; KRiBSI | Confirmed (secondary legal press; Dz.U. 2026 poz. 1003 per infor.pl metadata) | https://gdpr.pl/ustawa-o-systemach-sztucznej-inteligencji-weszla-w-zycie ; https://www.infor.pl/akt-prawny/DZU.2026.208.0001003,metryka,ustawa-o-systemach-sztucznej-inteligencji.html |
| V18 | Belgium: BIPT lead authority by government policy only; no statute by mid-2026 | Unverifiable from primary sources (secondary sources only, consistent with the report) | https://www.regulatoryai.eu/ai-act-belgium/ ; https://cms.law/en/int/expert-guides/ai-regulation-scanner/belgium |
| V19 | Draft high-risk guidelines still draft; no final version | Confirmed (secondary sources say final adoption expected "by end of 2026"; one secondary source dates the draft to 27 May rather than 19 May 2026) | https://digital-strategy.ec.europa.eu/en/library/draft-commission-guidelines-classification-high-risk-ai-systems ; https://www.hlc.com/en/publications/european-commission-publishes-long-awaited-guidelines-on-high-risk-ai-systems |
| V20 | CRA reporting from 11 Sep 2026, full application 11 Dec 2027; RED Delegated Reg. 2022/30 applies from Aug 2025 | Confirmed | https://digital-strategy.ec.europa.eu/en/policies/cra-summary ; https://single-market-economy.ec.europa.eu/sectors/electrical-and-electronic-engineering-industries-eei/radio-equipment-directive-red_en |
| V21 | UniPwn unpatched | Confirmed, and no patched version documented. CVE IDs added inline | https://github.com/Bin4ry/UniPwn ; https://github.com/advisories/GHSA-27p8-m7h9-xchc |
| V22 | GDPR Digital Omnibus (2025/0360(COD)) still in committee | Confirmed (no committee vote as of mid-Sep 2026, per secondary trackers) | https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2025/0360(COD) |
| V23 | EDPB children's-data guidelines not adopted | Confirmed (on the 2026-2027 work programme, not adopted) | https://www.edpb.europa.eu/system/files/documents/2026-02/edpb_work-programme_2026-2027_en.pdf |

## Omissions added by verifier (second pass)

1. **Art. 5(1)(f) protects workers, not visitors.** See the inline corrections in sections 0 and 4.3. Keep the "no emotion inference" rule, but justify it in the proposal and DPIA as: (a) staff and teachers inevitably in frame; (b) the education-institution question is unsettled; (c) Annex III 1(c) high-risk status and the Art. 50(3) notice; (d) weak science and UNICEF/CRC guidance. Do not claim a blanket legal ban.
2. **Criminal-record checks beyond the register (Art. 21, Polish Act of 13 May 2016 as amended).** Besides the Register of Sex Offenders, KRK information is required. Foreign citizens, and anyone who lived abroad in the last 20 years, must supply criminal-record certificates from those countries, or sworn statements where none are issued (MoJ FAQ: https://www.gov.pl/web/sprawiedliwosc/pytania-do-ustawy-o-ochronie-dzieci2). The TUAI DCs are likely non-Polish under the MSCA mobility rule, so start in Jan 2027. A further amending Act of 5 Aug 2025 exists (Sejm print 1381); its exact changes to Art. 21 are **UNVERIFIED**.
3. **SUT reorganisation.** The Information Security Office (BBI) named in Order 62/2024 is absent from the 1 Jan 2026 org chart. The DPO is in the Biuro Kontroli Zarządczej i Bezpieczeństwa (BKZB@polsl.pl). Ask the DPO whether Order 62/2024 has been amended or replaced before relying on its §16-17 wording (**UNVERIFIED**).
4. **New EU Toy Safety Regulation (EU) 2025/2509** (adopted 26 Nov 2025, OJ 12 Dec 2025) repeals Directive 2009/48/EC. It requires toys with AI to comply with the AI Act, requires internet-connected toys to carry RED cybersecurity safeguards, and calls for "safety, security and privacy by design" (https://eur-lex.europa.eu/eli/reg/2025/2509/oj/eng). Its application date is **UNVERIFIED** (believed to be several years out). Until then, the Toy Safety Directive 2009/48/EC applies. If the robot we buy is marketed as a toy (e.g. a hobby or educational robot dog for under-14s), check its CE marking under the toy rules as well as RED. If it is not a toy (e.g. Unitree Go2), the GPSR applies.
5. **UniPwn CVEs and vendor stance.** CVE-2025-35027, -60017, -60250 and -60251. No patched version is documented, and Unitree reportedly said a fix needs "quarters or years". Any Go2-family purchase must assume BLE is exploitable: physically disable or shield BLE where possible, never power the robot near the public with BLE on, and keep it on an isolated network.
