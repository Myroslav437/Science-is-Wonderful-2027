# Demo video - storyboard and script

Rendered automatically by `prototype/video/render_video.py` from the real prototype UI (real recordings, real model outputs). Stage titles and captions are added for the video; the robot's lines are spoken by an offline TTS voice (Piper, en_US-amy); the visitors' own recorded voices are mixed in (loudness-matched, lowered while the robot speaks).

| # | Scene | Time | On screen | Visitor audio | Robot says | Caption |
|---|---|---|---|---|---|---|
| 1 | How does a robot see you? | 0:00-0:07 | visitor v01 (clean), sensors: off |  |  | A small robot dog builds a picture of a visitor from its senses - and explains itself. |
| 2 | meet | 0:07-0:16 |  |  | Hi! I'm a robot dog. I'm a computer program, not alive. Let's see what I can learn about you. | The robot's camera and microphone stay OFF until the visitor switches them on. |
| 3 | Demo A - Eyes + ears | 0:16-0:50 | sensors: eyes+ears, playing x1.0 | v01 clean 0-33 s | Thank you! My eyes and ears are on. | On the screen the picture is pixelated. The robot looks, then forgets each picture. / The ears pick out 'horse' from what the visitor says: favourite animal - horse. / The eyes measure the colours of the top: white clothes - but only a guess. / Every answer comes with how sure the robot is, and why. |
| 4 | Demo B - Eyes only | 0:50-1:01 | visitor v01 (clean), sensors: eyes only |  | OK. I'll only use my eyes. | Ears off: the favourite animal turns into a question mark. The clothes colour stays. |
| 5 | Demo C - Ears only | 1:01-1:12 | sensors: ears only |  | OK. I'll only use my ears. | Eyes off: it still heard 'horse', but it cannot know what the visitor is wearing. |
| 6 | Demo D - Why does the robot think this? | 1:12-1:44 | visitor v02 (clean), sensors: eyes+ears | v02 clean 2.8-13.4 s; v02 clean 26-31.5 s | I heard 'brown' twice, so I think your favourite colour is brown. Was I right? | Clue balance: 'bunny' and 'rabbit' many times. Even 'not a cat or a dog' adds small cat and dog clues. / Favourite colour BROWN? Listen: she said 'ginger brown' about her rabbit's fur. / The robot spots words but does not understand them. AI can be sure - and still wrong. |
| 7 | Trouble 1 - Noisy room | 1:44-1:57 | visitor v06 (noisy-ears) | v06 noisy-ears 20-26.5 s |  | Listen to what the robot heard: she says 'elephant', but the crowd drowns it - so the robot says it doesn't know. |
| 8 | Trouble 1b - Other voices | 1:57-2:09 | visitor v05 (noisy-ears) | v05 noisy-ears 12-18 s |  | Now the robot is SURE her favourite colour is white. Listen: the 'white' comes from other people in the crowd, not from her. |
| 9 | Trouble 2 - Foggy lens | 2:09-2:20 | visitor v01 (foggy-eyes) |  |  | Foggy lens: the white top now looks dark, so the robot guesses BLACK. A bad sensor can fool the robot, not only make it unsure. |
| 10 | Demo E - The picture builds up | 2:20-2:51 | visitor v06 (clean), playing x1.0 | v06 clean 0-30 s |  | At first the robot knows nothing. Clue by clue its picture fills in: glasses, clothes, words. / Each part of the drawing shows which sense found it - eyes or ears. |
| 11 | The robot's imagination | 2:51-3:02 | visitor v01 (clean) |  |  | An image generator restyles the robot's own drawing into a robot friend - using only the words the robot believes, never a photo. |
| 12 | Things the robot will never guess | 3:02-3:12 |  |  | I will never guess who you are, how you feel, your age, your gender, or where you come from. | Faces and voices don't reveal these reliably - and guessing them about children is not OK. |
| 13 | card | 3:12-3:22 |  |  | Here is how I saw you. Now I will forget everything. Bye! | The take-home card has no photo and no name. When the visitor leaves, the robot forgets everything. |
| 14 | TUAI doctoral network - DC5 sensor fusion & DC7 explainable AI | 3:22-3:31 |  |  |  | Recordings: Seamless Interaction (Meta, CC BY-NC 4.0, pixelated). Models: MediaPipe, CLIP ViT-B/32, Silero VAD, Whisper small, LCM-Dreamshaper. All on one laptop, offline. |

Total length: 3 min 31 s.
