Pentago
Min-Max adversarial AI for Pentago game
Video on how to play pentago: https://www.youtube.com/watch?v=4kipCMwmUso

****************************************************
Pentago.py is the main execution file
****************************************************

The player is randomly chosen to go first or second against the AI.

During each move, the player must input their actions in the format of "b/p bd" (no quotations).
"b/p" chooses the block and location in said block, "bd" chooses a block and which direction to rotate it in.

  b: the chosen block, 1 - 4. The two b's in the format can be different numbers. (Blocks numbered below)
      +-------+-------+
      |       |       |
      |   1   |   2   |
      |       |       |
      +-------+-------+
      |       |       |
      |   3   |   4   |
      |       |       |
      +-------+-------+
      
  p: the chosen location in the block, 1-9. (Numbered below)
      +-------+-------+
      | 1 2 3 | 1 2 3 |
      | 4 5 6 | 4 5 6 |
      | 7 8 9 | 7 8 9 |
      +-------+-------+
      | 1 2 3 | 1 2 3 |
      | 4 5 6 | 4 5 6 |
      | 7 8 9 | 7 8 9 |
      +-------+-------+
      
  d: the direction to rotate block b (CASE SENSITIVE).
     
     R: clockwise 90 degrees
     L: counter-clockwise 90 degrees
     
  Example inputs:
      1/5 1L
      4/9 3R
      2/2 2L
       
An output.txt is generated detailing the entire game at the end.
