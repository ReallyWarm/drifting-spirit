import os, sys
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(MAIN_DIR))
from engine.genlevel import gen_level

level = list()
level_data = gen_level('data/map.json')
for layer in level_data:
    layer_data = list()
    for data in layer:
        if data[0] in ['n1b','n2b','n3b']:
            plat = (data[2],320-data[3])
            layer_data.append(plat)
    level.append(layer_data)

print(level)
dis = list() 
c_loop = 0
for layer in reversed(level):
    # print(layer)
    for data in layer:
        dis.append(data)

    c_loop += 1
    if c_loop >= 5:
        break