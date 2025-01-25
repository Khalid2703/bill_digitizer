# Bill Digitizer

## Project Overview
Bill Digitizer is an advanced Python-based Optical Character Recognition (OCR) tool designed to extract and structure text from bill and receipt images automatically.

## Key Features
- Automated text extraction from bill images
- Advanced image preprocessing techniques
- Structured data generation
- Visual text area detection
- Confidence-based text filtering

## Technical Capabilities
- Uses pytesseract for OCR
- Leverages OpenCV for image processing
- Supports various bill and receipt formats
- Generates structured JSON output
- Provides visual annotation of detected text

## Installation Requirements
### Prerequisites
- Python 3.8+
- Tesseract OCR installed
- OpenCV
- pytesseract

### Setup Steps
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt


   from bill_digitizer import BillDigitizer

# Initialize the digitizer
digitizer = BillDigitizer()

# Process a bill image
image_path = 'path/to/your/bill/image.jpg'
structured_data = digitizer.process_image(image_path)
