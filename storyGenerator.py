from openai import OpenAI
from dotenv import load_dotenv
import os 
import json

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

# Model
llm = OpenAI(api_key=openai_api_key)

# Story generation model
def story_gen(prompt):
    response = llm.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant whose mission is to generate stories based on user prompts. These stories will be used to create comic books for readers that will buy the book."},
        {"role": "user", "content": prompt}
    ]
)
    return response.choices[0].message.content.strip()

# Prompt generator :
def prompt_gen(subject, subtheme, language , age_range, setting, tone, character_type, desired_length, specific_region, key_message, art_style):
    return f'''Generate a comic book story about {subject} in Morocco with focus on {subtheme} with the following parameters:

- Language: {language}
- Target audience age range: {age_range}
- Setting: {setting}
- Tone: {tone}
- Main character: {character_type}
- Length: {desired_length}
- Region: {specific_region}
- Key message: {key_message}
- Art style: {art_style}

Story requirements:
1. Before starting the story outline, you should cite all the Characters and give a very detailed description on how do they look.
2. The story should be engaging and appropriate for the specified age range.
3. Include accurate information about the environmental issue and its impact on Morocco.
4. Incorporate local cultural elements and landmarks when possible.
5. Present potential solutions or positive actions related to the environmental issue.
6. Divide the story into clear and very detailed scenes or panels suitable for comic book illustration, when you describe the scenes you should not name the characters, all I care about is how do they look and weither they are the main charcter or which caracter of the side characters (no names).
7. Use dialogue and narration to convey information and move the story forward.
8. End with a call to action or inspirational message for readers.

Please generate a complete story outline with detailed descriptions for each scene or panel, including character actions, dialogue, and important visual elements to be illustrated.'''


def images_desc(story):
    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": '''Act as a meticulous scene breakdown scriptwriter. Craft a JSON file outlining each panel of a story, providing comprehensive and detailed descriptions for each panel essential for generating highly detailed and accurate images, if the panel description provided to you in the prompt is in a language other than English, translate it to English. Ensure each description is rich in visual cues, character interactions, and environmental elements. Don't focus on characters names and on their emotions. Your descriptions must be in the form of prompts that will be fed to an image generation model so you should combine the whole description in one paragraph. The prompts SHOULD NOT be dependant, but in each prompt you should REDESCRIBE the characters again and respect the old descriptions you gave in the other prompts. So for example, if in the first prompt you describe the look of the main charcter, in the second pannel if she's always present you should redescribe it again and not just reference to it, act as if we still don't know them. In each prompt and after you describe the character you should mention if they are the main character or a side character. Here is an example of the JSON output expected from you :
            {
            "story": {
            "prompts" : [
            prompt1_for_panel1, 
            prompt2_for_panel2,
            etc ...
            ]}
            }
            '''},
            {"role": "user", "content": story}
    ]   
)
    return response.choices[0].message.content.strip()


def main():
    print("Welcome to the Story Generator!")

    subject = input("Enter the subject of the story: ")
    subtheme = input("Enter the subtheme of the story: ")
    language = input("Enter the language for the story: ")
    age_range = input("Enter the age range of your target audience: ")
    setting = input('Enter the setting of your story and where should it take place? (e.g., urban, rural, coastal, mountainous): ')
    tone = input('Enter the tone of your story  (e.g., educational, humorous, dramatic, inspirational): ')
    character_type = input('Enter the main charachter type (e.g., child, teenager, adult, animal): ')
    desired_length = input('Enter the desired length of the story (e.g., short story, medium-length, full comic book): ')
    specific_region = input('Enter the desired region in Morocco: ')
    key_message = input('Enter a desired a moral or key message that the story should have: ')
    art_style = input('Enter the preferred art style  (e.g., realistic, cartoonish, manga-inspired): ')
       
    user_prompt = prompt_gen(subject, subtheme, language, age_range, setting, tone, character_type, desired_length, specific_region, key_message, art_style)
    story = story_gen(user_prompt)

    json_descrip = images_desc(story=story)

    print("\nGenerated Story:\n")
    print("\nThe Story\n")
    print(story)

    file_path = 'C:\\Users\\Asus\\story_gen_project\\data.json'

    # Save JSON data to a file
    with open(file_path, 'w') as json_file:
        json.dump(json_descrip, json_file, indent=4)

if __name__ == "__main__":
    main()


