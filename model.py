"""
FILE: model.py
DESCRIPTION: Represents the logic behind the 'Boggle' game
"""
# region import
import math
from typing import List, Set, Tuple

import utils
import boggle_board_randomizer as bb_randomizer


# endregion import


class Model:
    """
    Represents the logic behind the 'Boggle' game
    """

    def __init__(self) -> None:
        self.__board: List[List[str]] = [[]]
        self.__words_collection: Set[str] = set()
        self.__words_found: Set[str] = set()
        self.__current_word: str = ""
        self.__current_path: utils.Path = []
        self.__score: int = 0

    # region GET & SET
    @property
    def board(self) -> List[List[str]]:
        """
        Returns the current board's values in a 2 dimensional matrix
        """
        return self.__board

    @property
    def current_word(self) -> str:
        """
        Returns the current word
        """
        return self.__current_word

    @property
    def current_path(self) -> utils.Path:
        """
        Returns the current path
        """
        return self.__current_path

    # region property: score
    @property
    def score(self) -> int:
        """
        Returns the current score
        """
        return self.__score

    def __increase_score(self) -> int:
        """
        Increases the score by the square of the path length
        :return: the new score
        """
        self.__score += int(math.pow(len(self.__current_path), 2))
        return self.__score

    # endregion property: score
    # region property: words_collection
    @property
    def words_collection(self) -> Set[str]:
        """
        Returns the current words collection
        """
        return self.__words_collection

    @words_collection.setter
    def words_collection(self, words_collection: Set[str]) -> None:
        """
        Sets the words collection

        :param words_collection: the new words collection
        """
        self.__words_collection = words_collection

    # endregion property: words_collection

    # endregion GET & SET

    def create_board(self) -> None:
        """
        Creates a new board: 2 dimentional matrix with letter values
        """
        self.__board = bb_randomizer.randomize_board()

    def update_word_and_path(self, board_coordinate: Tuple[int, int]) -> None:
        """
        Updates the current word and path according to a given coordinate

        :param board_coordinate: the pressed coordinate on the board
        """
        y, x = board_coordinate

        # checks whether the last button pressed is the same as now
        if self.__current_path and self.__current_path[-1] == board_coordinate:
            # undo
            self.__current_path.remove(board_coordinate)
            slice_index = len(self.__current_word) - len(self.__board[y][x])
            self.__current_word = self.__current_word[:slice_index]
        else:
            # add
            self.__current_word += self.__board[y][x]
            self.__current_path.append(board_coordinate)

    def check_word(self) -> str:
        """
        Reacts to the given word input with an appropriate message to the
        situation
        """

        # verifications
        existing_word = self.__current_word not in self.__words_collection
        if existing_word:
            return f"'{self.__current_word}' is not a word"

        word_found = self.__current_word in self.__words_found
        if word_found:
            return f"You already found '{self.__current_word}'"

        # passed verifications
        self.__words_found.add(self.__current_word)
        self.__increase_score()

        # show message based on word length
        if len(self.__current_word) < 6:
            return f"You found '{self.__current_word}'"
        else:
            return f"You found '{self.__current_word}'. Nice work!"

    def reset_current_input(self) -> None:
        """
        Resets the current user's input
        """
        self.__current_word = ""
        self.__current_path = []

    def get_buttons_to_enable(self) -> List[Tuple[int, int]]:
        """
        Returns a list of buttons to enable, including the last button
        pressed, and all of its neighbors that haven't been selected yet
        """
        base_row, base_col = self.__current_path[-1]
        button_coordinates_list = [(base_row, base_col)]

        # iterates through neighbours
        for delta_row, delta_col in utils.NEIGHBOURS_DELTA.values():
            neighbour_coordinate = (base_row + delta_row, base_col + delta_col)

            inbounds = self.__is_coordinate_in_boundaries(neighbour_coordinate)
            not_chosen = neighbour_coordinate not in self.__current_path
            if inbounds and not_chosen:
                button_coordinates_list.append(neighbour_coordinate)

        return button_coordinates_list

    def __is_coordinate_in_boundaries(self, coordinate: Tuple[int, int]) -> \
            bool:
        """
        Checks if the given coordinate is within the board's boundaries

        :param coordinate: the coordinate to check
        :return: True if the coordinate is within the board's boundaries,
                 False otherwise
        """
        return 0 <= coordinate[0] < len(self.__board) and \
               0 <= coordinate[1] < len(self.__board[0])


if __name__ == "__main__":
    print("The file is part of the game 'Boggle'.\n"
          "You can play it by running:\n"
          "> python boggle.py")
