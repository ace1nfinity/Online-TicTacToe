# Online-TicTacToe
This is a simple online game implementing the rules of Tic Tac Toe.

**Files:**
* `server.py` Runs the front end of the server. Manages connections and game state
* `TTTserver.py` Back end of the Server. Manages processing of messages for both receiving and sending.
* `server_log.txt` Server logging from the last run of the game.
* `client.py` Runs the front end of the client, outputting the current game board and managing player input.
* `TTTclient.py` Back end of the client. Manages processing of messages for both receiving and sending.
* `GameManager.py` Script that managed the Tic-Tac-Toe game. Will communicate with server.py yo send updates information for the clients to render.
* `python.txt` Contains one-line which has the python version used to create this game.
* `requirements.txt` Contains a list of needed packages to run the game.
* `SOW.md` Statement of Work.
* `README.md` this file.

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

**Change Log:**
* October 4th: added first implementation of server and client
* October 9th: Updated server and made connections continuous
* October 15th: Switched to json for messaging format between server & clients
* October 20th: Implemented partial message protocol
* October 28th-29th: Created Sprint 3 branch. Implemented Game State and Synchronized it across clients. Also implemented user-name capabilities, allowing players to choose a user-name at the start of the game.

**Additional resources:**
* [Link to Python documentation]
* [Link to sockets tutorial]
