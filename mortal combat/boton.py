import pygame
from menu import get_image
from settings import *
from colors import * 
class Boton:
    '''Clase para crear botones'''
    def __init__(self, text, x, y, width=300, height=100, font_size=60, font_color=DORADO, bg_color=NEGRO):
        self.text = text
        self.width = width
        self.height = height
        self.font_size = font_size
        self.font_color = font_color
        self.bg_color = bg_color
        self.font = pygame.font.Font(font_path, self.font_size)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA) # set SRCALPHA flag for transparent background
        self.image.set_colorkey(NEGRO) #Hacer que los pixeles negros sean transparentes
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) #Centrar el botón
        self.mouse_over = False
        self.redraw()

    def redraw(self) -> None:
        '''Método para actualizar la imagen del botón'''
        self.image.fill((0, 0, 0, 0)) # Poner el fondo transparente
        button_frame = get_image(button_sheet, 70, 42, 1, NEGRO, 0)  # Obtener el frame de los botones
        button_frame_scaled = pygame.transform.scale(button_frame, (self.width+50, self.height+50))
        button_rect = button_frame_scaled.get_rect()
        button_rect.center = self.image.get_rect().center
        self.image.blit(button_frame_scaled, button_rect)
        text_surf = self.font.render(self.text, True, self.font_color)
        text_rect = text_surf.get_rect()
        text_rect.center = self.image.get_rect().center
        self.image.blit(text_surf, text_rect)

    def draw(self, screen) -> None:
        '''Método para renderear el botón en la pantalla.'''
        screen.blit(self.image, self.rect)
        if self.mouse_over:
            border_rect = self.rect.inflate(10, 10)
            pygame.draw.rect(screen, self.font_color, border_rect, 2)
            
