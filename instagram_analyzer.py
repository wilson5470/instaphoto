import cv2
import numpy as np

def calculate_brightness(image):
    """Calculate the average brightness of the image."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    _, _, v = cv2.split(hsv)
    return np.mean(v)

def calculate_colorfulness(image):
    """Calculate a simple colorfulness metric."""
    (B, G, R) = cv2.split(image.astype("float"))
    rg = np.absolute(R - G)
    yb = np.absolute(0.5 * (R + G) - B)
    (rb_mean, rb_std) = (np.mean(rg), np.std(rg))
    (yb_mean, yb_std) = (np.mean(yb), np.std(yb))
    std_root = np.sqrt((rb_std ** 2) + (yb_std ** 2))
    mean_root = np.sqrt((rb_mean ** 2) + (yb_mean ** 2))
    return std_root + (0.3 * mean_root)

def detect_faces(image):
    """Detect faces in the image using Haar Cascade."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(faces)

def analyze_image(image_path):
    """Analyze the image and return a score and comment."""
    image = cv2.imread(image_path)
    if image is None:
        return "Error: Could not load image."

    brightness = calculate_brightness(image)
    colorfulness = calculate_colorfulness(image)
    faces = detect_faces(image)

    # Normalize metrics (these thresholds can be adjusted)
    brightness_score = min(max((brightness - 50) / 150, 0), 1)  # Assuming 0-255 range
    colorfulness_score = min(colorfulness / 100, 1)  # Assuming colorfulness < 100 is good
    face_score = min(faces, 1)  # 0 or 1 face

    # Weighted sum for final score
    score = (brightness_score * 0.4) + (colorfulness_score * 0.4) + (face_score * 0.2)
    score = int(score * 100)

    # Generate humorous comment
    if score > 80:
        comment = "90% - Ready for the 'gram! Expect likes to rain."
    elif score > 60:
        comment = "75% - Solid, but a filter wouldn't hurt."
    elif score > 40:
        comment = "50% - Meh, maybe crop it or something."
    else:
        comment = "30% - Better luck next time, or keep it for the memories."

    return f"Score: {score}% - {comment}"

# Example usage
image_path = "path/to/your/image.jpg"
print(analyze_image(image_path))
