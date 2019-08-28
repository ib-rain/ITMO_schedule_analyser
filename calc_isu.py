#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
from os import path, getcwd
from sys import argv, exit
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

DRIVER = webdriver.Firefox(executable_path=path.join(getcwd(), 'geckodriver'))
XPATH = "//table[@id='report_R1725000247147253423']/tbody/tr[position()=last()]/td"
LOGIN = "123456"
PASSWORD = "******"


def get_group_count(group):
    url = 'https://isu.ifmo.ru/pls/apex/f?p=2143:GR:100054145359156::NO:RP:GR_GR,GR_DATE:{},'.format(
        group)
    DRIVER.get(url)
    try:
        elem = DRIVER.find_element_by_xpath(XPATH)
    except NoSuchElementException:
        return 0
    return int(elem.text)


def setup():
    DRIVER.get("https://isu.ifmo.ru/pls/apex/f?p=2143:LOGIN:100872902374855")
    elem = DRIVER.find_element_by_name("p_t12")
    elem.clear()
    elem.send_keys(LOGIN)
    elem = DRIVER.find_element_by_name("p_t13")
    elem.clear()
    elem.send_keys(PASSWORD)
    elem.send_keys(Keys.RETURN)


def teardown():
    DRIVER.quit()


def main():
    if len(argv) != 2:
        print('usage: python '+argv[0]+' groups.txt\n')
        teardown()
        exit(1)

    f = open(argv[1])

    groups = set()
    for line in f.readlines():
        groups |= eval(line)

    setup()
    sleep(1)
    group_students = {}
    for group in groups:
        group_students[group] = get_group_count(group)
        sleep(1)

    teardown()
    print(group_students)
    return 0

if __name__ == '__main__':
    main()
