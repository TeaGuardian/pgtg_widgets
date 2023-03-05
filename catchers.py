from widgets import Switch, Button, ProgressBar
from datetime import datetime, timedelta
import pygame as pg


COLORS = {"wh": (30, 30, 30), "gr": (150, 150, 150), "fn": (90, 100, 90), "li": (255, 230, 190),
          'grey': (150, 150, 150), 'lilac': (100, 130, 250), 'red': (250, 40, 80),
          'blue': (40, 120, 200), 'dark': (60, 60, 60), 'green': (40, 250, 80),
          'yellow': (240, 200, 10), 'meddle': (90, 90, 100), 'dark_blue': (30, 90, 150), 'white': (255, 255, 255),
          'black': (0, 0, 0), 'orange': (180, 120, 40), 'dark_green': (20, 120, 60)}


def lim_255(g):
    if g > 255:
        return 255
    elif g < 0:
        return 0
    return g


def switch_catcher(pos_x: int, pos_y: int, pressed: bool, switch: Switch):
    sel = switch.show(pos_x, pos_y)
    if pressed and sel:
        switch.switch()


def button_catcher(pos_x: int, pos_y: int, pressed: bool, button: Button, color=None, light=0.6):
    sel = button.show(pos_x, pos_y)
    if color is None:
        color = button.col[:]
    color = list(map(lambda g: lim_255(int(g * light)), color))
    if pressed and sel:
        button.task_animation(pos_x, pos_y, color, 50)
        return True
    return False


class Timer:
    """класс задержки"""
    def __init__(self, tick):
        self.tick, self.last = tick, datetime.now()

    def tk(self):
        if (datetime.now() - self.last) > timedelta(seconds=self.tick):
            self.last = datetime.now()
            return True
        return False


if __name__ == "__main__":
    pg.init()
    prog, timer = 0, Timer(0.05)
    cl = pg.time.Clock()
    sc = pg.display.set_mode((800, 800))
    switch = Switch(sc, 10, 10, 100, 40, COLORS['lilac'], COLORS['dark_blue'], COLORS['yellow'])
    button = Button(sc, 10, 80, 100, 40, COLORS['blue'], text="SET 0%..", text_color=COLORS['green'])
    button2 = Button(sc, 120, 80, 100, 40, COLORS['blue'], text="SET 50%..", text_color=COLORS['green'])
    progress_bar = ProgressBar(sc, 10, 140, 400, 20, COLORS['dark_green'], COLORS['orange'], COLORS['yellow'], border=4)
    while True:
        if prog < 100 and timer.tk() and prog >= 0:
            prog += -0.3 if switch.get_real_state() else 0.3
            progress_bar.set_prog(prog)
        elif prog < 0:
            prog = 0.6
        sc.fill(COLORS["gr"])
        pressed = False
        pos_x, pos_y = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                pressed = True
        switch_catcher(pos_x, pos_y, pressed, switch)
        button_rez = button_catcher(pos_x, pos_y, pressed, button, light=0.7)
        button2_rez = button_catcher(pos_x, pos_y, pressed, button2, light=0.1)
        progress_bar.show(pos_x, pos_y)
        button.show(pos_x, pos_y)

        if button_rez:
            prog = 0
        if button2_rez:
            prog = 50
        pg.display.flip()
