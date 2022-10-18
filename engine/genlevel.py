import json, random

def gen_level(location):
    TILE_SIZE = 32
    SCALE = 3/2
    level_data = []

    with open(location, 'r') as f:
            map = json.load(f)
            f.close()

    for height in map:
        this_data = map[height]
        height_data = list()
        pos_y = int(height) * TILE_SIZE * SCALE
        rand_x = [0,1,2,3,4,5,6,7]
        for name in this_data:
            if name == 'n2b':
                rand_x.remove(7)
            elif name == 'n3b':
                rand_x.remove(7)
                rand_x.remove(6)
            for _ in range(this_data[name]):
                index_x = random.choice(rand_x)
                rand_x.remove(index_x)
                
                remove = 0
                if name == 'n2b':
                    remove = 1
                elif  name == 'n3b':
                    remove = 2
                
                for i in range(remove):
                    for side in range(-1,2,2):
                        ix = (i+1) * side
                        if index_x+ix in rand_x:
                            rand_x.remove(index_x+ix)
                
                pos_x = index_x * TILE_SIZE
                height_data.append([name, index_x, pos_x, pos_y])
        level_data.append(height_data)

    return level_data
