#!/usr/bin/python3
# coding: UTF-8


def rgb2hex(r, g, b):
    """RGB値をHTMLなどで使われる16進数表現に変換"""
    return '#%02X%02X%02X' % (r, g, b)


def make_gray_code(i):
    gray_tone = (255, 245, 220, 211, 192, 169, 128, 105, 0)
    if 0 <= i < len(gray_tone):
        gray = gray_tone[i]
        return rgb2hex(gray, gray, gray)
    else:
        return 'Error'


def make_rgb_code(n, i):
    """引数:n=色数(3の倍数)、i=色番号"""

    if n % 3 != 0:
        return 'Error:nが3の倍数では無い'

    def rgb_tone(x):
        return max(abs(256 * 3 // 2 - 256 * 3 * x // n) - 256 // 2, 1) - 1

    r = rgb_tone(i)
    g = rgb_tone((i - n * 1 // 3) % n)
    b = rgb_tone((i - n * 2 // 3) % n)
    return rgb2hex(r, g, b)


def make_color_code(n, i, gray=False):
    """引数:n=色数、i=色番号、gray=False(カラー),True(白黒)"""
    if 0 <= i < n:
        return make_rgb_code(n, i)
    elif gray:
        return make_gray_code(i - n)
    else:
        return 'Error'


if __name__ == '__main__':
    for i in range(12):
        print(make_color_code(12, i, gray=False))  # 色の数=12
    print('-------')
    for i in range(12, 12 + 9):
        print(make_color_code(12, i, gray=True))  # 色の数=12