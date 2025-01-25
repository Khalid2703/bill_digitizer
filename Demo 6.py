import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import subprocess
import tkinter as tk
from tkinter import filedialog


image = cv2.imread("assets/b3.jpg")
image = cv2.resize(image,(0,0),fx = 1, fy =1)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

scale_percent = 150  
width = int(gray.shape[1] * scale_percent / 100)
height = int(gray.shape[0] * scale_percent / 100)
dim = (width, height)
resized_image = cv2.resize(gray, dim, interpolation=cv2.INTER_LINEAR)
a=resized_image




cv2.imshow("Processed Image", a)

custom_config = r'--oem 3 --psm 6'  


extracted_text = pytesseract.image_to_string(a, config=custom_config)


print("Extracted Text:\n", extracted_text)

with open("bill_text.txt", "w") as file:
    file.write(extracted_text)

#subprocess.Popen(["notepad.exe", "bill_text.txt"])


cv2.waitKey(0)
cv2.destroyAllWindows()

def display_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        text_widget.delete(1.0, tk.END)  # Clear any existing text
        text_widget.insert(tk.END, content)  # Insert the file content
    except FileNotFoundError:
        text_widget.insert(tk.END, "File not found.")


root = tk.Tk()
root.title("Display Notepad File Content")
widget1=tk.Label(root,text='Welcome Back')
widget1.pack()
file_path = file_path = r"C:\Users\hp\OneDrive\Documents\OpenCV Project\bill_text.txt"
widget2 = tk.Button(root, text="Show the Bill", 
                   command=lambda: display_file_content(file_path))
widget2.pack()

text_widget = tk.Text(root, wrap='word', height=20, width=60)
text_widget.pack(padx=10, pady=10)


#display_file_content(file_path)

root.mainloop()