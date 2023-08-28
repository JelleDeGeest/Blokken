import pygame as pg

vec = pg.math.Vector2

FPS = 60
FIELD_COLOR = (48, 39, 32)
BG_COLOR = (24,89,117)

FONT_PATH = 'assets/fonts/tetris_font.ttf'

ANIM_TIME_INTERVAL = 500
ANIM_FAST_TIME_INTERVAL = 15

MUSIC = 'assets/sounds/Tetromino_falling.wav'
SOUND_READY_TO_ANSWER = 'assets/sounds/ready_to_answer.wav'


AMOUNT_OF_PLAYERS = 4
PLAYER_COLORS = ["red", "blue", "green", "yellow", "purple", "orange", "cyan"]
NUMBER_KEYS = [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7]
BLOCKS_PER_TURN = 2

TILE_SIZE = 50
FIELD_SIZE = FIELD_W, FIELD_H = 10, 20
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE

FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0
WIN_RES = WINW, WINH = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H

INIT_POS_OFFSET = vec(FIELD_W //2, 0)
NEXT_POS_OFFSET = vec(FIELD_W * 1.3, FIELD_H * 0.45)
MOVE_DIRECTIONS = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)}

TETROMINOES = {
    'T':[(0,0),(-1,0),(1,0),(0,-1)],
    'O':[(0,0),(1,0),(0,-1),(1,-1)],
    'J':[(0,0),(-1,0),(0,-1),(0,-2)],
    'L':[(0,0),(1,0),(0,-1),(0,-2)],
    'I':[(0,0),(0,1),(0,-1),(0,-2)],
    'S':[(0,0),(-1,0),(0,-1),(1,-1)],
    'Z':[(0,0),(1,0),(0,-1),(-1,-1)]
}