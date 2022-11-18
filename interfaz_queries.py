from tkinter import *
import pandas as pd
import tweepy

raiz = Tk()
raiz.title("Interfaz Queries")
raiz.config(bg='gray', bd=5, relief='groove')
raiz.geometry('1010x150')
raiz.resizable(False,False)

raiz.columnconfigure(0, weight=1)
raiz.rowconfigure(0, weight=1)

raiz.columnconfigure(0, weight=1)
raiz.rowconfigure(1, weight=1)

raiz.columnconfigure(0, weight=1)
raiz.rowconfigure(2, weight=1)

frame1 = Frame(raiz, bg='gray26')
frame1.grid(column=0, row=0, sticky='nsew')
frame2 = Frame(frame1, bg='gray26')
frame2.grid(column=0, row=1, sticky='nsew')
frame3 = Frame(frame1)
frame3.grid(column=0, row=2, sticky='nsew')

frame1.columnconfigure(0, weight=1)
frame1.rowconfigure(0, weight=1)

frame2.columnconfigure(0, weight=1)
frame2.rowconfigure(0, weight=1)

frame3.columnconfigure(0, weight=1)
frame3.rowconfigure(0, weight=1)

frame3.columnconfigure(1, weight=1)
frame3.rowconfigure(0, weight=1)


def generarQuery():
    bearer_token = bt.get()
    query = x.get()
    path = ''
    print(bearer_token)
    client = tweepy.Client(bearer_token=bearer_token)
    
    response = pd.DataFrame(client.search_recent_tweets(query=query, max_results=100))
    response.to_csv(path, header=None, index=None, sep=',', mode='w')
    
    



# button
boton2 = Button(frame2, text='Generar Archivos',  bg='brown', fg='white', font=('helvetica', 9, 'bold'),command=generarQuery)
boton2.grid(column=0, row=0, sticky='nsew', padx=10, pady=10)




# BEARER_TOKEN
label2 = Label(frame3, text='Bearer Token:')
label2.grid(column=0,row=2,sticky='new',padx=10,pady=10)

bt = Entry(frame3, width=5)
bt.grid(column=1,row=2,sticky='nsew',padx=10,pady=10)

# Query
label3 = Label(frame3, text='Query:')
label3.grid(column=0,row=3,sticky='new',padx=10,pady=10)

x = Entry(frame3, width=5)
x.grid(column=1,row=3,sticky='nsew',padx=10,pady=10)


raiz.mainloop()