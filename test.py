from snake import SnakeGame

game = SnakeGame()
while True:
    game.go([1,0,0])

    inp = input("Play again? (y/n) ")
    if inp != "y":
        break
