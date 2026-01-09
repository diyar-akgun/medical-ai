import cv2

# Grayscale medical image example
img = cv2.imread("sample.png", cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Image not found.")
else:
    print("Image shape:", img.shape)
    cv2.imwrite("output.png", img)
