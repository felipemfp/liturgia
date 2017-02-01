#!/usr/bin/env python3

import time
import datetime
import requests
import subprocess
from os import path, mkdir
from bs4 import BeautifulSoup

URL_HOST = 'http://liturgiadiaria.cnbb.org.br'
URL_TEMPLATE = URL_HOST + '/app/user/user/UserView.php?ano={}&mes={}&dia={}'
SLEEP_TIME = 24 * 60 * 60
TRY_AGAIN_TIME = 20 * 60


def pull():
    return subprocess.call(['git', 'pull', 'origin', 'master', '--rebase'])


def commit_and_push(filename):
    subprocess.call(['git', 'add', '.'])
    subprocess.call(
        ['git', 'commit', '-am', ':church: Add {}'.format(filename)])
    return subprocess.call(['git', 'push', 'origin', 'master'])


def scrape(url, folder, filename):
    mdfile = open(path.join(folder, filename), mode='w', encoding='utf8')
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    day_calendar = " ".join(
        soup.find('div', class_='bs-callout bs-callout-info')
        .find('h2')
        .get_text(strip=True)
        .split()
    )
    mdfile.write('# {}\n\n'.format(day_calendar))
    divs = soup.find(id="corpo_leituras").find_all(
        'div', id=True, recursive=False)
    for div in divs:
        title_element = div.find('h3')
        italic_element = div.find('div', class_='cit_direita_italico')
        enunciation_element = div.find('div', class_='cit_direita')
        chorus_element = div.find('div', class_='refrao_salmo')
        content_element = div.find_all('div', recursive=False)[-1]

        title_text = title_element.get_text(
            strip=True) if title_element else ''
        italic_text = italic_element.get_text(
            ' ', strip=True) if italic_element else ''
        enunciation_text = enunciation_element.get_text(
            strip=True)if enunciation_element else ''
        chorus_text = chorus_element.get_text(
            strip=True) if chorus_element else ''

        if italic_element:
            italic_element.clear()
        if enunciation_element:
            enunciation_element.clear()
        if chorus_element:
            chorus_element.clear()

        content_text = content_element.get_text(' ').strip()

        mdfile.write('## {}\n\n'.format(title_text))
        if italic_text:
            mdfile.write('> {}\n\n'.format(italic_text))
        if enunciation_text:
            mdfile.write('**{}**\n\n'.format(enunciation_text))
        if chorus_text:
            mdfile.write('`{}`\n\n'.format(chorus_text))
        mdfile.write('{}\n\n'.format(content_text))
    mdfile.write('Veja mais no [Liturgia Diária - CNBB]({})'.format(url))
    mdfile.close()

if __name__ == '__main__':
    while True:
        if pull() == 0:
            now = datetime.datetime.now()
            url = URL_TEMPLATE.format(now.year, now.month, now.day)
            folder = '{0:4d}/{1:02d}'.format(now.year, now.month)
            filename = '{0:4d}-{1:02d}-{2:02d}.md'.format(
                now.year, now.month, now.day)
            print('Today\'s URL: {}'.format(url))
            print('Today\'s filename: {}'.format(filename))
            if not path.exists(folder[:4]):
                mkdir(folder[:4])
            if not path.exists(folder):
                mkdir(folder)
            if not path.isfile(path.join(folder, filename)):
                scrape(url, folder, filename)
                commit_and_push(filename)
            else:
                print('Today was already scraped.')
            time.sleep(SLEEP_TIME)
        else:
            time.sleep(TRY_AGAIN_TIME)
