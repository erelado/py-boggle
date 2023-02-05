"""
FILE: utils.py
DESCRIPTION: Utility functions that we were required to implement
"""
from typing import List, Tuple, Iterable, Optional, Dict, Set, Callable, Union

Board = List[List[str]]
Path = List[Tuple[int, int]]

# region CONSTANTS
NEIGHBOURS_DELTA: Dict[str, Tuple[int, int]] = {
    # "direction": (row_delta, col_delta)
    "N": (-1, 0),
    "NE": (-1, 1),
    "E": (0, 1),
    "SE": (1, 1),
    "S": (1, 0),
    "SW": (1, -1),
    "W": (0, -1),
    "NW": (-1, -1)
}


# endregion CONSTANTS

def load_words_dict(filepath):
    """
    Loads a dictionary of words from a file

    :param filepath: The path of the file to load
    :return: A set of words
    """
    with open(filepath) as file:
        return set(file.read().splitlines())


def __get_value_by_coordinate(board: Board, coordinate: Tuple[int, int]) -> \
        str:
    """
    Returns the current value of the given coordinate

    :param board: the board
    :param coordinate: a coordinate on the board
    :return: The value in board of the given coordinate
    """
    row, col = coordinate
    return board[row][col]


def __are_neighbours(coordinate1: Tuple[int, int],
                     coordinate2: Tuple[int, int]):
    """
    Checks if two coordinates are neighbours

    :param coordinate1: the first coordinate to compare
    :param coordinate2: the second coordinate to compare
    :return: True if both coordinates are neighbours, False otherwise
    """
    row1, col1 = coordinate1

    for row_delta, col_delta in NEIGHBOURS_DELTA.values():
        if (row1 + row_delta, col1 + col_delta) == coordinate2:
            return True

    return False


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> \
        Optional[str]:
    """
    Checks if a path is valid, meaning: whether the path is made of
    neighbours, and the word exists in the words' collection

    :param board: the board
    :param path: the current path of cells chosen
    :param words: the words collection
    :return: The word if it is valid, None otherwise
    """
    word: str = ''

    for path_index in range(len(path) - 1):
        # check whether two following cells are actually neighbours on board
        if not __are_neighbours(path[path_index], path[path_index + 1]):
            return None

        # add the current coordinate's value
        word += __get_value_by_coordinate(board, path[path_index])

    # add the last value
    word += __get_value_by_coordinate(board, path[-1])

    if word in words:
        return word

    return None


def __is_coordinate_in_board(board: Board, coordinate: Tuple[int, int]) -> \
        bool:
    """
    Checks if the given coordinate is within the board's boundaries

    :param board: the board
    :param coordinate: the coordinate to check
    :return: True if the coordinate is within the board's boundaries,
             False otherwise
    """
    return 0 <= coordinate[0] < len(board) and \
           0 <= coordinate[1] < len(board[0])


def __find_neighbour_coordinate(coordinate: Tuple[int, int],
                                delta: Tuple[int, int]) -> Tuple[int, int]:
    """
    Computes the neighbour's coordinate by a given delta

    :param coordinate: the starting coordinate
    :param delta: the delta for the required neighbour
    :return: the neighbour's coordinate
    """
    neighbour_row = coordinate[0] + delta[0]
    neighbour_col = coordinate[1] + delta[1]
    return neighbour_row, neighbour_col


def __filter_words_set_by_prefix(words_set: Set[str], prefix: str) -> Set[str]:
    """
    Filters the words set, finding only the words starting with the
    given prefix

    :param words_set: the set to filter
    :param prefix: the prefix to filter by
    :return: a filtered set
    """
    return set(filter(lambda s: s.startswith(prefix), words_set))


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> \
        List[Path]:
    """
    Finds all valid paths of length 'n'

    :param n: the length of the required paths
    :param board: the board
    :param words: the words collection
    :return: a list containing all valid paths of length 'n'
    """

    def stop(n: int, path: Path, word: str) -> bool:
        return len(path) == n

    def update(lst_paths: List[Path], path: Path, word: str) -> None:
        lst_paths.append(path[:])

    lst_paths: List[Path] = []

    __backtracking_start(stop, update, n, board, words, lst_paths)

    return lst_paths


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> \
        List[Path]:
    """
    Finds all paths on the board that yield words of length 'n'

    :param n: the length of the required paths
    :param board: the board
    :param words: the words collection
    :return: a list of paths to words of length 'n'; may include more than
             one path to a word
    """

    def stop(n: int, path: Path, word: str) -> bool:
        return len(word) == n

    def update(lst_paths: List[Path], path: Path, word: str) -> None:
        lst_paths.append(path[:])

    lst_paths: List[Path] = []

    __backtracking_start(stop, update, n, board, words, lst_paths)

    return lst_paths


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
    By a given board and words collection, returns a list of valid
    routes that provide the maximum score

    :param board: the board
    :param words: the words collection
    :return: a list of valid routes that provide the maximum game score
    """

    def stop(n: int, path: Path, word: str) -> bool:
        return len(word) == n

    def update(dict_paths: Dict[str, List[Path]], path: Path,
               word: str) -> None:
        if word not in dict_paths.keys():
            dict_paths[word] = []
        dict_paths[word].append(path[:])

    dict_paths: Dict[str, List[Path]] = {}

    # perform a similar function to find_length_n_words, for each
    # word-length that can be found in the given words bank.
    # this has the same effect as iterating over all words, but with
    # fewer actions to perform.
    word_lengths: Set[int] = set(map(lambda s: len(s), words))
    for length in word_lengths:
        __backtracking_start(stop, update, length, board, words, dict_paths)

    # create a list of the longest paths found, by taking the longest
    # path for each word found.
    longest_paths: List[Path] = []
    for lst_paths in dict_paths.values():
        longest_paths.append(max(lst_paths, key=lambda p: len(p)))

    return longest_paths


def __backtracking_start(stop_condition: Callable, data_update_func: Callable,
                         n: int, board: Board, words: Iterable[str],
                         dataset: Union[List[Path], Dict[str, List[Path]]]) -> \
        None:
    """
    Start the backtracking action for each coordinate

    :param stop_condition: a boolean function that defines the recursion's
    stop condition. Recieves the integer 'n', the current path and the
    current word.
    :param data_update_func: a function that updates the dataset, to be
    called only when needed. This will update the dataset, so the function
    returns nothing.
    :param n: the length required
    :param board: the board
    :param words: the words collection
    :param dataset: either a list of paths, or a dictionary mapping words
    to lists of paths.
    """
    # create a set out of the iterator, so it can be read more than once
    words_set = set(words)

    # pick the starting coordinate
    for row_index in range(len(board)):
        for col_index in range(len(board[row_index])):

            # initialize values for this starting coordinate
            coordinate = (row_index, col_index)
            curr_word = __get_value_by_coordinate(board, coordinate)
            filtered_words = __filter_words_set_by_prefix(words_set, curr_word)

            # only proceed if words with this prefix can be found.
            # otherwise, skip to the next coordinate.
            if len(filtered_words) == 0:
                continue

            curr_path: Path = [coordinate]

            # recursively find paths starting from this coordinate
            __backtracking_action(stop_condition, data_update_func, n, board,
                                  words_set, dataset, curr_path, curr_word)


def __backtracking_action(stop_condition: Callable, data_update_func: Callable,
                          n: int, board: Board, words_set: Set[str],
                          dataset: Union[List[Path], Dict[str, List[Path]]],
                          curr_path: Path, curr_word: str) -> None:
    """
    Crawl the board. To be called from _backtracking_start.
    """
    if stop_condition(n, curr_path, curr_word):
        if curr_word in words_set:
            data_update_func(dataset, curr_path, curr_word)
        return

    # try all neighbours
    for delta in NEIGHBOURS_DELTA.values():
        neighbour = __find_neighbour_coordinate(curr_path[-1], delta)

        # try only if neighbour is within the board's boundaries
        if not __is_coordinate_in_board(board, neighbour):
            continue

        # try only if the neighbour hasn't been stepped through yet
        if neighbour in curr_path:
            continue

        # extend the word and filter the words set
        new_word = curr_word + __get_value_by_coordinate(board, neighbour)
        filtered_words = __filter_words_set_by_prefix(words_set, new_word)

        if len(filtered_words) == 0:
            continue

        # extend the path
        curr_path.append(neighbour)

        # recursive call with the path and word extended
        __backtracking_action(stop_condition, data_update_func,
                              n, board, filtered_words, dataset, curr_path,
                              new_word)

        # clean up for backtracking
        curr_path.pop()


if __name__ == "__main__":
    print("The file is part of the game 'Boggle'.\n"
          "You can play it by running:\n"
          "> python boggle.py")
