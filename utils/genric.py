"""all the generic funcation will be here for all modules """

import json

def read_file(file: str, extention: str="sql"):
    """reading the file, default file type is sql """

    with open(f"{file}.{extention}", "r") as f:
        if extention == "json":
            contents = json.load(f)
        else:
            contents = f.read()
        
    return contents


def change_case(string: str):
    res = []
    _split = string.split(".")[0]
    need_process = string.split('.')[-1]
    for index, value in enumerate(need_process): # MyNewValue
        if index == 0:
            res.append(value.lower())
            continue
        
        if value in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            if value == "_":
                print("found _ so skipping")
                continue
            else:
                res.append('_')
                res.append(value.lower())
        else:
            if value == "_":
                print("found _ so skipping")
                continue
            res.append(value)


    return str(_split) + "." + ''.join(res)
