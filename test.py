from snake import SnakeGame

game = SnakeGame(40)
while True:
    game.go([1,0,0])

    print(game.vision([0, 0, 1, 0]))
    # print(game.vision([1, 0, 0, 0]))
    # print(game.vision([0, 1, 0, 0]))
    inp = input("Play again? (y/n) ")
    if inp != "y":
        break
