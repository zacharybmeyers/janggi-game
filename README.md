# portfolio-project

**Remember that this project cannot be submitted late.**

Write a class named JanggiGame for playing an abstract board game called Janggi. Please read the "Board", "Pieces" and the overall "Rules" section on [the Wikipedia page](https://en.wikipedia.org/wiki/Janggi).  You do _not_ have to implement the rules regarding perpetual check, position repetition, any kind of draw or the miscellaneous rules. You **do** need to correctly handle checkmate. You also need to correctly handle all piece-specific rules, e.g. generals aren't allowed to leave the palace, horses and elephants can be blocked, cannons cannot capture other cannons, etc. A good video describing the rules is [here](https://www.youtube.com/watch?v=X5IJaPoQ0oQ).

A general is in check if it could be captured on the opposing player's next move. A player cannot make a move that puts or leaves their general in check. The game ends when one player **checkmates** the other's general.  You don't actually capture a general, instead you have to put it in such a position that it cannot escape being in check, meaning that no matter what, it could be captured on the next move.  This works the same as in chess, if you're familiar with that game.

Unlike chess, Janggi allows you to pass a turn and thus there is no stalemate (a scenario when no legal moves can be made).

Your program should have Blue and Red as the competing players and Blue as the starting player. You do not need to implement any special mechanism for figuring out who can start the game. 

Locations on the board will be specified using "algebraic notation", with columns labeled a-i and rows labeled 1-10, with row 1 being the Red side and row 10 the Blue side. Your initial board setup should have the Elephant transposed with the Horse, on the right side, as seen on the image from Wikipedia. You can use [this spreadsheet](https://docs.google.com/spreadsheets/d/1Lfl4IaSGqQaBYZmoD2wOrTVkXS2E7BP9v6N4p5sDPgM/edit?usp=sharing) as a reference to understand the initial board layout as well as to simulate your moves.

You're not required to print the board, but you will probably find it very useful for testing purposes.

Your JanggiGame class **must** include the following:
* An `init` method that initializes any data members.
* A method called `get_game_state` that just returns one of these values, depending on the game state: 'UNFINISHED' or 'RED_WON' or 'BLUE_WON'.
* A method called `is_in_check` that takes as a parameter either 'red' or 'blue' and returns True if that player is in check, but returns False otherwise.
* A method called `make_move` that takes two parameters - strings that represent the square to move from and the square to move to.  For example, `make_move('b3', 'b10')`.  If the square being moved from does not contain a piece belonging to the player whose turn it is, or if the indicated move is not legal, or if the game has already been won, then it should just return False.  Otherwise it should make the indicated move, remove any captured piece, update the game state if necessary, update whose turn it is, and return True.

If the `make_move` method is passed the same string for the square moved from and to, it should be processed as the player passing their turn, and return True.

Feel free to add whatever other classes, methods, or data members you want.  All data members must be private.  Every class should have an init method that initializes all of the data members for that class.

Here's a very simple example of how the class could be used:
```
game = JanggiGame()
move_result = game.make_move('c1', 'e3') #should be False because it's not Red's turn
move_result = game.make_move('a7,'b7') #should return True
blue_in_check = game.is_in_check('blue') #should return False
game.make_move('a4', 'a5') #should return True
state = game.get_game_state() #should return UNFINISHED
game.make_move('b7','b6') #should return True
game.make_move('b3','b6') #should return False because it's an invalid move
game.make_move('a1','a4') #should return True
game.make_move('c7','d7') #should return True
game.make_move('a4','a4') #this will pass the Red's turn and return True
```

The file must be named: **JanggiGame.py** and it should not contain any test code outside the main() function. Your code for this project should **not** be made public, in any manner, until after the term has ended.
