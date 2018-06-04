# coding: utf-8
from ..model.models import DogBase, DogInfo
import json
import re


def update_dog_base(dog_base_list):
    for node in dog_base_list:
        dog_base = DogBase()
        dog_base.dog_name = node['name']
        dog_base.dog_name_id = node['english_name'][:32]
        dog_base.dog_size = node['personality'].split(";")[0]
        dog_base.dog_type = node['personality'].split(";")[1][:3]
        #import pdb
        #pdb.set_trace()
        # print(">>>>>12")
        dog_base_node, create = DogBase.objects.update_or_create(
            dog_name=dog_base.dog_name,
            dog_name_id=dog_base.dog_name_id,
            dog_size=dog_base.dog_size,
            dog_type=dog_base.dog_type)
        #import pdb
        #pdb.set_trace()


def do_update_info(dog_info_list):
    for node in dog_info_list:
        dog_info = DogInfo()
        dog_info.dog_type = node['dog_type']
        dog_info.dog_size = node['dog_size']
        try:
            dog_info.dog_age_min = int(re.sub("\D", "", node['dog_age_min']))
        except:
            dog_info.dog_age_min = 0
        try:
            dog_info.dog_age_max = int(re.sub("\D", "", node['dog_age_max']))
        except Exception:
            dog_info.dog_age_max = 0
        dog_info.english_name = node['english_name'][:60]
        dog_info.chinese_name = node['chinese_name']
        dog_info.homeland = node['homeland'][:31]
        dog_info.dog_personality = node['dog_personality']
        try:
            dog_info.dog_description = node['dog_description']
        except:
            dog_info.dog_description = ''
            print("description:", node)

        try:
            dog_base = DogBase.objects.get(dog_name=node['chinese_name'])
            dog_name_id = dog_base.dog_name_id
        except Exception as e:
            dog_name_id = node['english_name'][:32]


        dog_info_node, create = DogInfo.objects.update_or_create(
            dog_type=dog_info.dog_type,
            dog_size=dog_info.dog_size,
            dog_age_min=dog_info.dog_age_min,
            dog_age_max=dog_info.dog_age_max,
            english_name=dog_info.english_name,
            chinese_name=dog_info.chinese_name,
            dog_personality=dog_info.dog_personality,
            dog_description=dog_info.dog_description,
            dog_name_id=dog_name_id,
            homeland=dog_info.homeland
        )

        print(">>>>>")


    pass


def read_json(path):
    with open(path, 'r') as f:
        json_str = f.read()
        data = json.loads(json_str)

    data_dedup = []
    for node in data:
        if node in data_dedup:
            continue
        data_dedup.append(node)

    # print("data_len", len(data_dedup))

    return data


def do_update():
    path = 'dogwiki/data/base.json'
    data = read_json(path)
    update_dog_base(data)




if __name__ == "__main__":
    read_json("dogwiki/data/base.json")