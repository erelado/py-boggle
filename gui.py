"""
FILE: gui.py
DESCRIPTION: Represents the 'Boggle' game's GUI. There is no game logic
associated with it, only visual design elements
"""
# region import
from typing import List, Dict, Tuple, Callable, Literal
from idlelib.tooltip import Hovertip
from datetime import timedelta
import tkinter as tki
import tkinter.messagebox

# endregion import

# region GAME SETTINGS
BOARD_SIZE: int = 4
TIMER_DURATION: int = 180  # default duration of the timer, in seconds
TIMER_DELAY_IN_MS: int = 1000  # default delay in milliseconds
BOARD_BUTTON_TEXT: str = "❓"  # default text of a button on the board
FONT: str = 'Segoe UI'
# endregion GAME SETTINGS
# region COLORS
TEXT_FG_COLOR: str = "#27333F"
LIGHT_TEXT_FG_COLOR: str = "#FDFDFD"
INFO_HUD_BG_COLOR: str = "#1C82AD"
BOARD_FRAME_BG_COLOR: str = "#82AAE3"
BUTTON_FG_COLOR: str = "#F1F6F5"
BOARD_BUTTON_BG_COLOR: str = "#344D67"
BOARD_BUTTON_ACTIVE_FG_COLOR: str = "#E3F6FF"
BOARD_BUTTON_ACTIVE_BG_COLOR: str = "#00337C"
ACTION_BUTTON_BG_COLOR: str = "#6ECCAF"
ACTION_BUTTON_ACTIVE_FG_COLOR: str = "#F3ECB0"
ACTION_BUTTON_ACTIVE_BG_COLOR: str = "#86C8BC"

# endregion COLORS
# region CONSTANTS
FONT_TYPES: Dict = {
    "button": (FONT, 20, 'bold'),
    "board_button": (FONT, 16, 'bold'),
    "info_title": (FONT, 20, 'bold', 'underline'),
    "info": (FONT, 20),
    "listbox": (FONT, 14)
}
BOARD_BUTTON_STYLE: Dict = {
    "font": FONT_TYPES['board_button'],
    "text": BOARD_BUTTON_TEXT,
    "foreground": BUTTON_FG_COLOR,
    "background": BOARD_BUTTON_BG_COLOR,
    "activeforeground": BOARD_BUTTON_ACTIVE_FG_COLOR,
    "activebackground": BOARD_BUTTON_ACTIVE_BG_COLOR,
    "padx": 5,
    "pady": 5
}
ACTION_BUTTON_STYLE: Dict = {
    "font": FONT_TYPES['button'],
    "foreground": BUTTON_FG_COLOR,
    "background": ACTION_BUTTON_BG_COLOR,
    "activeforeground": ACTION_BUTTON_ACTIVE_FG_COLOR,
    "activebackground": ACTION_BUTTON_ACTIVE_BG_COLOR
}

MESSAGES = {
    "GAME_OVER": "The game has come to an end.\n"
                 "You managed to find {0} words, and score a total of {1} "
                 "points.",
    "STOP_GAME": "It is too bad you did not stay until the end...\n"
                 "You managed to find {0} words, and score a total of {1} "
                 "points."
}


# endregion CONSTANTS


class GUI:
    """
    Represents the user interface of the 'Boggle' game
    """

    # region INIT GAME WINDOW
    def __init__(self) -> None:
        self._init_vars()  # creates all variables
        self._init_window()  # creates all screen components

    def _init_vars(self) -> None:
        """
        Initializes all the variables used in the game
        """
        # jobs
        self.__word_input_label_job = None

        # variables
        self.__score: int = 0
        self.__current_word: str = "❓"
        self.__is_game_running: bool = False
        self.__time_left: int = TIMER_DURATION

    def _init_window(self) -> None:
        """
        Initializes the main window
        """
        self._root = tki.Tk()
        self._root.title('Boggle')

        # sets the screen size relative to the user's
        self._screen_width = self._root.winfo_screenwidth() // 2
        self._screen_height = self._root.winfo_screenheight() // 2
        # sets minimum window size
        self._root.minsize(width=960, height=620)

        # changes icon
        icon = tki.PhotoImage(file='media/boggle-icon.png')
        self._root.wm_iconphoto(False, icon)

        # creates the game window
        self._frame_game_init()
        self._frame_info_init()

    # region game frame
    def _frame_game_init(self) -> None:
        """
        Creates the 'game' frame: the main frame which includes the game
        board and action buttons
        """
        self._frame_game = tki.Frame(self._root, highlightthickness=10)
        self._frame_game.pack(side=tki.LEFT, fill=tki.BOTH, expand=True)

        self._label_timer_init()
        self._frame_board_init()
        self._frame_board_word_input_init()
        self._frame_board_actions_init()

    def _label_timer_init(self) -> None:
        """
        Creates and displays the timer
        """
        td = str(timedelta(seconds=TIMER_DURATION))
        self._label_timer = tki.Label(
            self._frame_game,
            font=FONT_TYPES['info'],
            text=td
        )
        self._label_timer.pack(side=tki.TOP)

    def _frame_board_init(self) -> None:
        """
        Creates and displays the game's board
        """
        self._frame_board = tki.Frame(
            self._frame_game,
            bg=BOARD_FRAME_BG_COLOR
        )
        self._frame_board.pack(expand=True)

        self._buttons_board = dict()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self._buttons_board[(i, j)] = tki.Button(
                    self._frame_board,
                    width=5,
                    height=2,
                    **BOARD_BUTTON_STYLE
                )
                self._buttons_board[(i, j)].grid(
                    row=i, column=j,
                    padx=10, pady=10
                )

    def _frame_board_word_input_init(self) -> None:
        """
        Creates and displays the word input label, which responds to a given
        word by the user
        """
        self._label_word_input = tki.Label(
            self._frame_game,
            font=FONT_TYPES['info']
        )
        self._label_word_input.pack(side=tki.TOP)

    def _frame_board_actions_init(self) -> None:
        """
        Creates and displays the 4x4 board cells
        """
        self._frame_board_actions = tki.Frame(self._frame_game)
        self._frame_board_actions.pack(expand=True)

        self._button_play_init()

    def _button_play_init(self) -> None:
        """
        Creates the play button
        """
        self._button_play = tki.Button(
            self._frame_board_actions,
            text='▶',
            width=25,
            **ACTION_BUTTON_STYLE
        )
        self._tooltip_play = Hovertip(
            self._button_play, "Start game", hover_delay=200
        )
        self._button_play.grid(column=0, row=0, padx=20)

    def _button_board_actions_init(self) -> None:
        """
        Creates the board's action buttons
        """
        # stop button
        self._button_stop = tki.Button(
            self._frame_board_actions,
            width=6,
            text='■',
            command=self.button_stop_on_press,
            **ACTION_BUTTON_STYLE
        )
        self._tooltip_stop = Hovertip(
            self._button_stop, "Stop game", hover_delay=200
        )

        # restart button
        self._button_restart = tki.Button(
            self._frame_board_actions,
            width=6,
            text='↻',
            **ACTION_BUTTON_STYLE
        )
        self._tooltip_restart = Hovertip(
            self._button_restart, "Restart game", hover_delay=200
        )

        # check button
        self._button_check = tki.Button(
            self._frame_board_actions,
            width=6,
            text='✓',
            **ACTION_BUTTON_STYLE
        )
        self._tooltip_check = Hovertip(
            self._button_check, "Check word", hover_delay=200
        )

        self.__show_game_actions_buttons()

    # endregion game frame
    # region info frame
    def _frame_info_init(self) -> None:
        """
        Creates the 'information' frame: the side frame which includes data
        about the game itself
        """
        self._frame_info = tki.Frame(
            self._root,
            background=INFO_HUD_BG_COLOR,
            width=300
        )
        self._frame_info.pack(side=tki.RIGHT, fill=tki.BOTH, expand=False)
        self._frame_info.pack_propagate(False)  # overrides default width

        self._container_score_init()
        self._container_curr_word_init()
        self._container_words_found_init()

    def _container_score_init(self) -> None:
        """
        Creates a container for the score's data
        """
        # container
        self._container_score = tki.Frame(
            self._frame_info,
            background=INFO_HUD_BG_COLOR
        )
        self._container_score.pack(
            side=tki.TOP,
            fill=tki.BOTH,
            pady=(0, 60))

        # title
        self._label_score_title = tki.Label(
            self._container_score,
            text='Score:',
            background=INFO_HUD_BG_COLOR,
            font=FONT_TYPES['info_title']
        )
        self._label_score_title.pack(side=tki.TOP)

        # data label
        self._label_score = tki.Label(
            self._container_score,
            text=self.__score,
            foreground=LIGHT_TEXT_FG_COLOR,
            background=INFO_HUD_BG_COLOR,
            font=FONT_TYPES['info']
        )
        self._label_score.pack(side=tki.TOP)

    def _container_curr_word_init(self) -> None:
        """
        Creates a container for the current word selected by the user
        """
        # container
        self._container_current_word = tki.Frame(
            self._frame_info,
            background=INFO_HUD_BG_COLOR
        )
        self._container_current_word.pack(
            side=tki.TOP,
            fill=tki.BOTH,
            pady=(0, 60))

        # title
        self._label_curr_word_title = tki.Label(
            self._container_current_word,
            text='Current word:',
            background=INFO_HUD_BG_COLOR,
            font=FONT_TYPES['info_title']
        )
        self._label_curr_word_title.pack(side=tki.TOP)

        # data label
        self._label_current_word = tki.Label(
            self._container_current_word,
            text=self.__current_word,
            foreground=LIGHT_TEXT_FG_COLOR,
            background=INFO_HUD_BG_COLOR,
            font=FONT_TYPES['info']
        )
        self._label_current_word.pack(side=tki.TOP)

    def _container_words_found_init(self) -> None:
        """
        Creates a container for the words found by the user
        """
        # container
        self._container_words_found = tki.Frame(
            self._frame_info,
            background=INFO_HUD_BG_COLOR
        )
        self._container_words_found.pack(
            side=tki.TOP,
            fill=tki.BOTH)

        # title
        self._label_words_found_title = tki.Label(
            self._container_words_found,
            text='Words found:',
            background=INFO_HUD_BG_COLOR,
            font=FONT_TYPES['info_title']
        )
        self._label_words_found_title.pack(side=tki.TOP)

        # data listbox
        self._label_words_found = tki.Listbox(
            self._container_words_found,
            width=28,
            height=200,
            activestyle='dotbox',
            foreground=LIGHT_TEXT_FG_COLOR,
            background=INFO_HUD_BG_COLOR,
            font=FONT_TYPES['listbox']
        )
        self._label_words_found.pack(side=tki.LEFT, fill=tki.BOTH)

        # scrollbar
        self._scrollbar = tki.Scrollbar(self._container_words_found)
        self._scrollbar.pack(side=tki.RIGHT, fill=tki.BOTH)

        # attaching listbox to scrollbar
        self._label_words_found.config(yscrollcommand=self._scrollbar.set)
        # setting vertical view
        self._scrollbar.config(command=self._label_words_found.yview)

    # endregion info frame
    # endregion INIT GAME WINDOW
    # region GET & SET
    @property
    def buttons_board(self) -> Dict[Tuple[int, int], tki.Button]:
        """
        Returns the board's buttons
        """
        return self._buttons_board

    @property
    def button_play(self) -> tki.Button:
        """
        Returns the 'play' button
        """
        return self._button_play

    @property
    def button_restart(self) -> tki.Button:
        """
        Returns the 'restart' button
        """
        return self._button_restart

    @property
    def button_check(self) -> tki.Button:
        """
        Returns the 'check' button
        """
        return self._button_check

    # region property: score
    @property
    def score(self) -> int:
        """
        Returns the game's score
        """
        return self.__score

    @score.setter
    def score(self, value: int) -> None:
        """
        Sets the score of the game

        :param value:  the score to set
        """
        self.__score = value

    # endregion property: score
    # region property: current_word
    @property
    def current_word(self) -> str:
        """
        Returns the current_word
        """
        return self.__current_word

    @current_word.setter
    def current_word(self, value: str) -> None:
        """
        Sets the current word
        :param value: the word to set
        """
        self.__current_word = value

    # endregion property: current_word

    # endregion GET & SET
    # region GAME RUN-TIME LOGIC
    # region timer
    def __countdown(self, time) -> None:
        """
        Starts the timer's countdown
        :param time: the starting time
        """
        self.__time_left = time
        self._label_timer['text'] = str(timedelta(seconds=time))

        if time == 0:
            # end game
            self.__is_game_running = False
            self.__end_game()
            return

        if self.__is_game_running:
            # continue the countdown
            self._countdown_job = \
                self._root.after(TIMER_DELAY_IN_MS, self.__countdown, time - 1)

    def __stop_countdown(self) -> None:
        """
        Stops the timer's countdown
        """
        if self._countdown_job is not None:
            self._root.after_cancel(self._countdown_job)
            self._countdown_job = None

    def __clear_word_input_job(self) -> None:
        """
        Clears the input's countdown, making room for a new one
        """
        if self.__word_input_label_job:
            self._root.after_cancel(self.__word_input_label_job)
            self.__word_input_label_job = None

    # endregion timer
    # region board buttons

    def show_board(self, board) -> None:
        """
        Generates & updates the board cells' values
        """
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self._buttons_board[(row, col)].config(
                    text=board[row][col], foreground=BUTTON_FG_COLOR)

    def hide_board(self) -> None:
        """
        Hides the board cells' values
        """
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self._buttons_board[(row, col)].config(
                    text=BOARD_BUTTON_TEXT,
                    foreground=TEXT_FG_COLOR
                )

    def set_board_buttons_command(self, coordinate: Tuple[int, int],
                                  command: Callable[[], None]) -> None:
        """
        Sets the command for the board buttons
        """
        self._buttons_board[coordinate].config(command=command)

    def set_all_board_buttons_state(
            self, state: Literal["disabled", "normal"]) -> None:
        """
        Sets the state to all board buttons
        """
        for button in self._buttons_board.values():
            button.config(state=state)

    def update_board_buttons_state(
            self, buttons_to_enable: List[Tuple[int, int]]) -> None:
        """
        Updates the state of specific board buttons
        """
        self.set_all_board_buttons_state(tki.DISABLED)
        self.enable_given_board_buttons(buttons_to_enable)

    def enable_given_board_buttons(
            self, buttons_to_enable: List[Tuple[int, int]]) -> None:
        """
        Enables specific board buttons
        """
        for coordinate in buttons_to_enable:
            self._buttons_board[coordinate].config(state=tki.NORMAL)

    # endregion board buttons
    # region game action buttons
    def button_play_on_press(self) -> None:
        """
        Starts the game
        """
        self.__is_game_running = True

        self.update_current_word()

        self._button_play['state'] = tki.DISABLED
        self._button_play.grid_forget()

        self._button_board_actions_init()
        self.set_all_board_buttons_state(tki.NORMAL)

        self.__countdown(TIMER_DURATION)

    def button_stop_on_press(self) -> None:
        """
        Stops the game
        """
        # pause game
        self.__is_game_running = False

        # popup messagebox
        msg_box = tki.messagebox.askquestion(
            "Stop game",
            "Are you sure you want to stop the current game?",
            icon="warning"
        )

        # resume game
        self.__is_game_running = True

        if msg_box == 'yes':
            self.__end_game()
            return

        self.__countdown(self.__time_left)

    def button_restart_on_press(self) -> None:
        """
        Restarts the game
        """
        self._init_vars()
        self._frame_game.destroy()
        self._frame_game_init()
        self._frame_info.destroy()
        self._frame_info_init()
        self.__stop_countdown()
        self.button_play_on_press()

    def button_check_on_press(self, response: str) -> None:
        """
        Validates the generated word by the player
        """
        self._label_word_input['text'] = response
        self.set_all_board_buttons_state(tki.NORMAL)
        self.__clear_word_input_job()
        self.__word_input_label_job = self._root.after(
            3000, self.__remove_word_input_text
        )

    def __show_game_actions_buttons(self) -> None:
        """
        Shows the board actions buttons
        """
        self._button_stop.grid(column=0, row=0, padx=22)
        self._button_restart.grid(column=1, row=0, padx=22)
        self._button_check.grid(column=2, row=0, padx=22)

    def __hide_game_action_buttons(self) -> None:
        """
        Hides the board's action buttons
        """
        self._button_stop.grid_forget()
        self._button_restart.grid_forget()
        self._button_check.grid_forget()

    # endregion game action buttons
    # region check word input
    def add_word_to_words_found(self, word) -> None:
        """
        Appends a word to the 'words found' listbox
        :param word: the word to be added
        """
        self._label_words_found.insert(tki.END, word)

    def update_current_word(
            self, content="", fg_color=LIGHT_TEXT_FG_COLOR) -> None:
        """
        Updates the current word
        :param content: the new content of the current word
        :param fg_color: the color of the current word
        """
        self._label_current_word.config(text=content, fg=fg_color)

    def update_score(self, score: int) -> None:
        """
        Updates the score
        :param score: the score to be updated
        """
        self.__score = score
        self._label_score.config(text=str(self.__score))

    def __remove_word_input_text(self) -> None:
        """
        Deletes the text on the label which indicates the validity of the
        input word given
        """
        self._label_word_input['text'] = ""

    # endregion check word input

    def __prompt_end_game_message(self) -> None:
        """
        Prompts the player with an end-game message according to the
        board's state
        """
        if self.__is_game_running:
            # stops the game
            self.__is_game_running = False

            # game over messagebox
            game_over_msg = MESSAGES['STOP_GAME'].format(
                self._label_words_found.size(), self.__score
            )
            tki.messagebox.showinfo("Stay a little longer?", game_over_msg)
        else:
            # game over messagebox
            game_over_msg = MESSAGES['GAME_OVER'].format(
                self._label_words_found.size(), self.__score
            )
            tki.messagebox.showinfo("Time's up!", game_over_msg)

    def __end_game(self) -> None:
        # shows appropriate message
        self.__prompt_end_game_message()

        # reconfigures variables to their 'init' state
        self._init_vars()
        self.update_current_word(content=BOARD_BUTTON_TEXT)
        self.update_score(score=0)
        self._label_words_found.delete(0, tki.END)

        # timer
        self.__stop_countdown()
        self._label_timer['text'] = str(timedelta(seconds=TIMER_DURATION))

        # action button
        self.__hide_game_action_buttons()
        self._button_play['state'] = tki.NORMAL
        self._button_play.grid(column=0, row=0, padx=20)

        # hide board buttons
        self.set_all_board_buttons_state(tki.DISABLED)
        self.hide_board()

    def run(self) -> None:
        """
        Starts the mainloop
        """
        self._root.mainloop()
    # endregion GAME RUN-TIME LOGIC


if __name__ == "__main__":
    print("The file is part of the game 'Boggle'.\n"
          "You can play it by running:\n"
          "> python boggle.py")
