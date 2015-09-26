# HanoiTowers

This is a PoC I wrote about a year ago to play a little with A* algorithm. It attempts to solve the Hanoi Towers game.

## More Info

Implementation of A*:

F = G + H

Where G is the Cost function and H is the Heuristic.

I’ve defined the G() function in a way that only adds 1 to the current accumulated cost path: G = cost + 1

On the other hand, H() will decrement the total F() value by one for each ring placed in the position it should be for winning the game. For instance, if the current game is using 7 rings, and 5 of those 7 are correcly positioned in the target tower, then F will be decreased in 5.

This is really important because the next state to analyze is the one with the less F() value. The algorithm will continue searching for the solution by not moving the stack of 5 first. If this fails, then it will disarm the stack of five in order to generate new states that might lead to the solution.

Please note that you can transform this heuristic search in a breadth-first search by just using H = 0. In this case the algorithm would be managed only by G(), and given that this function always adds 1 to the current cost, the algorithm will look for each direct child of a State before going to the next depth level. It’s obvious that going that way will take longer though.

A good description of A* can be found [here](http://ee.usc.edu/~redekopp/cs102/L15_AStar.pdf)

## Author
* [Enrique Nissim](https://twitter.com/kiqueNissim)