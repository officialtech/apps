"""all the generic funcation will be here for all modules """

import json

def read_file(file, extention="sql"):
    """reading the file, default file type is sql """

    with open(f"{file}.{extention}", "r") as f:
        if extention == "json":
            contents = json.load(f)
        else:
            contents = f.read()
        
    return contents