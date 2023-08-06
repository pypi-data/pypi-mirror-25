#!/usr/bin/env python3
# coding=utf-8
import math
def Pascal_Triangle(n, r=[]):
    for x in range(n):
        l = len(r)
        r = [1 if i == 0 or i == l else r[i-1]+r[i] for i in range(l+1)]
        yield r

def draw_beautiful(n):
    ps = list(Pascal_Triangle(get_num_int))
    max = len(' '.join(map(str, ps[-1])))
    for p in ps:
        print(' '.join(map(str,p)).center(max)+'\n')


if __name__ == "__main__":
    print("please input a non negative digit:")
    get_num = input()
    get_num_int = int(get_num)
    print("num is:{}".format(get_num_int))
    print("the Pascal Triangle generate below")
    draw_beautiful(get_num_int)
