import os, cv2, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
M="models"
def base(f): return mpt.BaseOptions(model_asset_path=os.path.join(M,f))
for name in ["zidane.jpg","bus.jpg"]:
    fr=cv2.imread(os.path.join(M,name)); h,w=fr.shape[:2]
    img=mp.Image(image_format=mp.ImageFormat.SRGB,data=cv2.cvtColor(fr,cv2.COLOR_BGR2RGB))
    pl=vision.PoseLandmarker.create_from_options(vision.PoseLandmarkerOptions(base_options=base("pose_landmarker_full.task"),num_poses=5))
    fd=vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(base_options=base("blaze_face_short_range.tflite")))
    fl=vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=base("face_landmarker.task"),num_faces=5,output_face_blendshapes=True))
    od=vision.ObjectDetector.create_from_options(vision.ObjectDetectorOptions(base_options=base("efficientdet_lite0.tflite"),score_threshold=0.4,category_allowlist=["person"]))
    yn=cv2.FaceDetectorYN.create(os.path.join(M,"face_detection_yunet_2023mar.onnx"),"",(w,h),0.6,0.3,5000)
    _,faces=yn.detect(fr)
    fsz=[int(f[2]) for f in faces] if faces is not None else []
    r=fl.detect(img)
    print(name,(w,h),"| pose(full,num_poses=5):",len(pl.detect(img).pose_landmarks),"| blazeface-short:",len(fd.detect(img).detections),
          "| face_landmarker:",len(r.face_landmarks),"| EffDet-Lite0 persons:",len(od.detect(img).detections),"| YuNet faces:",len(fsz),"widths px",fsz)
    if r.face_blendshapes:
        top=sorted(r.face_blendshapes[0],key=lambda c:-c.score)[:5]; print("   top blendshapes:",[(c.category_name,round(c.score,2)) for c in top])
