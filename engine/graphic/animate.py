from engine.graphic.spritesheet import load_sheet

class Animate():
    def __init__(self, location, rect, image_count, pixel_jump=0, loop=True, frames=1):
        self.sprites = load_sheet(location, rect, image_count, pixel_jump)
        self.loop = loop
        self.image_num = 0
        self.image = self.sprites[self.image_num]
        self.frames_time = frames
        self.frame_num = 0

    def reset(self):
        self.image_num = 0
        self.frame_num = 0

    def update(self, dt):
        if self.frames_time > 1:
            size = len(self.sprites)
            if self.image_num >= size:
                if not self.loop:
                    self.image_num = size - 1
                else:
                    self.image_num = 0
            
            self.image = self.sprites[self.image_num]
            self.frame_num += 1
            if self.frame_num >= self.frames_time / dt:
                self.image_num += 1
                self.frame_num = 0

        return self.image

    def __add__(self, addSprite):
        self.sprites.extend(addSprite.sprites)

        return self

