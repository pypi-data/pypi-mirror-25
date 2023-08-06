import random

a = [random.randint(1, 100) for _ in range(1000)]
step = a[66]


def go(n):
    if n == 1:
        return "玉渡山有{}道弯（尝试去走走）".format(a[0])
    else:
        if n in a:
            i = a.index(n) + 1
            if n == step:
                return "玉渡山有101条河与{}道弯".format(a[0])
            if i < len(a):
                return "玉渡山有{}道弯".format(a[i])
            else:
                return "PEAK"
        else:
            return "TOP"
