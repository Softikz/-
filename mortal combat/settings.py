import pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60
#Crear la ventana del juego
ANCHO = 1050
ALTO = 670

#Fuente
font_path = 'Fonts/deutsch_gothic/Deutsch.ttf'
font_deutsch = pygame.font.Font(font_path, 50)
#Variables del juego
SALTO = 45

screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Monster Kombat")

#Healthbar
hb = pygame.image.load('Assets/empty health bar.png').convert_alpha()

#Sonidos
sound=pygame.mixer.Sound('Assets/Music/641216__spiderfair__highlightlong.wav')
hit= pygame.mixer.Sound('Assets/Music/425348__soundholder__8bit_hit_11.wav')
gameover = pygame.mixer.Sound('Assets/Music/527650__fupicat__winsquare.wav')



DOSBRAZOS_WIDTH = 190
DOSBRAZOS_HEIGHT = 185
DOSBRAZOS_SCALE = 3
DOSBRAZOS_OFFSET = [82, 66]
DOSBRAZOS_DATA = [DOSBRAZOS_HEIGHT, DOSBRAZOS_WIDTH, DOSBRAZOS_SCALE, DOSBRAZOS_OFFSET]
MDB_SCALE = 3
MDB_WIDTH = 190
MDB_HEIGHT = 155
MDB_OFFSET = [83,46]
MDB_DATA = [MDB_HEIGHT, MDB_WIDTH, MDB_SCALE, MDB_OFFSET]
dosBrazos_sheet = pygame.image.load('Spritesheets/2Brazos/DosBrazos.png').convert_alpha()
mdb_sheet = pygame.image.load('Spritesheets/MariposaDeBarrio/MDB.png').convert_alpha()

#Botones
button_sheet = pygame.image.load('Assets/buttons.png')

#definir pasos de cada animación   AS = Animation steps
#[walk, heavy attack, idle, hurt, Death, quick attack, light attack]
DOSBRAZOS_ANIMATION_STEPS = [8, 12, 8, 4, 8, 4, 8]
MDB_ANIMATION_STEPS = [8, 8, 8, 4, 8, 5, 7]
#TODO: Cambiar background
fondo = pygame.image.load('Assets/bulkhead-wallsx3.png').convert_alpha()


def draw_bg() -> None:
    '''Función que dibuja el fondo del juego'''
    screen.blit(fondo, (0,0))