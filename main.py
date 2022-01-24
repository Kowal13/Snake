from game import Game
from display import Display
from snake import Snake
from apple import Apple
from human_movement import HumanMovement
from a_star_movement import AStarMovement


#Game(Snake(), Apple(), Display(), HumanMovement()).run()
Game(Snake(), Apple(), Display(), AStarMovement()).run()
