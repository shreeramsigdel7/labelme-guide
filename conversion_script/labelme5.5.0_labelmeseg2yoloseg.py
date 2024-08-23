import json
import os


def labels_to_dict(file_path):
    """
    Converts a text file with label names in each line into a dictionary 
    where keys are indices starting from 0 and values are label names.
    
    Args:
        file_path (str): The path to the text file containing label names.
    
    Returns:
        dict: A dictionary with indices as keys and label names as values.
        example eg_dict = {
            0 : 'cat'
        }
    """
    labels_dict = {}
    
    # Read the text file and populate the dictionary
    with open(file_path, 'r') as file:
        for index, label in enumerate(file):
            # labels_dict[index] = label.strip()  # strip removes extra spaces at the start and end
            labels_dict[label.strip()] = index  # strip removes extra spaces at the start and end
    print(labels_dict)
    return labels_dict


def check_and_delete_file(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # If it exists, delete the file
        os.remove(file_path)


def replace_extension_with_txt(file_path):
    # Remove the current extension
    basename = os.path.splitext(os.path.basename(file_path))[0]
    # Add .txt extension
    new_path = basename + '.txt'
    return new_path


def normalize_segmentation_points(points, width, height):
    # This function normalizes segmentation points based on image dimensions
    normalized_points = []
    for point in points:
        normalized_x = point[0] / width
        normalized_y = point[1] / height
        normalized_points.append(f"{normalized_x:.6f} {normalized_y:.6f}")
    return ' '.join(normalized_points)



def convert_json_to_yolov8_segmentation(json_file_path,labels,output_dir):
    # labelme json file v5.5.0
    # Load JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    if data:
        width = data['imageWidth']
        height = data['imageHeight']
        # image_name = data['imagePath']
        base_name = replace_extension_with_txt(json_file_path)
        yolov8_annotation_path = os.path.join(output_dir,base_name)
        # check and delete if file exits
        check_and_delete_file(yolov8_annotation_path)
        # Open output .txt file in append mode, create if it doesn't exist
        with open(yolov8_annotation_path, 'a') as out_file:
            for annotation in data['shapes']:
                # Normalize segmentation points
                segmentation_str = normalize_segmentation_points(annotation['points'], width, height)
                yolov8_seg = str(labels[annotation['label']]) + ' ' + segmentation_str
                out_file.write(yolov8_seg + '\n')    
    else:
        print("Given Json file is empty.", json_file_path)
    
if __name__ == "__main__":
    classes_file_path = "/home/shreeram/workspace/ambl/labelme_build/labelme/conversion_script/classes.txt"
    classes_name = labels_to_dict(classes_file_path)
    yolo_annotation_output_dir = "output_yolo_seg_annotation"
    if not os.path.exists(yolo_annotation_output_dir):
        os.makedirs(yolo_annotation_output_dir)

    json_file_dir = "/home/shreeram/workspace/ambl/labelme_build/labelme/conversion_script/output_json_annotation"
    for json_filename in os.listdir(json_file_dir):

        json_file_path = os.path.join(json_file_dir,json_filename)
        
        convert_json_to_yolov8_segmentation(
            json_file_path=json_file_path,
            labels=classes_name,
            output_dir = yolo_annotation_output_dir)

