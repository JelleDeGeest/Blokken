from settings import *
import math
from tetromino import Tetromino
import pygame.freetype as ft

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)
    
    def draw(self):
        self.font.render_to(self.app.screen, (WINW * 0.6 + self.app.x_offset, WINH * 0.02), "BLOKKEN", size=70, fgcolor="white")
        self.font.render_to(self.app.screen, (WINW * 0.6 + self.app.x_offset, WINH * 0.22), "VOLGENDE", size=40, fgcolor="white")
        self.font.render_to(self.app.screen, (WINW * 0.6 + self.app.x_offset, WINH * 0.67), "SCORE", size=40, fgcolor="white")
        self.font.render_to(self.app.screen, (WINW * 0.6 + self.app.x_offset, WINH * 0.8), f'{self.app.tetris.score}', size=40, fgcolor="white")

class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False

        self.score = 0
        self.full_lines = 0
        self.points = {0:0, 1:100, 2:300, 3:700, 4:1500}

        self.destroying_lines = False

    def get_score(self):
        self.score += self.points[self.full_lines]
        self.full_lines = 0

    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                # if self.field_array[y][x]:
                #     self.field_array[row][x].pos = vec(x,y)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field_array[y][x].alive = False
                    self.field_array[y][x] = 0
                
                self.full_lines += 1

        if self.full_lines != 0:
            self.destroying_lines = self.full_lines

    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block    

    def get_field_array(self):
        return [[0 for _ in range(FIELD_W)] for _ in range(FIELD_H)]

    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction="left")
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction="right")
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                rect = pg.Rect(x * TILE_SIZE + self.app.x_offset, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pg.draw.rect(self.app.screen, "black", rect, 1)

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()

        
        self.sprite_group.update()
    
    


    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)
        
