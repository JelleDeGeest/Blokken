from settings import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True

        super().__init__(self.tetromino.tetris.sprite_group)
        self.set_rect()

        self.sfx_speed = 0.1
        self.sfx_cycles = 3
        self.sfx_count = 0
    
    def set_rect(self):
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        pg.draw.rect(self.image,PLAYER_COLORS[self.tetromino.tetris.currently_playing], (1,1,TILE_SIZE-2,TILE_SIZE-2), border_radius=8)
        self.rect = self.image.get_rect()

    def sfx_end_time(self):
        if self.tetromino.tetris.app.anim_trigger:
            self.sfx_count += 1
            if self.sfx_count >= self.sfx_cycles:
                self.sfx_count = 0
                self.sfx_fix_pos()
                self.tetromino.tetris.destroying_lines = 0
                if self.tetromino.tetris.tetrominos_to_play == 1:
                    pg.mixer.music.play(-1)
                return True
    
    def sfx_fix_pos(self):
        field_array = self.tetromino.tetris.field_array
        for y in range (FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                if field_array[y][x]:
                    field_array[y][x].pos = vec(x,y)

    def sfx_run(self):
        self.pos.x -= self.sfx_speed  

    def is_alive(self):
        if not self.alive:
            if not self.sfx_end_time():
                self.sfx_run()
            else:
                self.kill()

    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetromino.current] * TILE_SIZE
        pos += vec(self.tetromino.tetris.app.x_offset, 0)
        self.rect.topleft = pos

    def update(self):
        self.is_alive()
        self.set_rect_pos()
    
    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (y<0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True


class Tetromino:
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOES.keys()))
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        self.landing = False
        self.current = current

    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_positions):
            for i,block in enumerate(self.blocks):
                block.pos = new_block_positions[i]

    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))

    def move(self, direction):
        if self.tetris.destroying_lines == 0 and self.tetris.ready_to_play:
            move_direction = MOVE_DIRECTIONS[direction]
            new_block_positions = [block.pos + move_direction for block in self.blocks]
            is_collide = self.is_collide(new_block_positions)

            if not is_collide:
                for block in self.blocks:
                    block.pos += move_direction
            elif direction == 'down':
                self.landing = True

    def update(self):
        self.move(direction="down")
