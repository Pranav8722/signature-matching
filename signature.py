import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.feature import hog

def preprocess_image(path):
    # Read the image
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # Apply GaussianBlur to reduce noise
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # Apply adaptive thresholding
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                cv2.THRESH_BINARY, 11, 2)
    return img

def extract_features(image):
    features, hog_image = hog(image, orientations=9, pixels_per_cell=(8, 8),
                              cells_per_block=(2, 2), visualize=True)
    return features

def match(path1, path2):
    img1 = preprocess_image(path1)
    img2 = preprocess_image(path2)
    # Resize images for comparison
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))
    features1 = extract_features(img1)
    features2 = extract_features(img2)
    similarity_value = np.dot(features1, features2) / (np.linalg.norm(features1) * np.linalg.norm(features2))
    return float(similarity_value * 100)
