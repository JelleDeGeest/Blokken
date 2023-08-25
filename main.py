from settings import *
from tetris import Tetris, Text
import sys


class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        # self.screen = pg.display.set_mode(WIN_RES)
        self.screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.x_offset = pg.display.get_surface().get_size()[0] // 2 - FIELD_W * TILE_SIZE // 2

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.fast_user_event, ANIM_FAST_TIME_INTERVAL)
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)

    def update(self):
        self.clock.tick(FPS)
        self.tetris.update()

    def draw(self):
        self.screen.fill(color=BG_COLOR) 
        self.screen.fill(color=FIELD_COLOR, rect=(self.x_offset,0,*FIELD_RES))
        self.tetris.draw()
        self.draw_cuttoff()
        self.text.draw()
        pg.display.flip()
    
    def draw_cuttoff(self):
        pg.draw.rect(self.screen, BG_COLOR, (0,0,self.x_offset,WINH))
    

    def check_events(self):
        self.anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True


    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
