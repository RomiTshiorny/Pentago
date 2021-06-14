import Gameboard as gb, random, AI

def start(pentago,file,difficulty):
    # First player will always be white, and second will always be black (like chess)
    Human_first = True if random.randint(0, 1) == 1 else False
    order = ["Human", "AI"] if Human_first else ["AI", "Human"]

    #0 for min_max, 1 for alpha_beta
    PentagoAI = AI.AI(1)

    while (not pentago.win and not pentago.tie):
        file.write(order[0] + "\n")
        file.write(order[1] + "\n")
        file.write("W\n")
        file.write("B\n")
        file.write("1\n" if pentago.firstPlayerTurn else "2\n")
        file.write(str(pentago))
        for move in pentago.moves:
            file.write(move + "\n")

        print(pentago)
        player = "Player 1 (w)" if pentago.firstPlayerTurn else "Player 2 (b)"
        if((order[0] == "AI" and pentago.firstPlayerTurn) or (order[1] == "AI" and not pentago.firstPlayerTurn)):
            print("AI Thinking...")
            print(player, ": AI :",PentagoAI.makeMove(pentago,difficulty))
        else:
            print(player, ": Human <b/p bd>:", end="")
            move = input()
            pentago.makeMove(move)

    file.write(order[0] + "\n")
    file.write(order[1] + "\n")
    file.write("W\n")
    file.write("B\n")
    file.write("1\n" if pentago.firstPlayerTurn else "2\n")
    file.write(str(pentago))
    for move in pentago.moves:
        file.write(move + "\n")

    print(pentago)
    if (pentago.tie):
        print("Tie!")
        file.write("Tie!")
    elif (pentago.white_win):
        print("Player 1 wins!")
        file.write(order[0] + " wins!")
    else:
        print("Player 2 wins!")
        file.write(order[1] + " wins!")

file = open("Output.txt","w")
print("(1) EASY - AI only thinks one move ahead")
print("(2) NORMAL - (RECOMMENDED) Best option to test the AI")
print("(3) HARD - WARNING!! LONG WAIT TIMES")
print("Select a difficulty you wish to play in(1, 2 or 3):", end ="")
difficulty = int(input())
pentago = gb.Gameboard()
start(pentago,file,difficulty)
file.close()