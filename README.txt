This is a Reversi game played by different AI algorithms.

How to Use:
Run reversi.py with optional keys for different AI models.

The optional keys are:

 "-displayAllActions n": Displays all available actions at turn n (where n is the turn number).
 "-methodical n": Displays the game turns until turn n (where n is the turn number).
 "-random n": Actions will be picked at random, and the game turns will be displayed until turn n (where n is the turn number).
 "H1": Actions will be picked using heuristic function H1 (refer to section 2).
 "H2": Actions will be picked using heuristic function H2 (refer to section 2).
 "H1/H2 H1/H2": Example: reversi.py H1 H2. Use one of the combinations to set the AI model for each of the two players and observe how they play against each other.
 "H1/H2 -ahead n": Example: reversi.py H1 -ahead 2. Let the AI explore a deeper decision tree for a higher win rate; n specifies the depth of the tree.

Below are some examples of the output from my code.

Question 1:

    State: class GameState under game.py file
        grid: 2D matrix
        player: 2 players
        state: the state number
        player_turn: who out of the players goes next
        prev_game_state: previous state

    Action: (row, col, sign)
        row and col indicate where we want to put a disk on the board and the sign of the disk

    1.1:
        state space: we have 64 places to put a disk and we have 2 different disks plus an empty space,
        3*3*3*3*........*3*3 = 3**64

    1.2:
        illegal state:
            --------
            ------X-
            --------
            ---X0---
            ---0X---
            --------
            --------
            --------

        unreachable state:
            --------
            --------
            --------
            ---X0---
            --------
            --------
            --------
            --------

            * By the rules of the game we start at 4 disks on the middle, so any amount of disks that is less then 4
              or the disks are placed in a different position then on the middle is a unreachable state

    1.A:
        * Actions are picked from top to down and left to right
        run: reversi.py -displayAllActions 7
        output:
            State 3
            --------
            --------
            --XXX---
            ---XX---
            ---0X---
            --------
            --------
            --------
            State 4, Player 2 moved, Action: put 0 on position (1, 3)
            --------
            ---0----
            --X0X---
            ---0X---
            ---0X---
            --------
            --------
            --------
            Result - Player 1: 4 disks, Player 2: 4 disks, Total: 8 disks

            State 3
            --------
            --------
            --XXX---
            ---XX---
            ---0X---
            --------
            --------
            --------
            State 4, Player 2 moved, Action: put 0 on position (2, 5)
            --------
            --------
            --XXX0--
            ---X0---
            ---0X---
            --------
            --------
            --------
            Result - Player 1: 5 disks, Player 2: 3 disks, Total: 8 disks

            State 3
            --------
            --------
            --XXX---
            ---XX---
            ---0X---
            --------
            --------
            --------
            State 4, Player 2 moved, Action: put 0 on position (4, 5)
            --------
            --------
            --XXX---
            ---XX---
            ---000--
            --------
            --------
            --------
            Result - Player 1: 5 disks, Player 2: 3 disks, Total: 8 disks

    1.B:
        run: reversi.py -methodical 5
        output:
            State 0
            --------
            --------
            --------
            ---X0---
            ---0X---
            --------
            --------
            --------
            State 1, Player 1 moved, Action: put X on position (2, 4)
            --------
            --------
            ----X---
            ---XX---
            ---0X---
            --------
            --------
            --------
            Result - Player 1: 4 disks, Player 2: 1 disks, Total: 5 disks

            State 1
            --------
            --------
            ----X---
            ---XX---
            ---0X---
            --------
            --------
            --------
            State 2, Player 2 moved, Action: put 0 on position (2, 3)
            --------
            --------
            ---0X---
            ---0X---
            ---0X---
            --------
            --------
            --------
            Result - Player 1: 3 disks, Player 2: 3 disks, Total: 6 disks

            State 2
            --------
            --------
            ---0X---
            ---0X---
            ---0X---
            --------
            --------
            --------
            State 3, Player 1 moved, Action: put X on position (2, 2)
            --------
            --------
            --XXX---
            ---XX---
            ---0X---
            --------
            --------
            --------
            Result - Player 1: 6 disks, Player 2: 1 disks, Total: 7 disks

            State 3
            --------
            --------
            --XXX---
            ---XX---
            ---0X---
            --------
            --------
            --------
            State 4, Player 2 moved, Action: put 0 on position (1, 3)
            --------
            ---0----
            --X0X---
            ---0X---
            ---0X---
            --------
            --------
            --------
            Result - Player 1: 4 disks, Player 2: 4 disks, Total: 8 disks

            State 4
            --------
            ---0----
            --X0X---
            ---0X---
            ---0X---
            --------
            --------
            --------
            State 5, Player 1 moved, Action: put X on position (1, 2)
            --------
            --X0----
            --XXX---
            ---0X---
            ---0X---
            --------
            --------
            --------
            Result - Player 1: 6 disks, Player 2: 3 disks, Total: 9 disks

            Game ended
            XXXXXXX0
            XXXXXX00
            XXXXXX00
            X00X0X00
            X00X0X00
            X0X0X0X0
            XX0X0X00
            XXXXXXX0
            Black player won with 40 black disks to 24 white disk

    1.3:
        If we run the same command many time we will still get the same result because the players actions are the same
        for each run so the results have to be the same as well.

    1.C:
         run: Reversi.py -random 5
         first output:
            State 0
            --------
            --------
            --------
            ---X0---
            ---0X---
            --------
            --------
            --------
            State 1, Player 1 moved, Action: put X on position (3, 5)
            --------
            --------
            --------
            ---XXX--
            ---0X---
            --------
            --------
            --------
            Result - Player 1: 4 disks, Player 2: 1 disks, Total: 5 disks

            State 1
            --------
            --------
            --------
            ---XXX--
            ---0X---
            --------
            --------
            --------
            State 2, Player 2 moved, Action: put 0 on position (4, 5)
            --------
            --------
            --------
            ---XXX--
            ---000--
            --------
            --------
            --------
            Result - Player 1: 3 disks, Player 2: 3 disks, Total: 6 disks

            State 2
            --------
            --------
            --------
            ---XXX--
            ---000--
            --------
            --------
            --------
            State 3, Player 1 moved, Action: put X on position (5, 5)
            --------
            --------
            --------
            ---XXX--
            ---0XX--
            -----X--
            --------
            --------
            Result - Player 1: 6 disks, Player 2: 1 disks, Total: 7 disks

            State 3
            --------
            --------
            --------
            ---XXX--
            ---0XX--
            -----X--
            --------
            --------
            State 4, Player 2 moved, Action: put 0 on position (4, 6)
            --------
            --------
            --------
            ---XXX--
            ---0000-
            -----X--
            --------
            --------
            Result - Player 1: 4 disks, Player 2: 4 disks, Total: 8 disks

            State 4
            --------
            --------
            --------
            ---XXX--
            ---0000-
            -----X--
            --------
            --------
            State 5, Player 1 moved, Action: put X on position (5, 3)
            --------
            --------
            --------
            ---XXX--
            ---XX00-
            ---X-X--
            --------
            --------
            Result - Player 1: 7 disks, Player 2: 2 disks, Total: 9 disks

            Game ended
            XXXXXXXX
            XXXX00X0
            XXX00XX0
            X0X0XXX0
            X00X00X0
            X0X00000
            XXX00000
            00000000
            White player won with 33 white disks to 31 black disk

         second output:
            State 0
            --------
            --------
            --------
            ---X0---
            ---0X---
            --------
            --------
            --------
            State 1, Player 1 moved, Action: put X on position (4, 2)
            --------
            --------
            --------
            ---X0---
            --XXX---
            --------
            --------
            --------
            Result - Player 1: 4 disks, Player 2: 1 disks, Total: 5 disks

            State 1
            --------
            --------
            --------
            ---X0---
            --XXX---
            --------
            --------
            --------
            State 2, Player 2 moved, Action: put 0 on position (5, 2)
            --------
            --------
            --------
            ---X0---
            --X0X---
            --0-----
            --------
            --------
            Result - Player 1: 3 disks, Player 2: 3 disks, Total: 6 disks

            State 2
            --------
            --------
            --------
            ---X0---
            --X0X---
            --0-----
            --------
            --------
            State 3, Player 1 moved, Action: put X on position (5, 3)
            --------
            --------
            --------
            ---X0---
            --XXX---
            --0X----
            --------
            --------
            Result - Player 1: 5 disks, Player 2: 2 disks, Total: 7 disks

            State 3
            --------
            --------
            --------
            ---X0---
            --XXX---
            --0X----
            --------
            --------
            State 4, Player 2 moved, Action: put 0 on position (5, 4)
            --------
            --------
            --------
            ---X0---
            --XX0---
            --000---
            --------
            --------
            Result - Player 1: 3 disks, Player 2: 5 disks, Total: 8 disks

            State 4
            --------
            --------
            --------
            ---X0---
            --XX0---
            --000---
            --------
            --------
            State 5, Player 1 moved, Action: put X on position (5, 5)
            --------
            --------
            --------
            ---X0---
            --XXX---
            --000X--
            --------
            --------
            Result - Player 1: 5 disks, Player 2: 4 disks, Total: 9 disks

            Game ended
            XXXXXX0X
            XX0XX000
            00X00X00
            00XXX0XX
            00X0X0XX
            00000XXX
            00XXX0XX
            000XXXXX
            Black player won with 35 black disks to 29 white disk


Question 2:
    H1: We will use basic logic, the more black disks i have the better

    H2: We will use a strategy from Wikipedia.
        At the start of the game try to flip minimal amount of disks.
        (calculated by: 64 - (number of black disks minus the number of black disks in the previous state))
        We picked the first half as the start of the game.
        After the start of the game ended we will use the same tactic as H1.
        We will also check the corners, cause if you control them they cannot be flipped

    * we used the states from random run cause we need the prev state for H2
    example state 1:
            --------
            --------
            --------
            ---X0---
            --XXX---
            --000X--
            --------
            --------
        H1: 5 H2: 64 - (5-3) = 62

    example state 2:
            --------
            --------
            --------
            ---X0---
            --XX0---
            --000---
            --------
            --------
        H1: 3 H2: 64 - (3-5) = 66

    example state 3:
            --------
            --------
            --------
            ---X0---
            --XXX---
            --0X----
            --------
            --------
        H1: 5 H2: 64 - (5-3) = 62

    run: reversi.py H1
    output:
        Game ended
        XXXXX000
        XX0XX000
        XXXXXX00
        XXX00XX0
        XXX0XXX0
        XXXX0X00
        X00XXX00
        XXXXXX0-
        Black player won with 41 black disks to 22 white disk

    run: reversi.py H2
    output:
        Game ended
        XXXXXXXX
        -XXXXXXX
        00XXX0XX
        000X00XX
        00XXXXXX
        0X0X0XXX
        XXX000XX
        XXXX00--
        Black player won with 43 black disks to 18 white disk

    2.1:
        We will get the same result cause we always calculating the same next moves and picking the best one of them.

    2.2:
        Run both of H1 and H2, once player one will use H1 and player 2 H2, then replace them.
        The better evaluation functions will provide with bigger difference between black and white disks.


Question 3:
    3.1:
        run: reversi.py H1 H2 and reversi.py H2 H1

        H1:H1:  Black player won with 41 black disks to 22 white disk, difference 19 disks
        H2:H2:  Black player won with 43 black disks to 18 white disk, difference 25 disks
        H1:H2:  White player won with 50 white disks to 14 black disk, difference 36 disks
        H2:H1:  Black player won with 43 black disks to 18 white disk, difference 25 disks

        * H2:H2 and H2:H1: got the same result but the board looks different

    3.2:
        If we run in a different order H1 and H2 we get a different state tree and end game can look different.
        We see that it can even change the winner in the end.


Question 4:
    run: reversi.py H2 -ahead 2
    output:
        Game ended
        XXXXXXX0
        XX00XXX0
        XXX0XXX0
        XX0X0XX0
        XX0XXXX0
        XX0X0XX0
        XXXXXXX0
        0000000-
        Black player won with 41 black disks to 22 white disk

    4.1:
        We get the same result, the state tree always the same as well as our picks.

    4.2:
        the time complexity of a minimax tree is O(b**d), in our case b is 10 and d is 2
        so the time complexity will be O(10**2)

    4.3:
        the time complexity of a minimax tree is O(b**d), in our case b is 10 and d is 60 (first 4 disks already placed)
        so the time complexity will be O(10**60)

    4.4:
        We can use alfa-beta cutoff algorithm to remove not relevant subtrees

    4.5:
        To check who has the upper hand in game, the first player or the second,
        is the game really balanced.
        