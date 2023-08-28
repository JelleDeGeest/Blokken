import pygame as pg
pg.joystick.init()
joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
print(joysticks[0].get_numbuttons())
for button in range(joysticks[0].get_numbuttons()):
    print(joysticks[0].get_button(button))
