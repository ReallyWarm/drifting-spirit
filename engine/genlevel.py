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
        this_y = int(height) * TILE_SIZE * SCALE
        plat_x = [0,1,2,3,4,5,6,7]
        enmy_x = [0,1,2,3,4,5,6,7]
        for name in this_data:
            pos_y = this_y
            enmy = False
            remove_near = 0

            if name == 'n2b':
                plat_x.remove(7)
                remove_near = 1
            elif name == 'n3b':
                plat_x.remove(7)
                plat_x.remove(6)
                remove_near = 2
            elif name in ['ght','imp']:
                pos_y += TILE_SIZE
                enmy = True
            elif name == 'prt':
                pos_x = (5 * TILE_SIZE) // 2
                height_data.append(['n3b', 2, pos_x, pos_y])
                pos_y += TILE_SIZE * SCALE
                pos_x = (7 * TILE_SIZE) // 2
                height_data.append([name, 3, pos_x, pos_y])
                
            for _ in range(this_data[name]):
                if enmy:
                    index_x = random.choice(enmy_x)
                    enmy_x.remove(index_x)
                else:
                    index_x = random.choice(plat_x)
                    plat_x.remove(index_x)
                
                for i in range(remove_near):
                    for side in range(-1,2,2):
                        ix = (i+1) * side
                        if index_x+ix in plat_x:
                            plat_x.remove(index_x+ix)
                
                pos_x = index_x * TILE_SIZE
                height_data.append([name, index_x, pos_x, pos_y])
        level_data.append(height_data)

    return level_data
