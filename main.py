from game import Game
from display import Display
from snake import Snake
from apple import Apple
from human_movement import HumanMovement


Game(Snake(), Apple(), Display(), HumanMovement()).run()
