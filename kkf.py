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

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト（爆弾，こうかとん，ビーム）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

class Koukaton(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    def __init__(self, num: int, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/{num}.png"), 0, 2.0)
        img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん
        self.imgs = {
            (+1, 0): img,  # 右
            (-1, 0): img0,  # 左
        }
        self.dire = (+1, 0)
        self.image = self.imgs[self.dire]
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.hyper_key_pressed_last_frame = False
        self.hp = 100
        self.speed = 1.0
        
    def setHp(self, hp):
        self.hp = hp
    def getHp(self):
        return self.hp
    
    def setSpeed(self, speed):
        self.speed = speed
    def getSpeed(self):
        return self.speed
    
    
class Attack(pg.sprite.Sprite):  #追加機能
    """
    攻撃に関するクラス
    """
    def __init__(self, Koukaton: Koukaton):
        """
        パンチ画像Surfaceを生成する
        引数 bird：パンチを放つこうかとん
        """
        super().__init__()
        self.vx, self.vy = Koukaton.dire
        angle = math.degrees(math.atan2(-self.vy, self.vx))
        self.image = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/beam.png"), angle, 4.0)
        self.vx = math.cos(math.radians(angle))
        self.vy = -math.sin(math.radians(angle))
        self.rect = self.image.get_rect()
        self.rect.centery = Koukaton.rect.centery+Koukaton.rect.height*self.vy
        self.rect.centerx = Koukaton.rect.centerx+Koukaton.rect.width*self.vx #パンチの出る位置
        self.speed = 30 #パンチのスピード
        self.punch_distance = Koukaton.rect.centerx + self.speed*self.vx*6  #パンチの飛距離

    def update(self):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(+self.speed*self.vx, +self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()
        if  self.punch_distance < self.rect.centerx: #パンチの距離を超えると消滅する
            self.kill()
            

def main():
    pg.display.set_caption("大戦争スマッシュこうかとんファイターズ")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/pg_bg.jpg")
    koukaton = Koukaton(3, (100, 400))
    attacks = pg.sprite.Group()
    tmr = 0
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                attacks.add(Attack(koukaton))  #通常のビーム

        screen.blit(bg_img, [0, 0])
        #メイン処理
        
        attacks.update()
        attacks.draw(screen)

        pg.display.update()
        tmr += 1
        clock.tick(50)
            

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

    
