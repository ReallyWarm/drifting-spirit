import pygame

# returns a sprite image by cropping with rectangle
def sprite_at(location, rectangle):
    sheet = pygame.image.load(location).convert_alpha()
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size, pygame.SRCALPHA)
    image.blit(sheet, (0, 0), rect)

    return image

# returns a list of sprite image by cropping with rectangles list
def sprites_list(location, rectangles):
    return [sprite_at(location, rect) for rect in rectangles]

# create rectangles list to crop in a spritesheet and returns a list of sprite image
def load_sheet(location, rect, image_count, pixel_jump=0):
    rectangles = [((rect[0]+rect[2])*i+(pixel_jump*i), rect[1], rect[2], rect[3]) for i in range(image_count)]
    
    return sprites_list(location, rectangles)