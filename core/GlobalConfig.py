# -*- coding:  utf-8 -*-
class GlobalConfig:
    # 基线容差范围
    MAX_DIVISION = 3
    # 连续空白区域填充上限
    MAX_BLOCK_FEED = 5
    # 基线值
    BASE_VISION = 0x80

    def __init__(self):
        # 连续空白区域计数
        self.space_block_counter = 0
        # 处于空白区域标志
        self.is_in_space_block = False
