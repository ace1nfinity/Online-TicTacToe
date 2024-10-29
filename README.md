# Online-TicTacToe
This is a simple online game implementing the rules of Tic Tac Toe.

**How to play:**
1. **Start the server:** Run the `server.py` script.
2. **Connect clients:** Run the `client.py` script on two different machines or terminals.
3. **Enter User-Name:** Enter a user-name to use in game.
4. **Play the game:** Players take turns one at a time playing their moves. The first player to get three in a row wins.

**Technologies used:**
* Python
* Sockets
* NamedTuples

**Message Protocol:** `Protocol` `Protocol Specific Data if needed`
* Client to Server:
* `Connect`
* `Name` `User given name`
* `Quit`
* `Spectate`
* `Move` `Where on board to play move`
* Server to Client:
* `Name` `Server Message`
* `Waiting` `Server Message`
* `Your_Turn` `Server Message`
* `End` `Server Message`

**Additional resources:**
* [Link to Python documentation]
* [Link to sockets tutorial]
