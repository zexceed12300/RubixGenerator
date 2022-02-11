from PIL import Image, ImageDraw
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def three_dimension_rubic_renderer():
    print("fefaefa")

def new_rubix(path_saved, stack):
    colors = {0:"b.png", 1:"g.png", 2:"o.png", 3:"r.png", 4:"y.png", 5:"d.png"}

    pos = [(30, 30),
           (350, 30),
           (670, 30),
           (30, 350),
           (350, 350),
           (670,350),
           (30,670),
           (350,670),
           (670,670)]

    left_top = Image.open("assets/edge/left-top/{}".format(colors[stack[0]]))
    top = Image.open("assets/edge/top/{}".format(colors[stack[1]]))
    right_top = Image.open("assets/edge/right-top/{}".format(colors[stack[2]]))
    left = Image.open("assets/edge/left/{}".format(colors[stack[3]]))
    center = Image.open("assets/edge/center/{}".format(colors[stack[4]]))
    right = Image.open("assets/edge/right/{}".format(colors[stack[5]]))
    left_bottom = Image.open("assets/edge/left-bottom/{}".format(colors[stack[6]]))
    bottom = Image.open("assets/edge/bottom/{}".format(colors[stack[7]]))
    right_bottom = Image.open("assets/edge/right-bottom/{}".format(colors[stack[8]]))

    image = Image.new("RGB", (1000, 1000), (255, 255, 255, 255))
    image.paste(left_top, pos[0], left_top)
    image.paste(top, pos[1], top)
    image.paste(right_top, pos[2], right_top)
    image.paste(left, pos[3], left)
    image.paste(center, pos[4], center)
    image.paste(right, pos[5], right)
    image.paste(left_bottom, pos[6], left_bottom)
    image.paste(bottom, pos[7], bottom)
    image.paste(right_bottom, pos[8], right_bottom)

    image.save(path_saved, "PNG")

def probs_equalizer(props, selected_props):
    n = []

    if selected_props in props:
        a = 0
        b = 0
        for i in props:
            a += i
        for i in selected_props:
            b += i

        c = a / b
        for i in selected_props:
            n.append(i * c)

        return n

def rubix_colors_randomize(props = {1:0.06, 2:0.1, 3:0.14, 4:0.18, 5:0.22, 6:0.3}):

    # Runtime Variable
    colors = []

    p = []
    for i in props:
        p.append(props[i])

    colors_count = np.random.choice((1, 2, 3, 4, 5, 6), p=p)

    for i in range(0, colors_count):
        obj = []
        for j in range(6):
            if j in colors:
                pass
            else:
                obj.append(j)

        colors.append(np.random.choice(tuple(obj)))
    return colors

def rubix_column_randomize(colors, probs = {1:0.2, 2:0.2, 3:0.2, 4:0.1, 5:0.1, 6:0.094, 7:0.05, 8:0.05, 9:0.006}):

    # Runtime Variable
    column = []

    if len(colors) > 1:
        if (10 - len(colors)) > 1:
            obj = range(1, 10 - len(colors))
            p = []
            s = []
            for i in probs:
                p.append(probs[i])
            for i in obj:
                s.append(probs[i])

            column.append(np.random.choice(obj, p=probs_equalizer(p, s)))
        else:
            column.append(1)
    else:
        column.append(9)

    """
    [ n1 , n2, ... ]
    r = ((a - b) - c) + 1

    r: random range
    a: total random range
    b: total n
    c: sisa kolom array
    """
    for i in range(1, len(colors)):

        # Variable
        b = 0
        c = len(colors) - len(column)
        for j in range(len(column)):
            b += column[j]

        if i == len(colors) - 1:
            column.append(9 - b)
            break

        r = ((9 - b) - c) + 1

        if r == 0:
            column.append(1)
            continue

        obj = range(1, r+1)
        p = []
        s = []
        for i in probs:
            p.append(probs[i])
        for i in obj:
            s.append(probs[i])

        column.append(np.random.choice(obj, p=probs_equalizer(p, s)))

    return column

def rubic_stack_randomize(column, colors):
    # x : column
    # y : colors

    rubix_color = {0: "blue", 1: "red", 2: "green", 3: "orange", 4: "black", 5: "yellow"}

    stack = [0, 0, 0,
             0, 0, 0,
             0, 0, 0]

    probs = [0.05,0.16,0.05,
             0.16,0.16,0.16,
             0.05,0.16,0.05]

    r = 0
    for i in colors:
        for j in range(column[r]):
            obj = []
            s = []
            for j in range(len(stack)):
                if stack[j] == 0:
                    obj.append(j)
            for j in obj:
                s.append(probs[j])

            index = np.random.choice(tuple(obj), p=probs_equalizer(probs, s))
            stack[index] = i
        r += 1

    return stack


if __name__ == "__main__":

    color = []
    colum = []
    stack = []

    total = 1000
    colors_count = [0,0,0,0,0,0]
    column_count = [0,0,0,0,0,0,0,0,0]

    for i in range(total):
        colors = rubix_colors_randomize()
        column = rubix_column_randomize(colors)
        color.append(colors)
        colum.append(column)
        stack.append(rubic_stack_randomize(column, colors))

        for i in range(0, len(colors_count)):
            if len(colors) == i+1:
                colors_count[i] += 1

        for i in column:
            column_count[i-1] += 1

    print("Numbers of colors:")
    for i in range(len(colors_count)):
        print(" {} colors: {}".format(i+1, colors_count[i]))
    print("\nNumbers of column per colors:")
    for i in range(len(column_count)):
        print(" {} column: {}".format(i+1, column_count[i]))

    continues = input("\nContinue Rendering Rubic ? [Y/N] ")
    if continues == "Y":
        pass
    else:
        exit()

    for i in tqdm(range(total)):
        name = "results/"
        if len(color[i]) == 1:
            name += "1/"
        if len(color[i]) == 2:
            name += "2/"
        if len(color[i]) == 3:
            name += "3/"
        if len(color[i]) == 4:
            name += "4/"
        if len(color[i]) == 5:
            name += "5/"
        if len(color[i]) == 6:
            name += "6/"

        name += "rubix#{}.png".format(i+1)
        new_rubix(name, stack[i])
