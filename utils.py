import os

screen_height = 700
screen_width = 1200

MAP_WIDTH = 180
MAP_HEIGHT = 180

root = os.path.abspath(os.curdir).split("\\")




while root[-1] != "Level Editor ( Red Velvet )":
    root.pop(-1)
    
ROOT_DIR = ""

for n in root:
    ROOT_DIR += "{}\\".format(n)


