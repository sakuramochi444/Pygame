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

    stage0 = s.Stage0(chip_s)
    stage1 = s.Stage1(chip_s)
    stage2 = s.Stage2(chip_s)
    stage3 = s.Stage3(chip_s)
    stage4 = s.Stage4(chip_s)
    stage = stage0
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

            # 各ステージの移動条件を個別に処理
            if isinstance(stage, s.Stage1):
                if stage.block_pos == af_pos:
                    if stage.move_block(chara_p.x, chara_p.y, m_vec[cmd_move]):
                        chara_p += m_vec[cmd_move]
                elif d.is_walkable(stage.map_data, int(af_pos.x), int(af_pos.y)):
                    chara_p += m_vec[cmd_move]
                chara_d = cmd_move

            elif isinstance(stage, s.Stage2):
                if d.is_walkable(stage.map_data, int(af_pos.x), int(af_pos.y)):
                    chara_p += m_vec[cmd_move]
                chara_d = cmd_move
                stage.activate_invert(chara_p)

            elif isinstance(stage, s.Stage3):
                if stage.block_pos1 == af_pos:
                    if not stage.invert_tiles and stage.move_block1(chara_p.x, chara_p.y, m_vec[cmd_move]):
                        chara_p += m_vec[cmd_move]
                elif stage.block_pos2 == af_pos:
                    if not stage.invert_tiles and stage.move_block2(chara_p.x, chara_p.y, m_vec[cmd_move]):
                        chara_p += m_vec[cmd_move]
                elif d.is_walkable(stage.map_data, int(af_pos.x), int(af_pos.y)):
                    if not (stage.block_pos1 == af_pos or stage.block_pos2 == af_pos):
                        chara_p += m_vec[cmd_move]
                if stage.invert_tiles and (stage.block_pos1 == af_pos or stage.block_pos2 == af_pos):
                    chara_p += m_vec[cmd_move]
                chara_d = cmd_move
                stage.activate_invert(chara_p)

    while not exit_flag:
        cmd_move = -1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_flag = True
                exit_code = '001'
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if stage == stage0:
                        stage = stage1
                elif event.key in [pg.K_UP, pg.K_w]:
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
                    elif stage == stage3:
                        stage3 = s.Stage3(chip_s)
                        stage = stage3
                    chara_p, chara_s, chara_imgs, m_vec = d.chara()

        if stage != stage0 or stage != stage4:
            if chara_p == stage.goal_pos:
                if stage == stage1:
                    stage = stage2  # ステージ2を有効化する
                    chara_p = pg.Vector2(2, 7)  # 初期位置に戻す
                elif stage == stage2:
                    stage = stage3
                    chara_p = pg.Vector2(2, 7)
                elif stage == stage3:
                    stage = stage4
                    chara_p = pg.Vector2(2, 7)

        screen.fill(pg.Color('WHITE'))
        stage.draw(screen, chip_s)
        if stage != stage0 and stage != stage4:
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
