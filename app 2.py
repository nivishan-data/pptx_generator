import os
import streamlit as st
from app.ai_agent import plan_presentation, generate_slide_content, generate_image_prompts, generate_images
from app.pptx_generator import generate_ppt

st.title("AI-Powered Dynamic PowerPoint Generator with Images")

topic = st.text_input("Enter the topic of the presentation:")
num_slides = st.number_input("Enter the number of slides:", min_value=1, max_value=20, value=5)

if st.button("Generate Presentation"):
    if topic and num_slides:
        st.write("Planning presentation...")
        slide_plan = plan_presentation(topic, num_slides)
        
        st.write("Generating slide content...")
        slides_content = generate_slide_content(slide_plan)
        
        st.write("Generating image prompts...")
        image_prompts = generate_image_prompts(slide_plan)
        
        st.write("Generating images...")
        images = generate_images(image_prompts)
        
        st.write("Compiling PowerPoint presentation...")
        pptx_file = generate_ppt(slides_content, images)
        
        with open(pptx_file, "rb") as file:
            st.download_button(
                label="Download PowerPoint Presentation",
                data=file,
                file_name="generated_presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
    else:
        st.error("Please enter both a topic and select the number of slides.")
