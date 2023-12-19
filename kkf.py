import math
import os
import random
import sys
import time
from typing import Any
import pygame as pg

WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


class Koukaton(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 100
        self.speed = 1.0
        self.damage = 0
        
    def setHp(self, hp):
        self.hp = hp
    def getHp(self):
        return self.hp
    
    def setSpeed(self, speed):
        self.speed = speed
    def getSpeed(self):
        return self.speed
    
    def setDamage(self, damage: int):
        self.damage = damage
    def getDamage(self):
        return self.damage
    
class Guard(pg.sprite.Sprite):
    """
    ガードに関するクラス
    """
    def __init__(self,):
        super().__init__()
        self.guard_hp = 5

    def update(self, screen: pg.Surface,  koukaton: Koukaton):
        if self.guard_hp <= 0:  #ガードが不可能な場合
            koukaton.setSpeed(1.0)  #行動不可を解除
        else:
            if koukaton.getDamage() > 0:
                koukaton.setDamage(0)  #ダメージの無効化
                self.guard_hp -= 1  #ガード可能回数を減らす
            koukaton.setSpeed(0.0)  #こうかとんを移動不可にする
            pg.draw.circle(screen, (0, 255, 255), (500,500), 20 * self.guard_hp)  #ガード表示
                   

def main():
    pg.display.set_caption("大戦争スマッシュこうかとんファイターズ")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/pg_bg.jpg")

    tmr = 0
    clock = pg.time.Clock()
    guard = Guard()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        koukaton = Koukaton()
        screen.blit(bg_img, [0, 0])
        #メイン処理
        ###キーボード処理###
        key_lst = pg.key.get_pressed()

        #テスト用
        if key_lst[pg.K_e]:
            if tmr % 50 == 0:
                koukaton.setDamage(100)
        #テスト用終わり
            
        if key_lst[pg.K_q]:
            guard.update(screen, koukaton)
        else:
            guard = Guard()

        print(koukaton.getDamage())

        pg.display.update()
        tmr += 1
        clock.tick(50)
            

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

    
