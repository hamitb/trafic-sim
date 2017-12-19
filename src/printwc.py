base  = '\x1b[{};{};{}m{{}}\x1b[0m'

colors = {
    'green': base.format(1, 32, 49),
    'blue': base.format(1, 34, 49),
    'yellow': base.format(1, 33, 49),
    'red': base.format(1, 31, 49),
    'yellow_bg': base.format(6, 30, 43),
    'green_bg': base.format(6, 30, 42),
    'blue_bg': base.format(6, 37, 44),
    'red_bg': base.format(6, 30, 41),
}

def printwc(color, string):
    print(colors[color].format(string))

