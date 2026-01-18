import pygame as pg

class InputHandler:
    def get(self):
        pos = pg.mouse.get_pos()
        pressed = pg.mouse.get_pressed()
        return pos, pressed, pressed[0] # Retorna posição, botões e se o esquerdo foi clicado