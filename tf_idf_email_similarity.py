# -*- coding: utf-8 -*-

# импортируем библиотеки
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial import distance
import pandas as pd
import random


def generate_email(alph, domains):
    # 1 символ- буква или цифра
    email = random.choice(alph[:alph.index('.')])
    email += ''.join(random.choice(alph) for i in range(random.choice(range(4, 12))))

    # последний символ- буква или цифра
    email += random.choice(alph[:alph.index('.')])

    # добавляем @ и доменное имя
    email += '@' + random.choice(domains)
    return email


def generate_susp_emails(email, n=5):
    start = random.randint(0, 1000)
    login = email[:email.index('@')]
    domain = email[email.index('@'):]

    susp_emails = []
    for i in range(n):
        tmp = login
        tmp += str(start + i) + domain
        susp_emails.append(tmp)
    return susp_emails


def clean_email(email):
    return email[:email.index('@')]


def vectorize(vectorizer, emails, target):
    clean_emails = list(map(clean_email, emails))
    x = vectorizer.fit_transform(clean_emails)
    y = vectorizer.transform([clean_email(target)])

    return x.toarray(), y.toarray()


if __name__ == '__main__':
    domains = ["hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.ru", "yahoo.com"]
    alph = 'abcdefghijklmnopqrstuvwxyz1234567890._-'

    # предположим, обладатель ящика 'mmashnka11@gmail.com' - читер
    # и наша задача- найти похожие ящики в большом корпусе email-ов

    # сгенерим 10000 email-ов
    emails = [generate_email(alph, domains) for _ in range(10000)]

    # сгенерим 10 похожих (но не идеально) на подозрительный 
    susp_emails = generate_susp_emails('mashenka@mail.com', n=10)

    # добавим их к изначальным 
    emails.extend(susp_emails)

    # получаем вектора
    vectorizer = TfidfVectorizer(ngram_range=(2, 6), max_features=100000, analyzer='char')
    x, y = vectorize(vectorizer, emails, 'mmashnka11@gmail.com')

    # cчитаем косинусные расстояния
    distances = []
    for i in x:
        distances.append(1 - distance.cosine(i, y))

    # сводим результат в удобном формате
    final = pd.DataFrame({'email': emails, 'susp_rate': distances})
    print(final.sort_values(by='susp_rate', ascending=False).head(15))
