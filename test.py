from snake import SnakeGame

game = SnakeGame()
while True:
    game.go()

    inp = input("Play again? (y/n) ")
    if inp != "y":
        break
