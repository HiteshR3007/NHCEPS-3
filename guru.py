import streamlit as st
from PIL import Image
import pytesseract
import openai
import json

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# OCR function
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# GPT function to extract structured data
def extract_bill_data(text):
    prompt = f"""
    Extract the following from this bill text:
    - Vendor Name
    - Bill Date
    - Bill Number
    - Total Amount

    Format it in JSON like:
    {{
        "vendor": "...",
        "date": "...",
        "bill_number": "...",
        "amount": "..."
    }}

    Bill Text:
    {text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response['choices'][0]['message']['content']

# Display app
st.title("Gen AI Bill Reader")
st.write("Upload a bill image and watch the magic!")

uploaded_file = st.file_uploader("Upload Bill Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Bill", use_column_width=True)

    with st.spinner("Reading text with OCR..."):
        ocr_text = extract_text_from_image(image)
        st.subheader("OCR Text:")
        st.text_area("Extracted Text", ocr_text, height=200)

    with st.spinner("Extracting bill info using GPT..."):
        extracted_json = extract_bill_data(ocr_text)

        try:
            data = json.loads(extracted_json)
            st.subheader("Structured Data:")
            st.json(data)

            st.subheader("Filled Template:")
            st.markdown(f"""
            *Vendor:* {data['vendor']}  
            *Date:* {data['date']}  
            *Bill Number:* {data['bill_number']}  
            *Amount:* {data['amount']}  
            """)
        except:
            st.error("Couldn't parse the response. Check if the OCR text is clear or adjust the prompt.")