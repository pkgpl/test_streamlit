import streamlit as st

def show_message(msg):
    with st.chat_message(msg['role']):
        st.markdown(msg["content"])


# Initialization

client = st.session_state.get('openai_client', None)
if client is None:
    st.markdown("사이드바에 API Key를 입력하세요.")
    st.stop()

st.header("ChatPDF")

# file upload: vector store가 없을 때만 업로드 받기
# (rerun마다 새 vector store를 만들지 않도록 session_state에 저장)

if "vector_store" not in st.session_state:
    pdf_file = st.file_uploader("Upload a pdf file", type=['pdf'], accept_multiple_files=False)
    if pdf_file is None:
        st.markdown("PDF 파일을 업로드하세요.")
        st.stop()

    with st.spinner("Uploading...", show_time=True):
        vector_store = client.vector_stores.create(name="ChatPDF")
        client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=[pdf_file]
        )
    st.session_state.vector_store = vector_store
    st.session_state.pdf_name = pdf_file.name
    st.session_state.chatpdf_messages = []
    st.rerun()   # 업로드 칸을 화면에서 지워, Leave 후에는 빈 업로드 칸이 나오게 함


# Page

def clear_chat():
    st.session_state.chatpdf_messages = []

def leave():
    client.vector_stores.delete(st.session_state.vector_store.id)
    del st.session_state.vector_store
    st.session_state.chatpdf_messages = []

st.markdown(f"파일: `{st.session_state.pdf_name}`")

col1, col2 = st.columns(2)
with col1:
    st.button("Clear (Start a new chat)", on_click=clear_chat)
with col2:
    st.button("Leave (Delete VectorStore)", on_click=leave)

# previous chat
for msg in st.session_state.chatpdf_messages:
    show_message(msg)

# user prompt, assistant response (file_search)
if prompt := st.chat_input("What is up?"):
    msg = {"role":"user", "content":prompt}
    show_message(msg)
    st.session_state.chatpdf_messages.append(msg)

    with st.chat_message("assistant"):
        stream = client.responses.create(
            model = st.session_state["llm_model"],
            instructions = "첨부 파일의 내용을 이용해 대답하세요.",
            input = st.session_state.chatpdf_messages,
            tools = [{
                "type": "file_search",
                "vector_store_ids": [st.session_state.vector_store.id],
            }],
            stream = True,
        )
        response = st.write_stream(stream)
    st.session_state.chatpdf_messages.append({"role":"assistant", "content":response})
