#!pip install pandas
#!pip install tkinter
#!pip install tweepy
from tkinter import *
import pandas as pd
import tweepy
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk

CONSUMER_KEY = "BzmQkPjmwVdpYtoBOlMmYCaor"
CONSUMER_SECRET = "WVlZoN5kUE05niRYk6gyPF63qv7DczJzsgQcKEgmAVL5NlIhvl"
ACCESS_TOKEN = "870460343214100482-ACSdXsX9oIepo8qFC6FMmVTsu3Htj8B"
ACCESS_TOKEN_SECRET = "nEzPFnX9FDZt5CMV45SwURVKivArlxkSygANtVse2AoXS"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFaYfwEAAAAASTuGw59A5DxWQkgDFmjIlANs0Mk%3DAmnkAhCAr2gGw0nnpL3GmhdDKzzYnUdREUHBHyIfkdZVO0a1jR"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

raiz = Tk()
raiz.title("Interfaz Queries")
raiz.config(bg='gray', bd=5, relief='groove')

raiz.geometry('1510x550')
raiz.resizable(True,True)

raiz.columnconfigure(0, weight=1)
raiz.rowconfigure(0, weight=1)

raiz.columnconfigure(0, weight=1)
raiz.rowconfigure(1, weight=1)

raiz.columnconfigure(0, weight=1)
raiz.rowconfigure(2, weight=1)



frame1 = Frame(raiz, bg='gray26')
#frame1.grid(column=0, row=0, sticky='nsew')
frame1.pack(fill="both", expand=True)
frame2 = Frame(frame1, bg='gray26')
#frame2.grid(column=0, row=1, sticky='nsew')
frame2.pack(fill="both", expand=True)
frame3 = Frame(frame1)
#frame3.grid(column=0, row=2, sticky='nsew')
frame3.pack(fill="both", expand=True)

frame4 = Frame(frame1)
frame4.pack(fill='both', expand=True )

frame1.columnconfigure(0, weight=1)
frame1.rowconfigure(0, weight=1)

frame2.columnconfigure(0, weight=1)
frame2.rowconfigure(0, weight=1)

frame3.columnconfigure(0, weight=1)
frame3.rowconfigure(0, weight=1)

frame2.columnconfigure(1, weight=1)
frame2.rowconfigure(0, weight=1)


def generarQuery():

    query = str(x.get() + ' -RT')
    client = tweepy.Client(bearer_token = BEARER_TOKEN)
    tweets = []
    
    '''
    if(ubi_colombia.get() == 1):
        #lat, long, radius = 4.6097100, -74.0817500, "1000km"
        #response = client.search_recent_tweets(query=query, max_results=100, exclude_retweets=exclude_retweets, exclude_replies=exclude_replies, geocode=f"{lat},{long},{radius}", lang=lang)
    else:
        #response = client.search_recent_tweets(query=query, max_results=100, exclude_retweets=exclude_retweets, exclude_replies=exclude_replies, lang=lang)
        #response = client.search_recent_tweets(query=query, max_results=100)
    '''

    print(query)
    response = client.search_recent_tweets(query=query, expansions=['author_id'] ,user_fields = ['location', 'username', 'description', 'public_metrics', 'verified'], tweet_fields = ['author_id','created_at', 'public_metrics'], max_results=100)

    for tweet in response.data:
        tweets.append(tweet)

    data = {
        "author_id": [tweet.author_id for tweet in tweets],
        "username" : [tweet['username'] for tweet in response.includes['users']],
        "author_followers_count" : [tweet['public_metrics']['followers_count'] for tweet in response.includes['users']],
        "author_following_count" : [tweet['public_metrics']['following_count'] for tweet in response.includes['users']],
        "author_tweet_count" : [tweet['public_metrics']['tweet_count'] for tweet in response.includes['users']],
        "author_description" : [tweet['description'] for tweet in response.includes['users']],
        "author_verified" : [tweet['verified'] for tweet in response.includes['users']],
        "author_location" : [tweet['location'] for tweet in response.includes['users']],
        "text": [tweet.text for tweet in tweets],
        "created_at": [tweet.created_at for tweet in tweets],
        "retweet_count": [tweet.public_metrics['retweet_count'] for tweet in tweets],
        "reply_count": [tweet.public_metrics['reply_count'] for tweet in tweets],
        "like_count": [tweet.public_metrics['like_count'] for tweet in tweets],
        "quote_count": [tweet.public_metrics['quote_count'] for tweet in tweets],
        "impression_count": [tweet.public_metrics['impression_count'] for tweet in tweets],
    }

    # Imprimir resultado
    global df
    for key,value in data.items():
        while(len(data[key]) < 100):
            data[key].append('Sin información') 

    df = pd.DataFrame(data)
    df.fillna(value = 'Sin información', inplace=True)
    # Crear el ttk.Treeview

    tree = ttk.Treeview(frame4)
    tree["columns"] = list(df.columns)

    # Agregar los encabezados de columna
    for col in df.columns:
            tree.heading(col, text=col)

    # Agregar los datos al treeview
    for i, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    # Agregar scroll horizontal al treeview
    hscroll = ttk.Scrollbar(frame4, orient='horizontal', command=tree.xview)
    hscroll.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=hscroll.set)

    # Mostrar el ttk.Treeview
    tree.pack(expand=True, fill="both")
    

    
    
def descargarTweets():
    df.to_csv('datos.txt', sep='\t', index=False)


# button generar tweets
boton2 = Button(frame2, text='Generar Busqueda',  bg='brown', fg='white', font=('helvetica', 9, 'bold'),command=generarQuery)
boton2.pack(pady=10)

# button descargar tweets
boton3 = Button(frame4, text='Descargar Tweets',  bg='brown', fg='white', font=('helvetica', 9, 'bold'),command=descargarTweets)
boton3.pack(pady=10)

# Query
label3 = Label(frame3, text='Que desea buscar?')
label3.pack(pady=10)

x = Entry(frame3, width=5)
x.pack(pady=10, ipadx=200)

# checkbox
# retweet
retweet = tk.IntVar()
checkbox_retweet = tk.Checkbutton(frame3, text="Tweets originales (Que no sean retweet)", variable=retweet)
checkbox_retweet.pack(pady=10)

# Ubicación Colombia
ubi_colombia = tk.IntVar()
checkbox_ubi_colombia = tk.Checkbutton(frame3, text="Que se hayan generado únicamente en Colombia", variable=ubi_colombia)
checkbox_ubi_colombia.pack(pady=10)

# Idioma
idioma = tk.IntVar()
checkbox_idioma = tk.Checkbutton(frame3, text="Tweets únicamente en Español", variable=idioma)
checkbox_idioma.pack(pady=10)


raiz.mainloop()