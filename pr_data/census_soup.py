import urllib.request
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import logging
import time
import os

from pr_data.base import exports as exp


log = logging.getLogger(__name__)

LAT = '18.16608882'
LONG = '-66.04229489'


def make_soup(url):
    thepage = urllib.request.urlopen(url)
    soup_data = BeautifulSoup(thepage, "html.parser")
    soup_string = str(soup_data)

    return soup_string


def find_block_fips(soup_string):
    block_fips = soup_string.split('"></bloc',1)[0]
    return block_fips.split('fips="',1)[1]


def find_state_code(soup_string):
    state_code = soup_string.split('state code="',1)[1]
    return state_code.split('"',1)[0]


def find_state_name(soup_string):
    state_name = soup_string.split('name="',1)[1]
    state_name = state_name.split('name="',1)[1]
    state_name = state_name.split('"></state>',1)[0]
    return state_name


def find_county_name(soup_string):
    county_name = soup_string.split('name="',1)[1]
    return county_name.split('"',1)[0]


def get_block_data(latitude, longitude):
    url=('https://geo.fcc.gov/api/census/' + 'block/find?' +
        'latitude={lat}&longitude={long}'.format(lat=latitude, long=longitude))
    soup = make_soup(url)

    data_dict = dict()
    data_dict['latitude'] = latitude
    data_dict['longitude'] = longitude
    data_dict['state_name'] = find_state_name(soup)
    data_dict['county_name'] = find_county_name(soup)
    data_dict['state_code'] = find_state_code(soup)
    data_dict['block_fips'] = find_block_fips(soup)

    return data_dict


def main():
    logging.basicConfig(level=logging.INFO)

    #dat = get_block_data(LAT, LONG)
    #logging.info(dat)
    raw_data = exp.get_df_from_csv(file_name='data/mapa_del_crimen.csv')
    raw_data = raw_data[:10000]

    # -----------
    #  THIS NEED TO BE PULLED OUT AS A FUNCTION
    list_of_data = list()
    log_thresh = 100
    inc = log_thresh
    t0 = time.time()
    for index, row in raw_data.iterrows():
        # when to log
        if (index + 1) == log_thresh:
            now = time.time()
            run_time = now-t0
            log.info('Finished {count} Rows, Run Time: {time} seconds'.format(
                count=log_thresh, time=round(run_time, 2)))
            log_thresh += inc

        try:
            dat = get_block_data(latitude=row['POINT_X'], longitude=row['POINT_Y'])
            # log.info(dat)
            list_of_data.append(dat)
        except:
            logging.info('============= SKIPPED A ROW =============')
            pass

    t1 = time.time()
    total = t1-t0
    log.info('Total Run Time: {time} seconds'.format(time=round(total, 2)))

    # ------

    os.chdir('/Users/gsanchez/Desktop')
    data = pd.DataFrame(list_of_data)
    log.info('Writing {num} data point'.format(num=len(data)))
    data.to_csv('geo_coded_crimes.csv')


if __name__ == '__main__':
    main()
