import tkinter as tk
import sqlite3
import urllib.request
import time
import random
import string
from PIL import ImageTk, Image, ImageSequence
import bs4
import requests
import os
import matplotlib.pyplot as plt
from tkinter import ttk
from ttkthemes import themed_tk as tt
if (os.getcwd != 'TypeIt'):
    try:
        os.mkdir("TypeIt")
    except:
        os.chdir(os.getcwd() + "/TypeIt")
conn = sqlite3.connect("SpeedScores.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Users(
           UserID INTEGER PRIMARY KEY AUTOINCREMENT,
           UserName VARCHAR(20),
           Score INTEGER)""")
cur.execute("""SELECT DISTINCT(UserName) FROM Users""")
alluserlist = cur.fetchall()
cur.execute(
    """SELECT UserName,MAX(Score) FROM Users GROUP BY UserName HAVING UserName <>'Select User' AND Score NOTNULL ORDER BY Score DESC """)
scorelist = cur.fetchall()
highscore_list=list()
highscore_user=list()
for i in scorelist:
    highscore_list.append(i[0])
    highscore_user.append(i[1])
conn.commit()
def img_downloader(a):
    if(a==1):
        urllib.request.urlretrieve(
        'https://i.ibb.co/N3yQkNB/Screenshot-2021-01-28-084757.png', os.getcwd() + '//bgimg.png')
    if(a==2):
        urllib.request.urlretrieve(
        'https://sites.google.com/site/introductiontokeyboardingcmpld/_/rsrc/1330540565295/home/touch-typing/i_fingering_guide.gif', os.getcwd() + '//touchtyping.png')
    if(a==3):
        urllib.request.urlretrieve(
            'https://media.tenor.com/images/8d0e83860667fe684da6a4564f0fe3bd/tenor.gif',os.getcwd() + '//tenor.gif')
if not (os.path.exists(os.getcwd() + 'bgimg.png')):
    img_downloader(1)
if not (os.path.exists(os.getcwd() + 'touchtype.png')):
    img_downloader(2)
if not (os.path.exists(os.getcwd() + 'tenor.gif')):
    img_downloader(3)
with open("words.txt", 'w+') as file:
    if (len(file.readlines()) == 0):
        res = requests.get('https://www.ef.com/wwen/english-resources/english-vocabulary/top-1000-words/')
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        word = soup.select('p')
        x = word[11].getText()
        wordlist = x.split("\r\n\t")
        for i in wordlist:
            file.write(i + "\n")
with open("test_info.txt","r") as file2:
    testinfo=file2.read()
with open("tut_info.txt","r") as file3:
    tutinfo=file3.read()
def splash_screen():
        splash=tk.Tk()
        ws = splash.winfo_screenwidth()
        hs = splash.winfo_screenheight()
        width = (ws / 2) - (300 / 2)
        height = (hs / 2) - (100 / 2)
        splash.geometry('%dx%d+%d+%d' % (220, 100, width, height))
        splash.overrideredirect(True)
        def animate(counter):
            canvas.itemconfig(image, image=sequence[counter])
            splash.after(20, lambda: animate((counter + 1) % len(sequence)))
        canvas = tk.Canvas(splash, width=600, height=200)
        canvas.pack()
        sequence = [ImageTk.PhotoImage(img) for img in
            ImageSequence.Iterator(Image.open('tenor.gif'))]
        image = canvas.create_image(110, 75, image=sequence[0])
        animate(1)
        splash.update()
        splash.after(2175,splash.destroy)
        splash.mainloop()
splash_screen()
home = tt.ThemedTk()
home.get_themes()
home.set_theme('clearlooks')
home.title("type test")
ws = home.winfo_screenwidth()
hs = home.winfo_screenheight()
home.iconbitmap("iconimg.ico")
global height,width
width = (ws /2) - (700 / 2)
height = (hs / 2) - (500 / 2)
home.geometry('%dx%d+%d+%d' % (700, 500, width,height))
bg = ImageTk.PhotoImage(file="bgimg.png")
global bg_label
bg_label = ttk.Label(home, image=bg)
bg_label.place(relheight=1, relwidth=1)
def resize(a):
    global bg, new_bg, final_bg
    bg = Image.open("bgimg.png")
    new_bg = bg.resize((a.width, a.height), Image.ANTIALIAS)
    final_bg = ImageTk.PhotoImage(new_bg)
    bg_label.config(image=final_bg)
home.bind('<Configure>', resize)
def clean_word(word):
    word2 = str()
    word = str(word)
    for i in word:
        if i.isalnum():
            word2 += i
    return word2
with open("words.txt", "r") as f:
    wls = f.readlines()
def meaningful_word_giver(no, lis):
    worlis=[]
    for i in wls:
        if (no == len(i)):
            worlis.append(i)
    ran=random.randrange(0,len(worlis))
    return(worlis[ran])
cur.execute("SELECT UserName from Users")
global user_list
user_list = list(set(cur.fetchall()))
for i in range(len(user_list)):
    user_list[i] = clean_word(user_list[i])
def page1():
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return (result_str)
    def avg_size(l):
        x = random.randint(0, 1)
        if (x == 0):
            return (l - random.randint(0, l // 2))
        else:
            return (l + random.randint(0, l // 2))
    def word_display(t, l, c, n):
        if (t == 1 or t == 3):
            c.set(meaningful_word_giver(avg_size(l), wls).strip("\n"))
            n.set(meaningful_word_giver(avg_size(l), wls).strip("\n"))
        if (t == 2):
            c.set(get_random_string(avg_size(l)))
            n.set(get_random_string(avg_size(l)))
    global c
    c = 0
    def word_check(event):
        global c
        if (text_enter.get().strip() == display_text_cur.get()):
            c += 1
            text_display_label_2.config(bg="green")
            time.sleep(4)
            text_display_label_2.config(bg="blue")
            display_text_prev.set(display_text_cur.get().strip("\n"))
            display_text_cur.set(display_text_next.get().strip("\n"))
            if (word_type_choice.get() == "Random words"):
                display_text_next.set(get_random_string(word_length_choice.get()))
            else:
                display_text_next.set(meaningful_word_giver(word_length_choice.get(), wls).strip("\n"))
        else:
            text_display_label_2.config(bg="red")
        text_enter.delete(0, 'end')
    tim_var = tk.StringVar()
    def inserter():
        conn = sqlite3.connect("SpeedScores.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO Users(UserName,Score) VALUES(?,?)", (clean_word(user_choice.get()), c))
        conn.commit()
    def countdown(t, time_var=tim_var):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            tim_var.set(timer)
            time.sleep(1)
            t -= 1
            st_page.update()
        else:
            tim_var.set("times up")
            res_label = tk.Label(st_page, text="Score is " + str(c) + " Words Per Minute", bg="yellow", fg="black")
            res_label.place(relx=0.5, rely=0.8, relwidth=0.3, relheight=0.1)
            text_enter.config(state="disabled")
            if (user_choice.get() != "Select User"):
                inserter()
    def begin_time(var, index, mode):
        if enter_var.get():
            countdown(time_limit_choice.get() * 60)
    def give_val(d, v):
        for i in d.keys():
            if (d[i] == v):
                return (i)
    def ok():
        tim_var.set("time left")
        time_canvas = tk.Canvas(st_page, bg='black')
        time_canvas.place(relx=0.1, rely=.28, relwidth=0.9, relheight=0.12)
        time_label = tk.Label(time_canvas, bg="yellow", fg="blue", textvariable=tim_var)
        time_label.pack()
        ok_button.config(state="disabled")
        text_enter.config(state='normal')
        if (word_type_choice.get() == "choose word type"):
            word_type_choice.set("meaningful words")
        word_display(give_val(option_list_1, word_type_choice.get()), word_length_choice.get(), display_text_cur,
                     display_text_next)
    st_page = tk.Toplevel(home, bg="black")
    st_page.iconbitmap("iconimg.ico")
    frame = tk.Frame(st_page, bg="#44bcd8")
    frame.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.2)
    st_page.geometry("700x500")
    st_page.title("test your speed!")
    back_button = ttk.Button(st_page, text="go back", command=st_page.destroy)
    back_button.place(anchor="n", relx=0.96)
    word_type_choice = tk.StringVar(st_page)
    word_type_choice.set("meaningful words")
    option_list_1 = {1: "meaningful words",3:"meaningful words",2: "Random words"}
    drop_1 = ttk.OptionMenu(st_page, word_type_choice, *option_list_1.values())
    drop_1.place(relx=0.1, rely=0.28, relheight=0.1, relwidth=0.25)
    word_length_choice = tk.IntVar()
    word_length_choice.set(4)
    option_list_2 = [ 4, 5, 6, 7, 8, 9]
    drop2 = ttk.OptionMenu(st_page, word_length_choice, *option_list_2)
    word_length_info_label = ttk.Label(st_page, text="choose average \nword length")
    word_length_info_label.place(relx=0.38, rely=0.28, relwidth=0.15, relheight=0.1)
    drop2.place(relx=0.53, rely=0.28, relheight=0.1, relwidth=0.1)
    time_limit_choice = tk.IntVar()
    time_limit_choice.set(1)
    time_info_label = ttk.Label(st_page, text="chose time limit\n(minutes)")
    time_info_label.place(relx=0.65, rely=0.28, relwidth=0.2, relheight=0.1)
    option_list_3 = [1, 1, 2, 3]
    drop3 = ttk.OptionMenu(st_page, time_limit_choice, *option_list_3)
    drop3.place(relx=0.85, rely=0.28, relheight=0.1, relwidth=0.1)
    display_text_prev = tk.StringVar()
    text_display_label_1 = tk.Label(frame, textvariable=display_text_prev, bg="white", font="times 28 bold")
    text_display_label_1.place(relx=0.2, rely=0.5, relheight=0.41, relwidth=0.3, anchor="c")
    display_text_next = tk.StringVar()
    display_text_cur = tk.StringVar()
    text_display_label_2 = tk.Label(frame, textvariable=display_text_cur, font="times 28 bold", bg="blue", fg="yellow")
    text_display_label_2.place(relx=0.5, rely=0.5, relheight=0.41, relwidth=0.3, anchor="c")
    text_display_label_3 = tk.Label(frame, textvariable=display_text_next, bg="white", font="times 28 bold")
    text_display_label_3.place(relx=0.8, rely=0.5, relheight=0.41, relwidth=0.3, anchor="c")
    enter_var = tk.StringVar()
    enter_var.trace_add('write', begin_time)
    text_enter = ttk.Entry(st_page, textvariable=enter_var, font="times 28 bold", state="disabled")
    text_enter.place(relx=0.5, rely=0.5, anchor="c", relwidth=0.35, relheight=0.15)
    text_enter.bind("<space>", word_check)
    ok_button = ttk.Button(st_page, text="Start", command=ok)
    ok_button.place(relx=0.7, rely=0.5, relwidth=0.2)
    st_page.update()
    def test_info():
        info_box=tk.Toplevel(st_page)
        info_box.iconbitmap("iconimg.ico")
        info_box.geometry('%dx%d+%d+%d' % (450, 150, int(width*(2/3)), int(height*(2/3))))
        info_box.overrideredirect(True)
        info_label=tk.Label(info_box,bg="black",fg="yellow",text=testinfo)
        info_label.place(relx=0,rely=0,relheight=1,relwidth=1)
        close_button=tk.Button(info_box,text="close",command=info_box.destroy)
        close_button.place(relx=0.9,rely=0.05)
    info_button=tk.Button(st_page,command=test_info,text="info")
    info_button.place(relx=0.9,rely=0.187,relwidth=0.05,relheight=0.05)
new_user_var = tk.StringVar()
def createcommand():
    if (new_user_var.get()):
        conn = sqlite3.connect("SpeedScores.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO Users(UserName) VALUES(?)", (new_user_var.get(),))
        conn.commit()
        new_user_entry.delete(0, 'end')
frame_1 = ttk.Frame(home, height=100, width=310)
frame_1.place(relx=0.05, rely=0.05)
hello_label = tk.Label(frame_1, text="Hello", bg="#e9e8e1")
hello_label.place(relx=0.08, rely=0.1, height=24, anchor="n", relwidth=0.2)
user_choice = tk.StringVar()
user_choice.set('Select User')
user_drop = ttk.OptionMenu(frame_1, user_choice, *user_list)
user_drop.place(anchor='n', relx=0.39, rely=0.1, relwidth=0.4)
open_test_button = ttk.Button(frame_1, text="test your speed!", command=page1)
open_test_button.place(anchor="n", relx=0.8, rely=0.1, relwidth=0.4)
def plotter(a):
    if (clean_word(a) != "SelectUser"):
        conn = sqlite3.connect("SpeedScores.db")
        conn.row_factory = lambda cursor, row: row[0]
        cur = conn.cursor()
        cur.execute(" SELECT Score FROM Users WHERE Username=(?)", (clean_word(a),))
        conn.commit()
        x = cur.fetchall()
        plt.plot(x, 'b--')
        plt.xlabel("nth try")
        plt.ylabel("Words Per Minute")
        plt.xticks(list(range(0, len(x) + 1)))
        plt.yticks(list(range(5, 100, 5)))
        plt.title(clean_word(a)+" Progress")
        plt.show()
def stats_page(a):
    statspage = tk.Toplevel(home)
    statspage.overrideredirect(True)
    close_button = tk.Button(statspage, text="close", command=statspage.destroy)
    close_button.place(relx=0.88, rely=0.05)
    statspage.geometry('%dx%d+%d+%d' % (350, 300, int(width*(2/3)), int(height*(2/3))))
    user_result = tk.StringVar()
    user_result.set("Choose User To See Performance")
    choose_menu = ttk.OptionMenu(statspage, user_result, *user_list)
    choose_menu.place(relx=0.5, rely=0.1, anchor='n')
    ok_button = ttk.Button(statspage, text="View Progress", command=lambda: plotter(user_result.get()))
    ok_button.place(relx=0.5,rely=0.8,anchor='s')
def deleteuser():
    def deleter(page, name):
        x = clean_word(name)
        if (x != "Select User"):
            conn = sqlite3.connect("SpeedScores.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM Users WHERE Username=(?)", (x,))
            conn.commit()
        page.destroy()
    conn = sqlite3.connect("SpeedScores.db")
    new_page = tk.Toplevel(home)
    new_page.overrideredirect(True)
    close_button = tk.Button(new_page, text="close", command=new_page.destroy)
    close_button.place(relx=0.88, rely=0.05)
    new_page.geometry('%dx%d+%d+%d' % (350, 300, int(width*(2/3)), int(height*(2/3))))
    new_page.title("Delete User")
    del_var = tk.StringVar()
    del_var.set("Choose")
    del_user_menu = ttk.OptionMenu(new_page, del_var, *user_list)
    del_user_menu.place(relx=0.5, rely=0.2, relwidth=0.8, anchor='c')
    ok_button = tk.Button(new_page, text="Delete!", command=lambda: deleter(new_page, del_var.get()))
    ok_button.place(relx=0.5, rely=0.3, anchor='c')
    conn.commit()
def leaderboard(a, b):
    table_page = tk.Toplevel(home)
    table_page.overrideredirect(True)
    close_button = tk.Button(table_page, text="close", command=table_page.destroy)
    close_button.place(relx=0.88, rely=0.88)
    table_page.geometry('%dx%d+%d+%d' % (450, 300, int(width*(2/3)), int(height*(2/3))))
    table = ttk.Treeview(table_page, columns=(1, 2), show='headings')
    table.pack()
    table.heading(1, text="HighScore")
    table.heading(2, text="Name")

    def grapher():
        conn = sqlite3.connect("SpeedScores.db")
        cur = conn.cursor()
        cur.execute("""SELECT UserName, MAX(Score) FROM Users GROUP BY UserName HAVING Score NOTNULL ORDER BY MAX(Score) DESC""")
        x = cur.fetchall()
        bar_vals_1 = []
        bar_vals_2 = []
        for i in x:
            if(i[1]!=0):
                bar_vals_1.append(i[0])
                bar_vals_2.append(i[1])
        plt.bar(bar_vals_1, bar_vals_2)
        plt.ylabel("Words Per Minute")
        plt.show()
        conn.commit()
        conn.close()
    view_graph_button = ttk.Button(table_page, text="view comparison!", command=grapher)
    view_graph_button.place(relx=0.5, rely=0.9, anchor="s")
    try:
        for i in range(len(a)):
            table.insert('', 'end', values=(a[i], b[i]))
    except Exception:
        pass
frame_2 = ttk.Frame(home, height=200, width=310)
frame_2.place(relx=0.75, rely=0.05, anchor="n")
new_user_label = ttk.Label(frame_2, text="Enter Name To Create User")
new_user_label.place(relx=0, rely=0.05)
new_user_entry = ttk.Entry(frame_2, textvariable=new_user_var)
new_user_entry.place(relx=0.475, rely=0.05, relwidth=0.4)
create_new_user_button = ttk.Button(frame_2, text="Ok", command=createcommand)
create_new_user_button.place(relx=0.88, rely=0.05, height=22)
view_results_button = ttk.Button(frame_2, text="Track Progress", command=lambda: stats_page(user_list))
view_results_button.place(relx=0.01, rely=0.6, relwidth=0.4)
delete_user_button = ttk.Button(frame_2, text="Delete User", command=deleteuser)
delete_user_button.place(relx=0.01, rely=0.2, relwidth=0.4)
leaderboard_button = ttk.Button(frame_2, text="Leaderboard", command=lambda: leaderboard(highscore_user, highscore_list))
leaderboard_button.place(relx=0.01, rely=0.4, relwidth=0.4)
def page2():
    tut_page = tk.Toplevel(home, bg='black')
    tut_page.iconbitmap("iconimg.ico")
    tut_page.geometry("700x600")
    tut_page.title("Learn To Type")
    close_button = tk.Button(tut_page, text="Go Back", command=tut_page.destroy)
    close_button.place(relx=0.9, rely=0.05)
    sample_img=Image.open("touchtyping.png")
    sample_img=sample_img.resize((500,200))
    im = ImageTk.PhotoImage(sample_img)
    canvas = tk.Canvas(tut_page, width=300, height=300)
    canvas.place(anchor="c",relx=0.5,rely=0.4,relheight=0.3,relwidth=0.8)
    canvas.create_image(20, 0, image=im, anchor="nw")
    def tut_info():
        info_box=tk.Toplevel(tut_page)
        info_box.iconbitmap("iconimg.ico")
        info_box.geometry('%dx%d+%d+%d' % (450, 150, int(width*(2/3)), int(height*(2/3))))
        info_box.overrideredirect(True)
        info_label=tk.Label(info_box,bg="black",fg="yellow",text=tutinfo)
        info_label.place(relx=0,rely=0,relheight=1,relwidth=1)
        close_button=tk.Button(info_box,text="close",command=info_box.destroy)
        close_button.place(relx=0.9,rely=0.05)
    info_button=tk.Button(tut_page,command=tut_info,text="info")
    info_button.place(relx=0.9,rely=0.1,relwidth=0.05,relheight=0.05)
    global entry_var
    entry_var = tk.StringVar()
    def new_word(self):
        text_entry.delete(0,'end')
        display_text.set(" "+meaningful_word_giver(5, wls).strip())
        lo="letter"+str(labels.index(display_text.get()[1]))
        y[lo].config(bg="green", fg="white")
    global display_text
    display_text = tk.StringVar()
    display_text.set(meaningful_word_giver(5, wls).strip())
    text_display_label_ = tk.Label(tut_page, textvariable=display_text, font="times 28 bold", bg="blue", fg="yellow")
    text_display_label_.place(relx=0.5, rely=0.05, relheight=0.1, relwidth=0.25, anchor="n")
    global keyboard_layout
    keyboard_layout = tk.Label(tut_page)
    keyboard_layout.place(relx=0.5,rely=0.7,anchor='c')
    global labels
    labels = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
              'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
              'z', 'x', 'c', 'v', 'b', 'n', 'm']
    global text_entry
    text_entry = ttk.Entry(tut_page, textvariable=entry_var)
    text_entry.place(relx=0.5, rely=0.85, anchor='s')
    text_entry.bind("<space>", new_word)
    def key_display():
        global y
        y = {}
        varRow = 2
        varColumn = 0
        for i, label in enumerate(labels):
            x = 'letter' + str(i)
            y[x] = tk.Label(keyboard_layout, text=label, width=4, bg="#3c4987", fg="#ffffff",
                            activebackground="#ffffff",
                            activeforeground="#3c4987", relief='raised', padx=1, pady=1, bd=1)
            y[x].grid(row=varRow, column=varColumn)
            varColumn += 1
            if (varColumn > 9 and varRow == 2):
                varColumn = 0
                varRow += 1
            if (varColumn > 8 and varRow == 3):
                varColumn = 0
                varRow += 1
            if (varColumn > 8 and varRow == 4):
                varColumn = 0
                varRow += 1
        global p
        p = 0
        def overall():
            def timed_labeller(key, keyn, dec):
                if dec == "ok":
                    t = 1
                    y[keyn].config(bg="green", fg="white")
                    while t:
                        time.sleep(1)
                        t -= 1
                    else:
                        y[key].config(bg="#3c4987", fg="#ffffff")
                    y[keyn].config(bg="green", fg="white")
                    if len(str(entry_var.get())) == len(display_text.get()):
                        y[key].config(bg="#3c4987", fg="#ffffff")
                else:
                    if (len(entry_var.get()) > 0):
                        y[key].config(bg="red")
            global p
            if (p == 0):
                r = display_text.get()[0]
                q = labels.index(r)
                y["letter" + str(q)].config(bg="green", fg="white")
            else:
                r = display_text.get()[0]
                q = labels.index(r)
                y["letter" + str(q)].config(bg="#3c4987", fg="#ffffff")
            p += 1
            tut_page.update()
            def colour_scheme(var, indx, mode):
                if len(entry_var.get()) > len(display_text.get()):
                    entry_var.set(entry_var.get()[:len(display_text.get())])
                if len(str(entry_var.get())) == 0:
                    a = display_text.get()[len(str(entry_var.get()))]
                    an = display_text.get()[len(str(entry_var.get())) + 1]
                elif len(str(entry_var.get())) == len(display_text.get()):
                    a = display_text.get()[len(str(entry_var.get())) - 1]
                    an = display_text.get()[len(str(entry_var.get())) - 1]
                else:
                    a = display_text.get()[len(str(entry_var.get())) - 1]
                    an = display_text.get()[len(str(entry_var.get()))]
                if(a != " "):
                    b = labels.index(a)
                    bn = labels.index(an)
                    global key, keyn
                    key = 'letter' + str(b)
                    keyn = 'letter' + str(bn)
                    if (entry_var.get()[-1:] == display_text.get()[len(str(entry_var.get())) - 1]):
                        timed_labeller(key, keyn, "ok")
                    else:
                        if (len(entry_var.get()) > 0):
                            timed_labeller(key, keyn, "no")
                tut_page.update()
            entry_var.trace_add('write', colour_scheme)
        overall()
    key_display()
    tut_page.mainloop()
tutorial_button = ttk.Button(frame_1, text="Learn To Type!", command=page2)
tutorial_button.place(anchor="s", relx=0.5, rely=0.9, relwidth=0.5)
quit_button = ttk.Button(home, text="Quit!", command=lambda: home.destroy())
quit_button.place(relx=0.9, rely=0.9)
conn.commit()
conn.close()
home.mainloop()
