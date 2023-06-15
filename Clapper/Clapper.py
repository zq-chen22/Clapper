import random
import numpy as np
import sys

# instruction

# It's a game for AI to play clapping game, which is, gain bullets to shoot your enemy. Here some mode have been implemented,
# which are manual mode(human), random mode(rand), and a rookie AI(naive-AI). Rookie AI is trained only by inputting the rules
# and update its database. It's not that powerful but still have 2/3 win rate over random mode. Try it out and improve your skill to be a better clapper(or maybe your 
# own fancy AI)

# utils

def rprint(massage):
    begin_color = '\033[1;31m'
    end_color = '\033[0m'
    print(begin_color + massage + end_color)

def gprint(massage):
    begin_color = '\033[1;32m'
    end_color = '\033[0m'
    print(begin_color + massage + end_color)

def sprint(massage):
    begin_color = '\033[3;30m'
    end_color = '\033[0m'
    print(begin_color + massage + end_color)

# parameters

PLAYER_NUM = 2
turn = 0
powers = np.zeros(PLAYER_NUM)
moves = np.zeros(PLAYER_NUM)
movedic = {0:"bullet gain", 1:"normal shield", 2:"golden shield", 3:"gun shoot", 4:"strafing"}

# database

DB = np.zeros(80)

#run this part if you have had the datafile
with open('data.txt', 'r') as datafile:
    entry = 0
    for line in datafile.readlines():
        DB[entry] = int(float(line.strip()))
        entry += 1


DB = DB.reshape((4,4,5))

# move strategies

def human(i):
    result =  input("Please tell me your movement: ")
    if i == 1:
        sponsor[1].append((min(int(powers[1]) , 3),min(int(powers[0]) , 3),int(result)))
    else:
        sponsor[0].append((min(int(powers[0]) , 3),min(int(powers[1]) , 3),int(result)))
    return result

def rand(i):
    result = random.randint(0, 4)
    if i == 1:
        sponsor[1].append((min(int(powers[1]) , 3),min(int(powers[0]) , 3),result))
    else:
        sponsor[0].append((min(int(powers[0]) , 3),min(int(powers[1]) , 3),result))
    return result

sponsor = [[],[]]

def naive_AI(i):
    if i == 1:
        weight = DB[min(int(powers[1]) , 3)][min(int(powers[0]) , 3)]
    else:
        weight = DB[min(int(powers[0]) , 3)][min(int(powers[1]) , 3)]
    randx = random.random() * (np.dot(np.ones(5),np.exp(0.01 * weight)))
    coord = 0
    result = 0
    for item in range(5):
        coord += np.exp(weight[item])
        if coord >= randx:
            result = item
            break
    if turn >= 20 and random.random() < 0.1:
        result = rand(i)
    if i == 1:
        sponsor[1].append((min(int(powers[1]) , 3),min(int(powers[0]) , 3),result))
    else:
        sponsor[0].append((min(int(powers[0]) , 3),min(int(powers[1]) , 3),result))
    return result
    


dic = {0:human, 1:rand, 2:naive_AI}


# core part of the game

def show():
    global turn
    turn += 1
    sprint(f"Now it's turn {turn}, player 1 has {int(powers[0])} bullet(s), player 2 has {int(powers[1])} bullet(s).")

def move():
    for i in range(PLAYER_NUM):
        while True:
            x = strategies[i](i)
            if x not in ["0","1","2","3","4",0,1,2,3,4]:
                rprint("Invalid action")
                continue
            if  int(x) <= powers[i] + 2:
                moves[i] = x  
                break
            if strategies[i] == human:
                print("Unavailable action")
    gprint(f"Player 1 does a {movedic[moves[0]]}, Player 2 does a {movedic[moves[1]]}.")

def check():
    if moves[0] == 0:
        powers[0] += 1
    if moves[0] == 3:
        powers[0] -= 1
        if moves[1] not in [1,3,4]:
            return 1
    if moves[0] == 4:
        powers[0] -= 2
        if moves[1] not in [2,4]:
            return 1
    if moves[1] == 0:
        powers[1] += 1
    if moves[1] == 3:
        powers[1] -= 1
        if moves[0] not in [1,3,4]:
            return 2
    if moves[1] == 4:
        powers[1] -= 2
        if moves[0] not in [2,4]:
            return 2
    return 0  

def run():
    show()
    move()
    return check()
        
def game():
    global turn, powers, moves,sponsor
    turn = 0
    powers = np.zeros(PLAYER_NUM)
    moves = np.zeros(PLAYER_NUM)
    sponsor = [[],[]]
    m = 0
    while True:
        m = run()
        if m != 0:
            print(f"Player {m} win")
            for i in range(PLAYER_NUM):
                if strategies[i] == naive_AI:
                    if m == i+1:
                        for item in sponsor[i]:
                            if DB[item] < 200:
                                DB[item] += 1
                    else:
                        for item in sponsor[i]:
                            if DB[item] > -200:
                                DB[item] -= 1
                if strategies[i] == human:
                    if m == i+1:
                        for item in sponsor[i]:
                            if DB[item] < 200:
                                DB[item] += 20
                    else:
                        for item in sponsor[i]:
                            if DB[item] > -200:
                                DB[item] -= 20
            break
    return m

def train(turns):
    for _ in range(turns):
        game()

def intro():
    sprint("-----Intro-----")
    sprint("In this game you have five operations to fight with your enemy.")
    sprint("0 stands for bullet gain. You will get one extra bullet. By start you own no bullet")
    sprint("1 stands for gun shoot. It takes 1 bullets and can kill enemy with no defense or with golden defense.")
    sprint("2 stands for strafing. It takes 2 bullets can kill enemy in mode bullet gain, gun shoot and normal shield")
    sprint("3 stands for normal shield. It takes no bullets and can defense gun shoot.")
    sprint("4 stands for golden shield. It takes no bullets and can defense strafing.")
    sprint("-----Start-----")

def BO5():
    intro()
    print("Be the first one to get 3 kills")
    your_score = 0
    enemy_score = 0
    while True:
        winner = game()
        if winner == 1:
            your_score += 1
        else:
            enemy_score += 1
        gprint(f"Now it is {your_score} verses {enemy_score}")
        if your_score == 3:
            gprint("YOU WIN THE BO5")
            break
        if enemy_score == 3:
            rprint("YOU LOSE THE BO5")
            break

def tst(turns):
    your_score = 0
    enemy_score = 0
    with open('log.txt', 'w') as sys.stdout:
        for _ in range(turns):
            winner = game()
            if winner == 1:
                your_score += 1
            else:
                enemy_score += 1
    sys.stdout = save_stdout
    return(your_score, enemy_score)


save_stdout = sys.stdout
with open('log.txt', 'w') as sys.stdout:
    print('test')
    strategies = [dic[1],dic[2]]
    train(0)
    strategies = [dic[2],dic[2]]
    train(0)
    print(DB)
sys.stdout = save_stdout
strategies = [dic[1],dic[2]]
print(tst(5000))
with open('data.txt','w') as sys.stdout:
    for item in DB.reshape(80):
        print(item)
sys.stdout = save_stdout