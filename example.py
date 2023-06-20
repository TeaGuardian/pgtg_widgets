import pygame as pg
from pgtg_widgets.widgets import *


COLORS = {"wh": (30, 30, 30), "gr": (100, 100, 110), "fn": (90, 100, 90), "li": (255, 230, 190),
          'grey': (150, 150, 150), 'lilac': (100, 130, 250), 'red': (250, 40, 80),
          'blue': (40, 120, 200), 'dark': (60, 60, 60), 'green': (40, 250, 80),
          'yellow': (240, 200, 10), 'meddle': (90, 90, 100), 'dark_blue': (30, 90, 150), 'white': (255, 255, 255),
          'black': (0, 0, 0), 'orange': (180, 120, 40), 'dark_green': (20, 120, 60)}


class Timer:
    """delay class"""
    def __init__(self, tick):
        self.tick, self.last = tick, pg.time.get_ticks()

    def tk(self):
        if self.last + self.tick < pg.time.get_ticks():
            self.last = pg.time.get_ticks()
            print(20)
            return True
        return False


def start_demo():
    """can help you to see how to use it"""
    pg.init()
    print("and also Hello from pygame_widgets! Good luck! \nP.s. use this package how you want")
    prog, timer, st = 0, Timer(5000), -1
    sc = pg.display.set_mode((600, 600))
    font = pg.font.Font(None, 30)
    switch = Switch(sc, (10, 10, 120, 40), COLORS['lilac'], COLORS['dark_blue'], COLORS['yellow'], state=True)
    button = Button(sc, (10, 80, 120, 40), font, COLORS['blue'], text="SET 0%..", text_color=COLORS['green'], an_col=COLORS['blue'], an_li=0.5)
    button2 = Button(sc, (140, 80, 120, 40), font, COLORS['blue'], text="SET 50%..", text_color=COLORS['green'], an_col=COLORS['blue'], an_li=0.1)
    progress_bar = ProgressBar(sc, (10, 140, 400, 20), COLORS['dark_green'], COLORS['orange'], COLORS['yellow'], border=4, phis_t=50, phis_st=2, show_real=True)
    inp_u = InputBox(sc, (10, 180, 200, 40), font, COLORS['lilac'], COLORS['yellow'], sub_moo=-1)
    tex_u = TextBox(sc, (220, 180, 200, 40), font, COLORS['orange'], sub_moo=-1, text='u')
    inp_s = InputBox(sc, (10, 230, 200, 40), font, COLORS['lilac'], COLORS['yellow'], sub_moo=0)
    tex_s = TextBox(sc, (220, 230, 200, 40), font, COLORS['orange'], sub_moo=0, text='s')
    inp_d = InputBox(sc, (10, 280, 200, 40), font, COLORS['lilac'], COLORS['yellow'], sub_moo=1)
    tex_d = TextBox(sc, (220, 280, 200, 40), font, COLORS['orange'], sub_moo=1, text='d')
    al_ob = [switch, button, button2, progress_bar, inp_s, inp_d, inp_u, tex_d, tex_s, tex_u]
    while True:
        sc.fill(COLORS["gr"])
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            switch.handle_event(event)
            if button.handle_event(event):
                progress_bar.set_prog(0)
                prog = 0
            if button2.handle_event(event):
                progress_bar.set_prog(50)
                prog = 50
            inu, ins, ind = inp_u.handle_event(event), inp_s.handle_event(event), inp_d.handle_event(event)
            if inu:
                tex_u.render(inu)
            if ins:
                tex_s.render(ins)
            if ind:
                tex_d.render(ind)
        for i in al_ob:
            i.show()
        if timer.tk():
            prog += st * 2
            prog = 100 if prog > 100 else 0 if prog < 0 else prog
            progress_bar.set_prog(prog)
        st = 1 if switch.get_real_state() else -1

        pg.display.flip()


if __name__ == "__main__":
    start_demo()