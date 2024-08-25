import json
from shapely.geometry import Polygon
from shapely.ops import unary_union
import os 
import cv2



def labels_to_dict(file_path):
    """
    Converts a text file with label names in each line into a dictionary 
    where keys are indices starting from 0 and values are label names.
    
    Args:
        file_path (str): The path to the text file containing label names.
    
    Returns:
        dict: A dictionary with indices as keys and label names as values.
    """
    labels_dict = {}
    
    # Read the text file and populate the dictionary
    with open(file_path, 'r') as file:
        for index, label in enumerate(file):
            labels_dict[index] = label.strip()  # strip removes extra spaces at the start and end
    
    return labels_dict



def replace_extension_with_json(file_path):
    # Remove the current extension
    base = os.path.splitext(file_path)[0]
    # Add .txt extension
    new_path = base + '.json'
    return new_path


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

def simplify_polygon(polygon_coords, tolerance=5):
    """
    Simplifies a polygon based on the tolerance value.
    
    Parameters:
        polygon_coords (list of tuples): List of (x, y) coordinates defining the polygon.
        tolerance (float): The tolerance level for simplification.
        default 0.1
        small tolerance 1 or 2 pixels
        moderate tolerance 3 to 5 pixels
        large tolerance 6 or more

    
    Returns:
        list: A dictionary containing the simplified polygon's coordinates.
    """
    # Create a Polygon object
    polygon = Polygon(polygon_coords)
    
    # Simplify the polygon
    simplified_polygon = polygon.simplify(tolerance, preserve_topology=True)
    
    # Extract the simplified coordinates
    simplified_coords = list(simplified_polygon.exterior.coords)
    return simplified_coords

def parse_line(line,width,height, labels):
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
    # print("Count Before Simplyfy:",len(points))
    points = simplify_polygon(points)
    # print("Count After Simplyfy:",len(points))
    
    # labels = labels_to_dict(classes_file_path)


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

def create_annotation_json(input_file, output_file, labels, image_name, width, height, version="5.4.1"):
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
                shape = parse_line(
                    line=line, 
                    width=width, 
                    height= height, 
                    labels=labels)
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



def get_image_dimensions_cv2(image_path):
    """
    Get the height and width of an image using OpenCV.

    Args:
        image_path (str): The path to the image file.

    Returns:
        tuple: The width and height of the image.
    """
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    return width, height


if __name__ == "__main__":
    # classes_file_path: text file with class names in each line
    classes_file_path = "/home/shreeram/workspace/ambl/labelme_build/labelme/conversion_script/classes.txt"
    imageData= "null"
    # input_labels_dir = "/home/shreeram/workspace/ambl/autodistillation_roboflow/test_labelme/labels"
    input_labels_dir = "/home/shreeram/workspace/ambl/labelme_build/labelme/conversion_script/output_yolo_seg_annotation"
    input_images_dir = "/home/shreeram/workspace/ambl/autodistillation_roboflow/test_labelme/images"
    output_dir = "output_json_annotation"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List of images and annotation files
    image_lists = sorted(os.listdir(input_images_dir))
    annotation_file_lists = sorted(os.listdir(input_labels_dir))

    classes_name = labels_to_dict(classes_file_path)


    for imgfile_name, anno_filename in zip(image_lists, annotation_file_lists):
        if  (os.path.splitext(imgfile_name)[0]) == (os.path.splitext(anno_filename)[0]):
            each_filepath = os.path.join(input_labels_dir,imgfile_name)
            output_file = replace_extension_with_json(os.path.join(output_dir,imgfile_name))
            
            
            image_width, image_height = get_image_dimensions_cv2(os.path.join(input_images_dir,imgfile_name))

        create_annotation_json(
            input_file=os.path.join(input_labels_dir, anno_filename), 
            output_file=output_file, 
            labels=classes_name,
            image_name=imgfile_name, 
            width=image_width, 
            height=image_height
        )

