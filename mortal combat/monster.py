import pygame
from settings import *
from colors import *
from handlers import *

class Monster():
    '''Clase de los monstruos del juego'''
    def __init__(self, x, y, flip, velocidad, player_2, data, sprite_sheet, animation_steps):
        self.height = data[0]
        self.width = data[1]
        self.image_scale = data[2]
        self.offset = data[3]
        self.flip = flip
        self.animation_list = self.cargar_imagenes(sprite_sheet, animation_steps) 
        self.rect = pygame.Rect((x, y, 100, 180))
        self.velocidad=velocidad
        self.velY = 0
        self.player_2:bool = player_2 
        self.salto = False
        self.tipo_ataque:int = 0
        self.cooldown_ataque = 0
        self.atacando=False
        self.corriendo = False
        self.salud = 100
        #0:walk, 1:Heavy Attack, 2:Idle, 3:Take Hit. 4: Death 
        self.accion = 2
        self.frame_index = 2
        self.image = self.animation_list[self.accion][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.take_hit = False
        self.vivo = True
        self.dx = 0
        self.dy = 0
        self.gravedad = 2
        self.anim_cooldown = 90

    def cargar_imagenes(self, sprite_sheet, animation_steps) -> list:
        '''Función que carga las animaciones para cada acción desde el spritesheet de cada personaje'''
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.width, y * self.height, self.width, self.height)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.width * self.image_scale, self.height * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def caminarChain(self, surface, target) -> None:
        '''Función que se encarga del movimiento de los personajes'''
        self.gravedad = 2
        self.dx = 0
        self.dy = 0
        self.corriendo = False
        self.tipo_ataque = 0
        handler = MovimientoHandler()
        handler.siguiente(GravedadHandler()).siguiente(AtaqueHandler()).siguiente(LimiteHandler()).siguiente(SaltoHandler()).siguiente(CooldownHandler()).siguiente(FlipHandler())
        if self.vivo == False:
            pygame.QUIT
        else:
            if self.atacando == False:
                handler.handler(self, surface, target)
                self.rect.x += self.dx
                self.rect.y += self.dy
    
    def update(self) -> None:
        '''Función que se encarga de actualizar la animación del personaje dependiendo de la acción que esté realizando'''
        self.selector_accion()
        self.image = self.animation_list[self.accion][self.frame_index]
        #Verificar si suficiente tiempo ha pasado desde último update 
        if pygame.time.get_ticks() - self.update_time > self.anim_cooldown:
            self.frame_index +=1
            self.update_time = pygame.time.get_ticks()
        #Actualizar frame que se debe ver en el personaje
        if self.frame_index >= len(self.animation_list[self.accion]):
            self.accion_finalizada()
                    
    def selector_accion(self) -> None:
        '''Función que selecciona la animación que se pasará al personaje'''
        #Verificar acciones en uso
        if self.salud <= 0:
            self.salud = 0
            self.vivo = False
            self.cambio_accion(4) #4: Muerte
        elif self.take_hit == True:
            self.cambio_accion(3) #3: hit
        elif self.atacando == True:
            if self.tipo_ataque == 1:
                hit.play()
                self.cambio_accion(5) #5 ataque rapido
            elif self.tipo_ataque == 2:
                hit.play()
                self.cambio_accion(1) #1: Ataque pesado
            elif self.tipo_ataque == 3:
                hit.play()
                self.cambio_accion(6) #6: ataque ligero
        elif self.corriendo == True:
            self.cambio_accion(0) #0:caminar
        else:
            self.cambio_accion(2) #2:idle
        self.anim_cooldown = 90
    
    def accion_finalizada(self) -> None:
        '''Función que verifica si una animación ya terminó y si el personaje sigue vivo'''
        #Checar si el personaje murió
        if self.vivo == False:
            self.frame_index = len(self.animation_list[self.accion]) -1
        else:
            self.frame_index = 0
            if self.accion == 1:
                self.atacando = False
                self.cooldown_ataque = 50
            if self.accion == 3 or self.accion == 5 or self.accion == 6:
                self.take_hit = False
                self.atacando = False
                if self.accion == 5:
                    self.cooldown_ataque = 10
                elif self.accion == 6:
                    self.cooldown_ataque = 20
                elif self.accion == 3:
                    self.cooldown_ataque = 50
        

    def atacar(self, surface, target) -> None:
        '''Función que crea el rectángulo de colisión del ataque del personaje y hace el cálculo de daño'''
        if self.cooldown_ataque == 0:
            self.atacando = True
            rect_arma = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip), self.rect.y, 3* self.rect.width, self.rect.height)
            #TODO: Funcion recibir golpe
            if rect_arma.colliderect(target.rect):
                #Se usa un Facade al llamar al método colliderect
                if self.tipo_ataque == 1:
                    target.salud -= 5
                    target.take_hit = True
                elif self.tipo_ataque == 2:
                    target.salud -= 10
                    target.take_hit = True
                elif self.tipo_ataque == 3:
                    target.salud -= 5
                    target.take_hit = True
            #pygame.draw.rect(surface, VERDE, rect_arma)



    def cambio_accion(self, nueva_accion) -> None:
        '''Función que verifica si la nueva acción introducida es diferente a la anterior'''
        if nueva_accion != self.accion:
            self.accion = nueva_accion
            #Actualizar settings de la animación
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface) -> None:
        ''''Funcion para dibujar a los monstruos en la pantalla'''
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, ROJO, self.rect)
        surface.blit(img, (self.rect.x -(self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
    
