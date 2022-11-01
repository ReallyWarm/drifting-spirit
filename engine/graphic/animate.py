from engine.graphic.spritesheet import load_sheet

class Animate():
    def __init__(self, location, rect, image_count, pixel_jump=0, loop=True, frames=1, start_at=0):
        self.sprites = load_sheet(location, rect, image_count, pixel_jump, start_at)
        self.sprite_size = len(self.sprites)
        self.loop = loop
        self.ani_done = False
        self.image_num = 0
        self.image = self.sprites[self.image_num]
        self.frames_time = frames
        self.frame_num = 0

    def reset(self):
        self.image_num = 0
        self.frame_num = 0
        self.ani_done = False

    def update(self, dt):
        if self.frames_time > 0:
            if self.image_num >= self.sprite_size:
                if not self.loop:
                    self.image_num = self.sprite_size - 1
                    self.ani_done = True
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

