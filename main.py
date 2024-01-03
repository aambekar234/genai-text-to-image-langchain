"""
Author: Abhijeet Ambekar
Data: 01/01/2024
Website: https://www.linkedin.com/in/aambekar234/
"""
import json
import os
import openai
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, TransformChain
import prompts


def process_data(input: dict) -> dict:
    """
    Process the input data and generate a final description of scene/plot.

    Args:
        input (dict): The input data containing the raw text.

    Returns:
        dict: A dictionary containing the final description.

    """
    raw_text = input["data"]
    raw_text = raw_text.replace("```json", "")
    raw_text = raw_text.replace("```", "")
    json_data = json.loads(raw_text)
    characters = json_data["characters"]
    time_period = json_data["time-period"]
    geo_location = json_data["geo-location"]
    scene_frame = json_data["scene-picture-frame"]
    ambience = json_data["scene-ambience"]
    script = json_data["original-script"]

    character_descriptions = []
    for char in characters:
        char_desc = f"{char['full-name']} wearing {char['clothing']}, a {char['occupation']} with {char['facial-expression']} and {char['body-language']}. "
        character_descriptions.append(char_desc)

    location_str = f"Locaton:\nTime period in {time_period}, set in {geo_location}."
    characters = "".join(character_descriptions)
    characters_str = f"Main characters:\n{characters}"
    ambience_str = f"Scene ambience:\nScene Setting- {ambience['time-of-day']}, Lighting- {ambience['lighting']}, Environment- {ambience['environment']}, Atmosphere- {ambience['atmosphere']}"
    frame_str = f"Scene Surroundings:\n{scene_frame['description']}, {scene_frame['frame-picture-view']}"
    script_str = f"Main Script:\n{script}"

    final_description = f"{location_str}\n\n{characters_str}\n\n{ambience_str}\n\n{frame_str}\n\n{script_str}"

    return {"result": final_description }


def create_sequential_chain(model, text):
    """
    Creates a sequential chain of language models and transforms to process text.

    Args:
        model (LanguageModel): The language model to be used in the chain.
        text (str): The input text to be processed.

    Returns:
        dictionary: The output of the every step in the chain.
    """
    script_prompt = ChatPromptTemplate.from_template(prompts.script_prompt)
    chain_one = LLMChain(llm=model, prompt=script_prompt, output_key="script")

    # prompt template 1: 
    data_scene_prompt = ChatPromptTemplate.from_template(prompts.data_scene_prompt)
    chain_two = LLMChain(llm=model, prompt=data_scene_prompt, output_key="data")

    transform_chain = TransformChain(
        input_variables=["data"],
        output_variables=["result"],
        transform=process_data
    )

    dalle_prompt = ChatPromptTemplate.from_template(prompts.dalle_prompt)
    chain_four = LLMChain(llm=model, prompt=dalle_prompt, output_key="final_prompt")

    overall_chain = SequentialChain(
        chains=[chain_one, chain_two, transform_chain, chain_four],
        input_variables=["text"],
        output_variables=["script","data","result", "final_prompt"],
        verbose=False)

    return overall_chain(text)
   

def generate_image(prompt):
    """
    Generates an image based on the given prompt.

    Args:
        prompt (str): The prompt for generating the image.

    Returns:
        tuple: A tuple containing the URL of the generated image and the revised prompt used for generation.
    """
    disable_prompt_rewrite = "Do not revise provided prompt delimited by double quotes. DO NOT add any details, just use it AS-IS.:"
    prompt = f"{disable_prompt_rewrite}\n{prompt}"
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",
        quality="hd",
        style="vivid",
        n=1,
        )
    
    return response["data"][0]["url"], response["data"][0]["revised_prompt"]