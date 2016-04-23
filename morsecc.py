# -*- coding:  utf-8 -*-
import wave
import sys
import argparse
from os import R_OK as MODE_READ
from os import access
from os.path import exists
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
    parser = argparse.ArgumentParser(prog='morsecc',
        usage='%(prog)s [options] <file>',
        description='Convert the wave audio file to Morse Code')
    parser.add_argument('-b', '--base-vision', metavar='<N>', dest='base_vision', type=int, default=0x80,
        help='The base vision line of the wave audio, for 8-bits rates audio that is 0x80 by default.')
    parser.add_argument('-m', '--max-division', metavar='<N>', dest='max_division', type=int, default=3,
        help='The mute segment has no any sounds but with the noise bit closed to the value of \
        the base vision line, this value determine the max value of the noisze in one bit, default to 3.')
    parser.add_argument('file')

    parser.add_argument('-V', '--version', action='version', version='%(prog)s v0.2 Beta')
    args = parser.parse_args()

    # Setup the environment
    GlobalConfig.BASE_VISION = args.base_vision
    GlobalConfig.MAX_DIVISION = args.max_division

    config = GlobalConfig()
    try:
        if not exists(args.file):
            raise Exception('File %s not found.' % args.file)

        if not access(args.file, MODE_READ):
            raise Exception('Cannot access %s. Permission deined.' % args.file)

        try:
            handle = wave.open(args.file, 'rb')
            if handle == None:
                raise Exception('Invalid format of the wave audio file %s' % args.file)

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
    except Exception as e:
        print '[-] Error: ', e.message

if __name__ == '__main__':
    main()
