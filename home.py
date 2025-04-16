## IMPORT START ##
import streamlit as st
import asyncio
from openai import OpenAI
from openai import Client
from config import Config
## IMPORT END ##

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def show_sidebar() -> None:
    with st.sidebar:
        st.markdown(f"""
            <a href="/" style="color:black;text-decoration: none;">
                <div style="display:table;margin-top:-21rem;margin-left:0%;">
                    <img src="app/static/logo.png" width="40"><span style="color: white">&nbsp;ClimateDataChaty</span>
                    <span style="font-size: 0.8em; color: grey">&nbsp;&nbsp;v0.1.2</span>
                </div>
            </a>
            <br>
                """, unsafe_allow_html=True)

        reload_button = st.button("↪︎  Reload Page")
        if reload_button:
            st.session_state.clear()
            st.rerun()

st.set_page_config(
    page_title="ClimateDataChat",
    page_icon="🌏🤖",
    layout="wide"
)


def chat_interaction(user_input: str) -> str:
    """
    This function allows the user to interact with our open ai client.
    :param user_input: what the user types and enters into the chat box.
    :return: the client's response.
    """
    response = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=150,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6)
    
    ai_response = response.choices[0].message.content.strip()

    return ai_response


show_sidebar()

st.toast("Welcome to ClimateDataChat!", icon="🌏")

st.markdown("Welcome to ClimateDataChat, your AI-powered Climate Data Assistant!")
st.write("ClimateDataChat is designed to assist in finding and utilizing Climate Data sets for machine learning "
         "applications.")

st.header("Climate Data Chat")

system_prompt = """
            Forget all previous instructions.
        You are a chatbot named Terra. You are assisting a data scientist in 
        discovering climate data sets and creating exploratory data analysis
        for the chosen set.
        Each time the user converses with you, make sure the context is about
        * data set discovery,
        * or exploratory data analysis,
        * or data set usage,
        * or data science best practices,
        and that you are providing a helpful response.

        If the user asks you to do something that is not
        concerning one of those topics, you should refuse to respond.
        """

# Ensure the session state is initialized
if "messages" not in st.session_state:
    st.session_state.messages = [
         {"role": "system", "content": system_prompt}
    ]

# Print all messages in the session state
for message in [m for m in st.session_state.messages if m["role"] != "system"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to the user prompt
if prompt := st.chat_input("Ask a software development or coding question..."):
    #Adds user query to the session state messages
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate and store the model's response
    response = chat_interaction(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})

    #reruns the app for messages to show up
    st.rerun()



