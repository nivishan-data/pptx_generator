from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import openai
import requests
from PIL import Image
import io

# Set up your LLMs
llm = OpenAI(temperature=0.7)

# Define the prompt templates
planning_template = PromptTemplate(
    input_variables=["topic", "num_slides"],
    template="""
    You are an expert presentation planner. Create a plan for a PowerPoint presentation on the topic "{topic}" with exactly {num_slides} slides. 
    Provide a distinct title and a one-line description for each slide. 
    Do NOT use words like "Slide", "Title", or "Header". Only provide the descriptive title related to the content.
    The content should be concise, clear, and fit within one slide.
    """
)

content_template = PromptTemplate(
    input_variables=["slide_title", "slide_description"],
    template="""
    You are an expert content creator. Generate concise content for a PowerPoint slide titled "{slide_title}".
    Slide description: {slide_description}
    The content should be summarized, up to 100 characters, and fit within one PowerPoint slide.
    Do NOT include "Slide", "Title", or "Header" in the content. Focus on clear points or short paragraphs only.
    """
)

image_prompt_template = PromptTemplate(
    input_variables=["slide_title", "slide_description"],
    template="""
    You are an AI model that generates images for presentations. Create a concise image prompt for a slide titled "{slide_title}".
    The description is: {slide_description}. Keep the prompt simple and relevant to the slide content. Avoid using text or words in the image.
    The prompt should be short and easy to generate, under 1000 characters.
    """
)

# Create chains using LangChain
planning_chain = LLMChain(llm=llm, prompt=planning_template)
content_chain = LLMChain(llm=llm, prompt=content_template)
image_prompt_chain = LLMChain(llm=llm, prompt=image_prompt_template)

def plan_presentation(topic, num_slides):
    # Generate the plan for the slides
    response = planning_chain.run({"topic": topic, "num_slides": num_slides})
    return parse_plan_response(response)

def generate_slide_content(slide_plan):
    # Generate content for each slide
    slides_content = []
    for slide in slide_plan:
        content = content_chain.run({
            "slide_title": slide['title'],
            "slide_description": slide['description']
        })
        slides_content.append({"title": slide['title'], "content": content})
    return slides_content

def generate_image_prompts(slide_plan):
    # Generate image prompts for each slide
    image_prompts = []
    for slide in slide_plan:
        prompt = image_prompt_chain.run({
            "slide_title": slide['title'],
            "slide_description": slide['description']
        })
        image_prompts.append(prompt)
    return image_prompts

def generate_images(image_prompts):
    images = []
    for prompt in image_prompts:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
            response_format="url"
        )
        image_url = response['data'][0]['url']
        image = download_image(image_url)
        images.append(image)
    return images

def download_image(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    return img

def parse_plan_response(response):
    slides = []
    for line in response.split('\n'):
        if line.strip():
            parts = line.split(":")
            if len(parts) == 2:
                title, description = parts
                slides.append({"title": title.strip(), "description": description.strip()})
    return slides
