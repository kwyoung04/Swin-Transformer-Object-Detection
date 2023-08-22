import json
import os
from tqdm import tqdm

#fixed_list = ['person', 'bicycle', 'car', 'sign', 'trash bin', 'bench', 'roof', 'bird', 'cat', 'dog', 'chicken', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'muffler', 'hat', 'ball', 'shuttlecock', 'hulahoop', 'gripper', 'drone', 'pilates equipment', 'treadmill', 'dumbbell', 'golf club', 'billiards cue', 'skating shoes', 'tennis racket', 'badminton racket', 'goalpost', 'basketball hoop', 'carabiner', 'table tennis racket', 'rice cooker', 'gas stove', 'pot', 'pan', 'microwave', 'toaster', 'knives', 'chopping boards', 'ladle', 'silicon spatula', 'rice spatula', 'vegetable peeler', 'box grater', 'scissors', 'bowl', 'cutlery', 'plate', 'side dish', 'tray', 'mug', 'refrigerator', 'whisk', 'tongs', 'espresso machine', 'purifier', 'banana', 'apple', 'grape', 'pear', 'melon', 'cucumber', 'watermelon', 'orange', 'jujube', 'peach', 'chestnut', 'persimmon', 'lettuce', 'cabbage', 'radish', 'perilla leaf', 'garlic', 'onion', 'spring onion', 'carrot', 'corn', 'potato', 'sweet potato', 'egg plant', 'tomato', 'pumpkin', 'squash', 'chili', 'pimento', 'sandwich', 'hamburger', 'hotdog', 'pizza', 'donut', 'cake', 'white bread', 'ice cream', 'ttoke', 'tteokbokki', 'kimchi', 'gimbap', 'sushi', 'mandu', 'gonggibap', 'couch', 'mirror', 'window', 'table', 'lamp', 'door', 'chair', 'bed', 'toilet bowl', 'washstand', 'book', 'clock', 'doll', 'hair dryer', 'toothbrush', 'hair brush', 'TV', 'laptop', 'mouse', 'keyboard', 'cell phone', 'watch', 'smartwatch', 'camera', 'speaker', 'fan', 'air conditioner', 'piano', 'tambourine', 'castanets', 'guitar', 'violin', 'flute', 'recorder', 'xylophone', 'ocarina', 'thermometer', 'sphygmomanometer', 'blood glucose meter', 'defibrillator', 'massage gun', 'ceiling', 'floor', 'wall', 'road', 'building']

category_list = [
    'table tennis racket', 'bench', 'toilet bowl', 'toothbrush',
    'keyboard', 'trash bin', 'recorder', 'violin',
    'silicon spatula', 'watermelon', 'scissors', 'handbag', 'tv',
    'cutlery', 'pan', 'cake', 'gripper', 'garlic', 'couch',
    'defibrillator', 'knives', 'squash', 'blood glucose meter',
    'person', 'watch', 'book', 'egg plant', 'toaster', 'camera',
    'cucumber', 'umbrella', 'donut', 'basketball hoop', 'truck',
    'washstand', 'potato', 'drone', 'guitar', 'radish', 'chair',
    'golf club', 'goalpost', 'lettuce', 'hair brush',
    'spring onion', 'rice spatula', 'microwave', 'speaker',
    'doll', 'bowl', 'backpack', 'gas stove', 'fan', 'ball',
    'tambourine', 'door', 'Billiards cue', 'table',
    'ocarina', 'treadmill', 'skating shoes', 'cabbage',
    'xylophone', 'chicken', 'pizza', 'car', 'orange', 'sign',
    'mirror', 'pear', 'scooter', 'mouse', 'plate', 'icecream',
    'bus', 'muffler', 'pimento', 'Castanets', 'tray', 'banana',
    'hotdog', 'badminton racket', 'cat', 'whisk', 'laptop',
    'plum', 'tongs', 'dumbbell', 'carabiner', 'sushi',
    'shuttlecock', 'rice cooker', 'roof', 'perilla leaf', 'tomato',
    'peach', 'window', 'gimbap', 'tie', 'motorcycle', 'dog',
    'bicycle', 'grape', 'purifier', 'lamp', 'apple', 'mug',
    'ladle', 'carrot', 'melon', 'board', 'chopping boards', 'pot',
    'bed', 'hat', 'vegetable peeler', 'cell phone', 'bird',
    'tteokbokki', 'pumpkin', 'sphygmomanometer', 'persimmon',
    'kimchi', 'massage gun', 'tennis racket', 'piano',
    'refrigerator', 'clock', 'chili', 'side dish', 'strawberry',
    'flute', 'corn', 'tree', 'building', 'chestnut',
    'box grater', 'onion', 'hair drier', 'hamburger', 'ttoke',
    'thermometer', 'white bread', 'Tambourine', 'air conditioner',
    'hulahoop', 'sandwich', 'pilates equipment', 'gonggibap',
    'espresso machine', 'ceiling', 'floor', 'wall', 'billiards cue',
    'smartwatch', 'road', 'castanets', 'jujube', 'sweet potato',
    'mandu', 'suitcase'
]



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
    

abs_path = "/home/ubuntu/data/train/fix_test/sample/"
json_files = find_json_files_in_folder(abs_path)
coco_file_path = "fixed_sample.json"

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
                
                category_name_to_id[category["name"]] = category_list.index(category["name"])
                category["id"] = category_list.index(category["name"])
                                
                coco_data["tmp"].append(tmp_category)
                coco_data["categories"].append(category)
        
        for annotation in data["annotations"]:
            key_to_find = annotation["category_id"]
            for tmp_category in coco_data["tmp"]:
                if str(key_to_find) == next(iter(tmp_category)):
                    category_name = tmp_category[str(key_to_find)]
                    break
            
            annotation["category_id"] = category_name_to_id[category_name]
            coco_data["annotations"].append(annotation)

#diff_class = len(category_list) - len(coco_data['categories'])
#for i in range(diff_class):
#    coco_data['categories'].append({'supercategory': "tmp", 'id': len(category_list)+i+1, 'name': "tmp"})



with open(coco_file_path, "w") as coco_file:
    json.dump(coco_data, coco_file)
       
with open(coco_file_path, "r") as coco_file:
    coco_data = json.load(coco_file)

if validate_coco_format(coco_data):
    print("### COCO 포맷이 올바르게 생성되었습니다.")
else:
    print("### COCO 포맷이 올바르게 생성되지 않았습니다.")
    
if json_ummary(coco_data):
    print("### CSV 파일이 성공적으로 저장되었습니다.")

