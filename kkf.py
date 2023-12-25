import math
import os
import random
import sys
import time
import pygame as pg


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


class Koukaton(pg.sprite.Sprite):
    def __init__(self):
        self.hp = 100
        self.speed = 1.0
        self.damege = 0
        
    def setHp(self, hp):
        self.hp = hp

    def getHp(self):
        return self.hp
    
    def setSpeed(self, speed):
        self.speed = speed

    def getSpeed(self):
        return self.speed
    
    def update(self):
        pass

class Status(pg.sprite.Sprite):
    """
    体力、必殺技のゲージ表示
    引数: 体力バーのx座標, 体力バーの減る方向
    """
    def __init__(self, x, bar_type):
        super().__init__()
        self.x = x
        self.w, self.h = 700, 40
        self.barx, self.bary = 700, 40
        self.bar_down = bar_type
        self.image = pg.Surface((self.w, self.h))
        self.image.set_colorkey((255, 255, 255))
        self.rect = pg.draw.rect(self.image, (0, 0, 0), (0, 0, self.w, self.h))
        self.damage = pg.draw.rect(self.image, (255, 0, 0), (2, 2, self.w-4, self.h-4))
        self.bar = pg.draw.rect(self.image, (0, 255, 0), (2, 2, self.barx-4, self.bary-4))
        self.rect.center = (self.x, 20)
        self.bar.center = self.rect.center
        self.damage.center = self.rect.center

    # hpバーの更新
    def update(self, hp):
        self.barx += hp
        self.rect = pg.draw.rect(self.image, (0, 0, 0), (0, 0, self.w, self.h))
        self.damage = pg.draw.rect(self.image, (255, 0, 0), (2, 2, self.w-4, self.h-4))
        self.bar = pg.draw.rect(self.image, (0, 255, 0), (2+(700-self.barx), 2, self.barx-4, self.bary-4))
        self.rect.center = (self.x, 20)
        self.bar.center = self.rect.center
        self.damage.center = self.rect.center


def main():
    pg.display.set_caption("大戦争スマッシュこうかとんファイターズ")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/pg_bg.jpg")

    tmr = 0
    clock = pg.time.Clock()

    statuses = pg.sprite.Group()
    statuses.add(Status(350, 1))
    statuses.add(Status(WIDTH-350, -1))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                print("retrun")
                statuses.update(-10)

        screen.blit(bg_img, [0, 0])
        #メイン処理

        statuses.draw(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)
            

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

    
