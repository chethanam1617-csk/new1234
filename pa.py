import streamlit as st
import wikipedia
from gtts import gTTS
import base64
import tempfile

# Title
st.title("🤖 Personal Assistant")

# Session state for conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to convert text to speech and return audio HTML
def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)
            audio_bytes = open(tmp_file.name, "rb").read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
            <audio autoplay controls>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """
        return audio_html
    except Exception as e:
        return f"⚠️ Error in speech synthesis: {e}"

# Define your assistant's logic
def assistant_response(user_input):
    user_input = user_input.lower()
    
    # Basic rule-based responses
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"
    elif "your name" in user_input:
        return "I'm your personal assistant!"
    elif "bye" in user_input:
        return "Goodbye! Have a great day."
    else:
        # Try Wikipedia if no rule-based response
        try:
            summary = wikipedia.summary(user_input, sentences=2)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            return f"That query is too broad. Did you mean: {', '.join(e.options[:5])}?"
        except wikipedia.exceptions.PageError:
            return "Sorry, I couldn't find anything on that."
        except Exception as e:
            return f"An error occurred: {e}"

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Assistant response
    response = assistant_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display conversation with voice
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":  # Only assistant messages get voice output
            audio_html = text_to_speech(msg["content"])
            st.markdown(audio_html, unsafe_allow_html=True)


