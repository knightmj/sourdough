import sys
import os
import json


def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield os.path.join(path, file)


def compare(a):
    return a["difficulty"]


def move_and_rename(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    levels = []
    for file in files(input_dir):
        if file.endswith(".json"):
            with open(file, "r") as h:
                level = json.load(h)
                levels.append(level)

    print("loaded", len(levels), "levels")
    levels.sort(key=compare)
    number = 1
    with open(os.path.join(output_dir,
                           "boards_" + str(len(levels))) + ".csv", "w") as f:
        f.write("id,difficulty,uniqueness,goal words,valid words,total words, cells, hint\n")
        for level in levels:
            total = len(level["valid"]) + len(level["invalid"])
            cells = len(level["board"]) * len(level["board"][0])
            values = [number, level["difficulty"], level["uniqueness"], level["number_of_words"],
                      len(level["valid"]), total, cells, level["rule_text"]]
            values = [str(x) for x in values]
            print(" ".join(values))
            f.write(",".join(values) + "\n")
            with open(os.path.join(output_dir, str(number) + ".json"), "w") as h:
                json.dump(level, h)
            number += 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("group.py <input folder> <output folder>")

    move_and_rename(sys.argv[1], sys.argv[2])
