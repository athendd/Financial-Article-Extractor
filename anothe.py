import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pandas as pd
from collections import OrderedDict
import spacy
import mysql.connector
from mysql.connector import Error
from transformers import pipeline
import os 
import numpy as np

def connect_to_server(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(host = host_name, user = user_name, password = user_password)
        
    except Error as e:
        print(f"The error {e} occurred")
    return connection
        
def connect_database(host, user, password, db_name):
    database_connection = None
    try:
        database_connection = mysql.connector.connect(host = host, user = user, password = password, database = db_name)
    except Error as e:
        print(f"Error {e} occurred while connecting to the databse")
    return database_connection

def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()
    return result is not None


def find_author(soup):
    div = soup.find('div', class_ = 'caas-attr-item-author')
    if div:
        author = div.find('span', class_ = 'caas-author-byline-collapse')
        if author:
            return author.text.strip()
        
        else:
            return None
    else:
        return None
    
def find_title(soup):
    title = soup.find('div', class_ = 'caas-title-wrapper')
    if title:
        return title.text.strip()
    else:
        return None

def find_time(soup):
    div = soup.find('div', class_ = 'caas-attr-time-style')
    if div:
        time = div.find('time')
        if time:
            return time.text.strip()
        else:
            return None
    else:
        return None
    
def find_body(soup):
    summarizer = pipeline("summarization")
    article_body = soup.find('div', class_ = 'caas-body')
    if article_body:
        summary = summarizer(article_body.text.strip(), max_length=200, min_length=50, do_sample=False)
        quick_summary = summary[0]['summary_text']
        if quick_summary:
            return article_body.text.strip(), quick_summary.strip()
        else:
            return article_body.text.strip(), None
    else:
        return None, None
    
def find_stocks(soup):
    fin_ticker_elements = soup.find_all('fin-ticker')
    if fin_ticker_elements:
        stocks = {}
        for stock in fin_ticker_elements:
            symbol = stock['symbol']
            if '^' in symbol:
                symbol = symbol.replace('^', '%5E')
            link = f'https://finance.yahoo.com/quote/{symbol}'
            third_response = requests.get(link)
            if third_response:
                third_soup = BeautifulSoup(third_response.content, 'html.parser')
                stocks[symbol] = find_stock(third_soup)
    else:
        return None
    return stocks
            
def find_stock(third_soup):
    stock_dic = {}
    Company_name = third_soup.find('h1', class_ = 'svelte-3a2v0c').text.split('(')[0]
    stock_dic['name'] = Company_name
    Current_Price = third_soup.find('fin-streamer', class_ = 'livePrice svelte-mgkamr').text
    stock_dic['price'] = Current_Price
    
    containers = third_soup.find('div', {'data-testid': 'quote-statistics'})
    labels = containers.find_all('span', class_ = 'label svelte-tx3nkj')
    values = containers.find_all('span', class_ = 'value svelte-tx3nkj')
    for i in range(len(values)):
        if values[i].text == '--':
            value = None
        value = values[i].text
        label = labels[i].text
        
        stock_dic[label] = value
    
    return stock_dic


def extract_sentences(text, company):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentence = ''
    for sent in doc.sents:
        if company in sent.text:
            sentence = sent.text
    return sentence

def contains_integer(s):
    for c in s:
        if c.isdigit():
            return True
    return False


url = "https://finance.yahoo.com/"
response = requests.get(url)
soup = BeautifulSoup(
        response.content, 
        'html.parser')
article_urls = soup.find_all('a', href=lambda href: href and href.startswith('https://finance.yahoo.com/news/'))
article_urls = set(article_urls)
article_dic = {}
all_stocks = {}
article_dic['link'] = []
article_dic['author'] = []
article_dic['title'] = []
article_dic['time'] = []
article_dic['sum_body'] = []
article_dic['stocks'] = []
counter = 0
for url in article_urls:
    if url['href'] == 'https://finance.yahoo.com/news/':
        continue
    if counter == 3:
        break
    link = url['href']
    article_dic['link'].append(url['href'])
    second_response = requests.get(link)
    second_soup = BeautifulSoup(second_response.content, 'html.parser')

    article_dic['author'].append(find_author(second_soup))
    article_dic['title'].append(find_title(second_soup))
    article_dic['time'].append(find_time(second_soup))    
    body, sum_body = find_body(second_soup)
    article_dic['sum_body'].append(sum_body)
    stock_info = find_stocks(second_soup)
    
    if stock_info:
        stocks = list(stock_info.keys())
        total_stocks = [stock.replace('%5E', '') for stock in stocks]
        result = ', '.join(total_stocks)
        article_dic['stocks'].append(result)
    else:
        article_dic['stocks'].append(None)
    if stock_info and body:
        for stock in stock_info.keys():
            if stock_info[stock]['name']:
                if contains_integer(stock_info[stock]['name']):
                   stock_name = stock_info[stock]['name']
                else: 
                    stock_name = stock_info[stock]['name'].split(' ')[0]
                stock_info[stock]['sentence'] = stock_sentences = extract_sentences(body, stock_name)
        all_stocks.update(stock_info)
    
    counter += 1
    

stock_df = pd.DataFrame(all_stocks)
stock_df.replace('--', np.nan, inplace=True)
one = stock_df.transpose()

if os.path.exists(r'C:\Users\thynnea\Downloads\stocks.csv'):
    one.to_csv(r'C:\Users\thynnea\Downloads\stocks.csv', mode= 'a', index = False, header = False)
else:
    one.to_csv(r'C:\Users\thynnea\Downloads\stocks.csv', index = False)

df = pd.DataFrame(article_dic)
if os.path.exists(r'C:\Users\thynnea\Downloads\articles.csv'):
    df.to_csv(r'C:\Users\thynnea\Downloads\articles.csv', mode = 'a', index = False, header = False)
else:
    df.to_csv(r'C:\Users\thynnea\Downloads\articles.csv', index=False, header = True)
    
df['time'] = pd.to_datetime(df['time'], format = '%a, %b %d, %Y, %I:%M %p')

df.drop('sum_body', axis = 1, inplace = True)

connection = connect_to_server("localhost", "root", "Password")
if connection != None:
    db_name = "Financial_Information"
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

    cursor.close()
    connection.close()
    database_connection = connect_database("localhost", "root", "Password", db_name)
    if database_connection is not None:
        database_cursor = database_connection.cursor()
        table_name = "Newspapers"
        #data_tuples = [tuple(row) for row in df.itertuples(index = False)]
        if not table_exists(database_cursor, table_name):
            table_query ="""
            CREATE TABLE Newspapers(
                id INT AUTO_INCREMENT PRIMARY KEY,
                link VARCHAR(255),
                author VARCHAR(255),
                title VARCHAR(255),
                time DATETIME, 
                stocks VARCHAR(255))"""
            
            
            database_cursor.execute(table_query)
            database_connection.commit()
        
        data_tuples = list(df.itertuples(index=False, name=None))
        database_cursor.executemany("""
        INSERT INTO Articles (link, author, title, time, stocks) VALUES (%s, %s, %s, %s, %s)
        , data_tuples""")
        database_connection.commit()
        database_cursor.close()
        database_connection.close()
