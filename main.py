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
    font = pg.font.Font(None, 15)
    exit_code = '000'

    stage1 = s.Stage1(chip_s)
    stage2 = s.Stage2(chip_s)
    stage = stage1
    chara_p, chara_s, chara_imgs, m_vec = d.chara()
    chara_d = 0

    if chara_p is None:
        print("キャラクター画像のロードに失敗しました。プログラムを終了します。")
        pg.quit()
        return '002'

    direction_map = {0: "up", 1: "right", 2: "down", 3: "left"}
    exit_flag = False

    def handle_move(cmd_move):
        nonlocal chara_p, chara_d, stage
        if cmd_move != -1:
            af_pos = chara_p + m_vec[cmd_move]
            # ステージによって移動条件を変更
            if stage == stage1:
                if stage1.block_pos == af_pos and stage1.move_block(chara_p.x, chara_p.y, m_vec[cmd_move]):
                    chara_p += m_vec[cmd_move]
                elif d.is_walkable(stage1.map_data, int(af_pos.x), int(af_pos.y)):
                    chara_p += m_vec[cmd_move]
                chara_d = cmd_move
            elif stage == stage2:
                if d.is_walkable(stage2.map_data, int(af_pos.x), int(af_pos.y)):
                    chara_p += m_vec[cmd_move]
                chara_d = cmd_move

                # change_tileに移動したときに反転効果を有効化
                if af_pos == stage2.change_tile:
                    stage2.activate_invert(chara_p)  # 反転を有効にする
                elif chara_p != stage2.change_tile:
                    stage2.invert_tiles = False  # 移動していない場合は反転を解除

    while not exit_flag:
        cmd_move = -1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_flag = True
                exit_code = '001'
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_UP, pg.K_w]:
                    cmd_move = 0
                elif event.key in [pg.K_RIGHT, pg.K_d]:
                    cmd_move = 1
                elif event.key in [pg.K_DOWN, pg.K_s]:
                    cmd_move = 2
                elif event.key in [pg.K_LEFT, pg.K_a]:
                    cmd_move = 3
                elif event.key == pg.K_r:
                    if stage == stage1:
                        stage1 = s.Stage1(chip_s)
                        stage = stage1
                    elif stage == stage2:
                        stage2 = s.Stage2(chip_s)
                        stage = stage2
                    chara_p, chara_s, chara_imgs, m_vec = d.chara()

        if chara_p == stage.goal_pos:
            stage = stage2  # ステージ2を有効化する
            chara_p = pg.Vector2(2, 7)  # 初期位置に戻す

        screen.fill(pg.Color('WHITE'))
        stage.draw(screen, chip_s)
        handle_move(cmd_move)

        screen.blit(chara_imgs[direction_map[chara_d]], chara_p * chip_s)
        screen.blit(font.render(f'{pg.time.get_ticks() // 1000:05}', True, 'BLACK'), (10, 10))

        pg.display.update()
        clock.tick(30)

    pg.quit()
    return exit_code

if __name__ == "__main__":
    code = main()
    print(f'プログラムを「コード{code}」で終了しました。')
