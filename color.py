import re


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

def generateColor() -> str:
    """Random color #ffffff"""
    pass