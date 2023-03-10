# AccCam
Accessibility Enabled Camera with Closed Captioning and Motion Tracking for Sr Design Capstone Project

Notes:
- Enabling the *imshow* function increases the latency (use for testing)
- FSM integrates both *FaceRecognition.py* and *TempContrast.py* scripts.
- Both live and prerecorded audio recognition scripts use Google Speech Recognition

Done:
- Image Recognition
- Optical Flow
- FSM Integration

TODO:
- Camera Centering
- Multiprocess NLP and CV
- Multithread CV processing and *imread*
- Tweak and tune recognition parameters

Sources:
- Haar Cascade Tutorial: https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html
- Haar Cascade Paper: https://www.researchgate.net/publication/220660094_Robust_Real-Time_Face_Detection

