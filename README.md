# Egyptian ID Card Recognition System 💳

A Python-based application to detect and process Egyptian ID cards using YOLO and EasyOCR.

---

## Features

- **ID Card Detection**: Automatically detects and crops the ID card.
- **Field Detection**: Identifies key fields like name, address, and national ID.
- **Text Extraction**: Extracts text in Arabic and English.
- **ID Decoding**: Decodes the national ID to extract:
  - Birth Date
  - Governorate
  - Gender
  - birth place
  - location
  - nationality

- **Web Interface**: Easy-to-use interface built with Streamlit.

---

Upload an Egyptian ID card image using the sidebar.

View the results, including:

Name
National ID
Address
Birth Date, Governorate, and Gender

Project Structure
egyptian-id-recognition/

- **`app.py`**: Main application file for running the Streamlit interface.  
- **`utils.py`**: Contains processing functions for detection and text extraction.  
- **`requirements.txt`**: Lists all dependencies required to run the project.  
- **`README.md`**: Project documentation and usage guide.  
- **YOLO Models**: Pretrained YOLO models (`detect_id.pt`, `detect_objects.pt`, `detect_id_card.pt`) for ID and field detection.  
- **`d2.jpg`**: Sample output image generated during processing.  


Contact
GitHub: naso7y

Email: ahmed.noshy2004@gmail.com
