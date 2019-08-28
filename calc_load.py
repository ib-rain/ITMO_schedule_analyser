#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
from sys import argv, exit, stderr
from time import sleep
from lxml import html
from itertools import chain


ADR = "Кронверкский пр., д.49, лит.А"
week_types = {u'четная неделя': '_0', u'нечетная неделя': '_1'}

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

url = 'http://www.ifmo.ru/ru/schedule/2/{}/schedule.htm'


def get_text(room):
    request = urllib2.Request(url.format(room))
    while True:
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            stderr.write('Error at room {}: {}\n'.format(room, str(e)))
            sleep(7)
        else:
            break
    page_text = response.read()
    response.close()
    return page_text


def get_sched(room):
    tree = html.fromstring(get_text(room))
    room_schedule = {}
    for i in range(1, 7):
        times = tree.xpath(
            '//*/table[@id="{}day"]//td[@class="time" \
            and count(@*)=1]/span'.format(i))
        if len(times) > 0:
            room_schedule[i] = {}
        else:
            continue

        for t in times:
            day = t.xpath(
                '../../..//th[@class="day" or @class="today day"]/span')[0].text
            if day not in room_schedule[i]:
                room_schedule[i][day] = {}
            if t.text not in room_schedule[i][day]:
                room_schedule[i][day][t.text] = []
            adr = t.xpath('../../td[@class="room"]/dl/dt/span')
            for a in adr:
                if a.text.encode('utf-8') == ADR:
                    for lssn in a.xpath('../../../../td[@class="time" \
                                        and @style="width:8%"]/span'):
                        oddness = lssn.xpath(
                            '../../td[@class="lesson"]/dl/dt[not(b)]')[0].text
                        if oddness in week_types:
                            oddness = week_types[oddness]
                        else:
                            oddness = ''

                        if t.text+oddness not in room_schedule[i][day]:
                            room_schedule[i][day][t.text+oddness] = [lssn.text]
                        else:
                            room_schedule[i][day][t.text+oddness].append(
                                lssn.text)
    return room_schedule


def main():
    if not argv or len(argv) != 3:
        print('usage: python '+argv[0]+'isu_groups.txt [12345]\n\
	where the number is the floor number you want to \
    calculate amount of classes for.')
        exit(1)

    with open(argv[1]) as f:
        groups_count = eval(f.readline())

    i = min(5, int(argv[2]))
    floor_schedule = {}
    for room in all_floors[i-1]:
        floor_schedule[room] = get_sched(room)

    for room in floor_schedule:
        for i in floor_schedule[room]:
            for day in floor_schedule[room][i]:
                for time in floor_schedule[room][i][day]:
                    floor_schedule[room][i][day][time] = sum(
                        list(map(lambda x: int(groups_count[x]),
                                 floor_schedule[room][i][day][time])))

    result = []

    for room in floor_schedule:
        stud_count = [0]
        for d in floor_schedule[room].values():
            for v in d.values():
                stud_count.extend(v.values())
        result.append((room, sum(stud_count), max(stud_count)))

    print(sorted(result, key=lambda x: x[1], reverse=True))
    return 0


if __name__ == '__main__':
    main()
