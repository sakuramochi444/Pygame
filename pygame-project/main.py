import pygame as pg
import data as d
import stage as s

def main():
    chip_s = 64
    map_s = pg.Vector2(15, 10)

    pg.init()
    pg.display.set_caption("白黒パズル")
    screen = pg.display.set_mode((chip_s * map_s.x, chip_s * map_s.y))
    clock = pg.time.Clock()
    font = pg.font.Font(None, 60)  # 大きなフォントサイズ
    small_font = pg.font.Font(None, 30)  # 小さなフォントサイズ
    exit_code = '000'

    stage0 = s.Stage0(chip_s)
    stage1 = s.Stage1(chip_s)
    stage2 = s.Stage2(chip_s)
    stage3 = s.Stage3(chip_s)
    stage = stage0
    chara_p, chara_s, chara_imgs, m_vec = d.chara()
    chara_d = 0

    if chara_p is None:
        print("キャラクター画像のロードに失敗しました。プログラムを終了します。")
        pg.quit()
        return '002'

    exit_flag = False

    while not exit_flag:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_flag = True
                exit_code = '001'
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    stage = stage1  # ステージ1に移行

        screen.fill(pg.Color('WHITE'))

        # スタート画面の描画
        title_surface = font.render("白黒パズル", True, 'BLACK')
        title_rect = title_surface.get_rect(center=(chip_s * map_s.x // 2, chip_s * map_s.y // 2 - 20))
        screen.blit(title_surface, title_rect)

        instruction_surface = small_font.render("SPACEキーを押してスタート！", True, 'BLACK')
        instruction_rect = instruction_surface.get_rect(center=(chip_s * map_s.x // 2, chip_s * map_s.y // 2 + 20))
        screen.blit(instruction_surface, instruction_rect)

        pg.display.update()
        clock.tick(30)

    pg.quit()
    return exit_code

if __name__ == "__main__":
    code = main()
    print(f'プログラムを「コード{code}」で終了しました。')