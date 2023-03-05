import pygame as pg


class Button:
    def __init__(self, screen: pg.Surface, x: int, y: int, sx: int, sy:int, color, grad=255, text="", font=20, text_color=[0, 0, 0]):
        self.plot, self.sc, self.llf, self.grad, self.an_flag = pg.Surface((sx, sy)), screen, False, grad, None
        self.x, self.y, self.sx, self.sy, self.col, self.an_plot = x, y, sx, sy, color[:], pg.Surface((sx, sy))
        self.font, self.text, self.text_c, self.pg = pg.font.SysFont(None, font), text, text_color, pg
        self.an_cord, self.an_color, self.an_grad, self.an_time = (0, 0), [0, 0, 0], 0, pg.time.get_ticks()
        self.render(color)

    def render(self, color):
        """updating Button surface"""
        self.plot.fill([0, 0, 0])
        self.plot.set_alpha(self.grad)
        bor = int(min(self.sx, self.sy) * 0.2)
        self.pg.draw.rect(self.plot, color, (0, 0, self.sx, self.sy), border_radius=bor)
        self.pg.draw.rect(self.plot, list(map(lambda g: int(g * 0.6), color)),
                          (0, 0, self.sx, self.sy), 2, border_radius=bor)
        text = self.font.render(self.text, True, self.text_c)
        self.plot.blit(text, text.get_rect(center=self.plot.get_rect().center))
        self.plot.set_colorkey([0, 0, 0])
        if self.an_flag is not None:
            self.an_plot.fill([0, 0, 0])
            self.an_plot.set_alpha(self.an_grad)
            pg.draw.circle(self.an_plot, self.an_color, self.an_cord, self.an_flag)
            self.plot.set_colorkey([0, 0, 0])
            if self.an_flag ** 2 > self.sx ** 2 + self.sy ** 2:
                x, y = pg.mouse.get_pos()
                lf = x in range(self.x, self.x + self.sx) and y in range(self.y, self.y + self.sy)
                self.an_flag, self.llf = None, not lf
            elif self.an_time + 3 < pg.time.get_ticks():
                self.an_time = pg.time.get_ticks()
                self.an_flag += 3
            self.plot.blit(self.an_plot, (0, 0), special_flags=pg.BLEND_RGB_SUB)

    def show(self, x, y):
        lf = x in range(self.x, self.x + self.sx) and y in range(self.y, self.y + self.sy)
        if lf and not self.llf:
            self.llf = True
            self.render(list(map(lambda g: int(g * 0.7), self.col)))
        elif self.llf and not lf:
            self.llf = False
            self.render(self.col)
        elif self.an_flag is not None:
            self.render(self.col)
        self.sc.blit(self.plot, (self.x, self.y))
        return lf

    def task_animation(self, x, y, color, grad=30):
        self.an_grad, self.an_cord, self.an_color, self.an_flag = grad, (x - self.x, y - self.y), color, 0


class Switch:
    """colors should be RGB, grad should be in range(0, 255)"""
    def __init__(self, sc: pg.Surface, x: int, y: int, sx: int, sy: int, col_bor, col_off, col_on, border=4, grad=255, state=False):
        self.x, self.y, self.sx, self.sy, self.col_bor, self.moo = x, y, sx, sy, col_bor, False
        self.plot, self.col_off, self.col_on, self.state = pg.Surface((sx, sy)), col_off, col_on, state
        self.bor, self.sc, self.grad, self.pg = border, sc, grad, pg
        self.rad, self.last_tick = (sy - 4 * self.bor) // 2, pg.time.get_ticks()
        self.ma, self.mi = sx - 2 * self.bor - self.rad, 2 * self.bor + self.rad
        self.step, self.las = (sx - 4 * self.bor) // 10, self.ma if state else self.mi
        self.render()

    def render(self):
        """updating Switch surface"""
        po = self.sy // 2
        self.plot.fill([0, 0, 0])
        self.plot.set_alpha(self.grad)
        if self.moo and self.pg.time.get_ticks() - 20 > self.last_tick:
            self.last_tick = self.pg.time.get_ticks()
            self.las += self.step // 2 if self.state else -self.step // 2
            if not self.state and self.las in range(self.mi - self.step, self.mi):
                self.moo, self.las = False, self.mi
            if self.state and self.las in range(self.ma, self.ma + self.step):
                self.moo, self.las = False, self.ma
        self.pg.draw.rect(self.plot, self.col_off, (0, 0, self.sx, self.sy), border_radius=po)
        self.pg.draw.rect(self.plot, self.col_on, (0, 0, self.las, self.sy), border_top_left_radius=po, border_bottom_left_radius=po)
        self.pg.draw.rect(self.plot, self.col_bor, (0, 0, self.sx, self.sy), self.bor, border_radius=po)
        self.pg.draw.circle(self.plot, self.col_bor, (self.las, self.sy // 2), self.rad)
        self.plot.set_colorkey([0, 0, 0])

    def switch(self):
        """switching switch state"""
        self.moo, self.state = True, False if self.state else True

    def set_state(self, state):
        """set switch state"""
        self.moo, self.state = self.state != state, state

    def show(self, x, y):
        if self.moo:
            self.render()
        """((x - self.las) ** 2 + (y - self.sy // 2) ** 2) <= self.rad ** 2"""
        lf = x in range(self.x, self.x + self.sx) and y in range(self.y, self.y + self.sy)
        self.sc.blit(self.plot, (self.x, self.y))
        return lf

    def get_real_state(self):
        """returns real switch state"""
        return self.state if not self.moo else not self.state

    def get_finally_state(self):
        """returns finally switch state"""
        return self.state


class ProgressBar:
    def __init__(self, sc, x, y, sx, sy, col_bor, col_off, col_on, border=4, grad=255):
        self.x, self.y, self.sx, self.sy, self.col_bor = x, y, sx, sy, col_bor
        self.plot, self.col_off, self.col_on = pg.Surface((sx, sy)), col_off, col_on
        self.bor, self.sc, self.grad, self.pg = border, sc, grad, pg
        self.ma, self.mi = sx - self.bor, 4 * self.bor
        self.step, self.las = (self.ma - self.mi) / 100, 0
        self.render()

    def render(self):
        po, now = self.sy // 10, int(self.mi + self.step * self.las)
        self.plot.fill([0, 0, 0])
        self.plot.set_alpha(self.grad)
        self.pg.draw.rect(self.plot, self.col_off, (0, 0, self.sx, self.sy), border_radius=po)
        self.pg.draw.rect(self.plot, self.col_on, (0, 0, now, self.sy), border_radius=po)
        self.pg.draw.rect(self.plot, self.col_bor, (0, 0, self.sx, self.sy), self.bor, border_radius=po)
        self.plot.set_colorkey([0, 0, 0])

    def show(self, x, y):
        lf = x in range(self.x, self.x + self.sx) and y in range(self.y, self.y + self.sy)
        self.sc.blit(self.plot, (self.x, self.y))
        return lf

    def set_prog(self, per):
        if per > 0 and per <= 100:
            self.las = per
            self.render()

    def add_prog(self, per):
        if per > 0 and self.las + per <= 100:
            self.las += per
            self.render()