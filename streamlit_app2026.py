import streamlit as st
import base64
from openai import OpenAI

st.session_state["llm_model"] = "gpt-5.4-mini"
st.session_state["image_model"] = "gpt-image-1-mini"
st.session_state["home_page"] = "streamlit_app2026.py"

def get_llm_response(prompt):
    response = client.responses.create(
        model=st.session_state["llm_model"],
        input=prompt
    )
    return response.output_text

def generate_image(image_prompt):
    img = client.images.generate(model=st.session_state["image_model"], prompt=image_prompt)
    image_bytes = base64.b64decode(img.data[0].b64_json)
    return image_bytes

st.title("OpenAI GPT model")

api_key= st.text_input("OpenAI API Key", type="password")
if api_key:
    client = OpenAI(api_key=api_key)
    st.session_state["openai_client"] = client
else:
    st.markdown("API KEY를 입력하세요.")

prompt = st.text_area("User prompt")

if st.button("Ask!", disabled=(len(prompt)==0)):
    st.write(get_llm_response(prompt))


image_prompt = st.text_area("Image prompt")

if st.button("Generate!", disabled=(len(image_prompt)==0)):
    st.image(generate_image(image_prompt))
