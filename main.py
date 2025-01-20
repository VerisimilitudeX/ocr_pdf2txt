from pdf2image import convert_from_path
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

def ocr_pdf_to_text(pdf_path, output_txt_path):
    try:
        images = convert_from_path(pdf_path)
        
        with open(output_txt_path, 'w') as output_file:
            for i, image in enumerate(images):
                print(f"Processing page {i + 1}/{len(images)}...")
                
                text = pytesseract.image_to_string(image)
                
                output_file.write(f"--- Page {i + 1} ---\n")
                output_file.write(text + "\n")
                
        print(f"Text successfully extracted to {output_txt_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    pdf_path = '/Users/verisimilitude/Documents/GitHub/math_ia/math_ia.pdf'  # replace with your PDF file path
    output_txt_path = '/Users/verisimilitude/Downloads/output.txt'  # replace with desired output file path

    ocr_pdf_to_text(pdf_path, output_txt_path)