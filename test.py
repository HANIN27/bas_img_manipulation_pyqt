import cv2

# Correct paths
AGE_PROTOTXT = r"C:\Users\Dr. HOMEIRA NISHAT\Desktop\pyqt sam\models\age_deploy.prototxt"
AGE_MODEL = r"C:\Users\Dr. HOMEIRA NISHAT\Desktop\pyqt sam\models\age_net.caffemodel"

# Load model
try:
    age_net = cv2.dnn.readNetFromCaffe(AGE_PROTOTXT, AGE_MODEL)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
