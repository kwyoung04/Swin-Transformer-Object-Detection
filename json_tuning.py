import sys
import os
import json
import argparse

from pathlib import Path

from pycocotools.coco import COCO

del_call = ['background_in', 'pillar', 'sky', 'tree', 'background_out']



def cheak_abs_name(name_list):
    for part_name in name_list:
        if (part_name >= '0' and part_name <= '9999999' and len(part_name) == 7):
          return part_name

    return 0


class custom_dataset:
    def __init__(self):
        self.cocoFormat = {'licenses': [], 'images': [], 'annotations': [], 'categories': []}
        self.categorieFlag = 1
        
        self.id_cnt = 1

    def invisible_data(self, inKey):
        pairName = {'images': 'images', 'categories': 'Categories', 'annotations': 'annotations'}
        for val in pairName.values():
            if val in inKey:
                continue
            else:
                print("error 0")
                exit()

    def count_keypoint(self, keypoints):
        cnt = 0
        i = 2
        while i < 50:
            if keypoints[i] == 0:
                cnt = cnt + 1
            i = i+3   

        return 17 - cnt

    def push_json(self, jsonFile):
        with open(jsonFile, 'rt', encoding='UTF-8-sig') as file:
            data = json.load(file)
            assert type(data)==dict, 'annotation file format {} not supported'.format(type(data))
           
            self.del_cate(data)
            
            
    def del_cate(self, data):
        cat_len = len(data['categories'])
        
        del_class_id = []
        i = 0
        cntt = 0
        while i < cat_len:
            if data['categories'][i]['name'] in del_call:
                del_class_id.append(data['categories'][i]['id'])
                data['categories'][i] = data['categories'][i+1]
                del(data['categories'][i+1])
                cat_len = cat_len-1
                cntt = cntt + 1
                i = i-1
            else:
                data['categories'][i]['id'] = data['categories'][i]['id'] - cntt
            i = i+1
            
            
        complet_list = []    
        for id in data['categories']:
            complet_list.append(id['id'])
        
        for del_id in del_class_id:
            complet_list.insert(del_id, 99999)
             
             
             
        anno_len = len(data['annotations'])
        i = 0
        while i < anno_len:
            data['annotations'][i]['category_id'] = complet_list[data['annotations'][i]['category_id']]-1
            if data['annotations'][i]['category_id'] > 10000:
                del(data['annotations'][i])
                anno_len = anno_len-1
                continue
            i = i+1   
            
        self.cocoFormat = data
        
    def compare_jpg_json(self):
        pass

    def save_json(self, abspath):
        filePath = abspath + "/" + "test" + "_instance.json"
        #filePath = "/home/ubuntu/koreaData/kapao_custom/data/datasets/test/annotations" + "/" + "person_keypoints_val2017.json"
        with open(filePath, 'w') as outfile:
            json.dump(self.cocoFormat, outfile)


def get_json():
    pass

def find_jsonSet(path):
    jsonList=[]
    
    for dirpath, dirname, filename in os.walk(path, topdown=False):
        aliveSet = ['json']
        jsonList.extend([dirpath+'/'+i for i in filename if i[-4:] in aliveSet])

    return jsonList



if __name__ == '__main__':
    print("### Change NIA Format to COCO Format")
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', dest='jsonFile', default='', help='json file')

    args = parser.parse_args()
    
    dirname = os.path.dirname(args.jsonFile)
    abspath = os.path.abspath(args.jsonFile)

    jsonList = args.jsonFile
    
    coco_keypoint = custom_dataset()
    
    coco_keypoint.push_json(jsonList)

    coco_keypoint.save_json(dirname)


    
    print("### Conversion complete")
    