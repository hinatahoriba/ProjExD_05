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

def draw_start_screen(screen, font, text, color):
        text_render = font.render(text, True, color)
        text_rect = text_render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_render, text_rect)

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
            


class start:
    """
    勝利条件に関するクラス
    """
    def __init__(self, koukaton):
        self.koukaton = koukaton
        self.timer = 60  # 初期時間
        self.reset_timer = 10  # リセットまでの時間について
        self.round = 5  # ラウンド回数について
        self.reset()

    def reset(self):
        """
        勝利条件をリセットする
        """
        self.timer = 60
        self.koukaton.hp = 100
        self.allow_input = True
        self.round -= 1
        if self.round <= 0:
            self.allow_input = False
            
    def update(self, dt):
        """
        勝利条件の更新
        """
        # 設定した時間かこうかとんのhpが0になったときに勝利
        self.timer == dt
        if self.koukaton.hp <= 0:
            self.allow_input = False
            if self.reset_timer <= 0:
                self.reset()
            else:
                self.reset_timer -= dt


def main():
    pg.display.set_caption("大戦争スマッシュこうかとんファイターズ")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/pg_bg.jpg")
    koukaton = Koukaton(3, (100, 400))
    attacks = pg.sprite.Group()
    tmr = 0
    clock = pg.time.Clock()
    pg.init()
    #koukaton = Koukaton() # クラスからオブジェクト生成
    vict_condition = start(koukaton)
    hyper_font = pg.font.Font(None, 50)  # 残り時間用のフォント
    hyper_color = (0, 0, 255)  # 残り時間の表示色
    fonto = pg.font.Font(None, 200)  # ゲームオーバーの文字を生成
    txt = fonto.render("Time UP", True, (255, 0, 0))
    start_screen_font = pg.font.Font(None, 200)
    start_screen_color = (200, 50, 100)  # 紫色の文字
    lnvalid_screen_color = (255, 0, 0)  # 赤色の文字)
    
    # スタート画面についての部分
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        keys = pg.key.get_pressed()

        if keys[pg.K_1]: # 「１」を押すとメインコード部分が読み込み開始
            draw_start_screen(screen, start_screen_font, "Game start", start_screen_color)
            pg.display.flip()
            pg.time.delay(2000)  # 表示を少し待つ
            break
        else: # 「１」が押されるまでの画面表示
            draw_start_screen(screen, start_screen_font, "Are you ready?", lnvalid_screen_color)
            pg.display.flip()
    tmr = 0
    clock.tick(50)
    # ここまでがスタート画面です。

    # メインコード部分
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                attacks.add(Attack(koukaton))  #通常のビーム

        screen.blit(bg_img, [0, 0])
        #メイン処理
        
        attacks.update()
        attacks.draw(screen)

        
        tmr += 1
        clock.tick(50)

        dt = 10 - tmr/50 # ゲームの経過時間を計算

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()


        # キー入力の処理 HPが減るかの確認用
        keys = pg.key.get_pressed() # キーボードの状態をゲットする
        
        if dt >= 0: # 時間が0になるまでの時間を右下に表示
            hyper_text = hyper_font.render(f"Time: {int(dt)}", True, hyper_color)
            hyper_pos = (WIDTH - hyper_text.get_width() - 10, HEIGHT - hyper_text.get_height() - 10)
            screen.blit(hyper_text, hyper_pos)  # 残り時間を表示
        elif dt <= 0: # 時間が0になった時に「Time UP」と表示
            txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(txt, txt_rect)  # Time UPを画面中央に表示
            pg.display.update()
            pg.time.delay(2000)
            return
        if koukaton.getHp() <= 0:
            txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            draw_start_screen(screen, start_screen_font, "Finish!!!", lnvalid_screen_color)  # Finissh!!!を画面中央に表示
            pg.display.update()
            pg.time.delay(2000)
            return   
        
        # 勝利条件の更新
        vict_condition.update(dt)

        # 画面の描画
        pg.display.flip()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

    
