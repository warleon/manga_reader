import base64

def as_base64(image_path)-> str:
    """
    Reads an image file and converts it to a Base64 encoded string.

    :param image_path: Path to the image file.
    :return: Base64 encoded string.
    """
    # Open the image file in binary read mode
    with open(image_path, "rb") as image_file:
        # Read the binary data
        image_data = image_file.read()
        # Encode the binary data to Base64
        base64_encoded = base64.b64encode(image_data).decode("utf-8")
        return base64_encoded