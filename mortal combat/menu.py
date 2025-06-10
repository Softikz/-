from settings import *
from colors import *

def get_image(sheet, ancho, alto, incrementar, color, frame) -> object:
    '''Función que pone en los botones o rects el fondo de una imagen'''
    image = pygame.Surface((ancho, alto)).convert_alpha()
    image.blit(sheet, (0,0), (frame*ancho,frame*alto, ancho, alto))
    image = pygame.transform.scale(image, (ancho*incrementar, alto*incrementar))
    image.set_colorkey(color)
    return image