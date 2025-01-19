import pygame as pg
import data as d

class Stage0:
    def __init__(self, chip_size):
        self.chip_size = chip_size
        
        # フォントの読み込み
        try:
            self.font = pg.font.Font('./material/TanukiMagic.ttf', 74)  # 大きなフォント
            self.sub_font = pg.font.Font('./material/TanukiMagic.ttf', 36)  # 小さなフォント
        except FileNotFoundError:
            raise FileNotFoundError("フォントファイルが見つかりません。./material/TanukiMagic.ttf を確認してください。")

    def draw(self, screen, chip_size):
        screen.fill(pg.Color('WHITE'))  # 背景を白に設定
        
        # タイトルとサブタイトルの描画
        title_surface = self.font.render("白黒パズル", True, pg.Color('BLACK'))
        subtitle_surface = self.sub_font.render("SPACEキーを押してスタート！", True, pg.Color('BLACK'))

        # 中央に配置
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
        subtitle_rect = subtitle_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40))

        # 描画
        screen.blit(title_surface, title_rect)
        screen.blit(subtitle_surface, subtitle_rect)

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
        new_block_pos = self.block_pos + direction
        if d.is_walkable(self.map_data, int(new_block_pos.x), int(new_block_pos.y)) and not d.is_block(self.map_data, int(new_block_pos.x), int(new_block_pos.y)):
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
        self.tile_pressed = False  # タイルが押された状態かどうか

    def activate_invert(self, chara_pos):
        if chara_pos == self.change_tile:
            if not self.tile_pressed:  # キャラクターがタイルに初めて乗った場合
                self.map_data = self.inverted_map_data if not self.invert_tiles else self.original_map_data
                self.invert_tiles = not self.invert_tiles  # 反転状態を切り替え
                self.tile_pressed = True
        else:
            self.tile_pressed = False  # キャラクターがタイルから離れたらリセット

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

class Stage3:
    def __init__(self, chip_size):
        # タイル画像をロード
        self.tile_images = d.get_tile_images(chip_size)

        # 初期のマップデータ（元の状態）
        self.original_map_data = [
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 0, 2, 0, 1, 1, 1, 1, 1]
        ]

        # 反転後のマップデータ
        self.inverted_map_data = [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0]
        ]

        

        # 反転効果が有効かどうか
        self.invert_tiles = False
        self.change_tile = pg.Vector2(8, 9)  # 反転タイルの座標（仮）
        self.goal_pos = pg.Vector2(12, 8)
        self.map_data = self.original_map_data
        self.tile_pressed = False
        self.block_pos1 = pg.Vector2(1, 2)
        self.block_pos2 = pg.Vector2(2, 2)

    def move_block1(self, chara_x, chara_y, direction):
        """ブロックを移動する処理"""
        if self.invert_tiles:
            return False  # 反転状態のときはブロックを移動させない
        new_block_pos1 = self.block_pos1 + direction
        if d.is_walkable(self.map_data, int(new_block_pos1.x), int(new_block_pos1.y)) and not d.is_block(self.map_data, int(new_block_pos1.x), int(new_block_pos1.y)):
            self.block_pos1 = new_block_pos1
            return True
        return False
    
    def move_block2(self, chara_x, chara_y, direction):
        """ブロックを移動する処理"""
        if self.invert_tiles:
            return False  # 反転状態のときはブロックを移動させない
        new_block_pos2 = self.block_pos2 + direction
        if d.is_walkable(self.map_data, int(new_block_pos2.x), int(new_block_pos2.y)) and not d.is_block(self.map_data, int(new_block_pos2.x), int(new_block_pos2.y)):
            self.block_pos2 = new_block_pos2
            return True
        return False

    def activate_invert(self, chara_pos):
        if chara_pos == self.change_tile:
            if not self.tile_pressed:  # キャラクターがタイルに初めて乗った場合
                self.invert_tiles = not self.invert_tiles  # 反転状態を切り替え
                self.tile_pressed = True

                # blockタイルとunblockタイルを反転
                for y, row in enumerate(self.map_data):
                    for x, tile in enumerate(row):
                        if tile == 1:  # blockタイル
                            self.map_data[y][x] = 0  # unblockタイルに変更
                        elif tile == 0:  # unblockタイル
                            self.map_data[y][x] = 1  # blockタイルに変更
        else:
            self.tile_pressed = False  # キャラクターがタイルから離れたらリセット

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
                    tile_color = "change"
                screen.blit(self.tile_images[tile_color], (x * chip_size, y * chip_size))

        # ゴールタイルを描画
        screen.blit(self.tile_images["goal"], self.goal_pos * chip_size)

        # 押せるブロックを描画
        block_image = self.tile_images["block"] if not self.invert_tiles else self.tile_images["unblock"]
        screen.blit(block_image, self.block_pos1 * chip_size)
        screen.blit(block_image, self.block_pos2 * chip_size)

class Stage4:
    def __init__(self, chip_size):
        self.chip_size = chip_size
        
        # フォントの読み込み
        try:
            self.font = pg.font.Font('./material/TanukiMagic.ttf', 74)  # 大きなフォント
            self.sub_font = pg.font.Font('./material/TanukiMagic.ttf', 36)  # 小さなフォント
        except FileNotFoundError:
            raise FileNotFoundError("フォントファイルが見つかりません。./material/TanukiMagic.ttf を確認してください。")

        self.goal_pos = pg.Vector2(-1, -1)  # ダミーのゴール位置

    def draw(self, screen, chip_size):
        screen.fill(pg.Color('WHITE'))  # 背景を白に設定
        
        # タイトルとサブタイトルの描画
        title_surface = self.font.render("Coming soon", True, pg.Color('BLACK'))

        # 中央に配置
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))

        # 描画
        screen.blit(title_surface, title_rect)