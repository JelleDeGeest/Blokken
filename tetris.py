from settings import *
import math
from tetromino import Tetromino
import pygame.freetype as ft
import random

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)
    
    def draw(self):
        self.font.render_to(self.app.screen, (WINW * 0.06 , WINH * 0.1), "BLOKINOHANNES", size=70, fgcolor="white")
        self.font.render_to(self.app.screen, (WINW * 0.65 + self.app.x_offset, WINH * 0.11), "VOLGENDE:", size=40, fgcolor="white")
        self.draw_score()
        self.draw_next_to_drink()
        self.draw_dranken()


    def draw_score(self):
        self.font.render_to(self.app.screen, (WINW * 0.65 + self.app.x_offset, WINH * 0.32 ), "SCORES:", size=40, fgcolor="white")
        for i in range(AMOUNT_OF_PLAYERS):
            self.font.render_to(self.app.screen, (WINW * 0.65  + self.app.x_offset, WINH * (0.42+0.13*i)), f'{TEAM_NAMES[i]}', size=40, fgcolor=PLAYER_COLORS[i])
            self.font.render_to(self.app.screen, (WINW * 0.65  + self.app.x_offset, WINH * (0.48+0.13*i)), f'{self.app.tetris.score[i]}', size=40, fgcolor="white")

    def draw_dranken(self):
        self.font.render_to(self.app.screen, (WINW * 0.24, WINH * 0.30), "DRANKEN", size=55, fgcolor="white")
        for i in range(len(DRANKEN)):
            self.font.render_to(self.app.screen, (WINW * 0.20, WINH * (0.40+0.07*i)), f'{DRANKEN[i][0]}', size=45, fgcolor="white")
            self.font.render_to(self.app.screen, (WINW * 0.50, WINH * (0.40+0.07*i)), f'{DRANKEN[i][1]}', size=45, fgcolor="white")

    def draw_next_to_drink(self):
        for i in range(AMOUNT_OF_PLAYERS):
            self.font.render_to(self.app.screen, (WINW * 1.05  + self.app.x_offset, WINH * (0.48+0.13*i)), f'{self.app.tetris.antwoorders[i]}', size=40, fgcolor="white")

class Tetris:
    def __init__(self, app, score):
        self.app = app
        self.currently_playing = 0
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False
        self.score = score
        self.full_lines = 0
        self.points = {0:0, 1:100, 2:300, 3:700, 4:1500}

        self.destroying_lines = False

        self.ready_to_play = False
        self.tetrominos_to_play = 0

        pg.mixer.music.load(MUSIC)

        self.sound_ready_to_answer = pg.mixer.Sound(SOUND_READY_TO_ANSWER)
        self.antwoorders = None
        self.draw_random_antwoorders()

        
    def draw_random_antwoorders(self):
        antwoorders = []
        if self.antwoorders == None:
            for i in range(len(TEAMS)):
                antwoorders.append(random.choice(TEAMS[i]))
        else:
            for i in range(len(TEAMS)):
                temp = TEAMS[i].copy()
                temp.remove(self.antwoorders[i])
                antwoorders.append(random.choice(temp))
        self.antwoorders = antwoorders            

    def get_score(self):
        self.score[self.currently_playing] += self.points[self.full_lines]
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
            pg.mixer.music.stop()

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
    
    def change_player(self, pressed_key):
        pressed_number = pressed_key - pg.K_1
        if pressed_number < AMOUNT_OF_PLAYERS:
            self.currently_playing = pressed_number
            [block.set_rect() for block in self.tetromino.blocks]
            [block.set_rect() for block in self.next_tetromino.blocks]
            # print(pressed_number)

    def setup_tetrominos_to_play(self):
        self.tetrominos_to_play = BLOCKS_PER_TURN
        self.ready_to_play = True
        pg.mixer.music.play(-1)

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            
            if self.is_game_over():
                self.score[self.currently_playing] -= 200
                self.__init__(self.app, self.score)
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)
                self.tetrominos_to_play -= 1
                if self.tetrominos_to_play == 0:
                    self.ready_to_play = False
                    pg.mixer.music.stop()

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT and self.ready_to_play:
            self.tetromino.move(direction="left")
        elif pressed_key == pg.K_RIGHT and self.ready_to_play:
            self.tetromino.move(direction="right")
        elif pressed_key == pg.K_UP and self.ready_to_play:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN and self.ready_to_play:
            # self.speed_up = True
            self.tetromino.move(direction="down")
        elif pressed_key in NUMBER_KEYS:
            self.change_player(pressed_key)
        elif pressed_key == pg.K_RETURN:
            self.setup_tetrominos_to_play()
        elif pressed_key == pg.K_x:
            self.sound_ready_to_answer.play()
        elif pressed_key == pg.K_r:
            self.draw_random_antwoorders()
        elif pressed_key == pg.K_PAGEUP:
            self.score[self.currently_playing] += 100
        elif pressed_key == pg.K_PAGEDOWN:
            self.score[self.currently_playing] -= 100


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
        
