Bad Minesweeper
===============

An interview guide recommended that to prepare for that specific interview I write a text based minesweeper. So I did.

Features
--------
 - Around about 200 lines
 - Runs using just the standard library
 - Clutters up your terminal with many print statements
 - Probably full of bugs and holes in my reasoning
 - Could do with a restructure

How to play
-----------

Run `python3 main.py` and it will present you with text like the below:

```
  0 1 2 3 4 5 6 7 8 9
0 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
1 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
2 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
3 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
4 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
5 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
6 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
7 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
8 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
9 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
Flags Remaining: 20
> 
```

You can use any of the following commands, where `[y]` stands for the y co-ordinate (along the left) and `[x]` for the x co-ordinate (along the top).

```
end
clear [y] [x]
flag [y] [x]
```

`clear` - Marks a square as free of mines. Be careful, if it does have a mine in then you lose. The first time you type `clear` you are guaranteed to not hit a mine.

`flag` - Marks a square as containing a mine. This prevents you from accidentally typing `clear` with this square's co-ordinates in future.
