import requests
from bs4 import BeautifulSoup
import TextSummarizer
import pandas as pd
import numpy as np
import spacy
import mysql.connector
from mysql.connector import Error
import os

nlp = spacy.load("en_core_web_sm")

def connect_to_server(host, user, password):
    try:
        return mysql.connector.connect(host=host, user=user, password=password)
    except Error as e:
        print(f"Connection error: {e}")
        return None

def connect_database(host, user, password, db_name):
    try:
        return mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    except Error as e:
        print(f"DB connection error: {e}")
        return None

def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None

def find_author(soup):
    tag = soup.select_one('div.caas-attr-item-author span.caas-author-byline-collapse')
    return tag.text.strip() if tag else None

def find_title(soup):
    tag = soup.select_one('div.caas-title-wrapper')
    return tag.text.strip() if tag else None

def find_time(soup):
    tag = soup.select_one('div.caas-attr-time-style time')
    return tag.text.strip() if tag else None

def find_body(soup):
    body_tag = soup.select_one('div.caas-body')
    if body_tag:
        full_text = body_tag.text.strip()
        summary = TextSummarizer.perform_textrank(full_text)
        return full_text, summary
    return None, None

def contains_integer(s):
    return any(char.isdigit() for char in s)

def extract_sentences(text, company):
    doc = nlp(text)
    for sent in doc.sents:
        if company in sent.text:
            return sent.text
    return None

def find_stock_info(symbol):
    stock_url = f'https://finance.yahoo.com/quote/{symbol}'
    response = requests.get(stock_url)
    if not response.ok:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    stock_data = {}

    try:
        stock_data['name'] = soup.select_one('h1.svelte-3a2v0c').text.split('(')[0].strip()
        stock_data['price'] = soup.select_one('fin-streamer.livePrice').text
    except Exception:
        return None

    stats_container = soup.select_one('div[data-testid="quote-statistics"]')
    if stats_container:
        labels = stats_container.select('span.label')
        values = stats_container.select('span.value')
        for label, value in zip(labels, values):
            stock_data[label.text] = value.text if value.text != '--' else None

    return stock_data

def find_stocks(soup):
    stocks = {}
    for tag in soup.find_all('fin-ticker'):
        symbol = tag.get('symbol', '')
        symbol_url = symbol.replace('^', '%5E')
        stock_info = find_stock_info(symbol_url)
        if stock_info:
            stocks[symbol] = stock_info
    return stocks if stocks else None

def scrape_yahoo_articles(limit=3):
    base_url = "https://finance.yahoo.com/"
    soup = BeautifulSoup(requests.get(base_url).content, 'html.parser')
    links = set(a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('https://finance.yahoo.com/news/') and a['href'] != 'https://finance.yahoo.com/news/')

    articles = {
        'link': [], 'author': [], 'title': [], 'time': [],
        'sum_body': [], 'stocks': []
    }
    all_stocks = {}
    
    for i, link in enumerate(links):
        if i >= limit:
            break

        article_soup = BeautifulSoup(requests.get(link).content, 'html.parser')
        body, summary = find_body(article_soup)
        stock_info = find_stocks(article_soup)

        articles['link'].append(link)
        articles['author'].append(find_author(article_soup))
        articles['title'].append(find_title(article_soup))
        articles['time'].append(find_time(article_soup))
        articles['sum_body'].append(summary)
        articles['stocks'].append(', '.join([s.replace('%5E', '') for s in stock_info]) if stock_info else None)

        if stock_info and body:
            for symbol, data in stock_info.items():
                company = data['name']
                name_for_search = company if contains_integer(company) else company.split(' ')[0]
                data['sentence'] = extract_sentences(body, name_for_search)
            all_stocks.update(stock_info)

    return pd.DataFrame(articles), pd.DataFrame(all_stocks).T

def save_to_csv(df, path):
    header = not os.path.exists(path)
    df.to_csv(path, mode='a', header=header, index=False)

def save_to_mysql(df, db_name, table_name, host="localhost", user="root", password="Password"):
    conn = connect_to_server(host, user, password)
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    conn.close()

    db_conn = connect_database(host, user, password, db_name)
    if not db_conn:
        return

    db_cursor = db_conn.cursor()
    if not table_exists(db_cursor, table_name):
        db_cursor.execute(f"""
        CREATE TABLE {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            link TEXT,
            author VARCHAR(255),
            title TEXT,
            time DATETIME,
            stocks TEXT
        )""")

    df['time'] = pd.to_datetime(df['time'], format='%a, %b %d, %Y, %I:%M %p', errors='coerce')
    df = df.drop(columns=['sum_body'], errors='ignore')
    tuples = list(df.itertuples(index=False, name=None))

    db_cursor.executemany(
        f"INSERT INTO {table_name} (link, author, title, time, stocks) VALUES (%s, %s, %s, %s, %s)",
        tuples
    )
    db_conn.commit()
    db_cursor.close()
    db_conn.close()

if __name__ == "__main__":
    article_df, stock_df = scrape_yahoo_articles(limit=3)

    save_to_csv(stock_df.replace('--', np.nan), r'C:\Users\thynnea\Downloads\stocks.csv')
    save_to_csv(article_df, r'C:\Users\thynnea\Downloads\articles.csv')
    save_to_mysql(article_df, db_name="Financial_Information", table_name="Articles")
