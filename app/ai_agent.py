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
    You are an expert presentation planner. Create a plan for a PowerPoint presentation on the topic "{topic}" with {num_slides} slides. 
    Provide a brief title and a one-line description of what should be covered on each slide.
    """
)

content_template = PromptTemplate(
    input_variables=["slide_title", "slide_description"],
    template="""
    You are an expert content creator. Generate detailed content for a PowerPoint slide titled "{slide_title}".
    Slide description: {slide_description}
    Include headers, bullet points, and bold text for emphasis where necessary. And make sure to create the content which are 
    summarized and fit to a power point slide. only 75 to 100 characters per slide.
    """
)

image_prompt_template = PromptTemplate(
    input_variables=["slide_title", "slide_description"],
    template="""
    You are an AI model that generates images for presentations. Generate a concise prompt for an AI image generator to create an image for a slide titled "{slide_title}".
    Slide description: {slide_description}
    Keep the prompt under 1000 characters. The image should be very simple.
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
    # Generate image prompts for each slide, ensuring they are concise
    image_prompts = []
    for slide in slide_plan:
        prompt = image_prompt_chain.run({
            "slide_title": slide['title'],
            "slide_description": slide['description']
        })
        if len(prompt) > 1000:
            prompt = shorten_prompt(prompt)
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

def shorten_prompt(prompt):
    # Function to shorten the prompt to be within 1000 characters
    return prompt[:1000]
