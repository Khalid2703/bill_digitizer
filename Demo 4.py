import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import subprocess


image = cv2.imread("assets/captured_bill2.jpg")
image = cv2.resize(image,(0,0),fx = 0.2, fy =0.2)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


scale_percent = 150  
width = int(gray.shape[1] * scale_percent / 100)
height = int(gray.shape[0] * scale_percent / 100)
dim = (width, height)
resized_image = cv2.resize(gray, dim, interpolation=cv2.INTER_LINEAR)
a=resized_image

#thresh_image = cv2.adaptiveThreshold(resized_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
 #                                    cv2.THRESH_BINARY, 11, 2)


#processed_image = cv2.medianBlur(thresh_image, 3)

# Optionally sharpen the image
#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
#sharpened_image = cv2.dilate(processed_image, kernel, iterations=1)


cv2.imshow("Processed Image", a)

custom_config = r'--oem 3 --psm 6'  

extracted_text = pytesseract.image_to_string(a, config=custom_config)


print("Extracted Text:\n", extracted_text)

with open("bill_text.txt", "w") as file:
    file.write(extracted_text)

#subprocess.Popen(["notepad.exe", "bill_text.txt"])


cv2.waitKey(0)
cv2.destroyAllWindows()
