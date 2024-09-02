import os
import json

def remove_shapes(json_data, labels_to_remove):
    """
    Remove shapes from JSON data that have labels matching those in the labels_to_remove list.

    Args:
    json_data (dict): The JSON data containing shapes.
    labels_to_remove (list): List of labels to remove from the shapes.

    Returns:
    dict: The modified JSON data with specified shapes removed.
    """
    # Filter out shapes whose labels are in the labels_to_remove list
    filtered_shapes = [
        shape for shape in json_data['shapes'] 
        if shape['label'] not in labels_to_remove
    ]
    
    # Update the JSON data with the filtered shapes
    json_data['shapes'] = filtered_shapes
    return json_data


def load_and_save_json(folder_path, output_folder,labels_to_remove):
    """
        Load JSON files from a specified folder, remove shapes with certain labels, and save the modified JSON data to an output folder.

        Args:
        folder_path (str): Path to the folder containing the JSON files.
        output_folder (str): Path to the folder where the modified JSON files will be saved.
        labels_to_remove (list): List of labels to remove from the shapes in the JSON data.

        Description:
        - The function iterates over all JSON files in the specified input folder.
        - For each JSON file, it loads the content and removes shapes with labels that match any label in the `labels_to_remove` list.
        - The modified JSON data is then saved to the specified output folder, preserving the original filenames.
        - If the output folder does not exist, it is created automatically.
        - The function also handles any potential errors that may occur during JSON decoding.
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            # Construct full file paths
            input_file_path = os.path.join(folder_path, filename)
            output_file_path = os.path.join(output_folder, filename)
            
            # Read the JSON data from the file
            with open(input_file_path, 'r') as json_file:
                try:
                    json_data = json.load(json_file)
                    updated_json_data = remove_shapes(json_data, labels_to_remove)

                    with open(output_file_path, 'w') as output_json_file:
                        json.dump(updated_json_data, output_json_file, indent=4)
                
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {filename}: {e}")

# Example usage
input_folder_path = '../../labelme/examples/instance_segmentation/data_annotated'   # Replace with the path to your input folder
output_folder_path = '../../labelme/examples/instance_segmentation/test_dataannotated' # Replace with the path to your output folder
# Specify labels to remove
labels_to_remove = ["sofa","chair","test", "person"]
load_and_save_json(input_folder_path, output_folder_path,labels_to_remove)
