import os
import shutil

from generate_page import generate_page

def build(source:str, destination:str):
    # Clean destination folder
    for file in os.listdir(destination):
        filepath = os.path.join(destination, file)
        if os.path.isdir(filepath):
            shutil.rmtree(filepath)
        else:
            os.remove(filepath)
        
    copy(source, destination)
            
def copy(source:str, destination:str):
    for file in os.listdir(source):
        filepath = os.path.join(source, file)
        if os.path.isdir(filepath):
            new_destination = os.path.join(destination, file)
            if not os.path.exists(new_destination):
                print("Creating new directory", new_destination)
                os.mkdir(new_destination)
            copy(os.path.join(source,file), new_destination)
        else:
            print("Copying", filepath, "to", f"{destination}/{file}")
            shutil.copy(filepath, destination)
