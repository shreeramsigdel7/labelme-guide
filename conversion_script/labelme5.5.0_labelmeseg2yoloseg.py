import json
import os

def check_and_delete_file(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # If it exists, delete the file
        os.remove(file_path)


def replace_extension_with_txt(file_path):
    # Remove the current extension
    base = os.path.splitext(file_path)[0]
    # Add .txt extension
    new_path = base + '.txt'
    return new_path


def normalize_segmentation_points(points, width, height):
    # This function normalizes segmentation points based on image dimensions
    normalized_points = []
    for point in points:
        normalized_x = point[0] / width
        normalized_y = point[1] / height
        normalized_points.append(f"{normalized_x:.6f} {normalized_y:.6f}")
    return ' '.join(normalized_points)



def convert_json_to_yolov8_segmentation(json_file_path):
    # labelme json file v5.5.0
    # Load JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Initialize a dictionary for labels to class ID mapping
    label_list = {
        'dog':0, 
        'eye_R':1, 
        'eye_L':2, 
        'mouth':3, 
        'tounge':4, 
        'background':5
        }
    if data:
        width = data['imageWidth']
        height = data['imageHeight']
        image_name = data['imagePath']
        yolov8_annotation_path = replace_extension_with_txt(json_file_path)
        print(yolov8_annotation_path)
        # check and delete if file exits
        check_and_delete_file(yolov8_annotation_path)
        # Open output .txt file in append mode, create if it doesn't exist
        with open(yolov8_annotation_path, 'a') as out_file:
            
            # print(f"Width {width} Height {height} Image Name {image_name}")
            for annotation in data['shapes']:
                # Normalize segmentation points
                segmentation_str = normalize_segmentation_points(annotation['points'], width, height)
                yolov8_seg = str(label_list[annotation['label']]) + ' ' + segmentation_str
                # print(yolov8_seg)
                # Write YOLOv8 segmentation to file
                out_file.write(yolov8_seg + '\n')    
    else:
        print("Given Json file is empty.", json_file_path)
    

# Example usage:
json_file_path = '/home/shreeram/workspace/ambl/labelme_build/labelme/examples/classification/data_annotated/0002.json'

convert_json_to_yolov8_segmentation(json_file_path)

# Now, label_mapping can be used for other files as well
