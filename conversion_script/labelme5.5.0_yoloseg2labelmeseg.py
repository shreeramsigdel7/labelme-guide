import json

def unnormalize_points(points, width, height):
    """
    Unnormalizes a list of points based on the given image width and height.

    Args:
        points (list of tuples): A list of normalized (x, y) points.
        width (float): The width of the image.
        height (float): The height of the image.

    Returns:
        list of tuples: A list of unnormalized (x, y) points.
    """
    return [(x * width, y * height) for x, y in points]



def parse_line(line,width,height):
    """
    Parses a line of text and converts it into a JSON-like dictionary format.

    Args:
        line (str): A line of text containing annotation data.
        width (float): The width of the image.
        height (float): The height of the image.

    Returns:
        dict: A dictionary with label and points.
    """
    parts = line.strip().split()
    label_id = int(parts[0])
    points = [(float(parts[i]), float(parts[i+1])) for i in range(1, len(parts), 2)]
    
     # Unnormalize points
    points = unnormalize_points(points, width, height)

    # Define labels based on label_id
    labels = {
        0: "dog",
        1: "eye_R",
        2: "eye_L",
        3: "mouth",
        4: "tongue",
        5: "background"
    }
    
    label = labels.get(label_id, "unknown")
    
    return {
        "label": label,
        "points": points,
        "group_id": None,
        "description": "",
        "shape_type": "polygon",
        "flags": {},
        "mask": None
    }

def create_annotation_json(input_file, output_file, image_name, width, height, version="5.4.1"):
    """
    Creates a JSON object in the specified annotation format from a text file.

    Args:
        input_file (str): Path to the input text file.
        output_file (str): Path to the output JSON file.
        version (str): Version of the annotation format.
    """
    shapes = []
    flags = {}

    # Read and parse the input file
    with open(input_file, 'r') as f:
        for line in f:
            if line.strip():  # Ignore empty lines
                shape = parse_line(line, width, height)
                shapes.append(shape)
    
    # Create JSON object
    annotation_json = {
        "version": version,
        "flags": flags,
        "shapes": shapes,
        "imagePath": image_name,
        "imageData": None,
        "imageHeight": height,
        "imageWidth": width
    }

    # Write JSON to the output file
    with open(output_file, 'w') as f:
        json.dump(annotation_json, f, indent=4)

# Example usage
input_file = '/home/shreeram/workspace/ambl/labelme_build/labelme/examples/classification/data_annotated/0002.txt'

output_file = 'annotations.json'
image_width = 640
image_height = 480
imagePath= "0002.jpg"
imageData= "null"
image_name = imagePath
create_annotation_json(input_file, output_file, image_name, image_width, image_height)

