import re
import random

mint_leaf = '#00b894'
light_blue = '#00cec9'
elec_blue = '#0984e3'
purple = '#6c5ce7'
silver = '#b2bec3'
light_yellow = '#ffeaa7'
light_pink = '#ff7675'
orange = '#e17055'
red = '#d63031'
pink = '#e84393'

list_z = [
    mint_leaf,
    light_blue,
    elec_blue,
    purple,
    silver,
    light_yellow,
    light_pink,
    orange,
    red,
    pink
]

def getz():
    z = list_z[0]
    list_z.pop(0)
    return z

LIST_COLORS = []

def remove_color(doppelganger):
    if doppelganger in LIST_COLORS:
        LIST_COLORS.remove(doppelganger)

def hex_code_colors():
    z = ''
    while z not in LIST_COLORS:
        a = hex(random.randrange(0,256))
        b = hex(random.randrange(0,256))
        c = hex(random.randrange(0,256))
        a = a[2:]
        b = b[2:]
        c = c[2:]
        if len(a)<2:
            a = "0" + a
        if len(b)<2:
            b = "0" + b
        if len(c)<2:
            c = "0" + c
        x = a + b + c
        z = "#" + x
        if z in LIST_COLORS:
            continue
        if z == "#000000" or z == "#FFFFFF":
            continue
        LIST_COLORS.append(z)
        return z



if __name__ == "__main__":
    print(LIST_COLORS)
    print(hex_code_colors())




