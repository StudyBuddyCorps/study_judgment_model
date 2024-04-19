"""
Merge Yolo txt label files together
"""

import os
from tqdm import tqdm

if __name__ == "__main__":
    path = "//runs/detect/"
    folder = "sleep"

    face_files = os.listdir(path+folder+"/face-labels/")

    face_labels = []
    for file in face_files:
        if "txt" in file:
            face_labels.append(file)
    print(len(face_labels))
    face_labels.sort()

    cnt = 0
    for i in tqdm(range(len(face_labels))):
        new_lines = ""
        with open(path+folder+"/face-labels/"+f"{face_labels[i]}", 'r') as f:
            lines = f.readlines()
            for k in lines:
                k = k.rstrip()
                content = k.split(' ')
                if content[0] == "0":
                    content[0] = '0'
                    new_lines += (" ".join(content)+'\n')

        try:
            with open(path+folder+"/labels/"+f"{face_labels[i]}", 'r') as lf:
                lines = lf.readlines()
                for k in lines:
                    k = k.rstrip()
                    content = k.split(' ')
                    if content[0] == '0' or content[0] == "65":
                        content[0] = '1'
                    new_lines += (" ".join(content)+'\n')
        except:
            print(path+folder+"/labels/"+f"{face_labels[i]}")
        with open(path + folder + "/new_labels/" + f"{face_labels[i]}", "w") as wf:
            wf.write(new_lines)
