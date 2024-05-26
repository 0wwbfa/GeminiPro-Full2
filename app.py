import os
import streamlit as st
from streamlit_local_storage import LocalStorage
# Configure Streamlit page settings
st.set_page_config(
    page_title="Gemini-Pro Chatbot Full",
    page_icon=":alien:",  # Favicon emoji
    layout="wide",  # Page layout option
    menu_items={}
)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]

from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

localS = LocalStorage() 

# Get the Google API key from the local storage
GOOGLE_API_KEY = localS.getItem('gak')

# If the Google API key is not present in the local storage, open the sidebar to input it
if (GOOGLE_API_KEY==None):
    # Sidebar to input Google API Key
    with st.sidebar:
        st.sidebar.title("Gemini-Pro Configuration")
        GOOGLE_API_KEY = st.sidebar.text_input("Enter your Google API Key", type="password")

    # Close the sidebar when the Google API key is entered
    if GOOGLE_API_KEY:
        st.session_state.sidebar_state = 'collapsed'

# Check if API key is provided
if not GOOGLE_API_KEY:
    st.error("Please enter your Google API Key.")
    st.stop()

st.markdown('''
<style>
.stApp [data-testid="stToolbar"]{
    display:none;
}
</style>
''', unsafe_allow_html=True)

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel(
  model_name="gemini-1.5-pro",
  safety_settings=safety_settings,
  generation_config=generation_config,
)

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

st.markdown(
    """
    <script>
        document.querySelector("#root > div:nth-child(1) > div > div > button").style.display="none"
    </script>
    """,
    unsafe_allow_html=True,
)

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

localS.setItem('gak', GOOGLE_API_KEY)

# Display the chatbot's title on the page
# st.title("🤖 Gemini Pro - ChatBot")

# Add small text below the header
# st.markdown("Made by 😎 [Hardik](https://www.linkedin.com/in/hardikjp/)")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask ✨Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
