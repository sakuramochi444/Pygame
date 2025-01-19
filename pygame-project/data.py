import pygame as pg

def get_tile_images(chip_size):
    """タイル画像をリサイズして返す"""
    tile_images = {
        "white": pg.transform.scale(pg.image.load('./material/tile_white.png'), (chip_size, chip_size)),
        "black": pg.transform.scale(pg.image.load('./material/tile_black.png'), (chip_size, chip_size)),
        "block": pg.transform.scale(pg.image.load('./material/block_white.png'), (chip_size, chip_size)),
        "unblock": pg.transform.scale(pg.image.load('./material/block_black.png'), (chip_size, chip_size)),
        "goal": pg.transform.scale(pg.image.load('./material/goal.png'), (chip_size, chip_size)),
        "change": pg.transform.scale(pg.image.load('./material/change.png'), (chip_size, chip_size)),
    }
    return tile_images  # 辞書全体を返す

def is_walkable(map_data, x, y, invert_tiles=False):
    if invert_tiles:
        return 0 <= x < len(map_data[0]) and 0 <= y < len(map_data) and (map_data[y][x] == 0 or map_data[y][x] == 2 or map_data[y][x] == 1)
    return 0 <= x < len(map_data[0]) and 0 <= y < len(map_data) and (map_data[y][x] == 0 or map_data[y][x] == 2)

def move_block(map_data, block_pos, direction, invert_tiles=False):
    new_pos = block_pos + direction
    if is_walkable(map_data, int(new_pos.x), int(new_pos.y), invert_tiles) and not is_block(map_data, int(new_pos.x), int(new_pos.y)):
        return new_pos
    return block_pos

def is_block(map_data, x, y):
    return 0 <= x < len(map_data[0]) and 0 <= y < len(map_data) and map_data[y][x] == 1

def chara():
    chara_p, chara_s = pg.Vector2(2, 7), 64
    directions = ["up", "right", "down", "left"]
    chara_imgs = {direction: pg.transform.scale(pg.image.load(f'./material/chara_{direction}.png'), (chara_s, chara_s)) for direction in directions}
    m_vec = {0: pg.Vector2(0, -1), 1: pg.Vector2(1, 0), 2: pg.Vector2(0, 1), 3: pg.Vector2(-1, 0)}
    return chara_p, chara_s, chara_imgs, m_vec