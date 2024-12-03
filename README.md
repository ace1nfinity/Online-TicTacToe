# Online-TicTacToe
This is a simple online game implementing the rules of Tic Tac Toe.

**Files:**
* `server.py` Runs the front end of the server. Manages connections and game state
* `TTTserver.py` Back end of the Server. Manages processing of messages for both receiving and sending.
* `server_log.txt` Server logging from the last run of the game.
* `client.py` Runs the front end of the client, outputting the current game board and managing player input.
* `TTTclient.py` Back end of the client. Manages processing of messages for both receiving and sending.
* `GameManager.py` Script that managed the Tic-Tac-Toe game. Will communicate with server.py to send updated information for the clients to render.
* `python.txt` Contains one-line which has the python version used to create this game.
* `requirements.txt` Contains a list of needed packages to run the game.
* `SOW.md` Statement of Work.
* `README.md` this file.

**How to play:**
1. **Start the server:** Run the `server.py` script. It takes one argument: `Port`
2. **Connect clients:** Run the `client.py` script on two different machines or terminals. It takes two arguments: `IP Address` `Port`
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
* `Move` `Where on board to play move`
* Server to Client:
* `Name` `Server Message`
* `Waiting` `Server Message`
* `Your_Turn` `Server Message`
* `End` `Server Message`

**Change Log:**
* October 4th: added first implementation of server and client
* October 9th: Updated server and made connections continuous
* October 15th: Switched to json for messaging format between server & clients
* October 20th: Implemented partial message protocol
* October 28th-29th: Created Sprint 3 branch. Implemented Game State and Synchronized it across clients. Also implemented user-name capabilities, allowing players to choose a user-name at the start of the game.
* November 12th: Created Sprint 4 branch. Added actual Tic-Tac-Toe implementation. Players can now make actual moves and see those moves reflected on the game board. Added win conditions, so the game now properly ends when win condtion is met. Still need to add: letting players remake moves if they enter a bad move, print board after player makes their move. Not only show updated board when opponent make moves. Add spectator implementation. Add server console logging, not just .txt file logging.
* December 3rd: Made it so the game can have a draw ending. Made it so players can re-enter a move if they enter an invalid move option. Added server console logging. Scaled back the project just slightly by removing the spectate functionality from the project. Added error handling so that if a client disconnects, it cleanly ends the game. Made it so only two clients can connect to the server at a time, preventing more from connecting.

**Security Flaws:**
* There is no authentication required for this game, so it is possible that a third party could play moves for one of the players, making it unfair. A way to address this would be to add authentication and encryption, making it so no one outside the server and two clients could understand the current state of the game and whos turn it is. This would make it substantially harder for a third party to play moves in place of one of the other players.

**Additional resources:**
* [Link to Python documentation]
* [Link to sockets tutorial]
