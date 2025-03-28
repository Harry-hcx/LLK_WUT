import random
import math

n = 16
m = 10
TYPE = 10


def generate_map(n, m):
    s = []
    while len(s) < n * m:
        for i in range(TYPE):
            s.append(str(i))
            s.append(str(i))
            if len(s) >= n * m:
                break

    random.shuffle(s)
    return "".join(s)


print(n)
print(m)
print(generate_map(n, m))
print(int(n * m * 90 * 1.0002547 ** (-n * m)))
