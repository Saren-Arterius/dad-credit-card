#!/usr/bin/env python3
from selenium import webdriver
from Solver import Solver
from PIL import Image
from io import BytesIO
from time import sleep
import os

LOGIN_URL = 'https://its.bochk.com/login/ibs_lgn_index_c.jsp'

CHROME_UI_SCALE = float(
    os.environ['CHROME_UI_SCALE']) if 'CHROME_UI_SCALE' in os.environ else 1
USERNAME = os.environ['BOC_USERNAME']
PASSWORD = os.environ['BOC_PASSWORD']
WIDTHDRAW_ACCT = os.environ['WIDTHDRAW_ACCT']


def main():
    b = webdriver.Chrome()

    def login():
        b.get(LOGIN_URL)
        solver = None
        while True:
            elem = b.find_element_by_id('verifyImg')
            location = elem.location
            size = elem.size
            x = int(location['x'] * CHROME_UI_SCALE)
            y = int(location['y'] * CHROME_UI_SCALE)
            width = x + int(size['width'] * CHROME_UI_SCALE)
            height = y + int(size['height'] * CHROME_UI_SCALE)
            buffer = BytesIO(b.get_screenshot_as_png())
            img = Image.open(buffer)
            img = img.crop((x, y, width, height,))
            solver = Solver(img, 4)
            if len(solver.char_areas) == 4:
                break
            b.find_element_by_css_selector('a.apply:nth-child(1)').click()
            print('Refreshing captcha', len(solver.char_areas))
            sleep(1)
        b.find_element_by_id('checkCode').send_keys(solver.get_result())
        b.find_element_by_id('username').send_keys(USERNAME)
        b.find_element_by_id('password').send_keys(PASSWORD)
        b.find_element_by_css_selector(
            '#loginbox-nav > a:nth-child(1)').click()
        if 'IJ0305' in b.page_source:  # Wrong captcha
            login()
    login()
    b.get('https://its.bochk.com/cdc.overview.do')  # cc page

    b.find_element_by_css_selector(
        '#content > table:nth-child(4) > tbody > tr:nth-child(2) > td:nth-child(4) > a').click()  # click latest owe
    b.find_element_by_css_selector(
        '#content > form > table:nth-child(2) > tbody > tr:nth-child(11) > td.data_table_link.data_table_lastcell > table > tbody > tr > td > ul > li:nth-child(2) > a').click()  # click pay

    b.find_element_by_css_selector(
        '#content option[value="{}"]'.format(WIDTHDRAW_ACCT)).click()
    b.find_element_by_css_selector(
        '#content > form > table:nth-child(1) > tbody > tr:nth-child(4) > td.field > table > tbody > tr:nth-child(1) > td > input').click()  # pay now

    b.find_element_by_css_selector(
        '#content > form > table:nth-child(2) > tbody > tr > td.data_table_link > ul > li.large > a').click()
    print('Prompting for user action')
    sleep(1000000)


if __name__ == '__main__':
    main()
