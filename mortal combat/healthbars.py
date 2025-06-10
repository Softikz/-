from settings import *
from colors import *
import pygame

def draw_health_bar(health, x, y) -> None:
    '''Función para dibujar el rectángulo rojo que indica la salud de los personajes'''
    ratio = health / 100
    tiempo = 1700
    scaled_hb = pygame.transform.scale(hb, (440, 50))
    pygame.draw.rect(screen, ROJO_OSCURO, (x,y,400, 30))
    if pygame.time.get_ticks() < tiempo:
        pygame.draw.rect(screen, BLANCO, (x,y,400, 30)) if pygame.time.get_ticks() < tiempo else pygame.draw.rect(screen, ROJO_OSCURO, (x,y,400, 30))

    pygame.draw.rect(screen, ROJO, (x,y,400 * ratio,30))
    screen.blit(scaled_hb, (x-20, y-10))
