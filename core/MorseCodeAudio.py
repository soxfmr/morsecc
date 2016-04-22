# -*- coding:  utf-8 -*-
class MorseCodeAudio:
    def __init__(self):
        self.duration_dot = -1
        self.duration_dash = -1

        self.duration_space_dot_dash = -1
        self.duration_space_letter = -1
        # self.duration_space_words = 7

        self.entityMeasureList = []
        self.spaceMeasureList = []

        self.block_list = []

    def addblock(self, block):
        width = len(block)

        if '1' in block:
            self.entityMeasureList.append(width)
        else:
            self.spaceMeasureList.append(width)

        # 添加音频块
        self.block_list.append(block)

    def measureDuration(self):
        if len(self.entityMeasureList) == 0:
            raise Exception('Measurement list of entity is required.')

        # 去除重复值并升序排序
        self.entityMeasureList = list(set(self.entityMeasureList))
        self.spaceMeasureList = list(set(self.spaceMeasureList))

        self.entityMeasureList.sort()
        self.spaceMeasureList.sort()

        # 长段音频（dash或字母间隔）至少为短音频的两倍+，具体由音频软件生成
        # 因此通过该值可以快速区分长段音频和短音频
        entityMin = min(self.entityMeasureList)
        entityMax = entityMin * 2

        if (len(self.spaceMeasureList) > 0):
            spaceMin = min(self.spaceMeasureList)
            spaceMax = spaceMin * 2

            self.duration_space_letter = spaceMax
            self.duration_space_dot_dash = spaceMin

        self.duration_dot = entityMin
        self.duration_dash = entityMax
