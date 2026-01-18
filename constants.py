import pygame as pg

WINDOW_SIZE = (1280, 900)

WHITE = (255,255,255)
BLACK = (0,0,0)
BROWN = (110,50,30)

COLORS = {
    "red": (220,60,60),
    "yellow": (230,200,40),
    "green": (60,180,90),
    "blue": (60,120,220),
    None: (180,180,180)
}

PLAYER_NAMES = ["YOU", "PLAYER 1", "PLAYER 2", "PLAYER 3"]

def load_fonts():
    return {
        "big": pg.font.SysFont("arialblack", 72),
        "card": pg.font.SysFont("arialblack", 46),
        "name": pg.font.SysFont("arialblack", 26),
        "btn": pg.font.SysFont("arialblack", 32)
    }
