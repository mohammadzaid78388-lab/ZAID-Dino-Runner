__version__ = "1.0.0"

import random
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Triangle, Line
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex


class DinoGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.best = 0
        self.speed = 320
        self.dino_x = 0
        self.dino_y = 0
        self.dino_w = 48
        self.dino_h = 54
        self.jump_v = 0
        self.jumping = False
        self.cactus_x = 0
        self.cactus_w = 28
        self.cactus_h = 58
        self.game_over = False
        self.started = False
        self.clouds = [[0.18, 0.78], [0.58, 0.88], [0.86, 0.70]]

        self.title = Label(text="ZAID", bold=True, font_size="30sp",
                           color=get_color_from_hex("#17324D"),
                           size_hint=(None, None))
        self.score_label = Label(text="SCORE  0     BEST  0", bold=True,
                                 font_size="16sp",
                                 color=get_color_from_hex("#17324D"),
                                 size_hint=(None, None))
        self.message = Label(text="TAP TO START", bold=True, font_size="22sp",
                             color=get_color_from_hex("#17324D"),
                             halign="center", size_hint=(None, None))
        self.add_widget(self.title)
        self.add_widget(self.score_label)
        self.add_widget(self.message)

        self.bind(size=self.layout_game, pos=self.layout_game)
        Clock.schedule_interval(self.update, 1 / 60)

    def layout_game(self, *args):
        w, h = self.width, self.height
        self.title.size = (w, 55)
        self.title.pos = (self.x, self.y + h - 62)
        self.score_label.size = (w, 35)
        self.score_label.pos = (self.x, self.y + h - 100)
        self.message.size = (w * .9, 70)
        self.message.pos = (self.x + w * .05, self.y + h * .43)

        self.ground_y = self.y + h * .20
        self.dino_x = self.x + w * .16
        if not self.started:
            self.dino_y = self.ground_y
        self.dino_w = max(38, w * .075)
        self.dino_h = max(44, h * .17)
        self.cactus_w = max(22, w * .045)
        self.cactus_h = max(48, h * .18)
        if self.cactus_x == 0:
            self.cactus_x = self.x + w * .92
        self.draw_scene()

    def start_or_jump(self):
        if self.game_over:
            self.reset()
            self.started = True
            self.jump()
        elif not self.started:
            self.started = True
            self.message.text = ""
            self.jump()
        else:
            self.jump()

    def jump(self):
        if not self.jumping and self.started and not self.game_over:
            self.jump_v = self.height * 0.95
            self.jumping = True

    def reset(self):
        self.score = 0
        self.speed = 320
        self.cactus_x = self.x + self.width * .95
        self.dino_y = self.ground_y
        self.jump_v = 0
        self.jumping = False
        self.game_over = False
        self.message.text = ""

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.start_or_jump()
            return True
        return super().on_touch_down(touch)

    def on_key_down(self, window, key, *args):
        # Space bar support when running on a computer
        if key == 32:
            self.start_or_jump()
            return True
        return False

    def update(self, dt):
        if not self.width or not self.height:
            return
        dt = min(dt, 1 / 30)

        if self.started and not self.game_over:
            if self.jumping:
                self.dino_y += self.jump_v * dt
                self.jump_v -= self.height * 2.6 * dt
                if self.dino_y <= self.ground_y:
                    self.dino_y = self.ground_y
                    self.jumping = False
                    self.jump_v = 0

            self.cactus_x -= self.speed * dt
            if self.cactus_x + self.cactus_w < self.x:
                self.cactus_x = self.x + self.width * random.uniform(1.0, 1.35)
                self.score += 1
                self.best = max(self.best, self.score)
                self.speed = min(560, self.speed + 12)

            # Simple, forgiving rectangle collision
            dino_box = (self.dino_x + 8, self.dino_y + 5,
                        self.dino_w - 13, self.dino_h - 8)
            cactus_box = (self.cactus_x + 4, self.ground_y + 4,
                          self.cactus_w - 8, self.cactus_h - 4)
            if self.overlap(dino_box, cactus_box):
                self.game_over = True
                self.best = max(self.best, self.score)
                self.message.text = "GAME OVER\nTAP TO PLAY AGAIN"

        for cloud in self.clouds:
            cloud[0] -= dt * .035
            if cloud[0] < -.12:
                cloud[0] = 1.08

        self.score_label.text = f"SCORE  {self.score}     BEST  {self.best}"
        self.draw_scene()

    @staticmethod
    def overlap(a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

    def draw_cloud(self, x, y, scale):
        with self.canvas:
            Color(1, 1, 1, 0.92)
            Ellipse(pos=(x, y, 34*scale, 20*scale))
            Ellipse(pos=(x+15*scale, y+7*scale, 34*scale, 25*scale))
            Ellipse(pos=(x+34*scale, y, 34*scale, 20*scale))

    def draw_scene(self):
        if self.width <= 0 or self.height <= 0:
            return
        self.canvas.clear()
        w, h = self.width, self.height
        with self.canvas:
            # Sky
            Color(*get_color_from_hex("#BFE9FF"))
            Rectangle(pos=self.pos, size=self.size)

            # Sun
            Color(*get_color_from_hex("#FFD166"))
            Ellipse(pos=(self.x+w*.79, self.y+h*.68), size=(h*.14, h*.14))

            # Distant hills
            Color(*get_color_from_hex("#9BCB9B"))
            Triangle(points=[self.x, self.ground_y,
                             self.x+w*.20, self.y+h*.55,
                             self.x+w*.42, self.ground_y])
            Triangle(points=[self.x+w*.28, self.ground_y,
                             self.x+w*.58, self.y+h*.50,
                             self.x+w*.88, self.ground_y])

            # Clouds
            for cx, cy in self.clouds:
                px = self.x + cx*w
                py = self.y + cy*h
                Color(1, 1, 1, .95)
                Ellipse(pos=(px, py, 34, 20))
                Ellipse(pos=(px+15, py+7, 34, 25))
                Ellipse(pos=(px+34, py, 34, 20))

            # Ground and dashed track
            Color(*get_color_from_hex("#E7C58B"))
            Rectangle(pos=(self.x, self.y), size=(w, self.ground_y-self.y))
            Color(*get_color_from_hex("#9A7047"))
            Line(points=[self.x, self.ground_y, self.x+w, self.ground_y], width=2)
            for i in range(8):
                dx = (i * w/7 + (self.score * 13) % (w/7)) % w
                Line(points=[self.x+dx, self.ground_y-12,
                             self.x+dx+12, self.ground_y-12], width=1.2)

            # Dinosaur body and head
            Color(*get_color_from_hex("#287A4B"))
            RoundedRectangle(pos=(self.dino_x, self.dino_y+5),
                             size=(self.dino_w*.76, self.dino_h*.68),
                             radius=[8])
            RoundedRectangle(pos=(self.dino_x+self.dino_w*.43,
                                  self.dino_y+self.dino_h*.48),
                             size=(self.dino_w*.68, self.dino_h*.48),
                             radius=[8])
            # Tail
            Triangle(points=[self.dino_x+3, self.dino_y+25,
                             self.dino_x-13, self.dino_y+17,
                             self.dino_x+4, self.dino_y+12])
            # Eye
            Color(1, 1, 1)
            Ellipse(pos=(self.dino_x+self.dino_w*.91,
                         self.dino_y+self.dino_h*.77), size=(6, 6))
            Color(*get_color_from_hex("#17324D"))
            Ellipse(pos=(self.dino_x+self.dino_w*.94,
                         self.dino_y+self.dino_h*.79), size=(2.5, 2.5))
            # Legs
            Color(*get_color_from_hex("#174D35"))
            Rectangle(pos=(self.dino_x+8, self.dino_y), size=(8, 13))
            Rectangle(pos=(self.dino_x+27, self.dino_y), size=(8, 13))

            # Cactus
            cx, cy = self.cactus_x, self.ground_y
            Color(*get_color_from_hex("#25834A"))
            RoundedRectangle(pos=(cx+self.cactus_w*.35, cy),
                             size=(self.cactus_w*.38, self.cactus_h),
                             radius=[5])
            RoundedRectangle(pos=(cx, cy+self.cactus_h*.40),
                             size=(self.cactus_w*.43, self.cactus_h*.16),
                             radius=[4])
            RoundedRectangle(pos=(cx, cy+self.cactus_h*.40),
                             size=(self.cactus_w*.20, self.cactus_h*.43),
                             radius=[4])
            RoundedRectangle(pos=(cx+self.cactus_w*.65,
                                  cy+self.cactus_h*.22),
                             size=(self.cactus_w*.40, self.cactus_h*.16),
                             radius=[4])
            RoundedRectangle(pos=(cx+self.cactus_w*.82,
                                  cy+self.cactus_h*.22),
                             size=(self.cactus_w*.20, self.cactus_h*.38),
                             radius=[4])


class ZaidDinoApp(App):
    def build(self):
        self.title = "ZAID Dino Runner"
        Window.clearcolor = (0.75, 0.91, 1, 1)
        game = DinoGame()
        Window.bind(on_key_down=game.on_key_down)
        return game


if __name__ == "__main__":
    ZaidDinoApp().run()
