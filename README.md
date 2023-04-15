# AccCam
Accessibility Enabled Camera with Closed Captioning and Motion Tracking for Sr Design Capstone Project

### Notes:
- Enabling the `imshow` function increases the latency (use for testing)
- FSM integrates both *FaceRecognition.py* and *TempContrast.py* scripts.
- Both live and prerecorded audio recognition scripts use Google Speech Recognition
- For the `cap = cv2.VideoCapture(2)`, I have this set up, so it looks for our webcam. 
  - Mess around with the integer parameter until you find the camera you're looking for 
- If using an Arducam/Pi camera module, the framerate will significantly drop 
  - We found that using an external webcam connected to our servo yields good results

### Done:
- Image Recognition
- Optical Flow
- FSM Integration

### TODO:
- Camera Centering
- Multiprocess NLP and CV
- Multithread CV processing and `imread`
- Tweak and tune recognition parameters

### Sources:
- Haar Cascade Tutorial: https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html
- Haar Cascade Paper: https://www.researchgate.net/publication/220660094_Robust_Real-Time_Face_Detection

---

*This project aims to fulfill University of Pittsburgh Swanson School of Engineer's Electrical and Computer Engineering Senior Design Capstone Project*