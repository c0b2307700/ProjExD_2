import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数はこうかとんor爆弾のRect
    戻り値は真理値タプル(横判定結果, 縦判定結果)    docstring
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate 


def gameover(screen):
    """
    引数screen
    黒の透過背景にGameOver
    と出力される関数
    """
    surface = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(surface, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    surface.set_alpha(128)
    screen.blit(surface, [0, 0])
    fonto = pg.font.Font(None, 100)
    txt = fonto.render("GameOver", True, (255, 255, 255))
    screen.blit(txt, [WIDTH/2 -190, HEIGHT/2])
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bd_img = pg.Surface((20, 20))  # 空のSurface
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    # bb_rct.centerX = random.randint(0, WIDTH)
    # bb_rct.centerY = random.randint(0, HEIGHT)  # このように表記できる
    vx, vy = +5, +5  # 爆弾の移動の変化量

    accs = [a for a in range(1, 11)]  # 加速度のリスト

    clock = pg.time.Clock()
    tmr = 0
  
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        
        if kk_rct.colliderect(bd_rct):  # こうかとんと爆弾が重なっていたら collide...が衝突判定をしてくれる
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 横座標, 縦座標の順
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, tpl in DELTA.items():  # 最後の物は辞書のキーと値を取り出すやつ(復習)
            if key_lst[key]:  # key_lstに辞書のキーに合致する場合
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bd_rct.move_ip((vx, vy))
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bd_img, bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()