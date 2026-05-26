import streamlit as st

def show_message(msg):
    with st.chat_message(msg['role']):
        st.markdown(msg["content"])


# Initialization

client = st.session_state.get('openai_client', None)
if client is None:
    if st.button("API Key를 입력하세요."):
        st.switch_page("streamlit_app.py")
    st.stop()

# file upload

pdf_file = st.file_uploader("Upload a pdf file", type=['pdf'], accept_multiple_files=False)
if pdf_file is not None:
    vector_store = client.vector_stores.create(name="ChatPDF")
    file_batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=[pdf_file]
    )
    st.session_state.vector_store = vector_store

if 'vector_store' not in st.session_state:
    st.markdown("PDF 파일을 업로드하세요.")
    st.stop()


if "chatpdf_messages" not in st.session_state:
    st.session_state.chatpdf_messages = []


client = st.session_state.get('openai_client', None)
if client is None:
    if st.button("API Key를 입력하세요."):
        st.switch_page("streamlit_app.py")
    st.stop()

if "chatpdf_messages" not in st.session_state:
    st.session_state.chatbot_messages = [
        {"role":"system","content":f"""
첨부 파일의 내용을 이용해 대답하세요.
"""}
    ]


# Page

st.header("ChatPDF")

col1, col2 = st.columns(2)
with col1:
    if st.button("Clear (Start a new chat)"):
        st.session_state.chatpdf_messages = []
with col2:
    if st.button("Leave (Delete VectorStore)"):
        st.session_state.chatpdf_messages = []
        client.vector_stores.delete(st.session_state.vector_store.id)
        del st.session_state.vector_store

# previous chat
for msg in st.session_state.chatpdf_messages:
    show_message(msg)

# user prompt, assistant response
if prompt := st.chat_input("What is up?"):
    msg = {"role":"user", "content":prompt}
    show_message(msg)
    st.session_state.chatpdf_messages.append(msg)

    response = client.chat.completions.create(
        model = "gpt-5.4-mini",
        messages = st.session_state.chatpdf_messages
    )
    msg = {"role":"assistant", "content":response.choices[0].message.content}
    show_message(msg)
    st.session_state.chatpdf_messages.append(msg)