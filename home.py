## IMPORT START ##
import streamlit as st
import openai
from openai import Client
from config import Config
import os
from kaggle.api.kaggle_api_extended import KaggleApi

# set up kaggle api
os.environ["KAGGLE_USERNAME"] = Config.KAGGLE_USER
os.environ["KAGGLE_KEY"] = Config.KAGGLE_API_KEY
kaggle_api = KaggleApi()
kaggle_api.authenticate()


## IMPORT END ##

# -------------------------------
# 1. Define a class for in-memory ChatGPT management
# -------------------------------
class InMemoryChatGPTManager:
    def __init__(self):
        """
        Initializes the ChatGPTManager with an API key and sets up memory structures in st.session_state.
        """
        self.client = Client(api_key=Config.OPENAI_API_KEY)

        # We'll store conversation histories in st.session_state so that it persists across reruns.
        # conversation_histories: { user_id -> [ { "role": "user"/"assistant", "content": "..."} ] }
        if "conversation_histories" not in st.session_state:
            st.session_state.conversation_histories = {}

        # Optionally, we could store "summaries" or other metadata if needed:
        if "user_summaries" not in st.session_state:
            st.session_state.user_summaries = {}

        # We also define a system_prompt here or pass it in the constructor
        self.system_prompt = (
            "Forget all previous instructions.\n"
            "You are Terra, a climate data assistant. Help data scientists discover and download Kaggle climate datasets.\n\n"
            "Only assist with: data discovery, exploratory analysis, dataset usage, and data science best practices. "
            "Refuse requests outside these topics.\n\n"
            "Ask questions to understand the user's climate data needs.\n"
            "IMPORTANT: Only suggest climate datasets that you are CERTAIN exist on Kaggle."
            "If you're unsure, explain that you can only suggest looking for specific keywords on Kaggle rather than providing specific links.\n\n"
            "For datasets you are confident exist, suggest up to 3 as:\n"
            "DATASET 1: [title] - https://www.kaggle.com/datasets/[username]/[dataset-name]\n"
            "with brief descriptions. When formatting links, always use REAL dataset usernames and dataset-names.\n\n"
            "After suggestions, ask if they want to download any dataset.\n"
            "If they choose to download, end your message with 'DOWNLOAD:[username]/[dataset-name]' using ONLY the username and dataset name parts with NO other text."
        )

        # Maximum conversation messages to keep (excluding the system prompt)
        self.max_history = 20  # e.g., 10 user messages + 10 assistant messages

    def get_history(self, user_id: str):
        """
        Returns the conversation history for a given user.
        """
        return st.session_state.conversation_histories.get(user_id, [])

    def add_message(self, user_id: str, role: str, content: str):
        """
        Adds a message (user or assistant) to a user's conversation history.
        """
        if user_id not in st.session_state.conversation_histories:
            st.session_state.conversation_histories[user_id] = []

        st.session_state.conversation_histories[user_id].append({
            "role": role,
            "content": content
        })

        # Keep only the last N messages to avoid infinite growth
        # (We’ll keep the system prompt separate when we call the API.)
        if len(st.session_state.conversation_histories[user_id]) > self.max_history:
            # Trim from the front
            st.session_state.conversation_histories[user_id] = st.session_state.conversation_histories[user_id][
                                                               -self.max_history:]

    def generate_response(self, user_id: str, user_prompt: str) -> str:
        """
        Generates a response from ChatGPT based on the user's conversation history.
        """
        # 1. Add the user's new message to history
        self.add_message(user_id, "user", user_prompt)

        # 2. Build the conversation for the model:
        #    a) Start with system prompt
        #    b) Then all the (user+assistant) messages from st.session_state
        conversation_history = [
                                   {"role": "system", "content": self.system_prompt}
                               ] + self.get_history(user_id)

        # 3. Call the Chat Completion endpoint
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=conversation_history,
                max_tokens=500,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6
            )
            ai_response = response.choices[0].message.content.strip()
        except Exception as e:
            ai_response = "Sorry, I couldn't process your request."
            print(f"OpenAI API Error: {e}")

        # if DOWNLOAD, download data
        if "DOWNLOAD:" in ai_response:
            # Extract the dataset slug
            download_marker = ai_response.find("DOWNLOAD:")

            dataset_slug = ai_response[download_marker + 9:].split()[0].strip()
            # take out the part of the response just meant for backend download info
            response_index = ai_response.find(dataset_slug) + download_marker + len(dataset_slug)
            ai_response = ai_response[response_index + 1:]

            try:
                # Download the dataset
                os.makedirs("./downloads", exist_ok=True)
                kaggle_api.dataset_download_files(dataset_slug, path="./downloads", unzip=True)
                download_message = f"Successfully downloaded dataset: {dataset_slug} to the downloads folder."
                conversation_history.append({"role": "system", "content": download_message})
                ai_response = ai_response + "\n" + download_message
            except Exception as e:
                error_message = f"Error downloading dataset: {str(e)}"
                conversation_history.append({"role": "system", "content": error_message})
                ai_response = ai_response  + "\n" +  error_message

        # 4. Add the assistant's response to history
        self.add_message(user_id, "assistant", ai_response)

        return ai_response


# -------------------------------
# 2. Create a Streamlit app that uses the InMemoryChatGPTManager
# -------------------------------
def show_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """
            <a href="/" style="color:black;text-decoration: none;">
                <div style="display:table;margin-top:-21rem;margin-left:0%;">
                    <img src="app/static/logo.png" width="40">
                    <span style="color: white">&nbsp;ClimateDataChaty</span>
                    <span style="font-size: 0.8em; color: grey">&nbsp;&nbsp;v0.1.2</span>
                </div>
            </a>
            <br>
            """,
            unsafe_allow_html=True
        )

        reload_button = st.button("↪︎  Reload Page")
        if reload_button:
            st.session_state.clear()
            st.rerun()

# -------------------------------
# Main Streamlit page
# -------------------------------
def main():
    st.set_page_config(
        page_title="ClimateDataChat",
        page_icon="🌏🤖",
        layout="wide"
    )

    show_sidebar()
    st.toast("Welcome to ClimateDataChat!", icon="🌏")

    st.markdown("Welcome to ClimateDataChat, your AI-powered Climate Data Assistant!")
    st.write(
        "ClimateDataChat is designed to assist in finding and utilizing Climate Data sets "
        "for machine learning applications."
    )

    st.header("Climate Data Chat")

    # Initialize the manager (which sets up st.session_state)
    chat_manager = InMemoryChatGPTManager()

    # For demonstration, we'll just use a single user_id
    # If you had multiple users, you'd differentiate them here (e.g. user_id = st.session_state["current_user"])
    user_id = "demo_user"

    # Display any existing conversation
    conversation_so_far = chat_manager.get_history(user_id)
    for msg in conversation_so_far:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input at the bottom
    if prompt := st.chat_input("Ask something about climate data..."):
        # Generate a response from the LLM
        response_text = chat_manager.generate_response(user_id, prompt)

        # Force the app to rerun so messages appear immediately
        st.rerun()


if __name__ == "__main__":
    main()
