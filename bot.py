import telebot
import requests
from bs4 import BeautifulSoup
import time
import pitchfork_api


def post_news(title):
    link = title.parent.get('href')
    post = '#Pitchfork_News\n' + '"' + title.text.strip() + '"\n' + 'https://pitchfork.com' + link
    bot.send_photo(channel_id, title.parent.parent.parent.find('img').get('src'), caption=post)


def post_review(title):
    album_title = title.text.strip()
    artist = title.parent.find('li').text.strip()
    try:
        score = str(pitchfork_api.search(artist, album_title).score())
    except:
        score = 'N/A'
    post = '#Pitchfork_Reviews\n' + 'Исполнитель - ' + artist + '\n' + 'Альбом - ' + album_title + '\n' + 'Жанр - '
    post += title.parent.parent.parent.find_all('ul')[1].text.strip() + '\n'
    post += 'Оценка - ' + score + '\n' + 'Ссылка - ' + 'https://pitchfork.com' + title.parent.parent.get('href')
    bot.send_photo(channel_id, title.parent.parent.find('div').find('img').get('src'), caption=post)


def post_rs_news(title):
    if title.text.strip() != 'Latest News':
        post = '#Rolling_Stone_News\n"' + title.text.strip() + '"\n' + title.parent.find('p').text.strip()
        post += '\n' + title.parent.parent.get('href')
        bot.send_photo(channel_id, title.parent.parent.find('img').get('data-src'), caption=post)


def post_nme_news(title):
    post = '#NME_News\n'
    post += '"' + title.find('a').get('title') + '"\n' + title.parent.find('div', 'td-excerpt').text.strip() + '\n'
    post += title.find('a').get('href')
    bot.send_photo(channel_id, title.parent.parent.find('span').get('data-img-retina-url'), caption=post)


key = open('API_KEY.txt').read()
channel_id = '-1001461696042'
bot = telebot.TeleBot(key)
last_title = open('last_title.txt').read().strip().replace(u'\xa0', u' ')
last_r_title = open('last_r_title.txt').read().strip().replace(u'\xa0', u' ')
rs_last_title = open('rs_last_title.txt').read().strip().replace(u'\xa0', u' ')
nme_last_title = open('nme_last_title.txt').read().strip().replace(u'\xa0', u' ')

url = f'https://pitchfork.com/news/'
review_url = f'https://pitchfork.com/reviews/albums/'
rs_url = f'https://www.rollingstone.com/music/'
nme_url = f'https://www.nme.com/news/music'
while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if last_title == '':
        last_title = soup.find('h2').text.strip()
        last_title = last_title.replace(u'\xa0', u' ')

        title_file = open('last_title.txt', 'w')
        title_file.write(last_title)
        title_file.close()

        temp = soup.find_all('h2')
        temp.reverse()
        for title in temp:
            post_news(title)
    else:
        if soup.find('h2').text.strip().replace(u'\xa0', u' ') != last_title:
            previous_last_title = last_title
            last_title = soup.find('h2').text.strip()
            last_title = last_title.replace(u'\xa0', u' ')

            title_file = open('last_title.txt', 'w')
            title_file.write(last_title)
            title_file.close()

            news = soup.find_all('h2')
            news.reverse()

            flag = 0
            for article in news:
                title = article.text.strip()
                title = title.replace(u'\xa0', u' ')
                if flag:
                    post_news(article)
                if title == previous_last_title:
                    flag = 1

    review_response = requests.get(review_url)
    review_soup = BeautifulSoup(review_response.content, 'html.parser')
    if review_soup.find('h2').text.strip().replace(u'\xa0', u' ') != last_r_title:
        prev_r_title = last_r_title
        last_r_title = review_soup.find('h2').text.strip().replace(u'\xa0', u' ')

        r_title_file = open('last_r_title.txt', 'w+')
        r_title_file.write(last_r_title)
        r_title_file.close()

        reviews = review_soup.find_all('h2')
        reviews.reverse()

        flag = 0
        for review in reviews:
            name = review.text.strip()
            name = name.replace(u'\xa0', u' ')
            if flag:
                post_review(review)
            if name == prev_r_title:
                flag = 1

    rs_response = requests.get(rs_url)
    rs_soup = BeautifulSoup(rs_response.content, 'html.parser')
    if rs_soup.find('h3').text.strip().replace(u'\xa0', u' ') != rs_last_title:
        rs_prev_title = rs_last_title
        rs_last_title = rs_soup.find('h3').text.strip().replace(u'\xa0', u' ')

        rs_title_file = open('rs_last_title.txt', 'w+')
        rs_title_file.write(rs_last_title)
        rs_title_file.close()

        rs_news = rs_soup.find_all('h3')[4:13]
        rs_news.reverse()

        flag = False
        for rs_article in rs_news:
            rs_title = rs_article.text.strip().replace(u'\xa0', u' ')
            if flag:
                post_rs_news(rs_article)
            if rs_title == rs_prev_title:
                flag = True

    nme_response = requests.get(nme_url)
    nme_soup = BeautifulSoup(nme_response.content, 'html.parser')
    if nme_soup.find('h3').find('a').get('title').strip().replace(u'\xa0', u' ') != nme_last_title:
        nme_prev_title = nme_last_title
        nme_last_title = nme_soup.find('h3').find('a').get('title').strip().replace(u'\xa0', u' ')

        nme_title_file = open('nme_last_title.txt', 'w+')
        nme_title_file.write(nme_last_title)
        nme_title_file.close()

        nme_news = nme_soup.find_all('h3')[:10]
        nme_news.reverse()

        flag = False
        for nme_article in nme_news:
            nme_title = nme_article.find('a').get('title').strip().replace(u'\xa0', u' ')
            if flag:
                post_nme_news(nme_article)
            if nme_title == nme_prev_title:
                flag = True
    time.sleep(60)
