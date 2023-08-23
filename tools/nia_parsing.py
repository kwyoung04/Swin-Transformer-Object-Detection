import json
import os
from tqdm import tqdm

def find_json_files_in_folder(folder_path):
    json_files = []
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            json_files.append(file_name)
    
    return json_files

def validate_coco_format(coco_data):
    required_keys = ["images", "annotations", "categories"]
    for key in required_keys:
        if key not in coco_data:
            return False
    
    return True

def json_ummary(coco_data):
    categories = coco_data['categories']
    class_names = {category['id']: category['name'] for category in categories}

    print("# Calculate the number of images by class")
    class_counts = {category['name']: 0 for category in categories}
    for annotation in coco_data['annotations']:
        class_name = class_names[annotation['category_id']]
        class_counts[class_name] += 1

    print("# Calculate class proportions")
    total_images = len(coco_data['images'])
    class_ratios = {class_name: count / total_images for class_name, count in class_counts.items()}

    print("# Save class ratio ratio to CSV file")
    with open('coco_class_ratios.csv', 'w') as csv_file:
        csv_file.write('Class Name,Class Ratio\n')
        for class_name, ratio in class_ratios.items():
            csv_file.write(f'{class_name},{ratio}\n')

    print("# Save the class name corresponding to the class ID as a CSV file")
    with open('coco_class_id_to_name.csv', 'w') as csv_file:
        csv_file.write('Class ID,Class Name\n')
        for class_id, class_name in class_names.items():
            csv_file.write(f'{class_id},{class_name}\n')
    return 1
    

abs_path = "/home/ubuntu/data/train/fix_test/annotation/"
json_files = find_json_files_in_folder(abs_path)
coco_file_path = "fixed_anno.json"

coco_data = {
    "images": [],
    "annotations": [],
    "categories": [],
    "tmp": []
}

category_id = 1
category_name_to_id = {}

for json_file in tqdm(json_files, desc="Processing", unit="json_file"):
    with open(abs_path+json_file, "r") as f:
        data = json.load(f)
        
        for image_info in data["images"]:
            coco_data["images"].append(image_info)
        
        for category in data["categories"]:
            if category["name"] not in category_name_to_id:
                tmp_category = {category["id"]: category["name"]}
                
                category_name_to_id[category["name"]] = category_id
                category["id"] = category_id
                                
                coco_data["tmp"].append(tmp_category)
                coco_data["categories"].append(category)
                category_id += 1
        
        for annotation in data["annotations"]:
            key_to_find = annotation["category_id"]
            for tmp_category in coco_data["tmp"]:
                if str(key_to_find) == next(iter(tmp_category)):
                    category_name = tmp_category[str(key_to_find)]
                    break
            
            annotation["category_id"] = category_name_to_id[category_name]
            coco_data["annotations"].append(annotation)

with open(coco_file_path, "w") as coco_file:
    json.dump(coco_data, coco_file)
       
with open(coco_file_path, "r") as coco_file:
    coco_data = json.load(coco_file)

if validate_coco_format(coco_data):
    print("### Coco format creation completed")
else:
    print("### Failed to create coco format")
    
if json_ummary(coco_data):
    print("### Coco format clear")

