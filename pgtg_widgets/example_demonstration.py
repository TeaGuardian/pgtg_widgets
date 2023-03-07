from datetime import datetime, timedelta
import pygame as pg
from .widgets import Button, ProgressBar, Switch
from .catchers import button_catcher, switch_catcher, COLORS


class Timer:
    """delay class"""
    def __init__(self, tick):
        self.tick, self.last = tick, datetime.now()

    def tk(self):
        if (datetime.now() - self.last) > timedelta(seconds=self.tick):
            self.last = datetime.now()
            return True
        return False


def start_demo():
    """can help you to see how to use it"""
    pg.init()
    print("and also Hello from pygame_widgets! Good luck!")
    prog, timer = 0, Timer(0.05)
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


if __name__ == "__main__":
    start_demo()
