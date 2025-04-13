## IMPORT START ##
import streamlit as st
import asyncio
## IMPORT END ##

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
    initial_messages = [{"role": "system",
                         "content": system_prompt}]
    st.session_state.messages = initial_messages

# Print all messages in the session state
for message in [m for m in st.session_state.messages if m["role"] != "system"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to the user prompt
if prompt := st.chat_input("Ask a software development or coding question..."):
        print(prompt)
        # TODO: Run chat function with LLM -> Make sure to append output to st.session_state.messages
        # asyncio.run(util.chat(st.session_state.messages, prompt))
        # st.rerun()

