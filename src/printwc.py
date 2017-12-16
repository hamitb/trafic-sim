base  = '\x1b[1;{};{}m{{}}\x1b[0m'

colors = {
    'green': base.format(32, 49),
    'blue': base.format(34, 49),
    'yellow': base.format(33, 49),
    'red': base.format(31, 49),
}

def printwc(color, string):
    print(colors[color].format(string))

