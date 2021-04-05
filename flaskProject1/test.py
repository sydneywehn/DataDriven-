def myadd(s, e):
    s = s | {e}
    print(f"in myadd: {s}")
def myadd2(s, e):
    s |= {e}
    print(f"in myadd2: {s}")
s1 = {1}
print(f"1-s1: {s1}")
s1 = s1 | {2}
print(f"2-s1: {s1}")
s1 |= {3}
print(f"3-s1: {s1}")
myadd(s1, 4)
print(f"4-s1: {s1}")
myadd2(s1, 5)
print(f"5-s1: {s1}")