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

list_color = [
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

def getColor():
    color = list_color[0]
    list_color.pop(0)
    return color


def hex_code_colors():
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
    z = a + b + c
    return "#" + z.upper()
    #bạn thêm giúp mình là loại trường hợp #000000 và #FFFFFF ra, đó là màu trắng và đen


print(hex_code_colors())


