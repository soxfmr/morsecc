# -*- coding:  utf-8 -*-
class Translator:

    MORSE_CODE_TABLE = {
        'A' : [0, 1],
        'B' : [1, 0, 0, 0],
        'C' : [1, 0, 1, 0],
        'D' : [1, 0, 0],
        'E' : [0],
        'F' : [0, 0, 1, 0],
        'G' : [1, 1, 0],
        'H' : [0, 0, 0, 0],
        'I' : [0, 0],
        'J' : [0, 1, 1, 1],
        'K' : [1, 0, 1],
        'L' : [0, 1, 0, 0],
        'M' : [1, 1],
        'N' : [1, 0],
        'O' : [1, 1, 1],
        'P' : [0, 1, 1, 0],
        'Q' : [1, 1, 0, 1],
        'R' : [0, 1, 0],
        'S' : [0, 0, 0],
        'T' : [1],
        'U' : [0, 0, 1],
        'V' : [0, 0, 0, 1],
        'W' : [0, 1, 1],
        'X' : [1, 0, 0, 1],
        'Y' : [1, 0, 1, 1],
        'Z' : [1, 1, 0, 0],
        '0' : [1, 1, 1, 1, 1],
        '1' : [0, 1, 1, 1, 1],
        '2' : [0, 0, 1, 1, 1],
        '3' : [0, 0, 0, 1, 1],
        '4' : [0, 0, 0, 0, 1],
        '5' : [0, 0, 0, 0, 0],
        '6' : [1, 0, 0, 0, 0],
        '7' : [1, 1, 0, 0, 0],
        '8' : [1, 1, 1, 0, 0],
        '9' : [1, 1, 1, 1, 0],
        '.' : [0, 1, 0, 1, 0, 1],
        ',' : [1, 1, 0, 0, 1, 1],
        '?' : [0, 0, 1, 1, 0, 0],
        '\'' : [0, 1, 1, 1, 1, 0],
        '!' : [1, 0, 1, 0, 1, 1],
        '/' : [1, 0, 0, 1, 0],
        '(' : [1, 0, 1, 1, 0],
        ')' : [1, 0, 1, 1, 0, 1],
        '&' : [0, 1, 0, 0, 0],
        ':' : [1, 1, 1, 0, 0, 0],
        ';' : [1, 0, 1, 0, 1, 0],
        '=' : [1, 0, 0, 0, 1],
        '+' : [0, 1, 0, 1, 0],
        '-' : [1, 0, 0, 0, 0, 1],
        '_' : [0, 0, 1, 1, 0, 1],
        '"' : [0, 1, 0, 0, 1, 0],
        '$' : [0, 0, 0, 1, 0, 0, 1],
        '@' : [0, 1, 1, 0, 1, 0],
    }

    def __init__(self, mcAudio):
        self.morse_code = ''
        self.plain_text = ''

        self.mcAudio = mcAudio

    def translate(self):
        if self.mcAudio == None:
            return False

        letter = []
        for block in self.mcAudio.block_list:
            width = len(block)

            if '0' in block:
                if self.isLetterSpace(width):
                    self.parse(letter)

                    letter = []
                    self.morse_code += ' '
            elif '1' in block:
                letter.append(1 if self.isDash(width) else 0)

        self.parse(letter)

    def parse(self, letter):
        bFound = False
        for char, finger in Translator.MORSE_CODE_TABLE.iteritems():
            if finger == letter:
                self.plain_text += char
                self.morse_code += self.listToMorseCode(finger)
                bFound = True
                break

        if not bFound:
            print '[-] One character missed.'
            self.plain_text += '\0x1B'

    def listToMorseCode(self, value):
        result = ''
        for i in value:
            result += '.' if i == 0 else '_'
            #result += ' '

        return result

    def isDash(self, width):
        return True if width > self.mcAudio.duration_dash else False

    def isLetterSpace(self, width):
        if self.mcAudio.duration_space_dot_dash == -1 or \
            width < self.mcAudio.duration_space_letter:
            return False

        return True
