import cv2 
import pytesseract

def extract_text(image_path):
    img=cv2.imread(image_path)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    text=pytesseract.image_to_string(gray)

    return text 


if __name__=='__main__':
    image_path='D:/personal/Personal_Projects/student_rag_app/Backend/image.png'
    print(extract_text(image_path))  # prints the text extracted from the image
