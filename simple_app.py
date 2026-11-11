import streamlit as st
import base64
from openai import OpenAI

st.write("Hello World")

st.divider()

api_key = st.text_input("API Key", type="password")
if not api_key:
    st.stop()

client = OpenAI(api_key=api_key)

tab1, tab2 = st.tabs(["LLM","Image Generation"])

with tab1:
    prompt = st.text_area("Prompt")

    if st.button("Answer"):

        with st.spinner("Thinking...", show_time=True):
            response = client.responses.create(
                model='gpt-6-luna',
                input=prompt
            )
            st.write(response.output_text)

with tab2:
    image_prompt = st.text_area("Image Generation Prompt")

    if st.button("Generate"):

        with st.spinner("Generating...", show_time=True):
            img = client.images.generate(
                model='gpt-image-2.6-flare',
                prompt=image_prompt
            )
            image_bytes = base64.b64decode(img.data[0].b64_json)

            st.image(image_bytes)

