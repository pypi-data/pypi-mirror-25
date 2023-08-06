# Copyright (C) 2017 Pandorym
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import re
import json
import time
from urllib.parse import urljoin
from lxml import etree

MAIN = 'http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/'

logger = None

''' 从统计局获取行政区域代码，保存在本地 '''


def get_area_number():
    global logger
    import ChinaID
    logger = ChinaID.Logger

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
    }

    area_number = {}

    html = requests.get(MAIN, headers=header).content.decode('utf')
    res = re.search('	{6}<a [\s\S]*?最新县及县以上行政区划代码[\s\S]*?</font>', html).group(0)
    area_number['link'] = urljoin(MAIN, re.search('(?<=href=")[^"]*', res).group(0))
    area_number['due'] = re.search('(?<=（截止)[^）]*', res).group(0)
    area_number['post'] = re.search('(?<=<font class="cont_tit02">)2017-03-10(?=</font>)', html).group(0)
    area_number['download'] = time.time()

    page = etree.HTML(requests.get(area_number['link'], headers=header).content.decode('utf'))

    for NsoNormal in page.iterfind('.//p[@class="MsoNormal"]'):
        text = re.split('[\xa0\u3000]', NsoNormal.xpath('string(.)'))
        if not text[0] == '':
            area_number[text[0][0:2]] = text[-1]
            continue
        if not text[1] == '':
            area_number[text[1][0:4]] = text[-1]
            continue
        if not text[2] == '':
            area_number[text[2][0:6]] = text[-1]

    file = open('AreaNumber', 'w')
    try:
        file.write(json.dumps(area_number))
    finally:
        file.close()

    logger.info('Save the area code as AreaNumber file')


def load_area_number():
    try:
        file = open('AreaNumber', 'r')
        data = file.read()

    except IOError as e:
        logger.exception('it is harmless if errno=2 at load_area_number')
        if e.errno == 2:
            logger.info('Download AreaNumber...')
            return 'Init'
        else:
            logger.error('Failed to Open AreaNumber')
            return False

    try:
        area_number = json.loads(data)
        if not ('due' in area_number) or not ('link' in area_number) \
                or not ('post' in area_number) or not ('download' in area_number):
            raise Exception('AreaNumber is unlawful ')

    except Exception as e:
        logger.error('at load_area_number', e)
        logger.info('Failed to load AreaNumber')
        return False

    logger.info(u'Area Number File Info')
    logger.info(u'  Due date: %s' % area_number['due'])
    logger.info(u'  Post date: %s' % area_number['post'])
    logger.info(u'  Link: %s' % area_number['link'])
    return dict(area_number)


def parse(no):
    global logger
    import ChinaID
    logger = ChinaID.Logger

    area_number = load_area_number()
    if not area_number:
        return 'Fail'
    if area_number == 'Init':
        get_area_number()
        area_number = load_area_number()

    province = area_number[no[0:2]]
    city = area_number[no[0:4]]
    region = area_number[no[0:6]]
    return {
        'Province': province,
        'City': city,
        'Region': region
    }
