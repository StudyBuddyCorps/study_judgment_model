import yaml

data = {
        "train": '/Users/baejuhyeon/Documents/capstone/study_dataset/split_dataset/train/',
        "val": '/Users/baejuhyeon/Documents/capstone/study_dataset/split_dataset/valid/',
        "test": '/Users/baejuhyeon/Documents/capstone/study_dataset/split_dataset/test/',
        "names": {0: 'awake_face', 1: 'awake_person', 2: 'phone', 3: 'sleeping_face', 4: 'sleeping_person'}}

# awake_face
# awake_person
# phone
# sleeping_face
# sleeping_person

with open('../detector/coco.yaml', 'w') as f :
    yaml.dump(data, f)

# check written file
with open('../detector/coco.yaml', 'r') as f :
    lines = yaml.safe_load(f)
    print(lines)