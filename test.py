from snake import SnakeGame

game = SnakeGame(40)
while True:
    game.go([1,0,0])

    print(game.vision())
    inp = input("Play again? (y/n) ")
    if inp != "y":
        break
