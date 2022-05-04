import pythonSolver as pg
import game


def main():
    # game.Game()   # Play for manual game
    plays = pg.Stats(30)    # Automation Solver game
    plays.getStats()

if __name__ == '__main__':
    main()
