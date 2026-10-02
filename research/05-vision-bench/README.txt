Micro-benchmark scripts used for research/05-vision-models.md (run 2026-10-01/02 on the dev laptop,
Intel Core Ultra 7 255U, Windows 11, project .venv: Python 3.12, torch 2.14.1+cpu, onnxruntime 1.30,
mediapipe 1.0.1, opencv 5.0, ultralytics 8.4.171, open_clip 3.3.0, transformers 5.18).
Extra packages (onnx, openvino 2026.4.1, rtmlib 0.0.16, num2words) were installed into a separate
folder and added via PYTHONPATH, NOT into the project .venv.

Scripts expect a ./models folder containing:
  zidane.jpg, bus.jpg                      https://ultralytics.com/images/{zidane,bus}.jpg
  face_detection_yunet_2023mar.onnx        https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet
  MediaPipe .task/.tflite files            https://storage.googleapis.com/mediapipe-models/<task>/<model>/<precision>/latest/<file>
                                           (pose_landmarker_lite/full, blaze_face_short_range, face_landmarker,
                                            gesture_recognizer, selfie_multiclass_256x256, efficientdet_lite0 int8)
Re-run them on the actual exhibition machine with all components running concurrently.
Set YOLO_AUTOINSTALL=false so Ultralytics does not try to pip-install packages at runtime.
