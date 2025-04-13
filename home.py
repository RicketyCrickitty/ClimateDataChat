import streamlit as st

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
