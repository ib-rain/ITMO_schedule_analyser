#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import re
from sys import stderr,  argv
from time import sleep
from itertools import chain

GROUP_RE = '<td class="time" style="width:8%"><span>(.+)</span></td>'

first_floor = tuple(chain(range(136, 147), [
                    98, 99, 100, 151, 153, 154, 157, 162, 161, 160,
                    158, '147а', '147б', '147в', '147г', 190]))
second_floor = tuple(chain(range(251, 296), range(
                     201, 231), [235, 236, 237, 239, '209а', '210а']))
third_floor = tuple(chain(range(302, 338), [
                    '326б', '330а', '303а', '368а'], range(359, 382)))
fourth_floor = tuple(chain(range(401, 435), [
                     454, 458, 461, 464, 465, 466, 467, '467а', 478, 468,
                     469, 470, 471, 472, '472а', 473, 474, 475, 477, 479,
                     447, '406а', '425а', '430а', '430б', '430в', '431а',
                     '431б', '431в', '431г', '431д', '431е', '433а', '433б']))
fifth_floor = tuple(chain(range(560, 583), [
                    513, 501, 511, 512, 502, 505, '505а', '505б',
                    '504а', '504б', 551, 552, 553, 556, 583]))
all_floors = (first_floor,  second_floor,
              third_floor,  fourth_floor,  fifth_floor)


def get_groups(room):
    url = 'http://www.ifmo.ru/ru/schedule/2/{}/schedule.htm'.format(room)
    request = urllib2.Request(url)
    while True:
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError,  e:
            stderr.write('Error at room {}: {}\n'.format(room,  str(e)))
            sleep(7)
        else:
            break
    page_text = response.read()
    groups = set(re.findall(GROUP_RE,  page_text))
    response.close()
    return groups


def get_groups_per_room_on_floor(i):
    groups = set()
    for room in all_floors[i-1]:
        groups |= get_groups(room)
        sleep(1)
    return groups


def main():
    if not argv or len(argv) != 2:
        print('usage: python '+argv[0]+' [12345]\n\
    where the number is the floor number you want to \
    get groups from.')
        exit(1)

    i = min(5, int(argv[1]))
    all_groups = get_groups_per_room_on_floor(i)
    print(all_groups)
    return 0

if __name__ == '__main__':
    main()
