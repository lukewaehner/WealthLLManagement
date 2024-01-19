import streamlit as st
from transformers import pipeline
import io
import pytesseract
from PIL import Image
from pdf2image import convert_from_path


# Configure the page settings for the Streamlit app
st.set_page_config(page_title="AI Finance Chatbot")

# Set the header of the app
st.header('AI Finance Chatbot')

# Create a file uploader widget for uploading a PDF file
uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")

pdf_text = ""
if uploaded_file is not None:
    # Save the uploaded PDF to a temporary file
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getvalue())

    # Convert PDF pages to images
    pages = convert_from_path("temp.pdf", 500)  # 500 DPI is an example value

    # Initialize an empty string to store extracted text
    pdf_text = ""

    # Create a progress bar
    progress_bar = st.progress(0)
    total_pages = len(pages)

    # Apply OCR to each image and update the progress bar
    for i, page in enumerate(pages):
        pdf_text += pytesseract.image_to_string(page)
        progress_bar.progress((i + 1) / total_pages)

    # Hide the progress bar after processing is complete
    progress_bar.empty()

    # Print the extracted text (for debugging purposes)
    print(pdf_text)

    # Initialize the NLP pipeline for question answering
    nlp = pipeline(
        "question-answering",
        model="deepset/roberta-base-squad2",
        tokenizer="deepset/roberta-base-squad2",
    )
    # for better answers use this model, but I do NOT care to download 30 gigs of data
    # nlp = pipeline("text-generation",
    #                model="AdaptLLM/finance-chat",
    #                tokenizer="AdaptLLM/finance-chat",
    #                )


# Start a session state for storing chat messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about the document! If unreadable, try uploading a different scan of the file"}]


def generate_answer(prompt, pdf_text):
    # Function to generate an answer to a user's question based on the PDF text
    if not pdf_text.strip():
        # If the PDF text is empty, return a message indicating no text was extracted
        return "No text could be extracted from the document, this is likely due to blurred or blocked text, try a different scan."
    context = pdf_text
    question = prompt
    question_set = {"context": context, "question": question}
    # Use the NLP pipeline to find an answer to the question in the context
    # the model is not very good :(
    results = nlp(question_set)
    print("\nAnswer: " + results["answer"])
    return results["answer"]


# input section
if prompt := st.chat_input("Your question"):
    # If a prompt is entered and a file has been uploaded
    if uploaded_file is not None and prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt})  # adds the message
        # Generate a response using the generate_answer function
        response = generate_answer(prompt, pdf_text)
        # Append the assistant's response to the session state messages
        st.session_state.messages.append(
            {"role": "assistant", "content": response})

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

st.markdown("""
<style>
    [data-testid="stDecoration"] {
        background-image: linear-gradient(90deg, #6C63FF, #A9A6FF);
    }
</style>""",
            unsafe_allow_html=True)
