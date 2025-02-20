from my_agent import ImageReader
import dotenv
import os
import json
from gen_voice import gen_voice

def create_file_with_counter(directory, content, extension="txt"):
    """
    Creates a new file in the specified directory. The file name is based on the number of existing files.
    
    :param directory: Directory where the file will be created.
    :param content: Content to write to the new file.
    :param extension: File extension for the new file (default is "txt").
    """
    try:
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # List all files in the directory
        existing_files = os.listdir(directory)

        # Filter only files with the specified extension
        counter = len(existing_files) + 1

        # Construct the new file name
        new_file_name = f"{counter}.{extension}"
        new_file_path = os.path.join(directory, new_file_name)

        # Create and write to the file
        with open(new_file_path, "w") as file:
            file.write(content)

        print(f"File '{new_file_name}' successfully created in '{directory}'")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    #key =os.getenv("OPENAI_API_KEY")
    #agent = ImageReader(key)
    #text = agent.run("img\\preprocess_0.png")
    #create_file_with_counter("responses",text)
    # render final audio
    conversation=None
    mappings= {
        "narrator":"target_voices\\male_warleon.wav",
        "kawai":"target_voices\\female_yulisa.wav",
        "tadano":"target_voices\\male_noe.wav"
    }
    with open("responses\\komisan.json","r") as file:
        conversation = json.load(file)

    for text,i in zip(conversation,range(len(conversation))):
        print(i,text)
        if text["type"].lower() == "sound effect":
            continue
        gen_voice(text["content"],mappings[text["character"].lower()],f"result\\{i}.wav")



    

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()