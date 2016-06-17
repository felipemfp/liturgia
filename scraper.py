import time
import datetime
import requests
import subprocess
import os.path
from bs4 import BeautifulSoup

URL_TEMPLATE = 'http://liturgiadiaria.cnbb.org.br/app/user/user/UserView.php?ano={}&mes={}&dia={}'
SLEEP_TIME = 24 * 60 * 60

def pull():
    subprocess.run(['git', 'pull', 'origin', 'master', '--rebase'])

def commit_and_push(filename):
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-am', ':space_invader: Add {}'.format(filename)])
    subprocess.run(['git', 'push', 'origin', 'master'])

def scrape(url, filename):
    mdfile = open(filename, mode='w', encoding='utf8')
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    day_calendar = " ".join(soup.find('div', class_='bs-callout bs-callout-info').find('h2').get_text(strip=True).split())
    mdfile.write('# {}\n\n'.format(day_calendar))
    divs = soup.find(id="corpo_leituras").find_all('div', id=True, recursive=False)
    for div in divs:
        title_element = div.find('h3')
        italic_element = div.find('div', class_='cit_direita_italico')
        enunciation_element = div.find('div', class_='cit_direita')
        chorus_element = div.find('div', class_='refrao_salmo')
        content_element = div.find_all('div', recursive=False)[-1]

        title_text = title_element.get_text(strip=True) if title_element else ''
        italic_text = italic_element.get_text(' ', strip=True) if italic_element else ''
        enunciation_text = enunciation_element.get_text(strip=True)if enunciation_element else ''
        chorus_text = chorus_element.get_text(strip=True) if chorus_element else ''

        if italic_element: italic_element.clear()
        if enunciation_element: enunciation_element.clear()
        if chorus_element: chorus_element.clear()

        content_text = content_element.get_text(' ').strip()

        mdfile.write('## {}\n\n'.format(title_text))
        if italic_text: mdfile.write('> {}\n\n'.format(italic_text))
        if enunciation_text: mdfile.write('**{}**\n\n'.format(enunciation_text))
        if chorus_text: mdfile.write('`{}`\n\n'.format(chorus_text))
        mdfile.write('{}\n\n'.format(content_text))
    mdfile.write('Veja mais no [Liturgia Diária - CNBB]({})'.format(url))
    mdfile.close()

if __name__ == '__main__':
    while True:
        pull()
        now = datetime.datetime.now()
        url = URL_TEMPLATE.format(now.year, now.month, now.day)
        filename = '{:4d}-{:02d}-{:02d}.md'.format(now.year, now.month, now.day)
        print('Today\'s URL: {}'.format(url))
        print('Today\'s filename: {}'.format(filename))
        if not os.path.isfile(filename):
            scrape(url, filename)
            commit_and_push(filename)
        else:
            print('Today was already scraped.')
        time.sleep(SLEEP_TIME)
