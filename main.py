from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

""" product_category = int(input(
    "Lütfen bir kategori numarası girin: Ürün kategorileri: \n1- Beyaz Eşya \n2- Ankastre \n3- Elektronik \n4- Isıtma-Soğutma \n5- Küçük Ev Aletleri \n6- Su Arıtma \n7- Tamamlayıcı Ürünler \n"))


def switch(product_category):
    switcher = {1: "Beyaz Eşya",

                2:
                "Ankastre",

                3:
                "Elektronik",

                4:
                "Isıtma-Soğutma",

                5:
                "Küçük Ev Aletleri",

                6:
                "Su Arıtma",

                7:
                "Tamamlayıcı ürünler",
                }
    return switcher.get(product_category, "Yanlış girdi!")


product_category = switch(product_category) 

topic_items = BeautifulSoup(requests.get("https://destekvebilgimerkezi.arcelik.com.tr/s/", verify = False).content, 'lxml').findAll('li', {'class': 'topicItem forceTopicFeaturedTopicItem'})
topic_labels = BeautifulSoup(requests.get("https://destekvebilgimerkezi.arcelik.com.tr/s/", verify = False).content, 'lxml').findAll('div', {'class': 'topicLabel'})
"""

user_name = input('Merhaba ben Hamdi. Bana Vikipedi\'deki makalelerde geçen bilgilerle ilgili sorularını sorabilirsin! Adını öğrenebilir miyim: ')
def get_search_link(search_keyword = input("Ne aramak istersin?: ")):
    links = []
    #search_keyword = re.sub(r"[^\w\s]", '', search_keyword)
    search_keyword = re.sub(r"\s+", '_', search_keyword)

    try:
        search_link = "https://tr.wikipedia.org/w/index.php?search=" + search_keyword + "&title=%C3%96zel%3AAra&go=Git&ns0=1"
        results = BeautifulSoup(requests.get(search_link).content, 'lxml').findAll(
        'li', {'class': 'mw-search-result'})

        for result in results:
            link = "https://tr.wikipedia.org" + result.find('a')['href']
            links.append(link)

        article_link = links[0]

    except:
        article_link = "https://tr.wikipedia.org/wiki/" + search_keyword

    return article_link

def get_article(article_link):
    
    article = Article(article_link)
    article.download()
    article.parse()
    article.nlp()

    return article.text



def index_sort(liste):
    length = len(liste)
    list_index = list(range(0, length))

    x = liste
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index


def response_greet(article_text):
    article_text = article_text.lower()

    bot_greetings = ['hi', 'hey', 'hello', 'hey there', 'selam', 'merhaba', 'wassup']
    user_greetings = ['hi', 'hey', 'hello', 'hey there', 'selam', 'merhaba']

    for word in article_text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ""
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_score = cosine_similarity(cm[-1], cm)
    similarity_score_list = similarity_score.flatten()
    index = index_sort(similarity_score_list)[1:]
    isKnown = False

    j = 0

    for i in range(len(index)):
        if similarity_score_list[index[i]] > 0.0:
            bot_response = bot_response + ' ' + sentence_list[index[i]]
            isKnown = True
            j = j+1
        if j > 2:
            break

    if not isKnown:
        bot_response = bot_response + ' ' + 'Özür dilerim, anlayamadım. Farklı kelimelerle tekrar sorar mısın?'

    sentence_list.remove(user_input)

    return bot_response






exit_loop = ['çıkış', 'kapat', 'bitir', 'güle güle', 'hadi bb']

def create_sentence_list():
    try:
        sentence_list = nltk.sent_tokenize(get_article(get_search_link()))
        print("Bilgileri öğrendim, şimdi sorabilirsin!")
    except:
        print("Bir hata oluştu, yeniden dener misin?")
        create_sentence_list()
    return sentence_list

sentence_list = create_sentence_list()

while(True):
    user_input = input("{}: ".format(user_name))
    if user_input.lower() in exit_loop:
        print('Hamdi kaçar!')
        break
    else:
        if response_greet(user_input) != None:
            print('Hamdi: ' + response_greet(user_input))
        else:
            print('Hamdi: ' + bot_response(user_input))

