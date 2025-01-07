import pygame as pg
import data as d

class Stage1:
    def __init__(self, chip_size):
        # ステージ1のマップデータ
        self.map_data = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        # タイル画像をロード
        self.tile_images = d.get_tile_images(chip_size)

        # 押せるブロックの初期位置
        self.block_pos = pg.Vector2(9, 4)

        # ゴールタイルの位置
        self.goal_pos = pg.Vector2(12, 4)

    def draw(self, screen, chip_size):
        """マップとブロック、ゴールを描画する"""
        for y, row in enumerate(self.map_data):  # マップデータを1行ずつ処理
            for x, tile in enumerate(row):  # 各行の各タイルを処理
                # タイルの種類に応じて画像を選択
                if tile == 0:
                    tile_color = "white"
                elif tile == 1:
                    tile_color = "black"
                elif tile == 2:
                    tile_color = "goal"
                screen.blit(self.tile_images[tile_color], (x * chip_size, y * chip_size))

        # ゴールタイルを描画
        screen.blit(self.tile_images["goal"], self.goal_pos * chip_size)

        # 押せるブロックを描画
        screen.blit(self.tile_images["block"], self.block_pos * chip_size)

    def move_block(self, chara_x, chara_y, direction):
        """ブロックを移動する処理"""
        new_block_pos = d.move_block(self.map_data, self.block_pos, direction)
        if d.is_walkable(self.map_data, int(new_block_pos.x), int(new_block_pos.y)):
            self.block_pos = new_block_pos
            return True
        return False

    def is_goal_reached(self, chara_pos):
        """キャラクターがゴールに到達したかを判定"""
        return self.goal_pos == chara_pos

class Stage2:
    def __init__(self, chip_size):
        # タイル画像をロード
        self.tile_images = d.get_tile_images(chip_size)

        # 初期のマップデータ（元の状態）
        self.original_map_data = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        # 反転後のマップデータ
        self.inverted_map_data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        # 反転効果が有効かどうか
        self.invert_tiles = False
        self.change_tile = pg.Vector2(6, 4)  # 反転タイルの座標（仮）
        self.goal_pos = pg.Vector2(12, 3)
        self.map_data = self.original_map_data

    def activate_invert(self, chara_pos):
        if self.invert_tiles == False:
            self.map_data = self.inverted_map_data
            self.invert_tiles = True
        else:
            self.map_data = self.original_map_data
            self.invert_tiles = False

    def draw(self, screen, chip_size):
        # マップを描画
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == 0:
                    tile_color = "white"
                elif tile == 1:
                    tile_color = "black"
                elif tile == 2:
                    tile_color = "change"
                screen.blit(self.tile_images[tile_color], (x * chip_size, y * chip_size))

        # ゴールタイルを描画
        screen.blit(self.tile_images["goal"], self.goal_pos * chip_size)
