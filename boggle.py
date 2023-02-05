"""
FILE: boggle.py
DESCRIPTION: runs the 'Boggle' game
"""
# region import
from typing import Tuple, Callable
from tkinter import NORMAL

import utils
from model import Model
from gui import GUI

# endregion import
# region CONSTANTS
WORDS_FILEPATH = "./boggle_dict.txt"


# endregion CONSTANTS

class Controller:
    """
    The controller of the 'Boggle' game
    """

    def __init__(self) -> None:
        # init vars
        self.model = Model()
        self.gui = GUI()
        self.__words_collection = utils.load_words_dict(WORDS_FILEPATH)

        # additional actions
        self.model.words_collection = self.__words_collection
        self.gui.button_play.config(command=self.on_play_button_pressed)

    def create_board_button_callback(self, coordinate: Tuple[int, int]) -> \
            Callable:
        """
        Creates a callback function for the board's buttons

        :param coordinate: the coordinate of the button
        :return: the callback function
        """

        def board_button_callback() -> None:
            """
            The callback function for the board's buttons
            """
            self.model.update_word_and_path(coordinate)

            if self.model.current_path:
                buttons_to_enable = self.model.get_buttons_to_enable()
                self.gui.update_board_buttons_state(buttons_to_enable)
            else:
                self.gui.set_all_board_buttons_state(NORMAL)

            self.gui.update_current_word(self.model.current_word)

        return board_button_callback

    def initialize_button_actions(self) -> None:
        """
        Initializes the button actions
        """
        self.gui.button_play.config(command=self.on_play_button_pressed)
        self.gui.button_restart.config(command=self.on_restart_button_pressed)
        self.gui.button_check.config(command=self.on_check_button_pressed)
        self.set_board_buttons_command()

    def initialize_model(self) -> None:
        """
        Initializes the model
        """
        self.model = Model()
        self.model.words_collection = self.__words_collection
        self.model.create_board()

    def on_play_button_pressed(self) -> None:
        """
        The callback function for the 'play' button
        """
        self.initialize_model()
        self.gui.show_board(self.model.board)
        self.gui.button_play_on_press()
        self.initialize_button_actions()

    def on_restart_button_pressed(self) -> None:
        """
        The callback function for the 'restart' button
        """
        self.initialize_model()
        self.gui.button_restart_on_press()
        self.gui.show_board(self.model.board)
        self.initialize_button_actions()

    def on_check_button_pressed(self) -> None:
        """
        The callback function for the 'check' button
        """
        response = self.model.check_word()
        self.gui.update_current_word('')
        self.gui.button_check_on_press(response)
        self.gui.update_score(self.model.score)
        if response.startswith("You found"):
            self.gui.add_word_to_words_found(self.model.current_word)
        self.model.reset_current_input()

    def set_board_buttons_command(self) -> None:
        """
        Sets the callback functions for the board's buttons
        """
        for i in range(len(self.model.board)):
            for j in range(len(self.model.board[0])):
                callback_cmd = self.create_board_button_callback((i, j))
                self.gui.set_board_buttons_command((i, j), callback_cmd)


if __name__ == "__main__":
    controller = Controller()
    controller.gui.run()
