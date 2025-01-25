import easyocr
import cv2


img_path = 'assets/captured_bill2.jpg'
img = cv2.imread(img_path)

if img is None:
    print("Image not loaded. Please check the file path.")
else:
    print("Image loaded successfully.")
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    reader = easyocr.Reader(['en'])
    
   
    results = reader.readtext(img_gray)
    
   
    for (bbox, text, prob) in results:
        print(f" {text},{prob}")