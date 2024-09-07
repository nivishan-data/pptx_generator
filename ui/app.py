import os
import streamlit as st
from app.ai_agent import generate_dynamic_slide_content
from app.pptx_generator import generate_ppt

st.title("AI-Powered Dynamic PowerPoint Generator")

topic = st.text_input("Enter the topic of the presentation:")
num_slides = st.number_input("Enter the number of slides:", min_value=1, max_value=20, value=5)

if st.button("Generate Presentation"):
    if topic and num_slides:
        st.write("Generating presentation...")
        slides = generate_dynamic_slide_content(topic, num_slides)
        pptx_file = generate_ppt(slides)
        with open(pptx_file, "rb") as file:
            st.download_button(
                label="Download PowerPoint Presentation",
                data=file,
                file_name="generated_presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
    else:
        st.error("Please enter both a topic and select the number of slides.")
