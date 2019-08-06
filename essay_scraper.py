from bs4 import BeautifulSoup
import requests
import os
import re
keyword = input('Search Keyword: ')
base_url = f'https://libraryofessays.com/search?SearchForm%5Bq%5D={keyword}'
main_url = 'https://libraryofessays.com'
r = requests.get(base_url)
html_b = r.text
soup = BeautifulSoup(html_b, 'lxml')
try:
    max_pages = int(soup.find('li', attrs={'class': 'last'}).a.text)
except AttributeError:
    max_pages = 1
    pass
print(f'**Keyword - {keyword}')
print(f'**Total no. of pages - {max_pages}')

for page in range(1,max_pages+1):
    print(f'>>processing page {page} of {max_pages}')
    print('*******************************************')
    sub_url = f'https://libraryofessays.com/search?SearchForm%5Bq%5D={keyword}&page={str(page)}'
    html_sub = requests.get(sub_url).text
    soup_sub = BeautifulSoup(html_sub, 'lxml')
    all_read_text_tags = soup_sub.find_all('a', attrs={'class': 'btn_read_more'})
    all_essay_links = [main_url + a['href'] for a in all_read_text_tags]
    print(f'**Total essays on page {page}: {str(len(all_essay_links))}')
    for essay_link in all_essay_links:
        html_s2 = requests.get(essay_link).text
        soupy = BeautifulSoup(html_s2, 'lxml')
        text_extracted = soupy.find('div', attrs={'class': 'content_doc'}).text
        essay_title = soupy.find('li', attrs={'class': 'active'}).text
        essay_title = re.sub(r'[\\/*?:"<>|]', "", essay_title)
        if len(essay_title) > 200:
            essay_title = essay_title[:200]
        print('------------------------------')
        print(essay_title)
        try:
            os.mkdir(keyword)
        except FileExistsError:
            pass
        with open(f'{keyword}\\{essay_title}.txt', 'w', encoding='utf-8') as fp:
            fp.write(text_extracted)

print('------------------------------')
print('>>DONE!!')