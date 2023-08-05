#!/usr/bin/env python
import random

from PIL import Image


def split_rgb(image):
    '''(r, g, b) list to r, g, b matrices'''
    width, height = image.size

    def _list_to_matrix(data):
        return [data[n*width:(n+1)*width] for n in range(height)]

    if ''.join(image.getbands()).lower() != 'rgb':
        image = image.convert('RGB')

    bands = [
        list(image.getdata(band))
        for band in range(3)  # R, G, B
    ]

    return map(_list_to_matrix, bands)


def shift_horizontal(matrix, shift_width, ok_to_extend=False):
    # shift_width greater than actual width produces cycles
    if not ok_to_extend:
        shift_width = shift_width % len(matrix[0])

    matrix = matrix[:]  # lists are passed by reference

    if shift_width > 0:  # right shift
        for i, row in enumerate(matrix):
            matrix[i] = row[-shift_width:] + row[:len(row) - shift_width]
    else:  # left shift or no shift
        for i, row in enumerate(matrix):
            matrix[i] =  row[len(row) + shift_width:] + row[:shift_width]

    return matrix


def shift_vertical(matrix, shift_width, ok_to_extend=False):
    transpose = list(zip(*matrix))
    # after transpose, negative shift_width shifts *up* so the `-` makes
    # the args more natural
    return list(zip(*shift_horizontal(transpose, -shift_width, ok_to_extend)))


def flatten_matrix(matrix):
    return [item for row in matrix for item in row]


def shift_blue_test(image, amount):
    r, g, b = split_rgb(image)
    b_new = shift_vertical(b, amount)
    _r, _g, _b = map(flatten_matrix, [r, g, b_new])

    new_image = Image.new('RGB', image.size)
    new_image.putdata(list(zip(_r, _g, _b)))

    return new_image


def glitch(image):
    def _random_shift(band):
        width, height = image.size

        vertical_shift = random.randint(-width, width)
        horizontal_shift = random.randint(-height, height)

        return shift_horizontal(
                shift_vertical(band, vertical_shift),
                horizontal_shift
           )

    r, g, b = map(flatten_matrix, map(_random_shift, split_rgb(image)))

    new_image = Image.new('RGB', image.size)
    new_image.putdata(list(zip(r, g, b)))

    return new_image


if __name__ == '__main__':
    import argparse
    import string
    import sys

    parser = argparse.ArgumentParser(description=(
                    "RGB shift glitch an image. Outputs to PNG because I can't be bothered to"
                    "give you other options"))
    parser.add_argument('filepaths', help='PATH to image',
            metavar='PATH', type=str, nargs='+')
    parser.add_argument('-s', '--suffix', help='Save result with given suffix. overrides -r',
            metavar='SUFFIX', type=str)
    parser.add_argument('-r', '--random-suffix', help='Save result with a random suffix. overridden by -s',
            action='store_true')
    parser.add_argument('-o', '--output', help='Path to output. Same as -r when multiple files specified.',
            metavar='PATH')
    parser.add_argument('--no-display', help='Do not show image on completion.',
            action='store_true', default=False, dest='hide_result')

    args = parser.parse_args()

    should_write_out = args.output or args.random_suffix or args.suffix
    if not should_write_out and args.hide_result:
        sys.exit('Oops, you chose to not show or save the result.\nTry -h for help.')

    try:
        if len(args.filepaths) == 1:
            fname = args.filepaths[0]
            im = Image.open(fname)
            glitched = glitch(im)
            if should_write_out:
                _fname = fname[:-4] if len(fname) > 4 and fname[-4:].lower() == '.png' else fname
                output_fname = args.output \
                        or (_fname + (args.suffix \
                        or ''.join([random.choice(string.hexdigits) for _ in range(8)])))
                print('Saving glitched {} as {}.png...'.format(fname, output_fname))
                glitched.save('{}.png'.format(output_fname), 'png')
                print('Done.')
            if not args.hide_result:
                glitched.show()
        else:
            for fname in args.filepaths:
                im = Image.open(fname)
                glitched = glitch(im)
                if should_write_out:
                    _fname = fname[:-4] if len(fname) > 4 and fname[-4:].lower() == '.png' else fname
                    output_fname = (_fname + \
                        (args.suffix \
                        or ''.join([random.choice(string.hexdigits) for _ in range(8)])))
                    print('Saving glitched {} as {}.png...'.format(fname, output_fname))
                    glitched.save('{}.png'.format(output_fname), 'png')
                    print('Done.')
                if not args.hide_result:
                    glitched.show()
    except Exception as e:
        print('Oops {}'.format(e))
