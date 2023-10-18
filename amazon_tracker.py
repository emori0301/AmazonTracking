import tkinter as tk
from tkinter import Label, Entry, Button
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import webbrowser
import time

# Tkinterウィンドウを作成
window = tk.Tk()
window.title("Amazon検索アプリ")
window.geometry("800x600")  # ウィンドウサイズを500x500に設定

# ウェブスクレイピング関数
def search_amazon():
    global keyword
    keyword = keyword_entry.get()
    amazonTrackingPrice()

def open_amazon():
    webbrowser.open('https://www.amazon.co.jp/')

def amazonTrackingPrice():
    global result_labels, price_labels, intPrice
    amazonPage = requests.get(keyword)
    soup = BeautifulSoup(amazonPage.content, "html.parser")

    title = soup.find(id="productTitle").get_text()
    price = soup.find_all("span", class_="a-price-whole")
    # price = soup.find_all("span", class_="a-size-base")
    first_price = price[0]
    convertedPrice = first_price.get_text()
    convertedPrice = convertedPrice.replace("￥", "").replace(",", "").replace(' ', "")
    # convertedPrice = convertedPrice[:len(convertedPrice) // 2]
    # intPrice = int(convertedPrice)
    # result_labels = Label(window, text=title) 
    # result_labels.pack()
    # price_labels = Label(window, text=f"現在の価格：{intPrice}円") 
    # price_labels.pack()
    # choice_line()
    # repeat()

    if convertedPrice:
        intPrice = int(convertedPrice)
        result_labels = Label(frame_2, text=title, wraplength=350, anchor=tk.W ) 
        result_labels.place(x=10, y=180)
        price_labels = Label(frame_2, text=f"現在の価格：{intPrice}円") 
        price_labels.place(x=20, y=240)
        choice_line()
        repeat()
    else:
        failure_labels = Label(frame_2, text="価格情報を取得できませんでした") 
        failure_labels.pack()

# いいえボタンがクリックされたときの処理
def clear_text():
    keyword_entry.delete(0, tk.END)  
    result_labels.destroy()
    price_labels.destroy()
    line_labels.destroy()
    OK_button.destroy()
    NO_button.destroy()

def choice_line():
    global OK_button, NO_button, line_labels
    line_labels = Label(window, text="LINEに価格が希望額を下回ったら通知するようにしますか？") 
    line_labels.place(x=20, y=360)
    OK_button = Button(window, text="はい", command=choice_line_ok)
    OK_button.place(x=20, y=390)
    NO_button = Button(window, text="いいえ", command=clear_text)
    NO_button.place(x=80, y=390)

def choice_line_ok():
    global Asking_price
    Asking_price = Entry(window)
    Asking_price.place(x=20, y=440)
    setting_button = Button(window, text="この金額を希望する", command=completed)
    setting_button.place(x=230, y=440)

def completed():
    Ask_price = Asking_price.get()
    line_result = Label(window, text="LINE通知を設定しました!") 
    line_result.place(x=20, y=480)

    if(intPrice < int(f"{Ask_price}")):
        sendLineNotify()

def sendLineNotify():
    lineNotifyToken = "24wEN0pc0jSP9n0G0IYs3fCGucZCoTRcQwcB2Nm3M7a"
    lineNotifyApi = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {lineNotifyToken}"}
    data = {"message": f"今がお買い時です!{ keyword }"}
    requests.post(lineNotifyApi, headers=headers, data=data)

def repeat():
    amazonTrackingPrice()
    window.after(60000, repeat)  # 60000ミリ秒（＝60秒）後に再度実行

frame_1 = tk.Frame(window, width=800, height=75, bd=4, relief=tk.GROOVE)
frame_2 = tk.Frame(window, width=400, height=525, bd=4, relief=tk.GROOVE)
frame_3 = tk.Frame(window, width=400, height=525, bd=4, relief=tk.GROOVE)
frame_1.grid(row=0, column=0, columnspan=2, sticky=tk.W + tk.E)
frame_2.grid(row=1, column=0)
frame_3.grid(row=1, column=1, sticky=tk.N + tk.S)

title_label = tk.Label(frame_1, fg="red" ,font=("Menlo",50), text="Amazon Price Tracker")
title_label.place(x=65)
first_label = tk.Label(frame_2, font=("Menlo",20), text="1.Amazonで調べる", wraplength="300" ,anchor=tk.W )
first_label.place(x=15,y=0, width=300, height=50)
amazon_button = tk.Button(frame_2, font=("Menlo",15), text="Amazonを開く", command=open_amazon)
amazon_button.place(x=20, y=50)

# キーワード入力用のテキストボックス
keyword_label = tk.Label(frame_2, font=("Menlo",20), anchor=tk.W , text="2.Amazon商品URLを貼る", wraplength="350" )
keyword_label.place(x=15,y=100, width=300, height=30)
keyword_entry = Entry(frame_2, font=("Menlo",20))
keyword_entry.place(x=20, y=140)

# 検索ボタン
search_button = Button(frame_2,  font=("Menlo",15), text="検索", command=search_amazon)
search_button.place(x=310, y=145)

# while(True):
#     amazonTrackingPrice()
#     time.sleep(60*60)
    
window.mainloop()





# https://www.amazon.co.jp/%E3%82%B7%E3%82%B4%E3%83%88%E3%81%8C%E3%81%AF%E3%81%8B%E3%81%A9%E3%82%8B-Python%E8%87%AA%E5%8B%95%E5%87%A6%E7%90%86%E3%81%AE%E6%95%99%E7%A7%91%E6%9B%B8-%E3%82%AF%E3%82%B8%E3%83%A9%E9%A3%9B%E8%A1%8C%E6%9C%BA/dp/4839973857/ref=sr_1_16?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=33WJ2GGAOMFHD&keywords=python&qid=1697484614&sprefix=python%2Caps%2C196&sr=8-16


    