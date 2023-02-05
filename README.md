![Project Preview Image](https://github.com/E-RELevant/py-boggle/blob/main/media/preview.png)

# py-boggle (GUI)
## 📙 About the project

An implementation of the 'Boggle' game.

In this game, each dice is marked with a letter (or several), forming a 4x4
dice board. there is only one player, and the player has three minutes to get as
many points as possible by finding legal words on the board.

Legal words appear in the dictionary and consist of a route on the game
board that starts with one letter and goes to neighboring letters, when it is
forbidden to use the same dice more than once.

The length of each word's route is calculated into a square score; i.e. for a
word of length N, you will receive N<sup>2</sup> points.

## 🚩 Getting started

run:

```shell
> python boggle.py
```

The program uses `tkinter`, Python's standard GUI package. If you do not
already have `tkinter`, you can install it with:

```shell
> pip install -r requirements.txt
```

## ✨ Additional features

- [x] Responsive, modern design, with a custom icon and color palette.
- [x] At any point in the game, only legal moves can be made - buttons that allow
illegal moves are dynamically disabled.
- [x] The player can:
  - [x] UNDO their last step by pressing the same dice again.
  - [x] RESTART the game at any time. A new game board is generated, and the game
    starts immediately.
  - [x] STOP at any time. A message will be displayed to confirm the selection. If
    so, The game will end, displaying the results the player has achieved so
    far. Otherwise, the game will resume.
- [x] View a short description of the action buttons by hovering the mouse over
them.
- [x] A special congratulatory message is shown when the player finds a
remarkably long word.

### 💡 Ideas
- [ ] Menu bar
  - [ ] Settings
    - [ ] Custom time
      - [ ] Unlimited mode
    - [ ] Custom allowed shuffles/hints
    - [ ] Theme (GUI Color schemes)
      - [ ] Light/dark modes
  - [ ] Exit
- [ ] Actions
  - [ ] Shuffle: shuffle the game board for points/time
  - [ ] Hint: simulating pressing the board's buttons to select a random word from four to ten letters
  - [ ] Rotate: rotating the game board by 90 degrees for a realistic image of the game
- [ ] Information HUD
  - [ ] Best score: saving and displaying the maximum score
  - [ ] Available words: amount of words in the current board that can be found
  - [ ] Word definition: a dictionary definition will appear when you click on a word in the 'found words' bank
- [ ] Sound effects

## 💻 Built with

The game was built in `Python 3.9`, using the `tkinter` package ("Tk interface") GUI toolkit.

Designed and tested on Windows 11, and Ubuntu 18.04.
