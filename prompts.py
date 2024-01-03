"""
Author: Abhijeet Ambekar
Data: 01/01/2024
Website: https://www.linkedin.com/in/aambekar234/
Description:
This file contains various prompts used for text analysis and script generation. It includes a data format description, a script prompt, a data scene prompt, and a dalle prompt.
"""

dataFormat = """
The JSON Object has keys 'characters', 'time-period', 'geo-location', 'scene-picture-frame', 'scene-ambience', 'original-script' \ 
Each character in characters array should have five sub keys with single values such as 'full-name', 'clothing', 'age-range', 'occupation', 'facical-expression', 'body-language'. \
Scene-ambience should have four sub keys 'time-of-day', 'lighting', 'environment', 'atmosphere'.\
Scene-picture-frame should two sub keys 'desciption', 'frame-picture-view' .\
time-period should be a single string value.\
geo-location should be a single string vaule focused on name of the city followed name of Kingdom/Empire/Country.\
original-script is the detailed & immersive summarization of the provided script. This field should be a single string value. \
You must not neglect any crucial information from the original script.
"""

script_prompt = """
You are a script writer tasked with creating immersive and engaging script from a text. Your job is to analyze the text, \
first cleaning it for any odd special characters or formatting issues. Then, expand the text as a immersive movie script \
with detailed historical and cultural context, character interactions, environmental setting, and emotional undertones. \
Your expansion should be rich in detail, offering inspiration for a movie director or an artist to finalize the scene's frames. \
Focus on vivid descriptions that bring the era, cultural nuances, atmosphere, and characters' historic costume, occupation, emotional states to life:\
\n\n{text}
"""

data_scene_prompt = """You are a genius at movie script picturization, movie plot direction and ambience art depiction. \
Analyze the following movie script to identify or estimate the main characters, their either full name or full name with title \
example Jesus Christ of Nazareth, estimate the time period or era in which the scene is set, \
estimate the occupation of each character in the scene and their facial expressions and body language according to the plot. \
For character information focus on their full name, age, interactions, facial expressions, clothings, \
setting descriptions, environment, \
For scene ambience focus on the environment, time era, geolocatio, time of the day, lighting effect relvant to the scene etc. \
For scene picture frame focus on surrounding objects, infrastructure, relevant vegetations etc. \
Format your response as a JSON object as below: \
\n\n""" + dataFormat +"""

Analyze below script scene:
\n\n{script}
"""

dalle_prompt = """
You are an expert prompt writer for dall.e-3 diffusion model. Your job is to analyze below detailed information of a movie scene and characters in it to generate an image. \
You must analyze the characters, their age group, locations, best lighting, costumes to visualize the picture. You must consider the best camera angles for the picture. \
Your generated prompt must first focus on the character details and their interaction with each other then the surrondings and other scene related information. \
While creating the prompt you should consider following.\
1. Clarity and Specificity of the scene, time era with ruling Kingdom/Country etc \
2. Brevity of the intereaction between characters of the story \
3. Balance of information about surroundings and chracters \
4. Character distinct description with respect to the essense of the scene and story \
5. Avoiding overload of information \

While generating the prompt you must analyze the main characters in the scene and generate the prompt for the maximum immersion, story telling and emotions. \
Before providing the output you must checklist below requirements. \
1. The main characters should be highlighted with estimated age group distinctintly and correctly \
2. The background, ambience, historic context, time-period era with gekolocation is correctly incorported in the prompt with necessary details \
3. The prompt length is ideal for the dall.e-3 model for best results \
4. Refine the prompt again for the best output \

Your response should contain only the generated text as a string. \

analyze below information: \
\n\n{result}
"""
