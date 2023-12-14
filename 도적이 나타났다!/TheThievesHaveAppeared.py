import tkinter
import random
import datetime

class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.time_label = tkinter.Label(root, text="00:00:000", font=("Times New Roman", 20),bg="black", fg="white")
        self.time_label.place(x=350, y=50)
        self.start_time = None
        self.stop_time = None
        self.running = False

    def start(self):
        self.running = True
        self.start_time = datetime.datetime.now()
        self.update()

    def stop(self):
        self.running = False
        self.stop_time = datetime.datetime.now()

    def update(self):
        if self.running:
            delta = datetime.datetime.now() - self.start_time
            minutes = delta.seconds // 60 
            seconds = delta.seconds % 60
            milliseconds = delta.microseconds // 1000
            time_str = f"{minutes:02}:{seconds:02}:{milliseconds:03}"
            self.time_label.config(text=time_str)
            self.time_label.after(10, self.update)

stopwatch = None
click_start_btn = 0
index = 0
score = 0
score_label = 0
stopwatch_shown = False
click_count = 0
left_weapon = 12
target_button = None
ments_index=0

ments = [
    "주인공의 엄마가 아프다.",
    "엄마의 병을 치료하기 위해서는\n옆마을에서 파는 귀한 포션이 필요하다.",
    "주인공이 포션을 사러 위해 옆마을로 가는 중에\n도적들이 나타났다.",
    "그들은 주인공의 돈을 노리고 있었다.",
    "주인공 주위에 보이는건 돌멩이 12개.",
    "도적은 총 10명.",
    "기회는 12번 뿐.",
    "주인공은 최대한 빨리 도적을 해치우고\n포션을 사러가야한다."
    ]
enemy_img = ["enemy1.png", "enemy2.png", "enemy3.png", "enemy4.png", "enemy5.png"]

def change(): 
    global score_label, left_weapon, left_weapon_label
    global stopwatch, stopwatch_shown
    for wpack in root.pack_slaves():
        wpack.destroy()
    for wplace in root.place_slaves(): 
        wplace.destroy()
    root.geometry("800x600")
    game_cvs=tkinter.Canvas(root, width=800, height=600, bg="black")
    game_cvs.pack()
    game_bg=tkinter.PhotoImage(file="game_bg.png")
    game_cvs.create_image(300, 250, image=game_bg)
    game_cvs.image = game_bg
    score_label=tkinter.Label(root,text="0",font=("Times New Roman",20),bg="black", fg="white")
    score_label.place(x=330, y=10)
    left_weapon_label=tkinter.Label(root,text = f"남은 돌멩이: {left_weapon}", font=("Times New Roman", 20), bg="black", fg="white")
    left_weapon_label.place(x=400, y=10)
    stopwatch = Stopwatch(root)
    stopwatch_shown = True
    if stopwatch:
        stopwatch.start()
    game_cvs.bind("<Button-1>", mouse_click)
    random_target()

def mouse_click(event):
    global click_count, left_weapon, index
    click_count += 1
    if left_weapon > 0:
        left_weapon -= 1
        update_left_weapon()
    if left_weapon == 0:
        index =4
        fin()

def increase_decrease():
    global score, target_button, click_count, left_weapon
    score += 1
    click_count += 1
    left_weapon -= 1
    update_score()
    update_left_weapon()
    fin()

def fin():
    global index
    if left_weapon == 0 or score == 10:
        if stopwatch:
            stopwatch.stop()
        if score == 10 and left_weapon >= 0:
            index = 3
        elif left_weapon == 0:
            index = 4
        target_button.destroy()
        game_main()
    else:
        target_button.destroy()

def random_target():
    global target_button, root, index
    if index != 3 and index != 4: 
        if target_button:
            target_button.destroy()
        button_width = 90
        button_height = 70
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        x_range = window_width - button_width
        y_range = window_height - button_height
        random_img = random.choice(enemy_img)
        enemy = tkinter.PhotoImage(file=random_img)
        target_button = tkinter.Button(root, image=enemy, bg="black", command=increase_decrease)
        target_button.image = enemy
        x_pos = random.randint(0, x_range)
        y_pos = random.randint(90, y_range)
        if game_level == "easy":
            delay = random.randint(1000, 1500)
        elif game_level == "normal":
            delay = random.randint(500, 1000)
        elif game_level == "hard":
            delay = random.randint(300, 700)
        target_button.place(x=x_pos, y=y_pos)
        root.after(delay, random_target)

def fin_game():
    global fin_label, stopwatch, score
    global go_to_title, play_again_game
    for wpack in root.pack_slaves():
        wpack.destroy()
    for wplace in root.place_slaves():
        wplace.destroy()
    root.geometry("800x600")
    fin_cvs = tkinter.Canvas(root, width = 800, height = 600, bg = "black")
    fin_cvs.place(x=0, y=0)
    fin_label=tkinter.Label(root,text="Game Over",font=("Times New Roman",30), bg="black", fg="white")
    fin_label.pack() 
    if stopwatch:
        delta_time = stopwatch.stop_time - stopwatch.start_time
        minutes = delta_time.seconds // 60
        seconds = delta_time.seconds % 60
        milliseconds = delta_time.microseconds // 1000
        time_str = f"Time: {minutes:02}:{seconds:02}:{milliseconds:03}"
        time_label = tkinter.Label(root, text=time_str, font=("Times New Roman", 20), bg="black", fg="white")
        time_label.pack()
    go_to_title=tkinter.Button(root,text="타이틀 화면", font=("Times New Roman",20), bg="black", fg="white",command=fin_title_btn)
    go_to_title.place(x=200, y=400)
    play_again_game=tkinter.Button(root,text="다시하기", font=("Times New Roman",20), bg="black", fg="white",command=again_game_btn)
    play_again_game.place(x=400, y=400)
    fin_click_count_label=tkinter.Label(text=f"공격  횟수: {click_count}", bg="black", fg="white")
    fin_click_count_label.pack()
    fin_kill_enemy=tkinter.Label(text=f"해치운 도적 수: {score}", bg="black", fg="white")
    fin_kill_enemy.pack()
    fin_survive_enemy=tkinter.Label(text=f"남은 도적 수: {10-score}", bg="black", fg="white")
    fin_survive_enemy.pack()
    fin_accuracy=tkinter.Label(text=f"실패한 공격 횟수: {click_count-score}", bg="black", fg="white")
    fin_accuracy.pack()
    if index == 3:
        fin1_bg = tkinter.PhotoImage(file = "happyend.png")
        fin_cvs.create_image(400, 300, image = fin1_bg)
        fin_cvs.image = fin1_bg
        fin_label_1=tkinter.Label(root, text="성공적으로 도적을 해치우고\n옆마을에 가서 포션을 사서 집으로 돌아갔다.\n주인공의 엄마는 이제 건강하다!", font=("Times New Roman", 20), bg="black", fg="white")
        fin_label_1.pack()
    elif index == 4:
        fin2_bg = tkinter.PhotoImage(file = "sadend.png")
        fin_cvs.create_image(400, 300, image = fin2_bg)
        fin_cvs.image = fin2_bg
        fin_label_2=tkinter.Label(root, text="주인공은 도적을 해치우는데 실패했다.\n가지고 있던 돈은 모두 뺏겨버렸다.", font=("Times New Roman", 20), bg="black", fg="white")
        fin_label_2.pack() 

def fin_title_btn():
    global index, score, click_start_btn, click_count, left_weapon
    index=1
    score=0
    click_start_btn = 0
    click_count = 0
    left_weapon = 12
    game_main()

def again_game_btn():
    global index, score, click_count, left_weapon
    index=2
    score=0
    click_count = 0
    left_weapon = 12
    game_main()

def update_score():
    score_label.config(text=score)

def update_left_weapon() :
    left_weapon_label.config(text = f"남은 돌멩이: {left_weapon}")

def press_EASY_start_btn():
    global click_start_btn, game_level
    click_start_btn = 1
    game_level="easy"
    game_main()

def press_NORMAL_start_btn():
    global click_start_btn, game_level
    click_start_btn = 1
    game_level="normal"
    game_main()

def press_HARD_start_btn():
    global click_start_btn, game_level
    click_start_btn = 1
    game_level="hard"
    game_main()

def title_story():
    global index, ments_label
    title_story_cvs = tkinter.Canvas(root, width=600, height=500, bg="black")
    title_story_cvs.pack()
    ments_label = tkinter.Label(root, text="Enter키를 눌러 진행합니다.", font=("Times New Roman", 18), fg="white", bg="black")
    ments_label.place(x=10, y=200)
    root.bind("<Return>", update_ments)

def update_ments(event):
    global ments_index
    if ments_index < len(ments):
        ments_label.config(text=ments[ments_index])
        ments_index += 1
        if ments_index == len(ments):
            root.bind("<Return>", go_to_title)
    else:
        pass

def go_to_title(event):
    game_main()

def title():
    global ments_label
    for wpack in root.pack_slaves():
        wpack.destroy()
    for wplace in root.place_slaves():
        wplace.destroy()
    root.geometry("600x500")
    title_cvs=tkinter.Canvas(root, width=600, height=500, bg="black")
    title_cvs.pack()
    title_bg=tkinter.PhotoImage(file="title_bg.png")
    title_cvs.create_image(300, 250, image=title_bg)
    title_cvs.create_text(300, 25, text="도적이 나타났다 !", fill="white", font=("Times New Roman", 30, "bold"))
    HowPlay_label=tkinter.Label(text="<게임방법>\n1. 난이도를 고르세요.\n2. 10명의 도적을 최대한 빨리 클릭해서 해치우세요.\n3. 공격 기회는 12번 뿐입니다.\n\n난이도에 따라 도적이 등장하는 속도가 다릅니다!",font=("Times New Roman",15))
    HowPlay_label.place(x=80,y=200)
    EASY_play_button=tkinter.Button(root,text="EASY",font=("Times New Roman", 25),bg="green",command=press_EASY_start_btn)
    EASY_play_button.place(x=80, y=400)
    NORMAL_play_button=tkinter.Button(root,text="NORMAL",font=("Times New Roman", 25),bg="yellow",command=press_NORMAL_start_btn)
    NORMAL_play_button.place(x=210, y=400)
    HARD_play_button=tkinter.Button(root,text="HARD",font=("Times New Roman", 25),bg="red",command=press_HARD_start_btn)
    HARD_play_button.place(x=400, y=400)
    title_cvs.image = title_bg
    title_cvs.bind("<Button-1>", title_story)

def game_main():
    global index,score_label
    if index ==0:
        title_story()
        index =1
    elif index == 1:
        title()
        index = 2
    elif index == 2:
        if click_start_btn == 1:
            change()
    elif index == 3:
        fin_game()
    elif index == 4:
        fin_game()

root=tkinter.Tk()
root.title("도적이 나타났다!")
game_main()
root.mainloop()