# Python Tycoon

### Python Tycoon: A Peer-to-Peer Incremental Business Simulator in Python

**Python Tycoon** is a text-based, incremental business simulation game written in Python. Designed for the command line, this game lets players build and upgrade virtual businesses, earn revenue over time, and even transfer in-game money directly to other players via peer-to-peer networking. Here’s an overview of how it works and what features it offers.

---

#### 1. Starting the Game and Choosing a Username

When players first launch Python Tycoon, they are prompted to enter a username, which will identify them within the game and, optionally, to other players. This username is saved and loaded each time they play, personalizing the experience and allowing players to build their in-game reputation.

If a save file is detected, the game loads the player’s progress, including their username, balance, and the status of each business they own. Otherwise, a new save is created, starting the player with default businesses and a starting balance.

---

#### 2. Building and Upgrading Businesses

The core gameplay of Python Tycoon revolves around starting and growing virtual businesses. Players can view the status of their businesses with the `status` command, which displays details such as the business name, level, income, and income interval (the time required to generate each payout).

Each business in the game generates passive income based on its level and base income. As time passes, this income accumulates automatically, simulating the "idle" aspect of incremental games. Players can actively collect their revenue with the `collect` command, adding earnings to their balance. 

To increase revenue, players can **upgrade** their businesses. Each upgrade:
- Increases the business level, boosting its income.
- Decreases the time interval between income payouts, meaning the business generates money faster.

Upgrades cost money, which encourages players to reinvest their earnings strategically to maximize their long-term growth.

---

#### 3. Saving Progress

The game saves the player’s progress to a JSON file with the `save` command, recording their username, balance, and each business’s properties (level, income, and last collection time). This allows players to resume from where they left off whenever they reopen the game.

On exiting the game, players are prompted to save their progress one final time, ensuring no accidental loss of data.

---

#### 4. Peer-to-Peer Money Transfers

One of the unique features of Python Tycoon is the **peer-to-peer (P2P) money transfer system**. This feature allows players to send in-game currency directly to other players, without relying on a central server. Here’s how it works:

1. **Listening for Incoming Transfers**: When the game starts, it opens a network socket on a specific port, listening for incoming money transfers. This makes each player’s game instance act as a lightweight server that other players can connect to.

2. **Sending Money**: To send money to another player, users simply need the recipient's IP address. Using the `send [recipient_ip] [amount]` command, players can connect directly to another player's instance and transfer funds. The game sends a small message containing the sender’s username and the transfer amount, which the recipient’s game processes to update their balance.

3. **Receiving Money**: When a player receives a transfer, they are notified of the sender’s username and the amount received. The funds are automatically added to their balance.

This P2P feature opens the door for collaborative gameplay, where players can assist each other by sharing resources. However, it’s important to note that this P2P setup does not include encryption or player verification, which would be necessary for a secure production environment. As a result, this is more like a novelty, fun feature. However, given that this is Python  code, this can be modified.

---

#### 5. Core Commands

Here are some of the essential commands in Python Tycoon:

- **status**: Displays the player’s businesses, including each business’s income and level.
- **collect**: Collects all accumulated income from the player’s businesses, adding it to the player’s balance.
- **upgrade [number]**: Upgrades the specified business, increasing its income potential and reducing the interval between payouts.
- **wait**: Simulates a 5-second wait to generate passive income, which can then be collected.
- **save**: Saves the player’s progress, including their businesses and balance, to a local file.
- **send [recipient_ip] [amount]**: Sends a specified amount of money to another player, using their IP address for direct connection.
- **exit**: Exits the game, with a prompt to save progress.

---

#### Conclusion

Python Tycoon is a fun and engaging command-line game that introduces players to the world of incremental games while adding a peer-to-peer networking twist. By integrating basic networking with incremental gameplay mechanics, Python Tycoon demonstrates how command-line applications can incorporate multiplayer elements. Although it currently uses simple P2P connections, the game could be expanded with additional features like secure player verification, business variety, and more sophisticated mechanics, making it an excellent foundation for both learning and expansion.
