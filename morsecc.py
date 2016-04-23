# -*- coding:  utf-8 -*-
import wave
import sys
from core.GlobalConfig import GlobalConfig
from core.MorseCodeAudio import MorseCodeAudio
from core.Translator import Translator as MorseCodeTranslator

def translate(mcAudio):
    translator = MorseCodeTranslator(mcAudio)
    translator.translate()

    return translator

def measure(binary):
    mcAudio = MorseCodeAudio()

    dumps = ''.join(str(byte) for byte in binary)
    # 清空前后空白区域
    dumps = dumps.strip('0')

    block = ''
    blockCurrentMode = '1'

    for char in dumps:
        if blockCurrentMode != char:
            mcAudio.addblock(block)

            block = ''
            # 切换区块模式
            blockCurrentMode = char

        block += char

    # 追加最后一个未切换状态的区块
    mcAudio.addblock(block)
    mcAudio.measureDuration()

    return mcAudio

def binarize(data, frames, options):
    for i in range(0, frames):
        # 8-bits
        byte = abs(int(data[i]))
        # 和基准线的差值
        division = abs(byte - GlobalConfig.BASE_VISION)

        if division <= GlobalConfig.MAX_DIVISION:
            options.space_block_counter += 1
            # 达到计数上限
            if options.space_block_counter >= GlobalConfig.MAX_BLOCK_FEED:
                options.is_in_space_block = True
                # 填充预测区为空白区域
                for fallback in range(i - GlobalConfig.MAX_BLOCK_FEED, i):
                    data[fallback] = 0
        else:
            options.space_block_counter = 0
            options.is_in_space_block = False

        byte = 0 if options.is_in_space_block else 1
        data[i] = byte

    return data

def main():
    config = GlobalConfig()
    try:
        handle = wave.open(sys.argv[1], 'rb')
        frames = handle.getnframes()
        data = handle.readframes(frames)
        # 转换为数值数组
        data = bytearray(data)
        # 二值化
        binary = binarize(data, frames, config)
        # 测量宽度
        mcAudio = measure(binary)
        # 转换为字符
        translator = translate(mcAudio)

        print '[+] Morse Code: ', translator.morse_code
        print '[+] Plain Text: ', translator.plain_text
    except Exception as e:
        print '[-] Error: ', e.message
    finally:
        if handle != None: handle.close()

if __name__ == '__main__':
    main()
