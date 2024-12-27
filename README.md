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
- **Web Interface**: Easy-to-use interface built with Streamlit.

---

Upload an Egyptian ID card image using the sidebar.

View the results, including:

Name
National ID
Address
Birth Date, Governorate, and Gender

Project Structure
graphql
Copy code
egyptian-id-recognition/
├── app.py             # Main application
├── utils.py           # Processing logic
├── requirements.txt   # Dependencies
├── README.md          # Documentation
├── YOLO models        # Pretrained YOLO models (to download)
└── d2.jpg             # Processed image output


Contact
GitHub: naso7yy
Email: ahmed.noshy2004@gmail.com
