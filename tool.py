import psycopg2
from heapq import nlargest


def execute(q):
    db = psycopg2.connect(database="news")
    c = db.cursor()
    query = q
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def get_views_for_articles(slugs):
    views = 0
    for slug in slugs:
        slug = str(slug[0])
        res = execute("SELECT COUNT(*) FROM log WHERE path LIKE '%"+slug+"';")
        views += res[0][0]
    return views


def get_most_popular_three_articles():
    print('Q1: What are the most popular three articles of all time?')
    slugs = execute("SELECT slug FROM articles;")
    dictionary = {}
    for slug in slugs:
        dictionary[slug[0]] = get_views_for_articles([slug])
    most_popular_three_articles = nlargest(3, dictionary, key=dictionary.get)
    for slug in most_popular_three_articles:
        numberOfViews = dictionary[slug]
        at = execute("SELECT title FROM articles WHERE slug LIKE '"+slug+"';")
        print("* ", at[0][0], " - ", numberOfViews, " views.")


def get_most_popular_article_authors():
    print('Q2: Who are the most popular article authors of all time?')
    ids_names = execute("SELECT id, name FROM authors;")
    for id_name in ids_names:
        id = str(id_name[0])
        slugs = execute("SELECT slug FROM articles WHERE author = '"+id+"'")
        print(id_name[1], ": ", get_views_for_articles(slugs), " views.")


def get_percentage(date):
    date = str(date[0])
    all_requests = execute("SELECT * FROM log WHERE DATE(time) = '"+date+"';")
    q = "SELECT * FROM log WHERE DATE(time)='"+date+"'and status != '200 OK';"
    w_e = execute(q)
    return float(len(w_e))/len(all_requests)


def get_days_have_error_more_than_1_per():
    print('Q3: On which days did more than 1% of requests lead to errors?')
    dates = execute("SELECT DISTINCT DATE(time) FROM log;")
    requests_w_more_than_1_error = {}
    for date in dates:
        percentage = get_percentage(date)
        if percentage > 0.01:
            requests_w_more_than_1_error[date] = percentage
    for (key, value) in requests_w_more_than_1_error.items():
        print(str(key[0]), ": %", value)


get_most_popular_three_articles()
print()
get_most_popular_article_authors()
print()
get_days_have_error_more_than_1_per()
