SVG_BORDER = 15
SVG_SCALE = 10

SVG_OUTER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" version="1.1">
    <title>Computer Laboratory, Cambridge - Floor Code</title>
{background}
{grid}
{bits}
</svg>
"""

GRID = '<g id="floortile-grid" style="stroke:#999999;stroke-width=1;">\n{x}\n{y}\n</g>'
GRIDLINE_X = '<path d="M {x},{y} v {length}" id="grid-x-{id}"/>'
GIDLINE_X_HALF = GRIDLINE_X.replace("grid-x-", "grid-x-half-")
GRIDLINE_Y = '<path d="M {x},{y} h {length}" id="grid-y-{id}"/>'
GRIDLINE_Y_HALF = GRIDLINE_Y.replace("grid-y-", "grid-y-half-")

BACKGROUND = '<rect style="fill:#888888;stroke:#999999;stroke-width:1;paint-order:fill stroke;" id="floor" width="{width}" height="{height}" x="{x}" y="{y}" />'

BITS = '<g style="fill:#444444;stroke:#999999;stroke-width:1;paint-order:fill stroke;" id="binary-tiles">\n{}\n</g>'
BIT_1_TILE = '<rect id="tile-{i_x}-{i_y}" width="{width}" height="{height}" x="{x}" y="{y}" />'


def indent(text):
    indent_space = " " * 4
    return indent_space + text.replace("\n", "\n{}".format(indent_space))


# Some minimal obfuscation here to hide the message as Unicode code points.
# This could easily just be the string in ordinary text if desired!
MESSAGE_TEXT = "\u0043\u006F\u006D\u0070\u0075\u0074\u0065\u0072\u0020\u004C\u0061\u0062\u006F\u0072\u0061\u0074\u006F\u0072\u0079\u0020\u2014\u0020\u0041\u0044\u0020\u0032\u0030\u0030\u0031\u0020\u2014\u0020\u263A"
MESSAGE_BITS = [[int(bit) for bit in "{:08b}".format(byte)] for byte in MESSAGE_TEXT.encode("utf-8")]


# The SVG can be very simple, so don't do anything fancy with building XML, just append strings:
with open("images/computer-lab-street-floor.svg", "w") as svg_file:

    message_x = len(MESSAGE_BITS)
    message_y = len(MESSAGE_BITS[0])
    x_offset = (2 * SVG_SCALE)
    y_offset = (2 * SVG_SCALE)
    message_width = (4 * message_x * SVG_SCALE) + x_offset
    message_height = (2 * message_y * SVG_SCALE) + 2 * y_offset
    image_width = message_width + (2 * SVG_BORDER)
    image_height = message_height + (2 * SVG_BORDER)

    grid_x = []
    grid_y = []
    background = ""
    bits_tiles = []

    for i_x in range(message_x):
        svg_raw_x = SVG_BORDER + (4 * i_x * SVG_SCALE)
        svg_x = svg_raw_x + x_offset
        svg_x_half = svg_x + x_offset

        for i_y in range(message_y):
            svg_raw_y = SVG_BORDER + (2 * i_y * SVG_SCALE)
            svg_y = svg_raw_y + y_offset
            svg_y_half = svg_y + y_offset

            # Background floor:
            if i_x == 0 and i_y == 0:
                background = indent(BACKGROUND.format(x=svg_raw_x, y=svg_raw_y, width=message_width, height=message_height))

            # Grid Lines:
            if i_y == 0:
                grid_x.append(indent(GRIDLINE_X.format(x=svg_x, y=svg_raw_y, length=message_height, id=i_x)))
                grid_x.append(indent(GIDLINE_X_HALF.format(x=svg_x_half, y=svg_raw_y, length=message_height, id=i_x)))
            if i_x == 0:
                grid_y.append(indent(GRIDLINE_Y.format(x=svg_raw_x, y=svg_y, length=message_width, id=i_y)))
            if i_x == 0 and i_y == message_y - 1:
                grid_y.append(indent(GRIDLINE_Y_HALF.format(x=svg_raw_x, y=svg_y_half, length=message_width, id=i_y)))

            # Binary data:
            bit = MESSAGE_BITS[i_x][i_y]
            if bit:
                bit_width = 2 * SVG_SCALE
                bit_height = SVG_SCALE
                bits_tiles.append(BIT_1_TILE.format(i_x=i_x, i_y=i_y, x=svg_x, y=svg_y, width=bit_width, height=bit_height))

    grid = indent(GRID.format(x="\n".join(grid_x), y="\n".join(grid_y)))
    bit_tile = indent("\n".join(bits_tiles))
    bits = indent(BITS.format(bit_tile))
    svg_body = SVG_OUTER.format(grid=grid, background=background, bits=bits, width=image_width, height=image_height)

    svg_file.write(svg_body)
