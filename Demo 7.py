import pytesseract
from PIL import Image
import cv2
import numpy as np
from collections import defaultdict
import json
import re

class BillDigitizer:
    def __init__(self):
        
        self.custom_config = r'--oem 3 --psm 6'
        
    def clean_text(self, text):
        """
        Clean and validate text to prevent JSON errors
        """
        if not isinstance(text, str):
            return ""
        
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace('\n', ' ').replace('\r', '')
        return text.strip()

    def preprocess_image(self, image):
        """
        Enhance image for better text detection
        """
        try:
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            
            thresh = cv2.adaptiveThreshold(
                gray, 255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            
            denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
            
            
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
            processed = cv2.dilate(denoised, kernel, iterations=1)
            
            return processed
        except Exception as e:
            print(f"Error in image preprocessing: {str(e)}")
            return image

    def extract_text(self, image_path):
       
        try:
           
            img = cv2.imread(image_path)
            if img is None:
                raise FileNotFoundError(f"Could not read image at: {image_path}")
            
            
            processed = self.preprocess_image(img)
            
            
            cv2.imwrite("temp_processed.png", processed)
            
            
            data = pytesseract.image_to_data(
                Image.open("temp_processed.png"),
                config=self.custom_config,
                output_type=pytesseract.Output.DICT
            )
            
            return data, img.shape
            
        except Exception as e:
            print(f"Error in text extraction: {str(e)}")
            raise

    def create_bill_structure(self, data, image_shape):
        """
        Create structured bill data from extracted text
        """
        try:
            height = image_shape[0]
            structured_data = {
                'header': [],
                'items': [],
                'total': [],
                'footer': []
            }
            
            
            for i in range(len(data['text'])):
                conf = int(data['conf'][i])
                if conf > 0:  # Filter valid confidence scores
                    text = self.clean_text(data['text'][i])
                    if text:  # Only process non-empty text
                        item = {
                            'text': text,
                            'confidence': conf,
                            'coordinates': {
                                'x': data['left'][i],
                                'y': data['top'][i],
                                'width': data['width'][i],
                                'height': data['height'][i]
                            }
                        }
                        
                        
                        y_pos = data['top'][i] / height
                        if y_pos < 0.2:
                            structured_data['header'].append(item)
                        elif y_pos > 0.8:
                            structured_data['footer'].append(item)
                        elif self.is_total_line(text):
                            structured_data['total'].append(item)
                        else:
                            structured_data['items'].append(item)
            
            return structured_data
            
        except Exception as e:
            print(f"Error in creating bill structure: {str(e)}")
            raise

    def is_total_line(self, text):
        """
        Check if text line is related to totals
        """
        total_keywords = ['total', 'sum', 'amount', 'balance', 'due', 'tax']
        return any(keyword in text.lower() for keyword in total_keywords)

    def visualize_results(self, image_path, structured_data):
        """
        Create visual representation of detected text
        """
        try:
            img = cv2.imread(image_path)
            colors = {
                'header': (255, 0, 0),    
                'items': (0, 255, 0),     
                'total': (0, 0, 255),     
                'footer': (255, 255, 0)   
            }
            
            
            for section, items in structured_data.items():
                for item in items:
                    coords = item['coordinates']
                    x = coords['x']
                    y = coords['y']
                    w = coords['width']
                    h = coords['height']
                    
                    
                    cv2.rectangle(
                        img, 
                        (x, y), 
                        (x + w, y + h), 
                        colors[section], 
                        2
                    )
                    
                    
                    cv2.putText(
                        img,
                        f"{section}: {item['confidence']}%",
                        (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        colors[section],
                        1
                    )
            
            
            cv2.imwrite('bill_visualization.png', img)
            
        except Exception as e:
            print(f"Error in visualization: {str(e)}")

def main():
    try:
        
        digitizer = BillDigitizer()
        
        
        image_path = r"C:\Users\hp\OneDrive\Documents\OpenCV Project\assets\b3.jpg"
        
        
        print("Extracting text from image...")
        data, image_shape = digitizer.extract_text(image_path)
        
        print("Creating bill structure...")
        structured_data = digitizer.create_bill_structure(data, image_shape)
        
        
        print("Saving structured data...")
        with open('bill_data.json', 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, indent=4, ensure_ascii=False)
        
        
        print("Creating visualization...")
        digitizer.visualize_results(image_path, structured_data)
        
        print("\nProcessing complete!")
        print("- Structured data saved to 'bill_data.json'")
        print("- Visualization saved to 'bill_visualization.png'")
        
    except Exception as e:
        print(f"Program failed: {str(e)}")
        
    finally:
        
        import os
        if os.path.exists("temp_processed.png"):
            try:
                os.remove("temp_processed.png")
            except:
                pass

if __name__ == "__main__":
    main()