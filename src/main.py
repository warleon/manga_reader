from my_agent import ImageReader
import dotenv
import os

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
    key =os.getenv("OPENAI_API_KEY")
    agent = ImageReader(key)
    text = agent.run("img\\0.png")
    create_file_with_counter("responses",text)

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()