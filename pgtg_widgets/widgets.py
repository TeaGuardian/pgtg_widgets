import pygame as pg
lim255 = lambda g: 255 if g > 255 else g if g > 0 else 0


class Button:
    def __init__(self, screen: pg.Surface, int_rect, font, color, grad=255, text="", text_color=(0, 0, 0),
                 an_col=None, an_li=0.6):
        x, y, sx, sy = int_rect
        an_col = an_col if an_col is not None else color
        self.plot, self.sc, self.llf, self.grad, self.an_flag = pg.Surface((sx, sy)), screen, False, grad, None
        self.x, self.y, self.sx, self.sy, self.col, self.an_plot = x, y, sx, sy, color[:], pg.Surface((sx, sy))
        self.font, self.text, self.text_c, self.an_li, self.an_col_m = font, text, text_color, an_li, an_col
        self.an_cord, self.an_color, self.an_grad, self.an_time = (0, 0), an_col, 0, pg.time.get_ticks()
        self.render(color)

    def render(self, color):
        """updating Button surface"""
        self.plot.fill([0, 0, 0])
        self.plot.set_alpha(self.grad)
        bor = int(min(self.sx, self.sy) * 0.2)
        pg.draw.rect(self.plot, color, (0, 0, self.sx, self.sy), border_radius=bor)
        pg.draw.rect(self.plot, list(map(lambda g: int(g * 0.6), color)), (0, 0, self.sx, self.sy), 2, border_radius=bor)
        text = self.font.render(self.text, True, self.text_c)
        self.plot.blit(text, text.get_rect(center=self.plot.get_rect().center))
        self.plot.set_colorkey([0, 0, 0])
        if self.an_flag is not None:
            self.an_plot.fill([0, 0, 0])
            self.an_plot.set_alpha(self.an_grad)
            pg.draw.circle(self.an_plot, self.an_color, self.an_cord, self.an_flag)
            self.plot.set_colorkey([0, 0, 0])
            if self.an_flag ** 2 > self.sx ** 2 + self.sy ** 2:
                lf = pg.Rect((self.x, self.y, self.sx, self.sy)).collidepoint(pg.mouse.get_pos())
                self.an_flag, self.llf = None, not lf
            elif self.an_time + 30 < pg.time.get_ticks():
                self.an_time = pg.time.get_ticks()
                self.an_flag += 10
            self.plot.blit(self.an_plot, (0, 0), special_flags=pg.BLEND_RGB_SUB)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.Rect((self.x, self.y, self.sx, self.sy)).collidepoint(event.pos):
                self.task_animation(*event.pos, self.an_col_m, 50)
                return True
        if event.type == pg.MOUSEMOTION:
            lf = pg.Rect((self.x, self.y, self.sx, self.sy)).collidepoint(event.pos)
            if lf and not self.llf:
                self.llf = True
                self.render(list(map(lambda g: int(g * 0.7), self.col)))
            elif self.llf and not lf:
                self.llf = False
                self.render(self.col)
        return False

    def show(self):
        if self.an_flag is not None:
            self.render(self.col)
        self.sc.blit(self.plot, (self.x, self.y))

    def task_animation(self, x, y, color, grad=30):
        color = list(map(lambda g: lim255(int(g * self.an_li)), color))
        self.an_grad, self.an_cord, self.an_color, self.an_flag = grad, (x - self.x, y - self.y), color, 0

    def resize(self, sc, int_rect):
        x, y, sx, sy = int_rect
        self.plot, self.sc = pg.Surface((sx, sy)), sc
        self.x, self.y, self.sx, self.sy, self.an_plot = x, y, sx, sy, pg.Surface((sx, sy))
        self.render(self.col)


class Switch:
    """colors should be RGB, grad should be in range(0, 255)"""
    def __init__(self, sc: pg.Surface, int_rect, col_bor, col_off, col_on, border=4, grad=255, state=False, tick_time=20):
        x, y, sx, sy = int_rect
        self.x, self.y, self.sx, self.sy, self.col_bor, self.moo = x, y, sx, sy, col_bor, False
        self.plot, self.col_off, self.col_on, self.state = pg.Surface((sx, sy)), col_off, col_on, state
        self.bor, self.sc, self.grad, self.tk_k = border, sc, grad, tick_time
        self.rad, self.last_tick = (sy - 4 * self.bor) // 2, pg.time.get_ticks()
        self.ma, self.mi = sx - 2 * self.bor - self.rad, 2 * self.bor + self.rad
        self.step, self.las = (sx - 4 * self.bor) // 10, self.ma if state else self.mi
        self.render()

    def render(self):
        """updating Switch surface"""
        po = self.sy // 2
        self.plot.fill([0, 0, 0])
        self.plot.set_alpha(self.grad)
        if self.moo and pg.time.get_ticks() - self.tk_k > self.last_tick:
            self.last_tick = pg.time.get_ticks()
            self.las += self.step // 2 if self.state else -self.step // 2
            if not self.state and self.las in range(self.mi - self.step, self.mi):
                self.moo, self.las = False, self.mi
            if self.state and self.las in range(self.ma, self.ma + self.step):
                self.moo, self.las = False, self.ma
        pg.draw.rect(self.plot, self.col_off, (0, 0, self.sx, self.sy), border_radius=po)
        pg.draw.rect(self.plot, self.col_on, (0, 0, self.las, self.sy), border_top_left_radius=po, border_bottom_left_radius=po)
        pg.draw.rect(self.plot, self.col_bor, (0, 0, self.sx, self.sy), self.bor, border_radius=po)
        pg.draw.circle(self.plot, self.col_bor, (self.las, self.sy // 2), self.rad)
        self.plot.set_colorkey([0, 0, 0])

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.Rect((self.x, self.y, self.sx, self.sy)).collidepoint(event.pos):
                self.switch()

    def switch(self):
        """switching switch state"""
        self.moo, self.state = True, False if self.state else True

    def set_state(self, state):
        """set switch state"""
        self.moo, self.state = self.state != state, state

    def show(self):
        if self.moo:
            self.render()
        self.sc.blit(self.plot, (self.x, self.y))

    def get_real_state(self):
        """returns real switch state"""
        return self.state if not self.moo else not self.state

    def get_finally_state(self):
        """returns finally switch state"""
        return self.state

    def resize(self, sc, int_rect):
        x, y, sx, sy = int_rect
        self.x, self.y, self.sx, self.sy = x, y, sx, sy
        self.plot, self.sc = pg.Surface((sx, sy)), sc
        self.rad, self.last_tick = (sy - 4 * self.bor) // 2, pg.time.get_ticks()
        self.ma, self.mi = sx - 2 * self.bor - self.rad, 2 * self.bor + self.rad
        self.step, self.las = (sx - 4 * self.bor) // 10, self.ma if self.state else self.mi
        self.render()


class ProgressBar:
    def __init__(self, sc, int_rect, col_bor, col_off, col_on, border=4, grad=255):
        x, y, sx, sy = int_rect
        self.x, self.y, self.sx, self.sy, self.col_bor = x, y, sx, sy, col_bor
        self.plot, self.col_off, self.col_on = pg.Surface((sx, sy)), col_off, col_on
        self.bor, self.sc, self.grad = border, sc, grad
        self.ma, self.mi = sx - self.bor, 4 * self.bor
        self.step, self.las = (self.ma - self.mi) / 100, 0
        self.render()

    def render(self):
        po, now = self.sy // 10, int(self.mi + self.step * self.las)
        self.plot.fill([0, 0, 0])
        self.plot.set_alpha(self.grad)
        pg.draw.rect(self.plot, self.col_off, (0, 0, self.sx, self.sy), border_radius=po)
        pg.draw.rect(self.plot, self.col_on, (0, 0, now, self.sy), border_radius=po)
        pg.draw.rect(self.plot, self.col_bor, (0, 0, self.sx, self.sy), self.bor, border_radius=po)
        self.plot.set_colorkey([0, 0, 0])

    def show(self):
        self.sc.blit(self.plot, (self.x, self.y))

    def set_prog(self, per):
        if per > 0 and per <= 100:
            self.las = per
            self.render()

    def add_prog(self, per):
        if per > 0 and self.las + per <= 100:
            self.las += per
            self.render()

    def resize(self, sc, int_rect):
        x, y, sx, sy = int_rect
        self.x, self.y, self.sx, self.sy = x, y, sx, sy
        self.plot, self.sc = pg.Surface((sx, sy)), sc
        self.ma, self.mi = sx - self.bor, 4 * self.bor
        self.step, self.las = (self.ma - self.mi) / 100, 0
        self.render()


class InputBox:
    def __init__(self, sc, int_rect, font, inac_col=(0, 0, 0), ac_col=(0, 0, 0), text='', sub_moo=1):
        x, y, w, h = int_rect
        self.h, self.w, self.x, self.y, self.cur_t, self.cur_s = h, w, x, y, pg.time.get_ticks(), False
        self.color, self.lines, self.plot, self.font = inac_col, [""], pg.Surface((w, h)), font
        self.text, self.hs, self.ls, self.smb = text, font.size("A")[1], font.size("Щ")[0], sub_moo
        self.active, self.cur, self.sc, self.cin, self.cac = False, 0, sc, inac_col, ac_col
        self.lines = self.split_text(text, font)

    def split_text(self, text, font):
        lsmax = self.w - font.size("Щ")[0]
        trf, lp, ste = lsmax / 1.2, 0, 0
        if lsmax < 8:
            print("too small")
        rez, line = [], ""
        for si in text:
            if si == " " and ste == 0:
                continue
            if si == " ":
                lp = ste
            if font.size(line)[0] >= lsmax:
                if ste - lp > trf or ste - lp == 0:
                    rez.append(line)
                    line, ste, lp = "", -1, 0
                else:
                    if lp == 0:
                        lp = len(line)
                    rez.append(line[:lp])
                    line += si
                    line, ste, lp = line[lp:], len(line[lp + 1:]) - 1, 0
            else:
                line += si
            ste += 1
        if line:
            rez.append(line)
        return rez if len(rez) else [""]

    def handle_event(self, event):
        rez = ""
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.Rect((self.x, self.y, self.w, self.h)).collidepoint(event.pos):
                self.active = not self.active
                self.cur = len(self.text)
            else:
                self.active = False
            self.color = self.cac if self.active else self.cin
        if event.type == pg.KEYDOWN:
            if self.active:
                n = self.cur
                if event.key == pg.K_RETURN and len(self.text):
                    rez = self.text
                    self.text, self.lines, self.cur = '', [""], 0
                elif event.key == pg.K_BACKSPACE and len(self.text):
                    self.text = self.text[:n - 1] + self.text[n:]
                    self.cur -= 1
                    self.lines = self.split_text(self.text, self.font)
                elif event.key == pg.K_LEFT and self.cur > 0:
                    self.cur -= 1
                elif event.key == pg.K_RIGHT and self.cur < len(self.text):
                    self.cur += 1
                else:
                    self.text = self.text[:n] + event.unicode + self.text[n:]
                    if len(event.unicode):
                        self.cur += 1
                    self.lines = self.split_text(self.text, self.font)
                le_li = len(self.lines)
                if self.smb == -1:
                    if (self.hs + 2) * le_li > self.h and self.y - (self.hs + 2) * le_li > 0:
                        while (self.hs + 2) * le_li > self.h and self.y - (self.hs + 2) * le_li > 0:
                            self.y -= (self.hs + 2)
                            self.h += (self.hs + 2)
                        self.plot = pg.Surface((self.w, self.h))
                    elif (self.hs + 2) * (le_li + 1) < self.h and le_li:
                        while (self.hs + 2) * (le_li + 1) < self.h and le_li:
                            self.y += (self.hs + 2)
                            self.h -= (self.hs + 2)
                        self.plot = pg.Surface((self.w, self.h))
                elif self.smb == 1:
                    if (self.hs + 2) * le_li > self.h:
                        while (self.hs + 2) * le_li > self.h:
                            self.h += (self.hs + 2)
                        self.plot = pg.Surface((self.w, self.h))
                    elif (self.hs + 2) * (le_li + 1) < self.h and le_li:
                        while (self.hs + 2) * (le_li + 1) < self.h and le_li:
                            self.h -= (self.hs + 2)
                        self.plot = pg.Surface((self.w, self.h))
        if self.y - (self.hs + 2) * len(self.lines) <= 0:
            yc, yd = int((self.find_cur()[1] - 2) / (self.hs + 2)), int(self.h / (self.hs + 2))
            sp, ep = yc - yd + yd // 2, yc + yd // 2
            lines = self.lines[sp if sp > 0 else 0:ep if ep < len(self.lines) else None]
        else:
            lines = self.lines
        self.plot.fill((0, 0, 0))
        self.plot.set_colorkey((0, 0, 0))
        for i, s in enumerate(lines):
            self.plot.blit(self.font.render(s, True, self.color), (2 + self.ls // 4, self.hs // 2 + (self.hs + 2) * i))
        pg.draw.rect(self.plot, self.color, (0, 0, self.w, self.h - 4), 2)
        return rez

    def find_cur(self):
        y, pp = 0, 0
        for i in self.lines:
            if self.cur > pp + len(i) + 1:
                y += 1
                pp += len(i)
        return self.font.size(self.lines[y][:self.cur - pp])[0], 2 + (self.hs + 2) * y

    def show(self):
        self.sc.blit(self.plot, (self.x, self.y))
        if self.active:
            if self.cur_t + 600 < pg.time.get_ticks():
                self.cur_t, self.cur_s = pg.time.get_ticks(), not self.cur_s
            if self.cur_s:
                dx, dy = self.find_cur()
                x, y = 2 + self.ls // 4 + self.x + dx, 2 + self.y + dy
                if self.y - (self.hs + 2) * len(self.lines) <= 0:
                    p = int(self.h / (self.hs + 2)) - int(self.h / (self.hs + 2)) // 2
                    y = 4 + self.y + p * (self.hs + 2)
                pg.draw.rect(self.sc, self.color, (x, y + self.hs // 2 - 2, 2, self.hs - 6))

    def resize(self, sc, int_rect):
        self.x, self.y, self.w, self.h = int_rect
        self.plot, self.sc = pg.Surface((self.w, self.h)), sc


class TextBox:
    def __init__(self, sc, int_rect, font, col=(0, 0, 0), text='', sub_moo=1):
        self.x, self.y, self.w, self.h = int_rect
        self.color, self.plot, self.font, self.smb = col, pg.Surface((self.w, self.h)), font, sub_moo
        self.text, self.hs, self.ls = text, font.size("A")[1], font.size("Щ")[0]
        self.sc = sc
        self.render(text)

    def split_text(self, text, font):
        lsmax = self.w - font.size("Щ")[0]
        trf, lp, ste = lsmax / 1.2, 0, 0
        if lsmax < 8:
            print("too small")
        rez, line = [], ""
        for si in text:
            if si == " " and ste == 0:
                continue
            if si == " ":
                lp = ste
            if font.size(line)[0] >= lsmax:
                if ste - lp > trf or ste - lp == 0:
                    rez.append(line)
                    line, ste, lp = "", -1, 0
                else:
                    if lp == 0:
                        lp = len(line)
                    rez.append(line[:lp])
                    line += si
                    line, ste, lp = line[lp:], len(line[lp + 1:]) - 1, 0
            else:
                line += si
            ste += 1
        if line:
            rez.append(line)
        return rez if len(rez) else [""]

    def render(self, text):
        self.text = text
        lines = self.split_text(self.text, self.font)
        le_li = len(lines)
        if self.smb == -1:
            if (self.hs + 2) * le_li > self.h and self.y - (self.hs + 2) * le_li > 0:
                while (self.hs + 2) * le_li > self.h and self.y - (self.hs + 2) * le_li > 0:
                    self.y -= (self.hs + 2)
                    self.h += (self.hs + 2)
                self.plot = pg.Surface((self.w, self.h))
            elif (self.hs + 2) * (le_li + 1) < self.h and le_li:
                while (self.hs + 2) * (le_li + 1) < self.h and le_li:
                    self.y += (self.hs + 2)
                    self.h -= (self.hs + 2)
                self.plot = pg.Surface((self.w, self.h))
        elif self.smb == 1:
            if (self.hs + 2) * le_li > self.h:
                while (self.hs + 2) * le_li > self.h:
                    self.h += (self.hs + 2)
                self.plot = pg.Surface((self.w, self.h))
            elif (self.hs + 2) * (le_li + 1) < self.h and le_li:
                while (self.hs + 2) * (le_li + 1) < self.h and le_li:
                    self.h -= (self.hs + 2)
                self.plot = pg.Surface((self.w, self.h))
        self.plot.fill((0, 0, 0))
        self.plot.set_colorkey((0, 0, 0))
        for i, s in enumerate(lines):
            self.plot.blit(self.font.render(s.lstrip(" "), True, self.color), (2 + self.ls // 4, self.hs // 2 + (self.hs + 2) * i))
        pg.draw.rect(self.plot, self.color, (0, 0, self.w, self.h - 4), 2)

    def show(self):
        self.sc.blit(self.plot, (self.x, self.y))

    def resize(self, sc, int_rect):
        self.x, self.y, self.w, self.h = int_rect
        self.plot, self.sc = pg.Surface((self.w, self.h)), sc
        self.render(self.text)
