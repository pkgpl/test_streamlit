import streamlit as st
from openai import OpenAI

# 모든 페이지에서 쓰는 모델 이름
st.session_state["llm_model"] = "gpt-6-luna"
st.session_state["image_model"] = "gpt-image-2.6-flare"

# 진입 파일에 둔 위젯은 모든 페이지에 그려지므로, 페이지를 옮겨도 입력값이 유지된다.
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password")

if api_key:
    st.session_state["openai_client"] = OpenAI(api_key=api_key)

pg = st.navigation([
    st.Page("app_pages/Home.py", title="Home", icon=":material/home:"),
    st.Page("app_pages/Chat.py", title="Chat", icon=":material/chat:"),
    st.Page("app_pages/Chatbot.py", title="도서관 챗봇", icon=":material/local_library:"),
    st.Page("app_pages/ChatPDF.py", title="ChatPDF", icon=":material/picture_as_pdf:"),
])
pg.run()
