WIN_BET_MODIFIER= [.5,2,0,1,[10,20,30,40,50,60]]
def labouchere(won):
    bet=WIN_BET_MODIFIER[4][0]+WIN_BET_MODIFIER[4][-1]
    if WIN_BET_MODIFIER[4]!=[]: 
        if won == "Win":
            WIN_BET_MODIFIER[4].pop() 
            WIN_BET_MODIFIER[4].pop(0)
        else:
            WIN_BET_MODIFIER[4].append(WIN_BET_MODIFIER[4][0]+WIN_BET_MODIFIER[4][-1])
        return bet
print(labouchere("Lose") )
print(labouchere("Win") )
print(labouchere("Lose") )
print(labouchere("Lose") )
l="asddd"
print(labouchere("Lose") )
print(l[0:3])