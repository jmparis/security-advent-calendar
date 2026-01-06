For Christmas, Magnus received a strange electronic chessboard (probably corrupted by the Grinch's IA),
which seems to start directly on an incomplete game that he is unable to name.
Indeed, the missing move seems to be hidden in a binary file called ‘chess_game’,
which could be also very useful in finding the name of this famous game...

Your mission is to help Magnus recover the **missing move** and the **name of this game**.

By entering the **FEN code of the last position of the game** into the verifier available at the following address,
you'll be given the flag.

The format of the flag is **ADV{something}**.

PS: As this challenge has been simplified as much as possible for obvious reasons,
it does not require any execution of the executable file or any dynamic analysis.

https://advent.osecexperts.com/web/SmooEgr5oa2fcrtx4oCaAU3nxF3miP9k/

Hint 1:
When you want to reverse engineer an executable file (in our case, coded in "C" and compiled with "gcc"),
it is useful to look for tools such as a decompiler, which is very useful for recovering part of the original code.

Hint 2:
Using a online decompiler, we can statically analyse the executable and find interesting code,
particularly in the **.rodata**, .data and .text section.

Hint 3:
Two elements should catch your attention:

the variable declarations
two functions with explicit names
That's all you need to continue the challenge.

Hint 4:
Firstly, we can see that the famous chess move (originally encrypted) is decrypted with the use of a function via a XOR,
using a key indicated in plain text.

Hint 5:
Secondly, it would appear that the famous name of this game is deciphered using a logical operation,
which itself uses a certain ‘mystery_number’...

Hint 6:
You can reproduce the behaviour of this executable with a few lines of Python,
which will allow you to find the chess move, which in turn will allow you to find the name of the game.

Hint 7:
Congratulations on getting this far!

Now that you have the name of this chess game, you can easily find it on the Internet.

Reminder: the FEN format is required and must be entered on the website provided,
which will allow you to obtain the flag.
