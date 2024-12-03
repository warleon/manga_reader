from easyocr import Reader
import cv2
import numpy as np

reader = Reader(["es","en"],gpu=False)

def flip_image(image_path, quadrilaterals, output_folder):
    """
    Extract quadrilateral-shaped crops from an image, and paste each crop on top of the flipped image in its original orientation.
    Save only the final result.

    :param image_path: Path to the input image.
    :param quadrilaterals: List of quadrilaterals, each defined by four points [(x1, y1), (x2, y2), (x3, y3), (x4, y4)].
    :param output_folder: Folder to save the final image.
    """
    # Load the image
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError("Image could not be loaded. Check the path.")
    
    # Flip the original image horizontally
    flipped_image = cv2.flip(image, 1)

    for i, quad in enumerate(quadrilaterals):
        # Ensure quadrilateral has exactly four points
        if len(quad) != 4:
            raise ValueError(f"Quadrilateral at index {i} does not have 4 points.")

        # Convert points to int32 numpy array for OpenCV
        quad_pts = np.array(quad, dtype=np.int32)

        # Create a mask for the quadrilateral
        mask = np.zeros(image.shape[:2], dtype=np.uint8)  # Single-channel mask
        cv2.fillPoly(mask, [quad_pts], 255)

        # Apply the mask to the image
        masked_image = cv2.bitwise_and(image, image, mask=mask)

        # Extract the bounding rectangle of the quadrilateral
        x, y, w, h = cv2.boundingRect(quad_pts)

        # Crop the bounding rectangle from the masked image
        crop = masked_image[y:y+h, x:x+w]

        nx = image.shape[1] - x

        # Paste the crop back onto the flipped image in the same position
        flipped_image[y:y+h, nx-w:nx] = crop

    # Save the final image with all pasted crops
    output_path = f"{output_folder}/final_result.png"
    cv2.imwrite(output_path, flipped_image)
    print(f"Saved final image with pasted crops to {output_path}")


def preprocess(image_path):
   results =  reader.readtext(image_path)
   quads = [r[0] for r in results]
   flip_image(image_path,quads,".\\preprocess")

preprocess("img\\0.png")