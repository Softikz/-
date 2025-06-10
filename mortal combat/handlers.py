import pygame
from settings import *
from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def siguiente(self, manejador) -> None:
        pass
    def handler(self, monstruo, surface, target) -> None:
        pass


class BaseHandler(Handler):
    siguiente_manejador: Handler = None
    def siguiente(self, manejador: Handler) -> Handler:
        '''Define al siguiente manejador'''
        self.siguiente_manejador = manejador
        return manejador

    def handler(self, monstruo, surface, target) -> Handler:
        '''Maneja la continuidad de las acciones'''
        if self.siguiente_manejador:
            return self.siguiente_manejador.handler(monstruo, surface, target)
        return None

    

class MovimientoHandler(BaseHandler):
    def handler(self, monstruo, surface, target) -> Handler:  
        '''Función que maneja el movimiento horizontal del personaje'''
        key = pygame.key.get_pressed()
        if monstruo.player_2:
            if key[pygame.K_a]:
                monstruo.dx = -(monstruo.velocidad)
                monstruo.corriendo = True
            elif key[pygame.K_d]:
                monstruo.dx = monstruo.velocidad
                monstruo.corriendo = True
            else:
                monstruo.dx = 0
        else:
            if key[pygame.K_LEFT]:
                monstruo.dx = -(monstruo.velocidad)
                monstruo.corriendo = True
            elif key[pygame.K_RIGHT]:
                monstruo.dx = monstruo.velocidad
                monstruo.corriendo = True
            else:
                monstruo.dx = 0
        return super().handler(monstruo, surface, target)
    
class AtaqueHandler(BaseHandler):
    def handler(self, monstruo, surface, target) -> Handler:
        '''Función que maneja los ataques del personaje'''
        key = pygame.key.get_pressed()
        if monstruo.player_2:
            if key[pygame.K_q]:
                monstruo.tipo_ataque = 1
                monstruo.atacar(surface, target)
            elif key[pygame.K_e]:
                monstruo.tipo_ataque = 2
                monstruo.atacar(surface, target)
            elif key[pygame.K_r]:
                monstruo.tipo_ataque = 3
                monstruo.atacar(surface, target)
        else:
            if key[pygame.K_KP_1]:
                monstruo.tipo_ataque = 1
                monstruo.atacar(surface, target)
            elif key[pygame.K_KP_2]:
                monstruo.tipo_ataque = 2
                monstruo.atacar(surface, target)
            elif key[pygame.K_KP_3]:
                monstruo.tipo_ataque = 3
                monstruo.atacar(surface, target)
        return super().handler(monstruo, surface, target)
       
class SaltoHandler(BaseHandler):
    def handler(self, monstruo, surface, target) -> Handler:
        '''Función que maneja los saltos del personaje'''
        key = pygame.key.get_pressed()
        if monstruo.salto == False:
            if monstruo.player_2 and key[pygame.K_w]:
                monstruo.velY = -SALTO + monstruo.velocidad
                monstruo.salto = True
            elif not monstruo.player_2 and key[pygame.K_UP]:
                monstruo.velY = -SALTO + monstruo.velocidad
                monstruo.salto = True
        return super().handler(monstruo, surface, target)

class GravedadHandler(BaseHandler):
    def handler(self, monstruo, surface, target) -> Handler:
        '''Función encargada del efecto de gravedad en el personaje'''
        monstruo.velY += monstruo.gravedad
        monstruo.dy += monstruo.velY
        return super().handler(monstruo, surface, target)

class LimiteHandler(BaseHandler):
    def handler(self, monstruo, surface, target) -> Handler:
        '''Función que maneja los límites del personaje para que no salga de la pantalla'''
        if monstruo.rect.left+monstruo.dx <0:
            monstruo.dx = -monstruo.rect.left

        if monstruo.rect.right+monstruo.dx > ANCHO:
            monstruo.dx = ANCHO - monstruo.rect.right
        if monstruo.rect.bottom + monstruo.dy > ALTO - 130:
            monstruo.velY = 0
            monstruo.salto = False
            monstruo.dy = ALTO -130 - monstruo.rect.bottom 
        return super().handler(monstruo, surface, target)

class CooldownHandler(BaseHandler):
    def handler(self, monstruo, surface, target) -> Handler:
        '''Función que maneja el enfriamento de los ataques que puede realizar el personaje'''
        if monstruo.cooldown_ataque > 0:
            monstruo.cooldown_ataque -= 1
        return super().handler(monstruo, surface, target)
    
class FlipHandler(BaseHandler):
    def handler(self, monstruo, surface, target) -> Handler:
        '''Función encargada de que ambos personajes siempre estén de frente entre ellos'''
        if target.rect.centerx > monstruo.rect.centerx:
            monstruo.flip = False
        else:
            monstruo.flip = True
        return super().handler(monstruo, surface, target)