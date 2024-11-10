import time
import json
import os
import socket
import threading
import struct

SAVE_FILE = "python_tycoon_save.json"
LISTEN_PORT = 5050  # Port to listen on for incoming money transfers

class Business:
    def __init__(self, name, base_income, income_interval, level=1, last_collected=None):
        self.name = name
        self.base_income = base_income
        self.income_interval = income_interval
        self.level = level
        self.last_collected = last_collected or time.time()

    def collect_income(self):
        current_time = time.time()
        if current_time - self.last_collected >= self.income_interval:
            self.last_collected = current_time
            return self.base_income * self.level
        return 0

    def upgrade(self):
        self.level += 1
        self.income_interval *= 0.9
        self.base_income *= 1.2
        print(f"Upgraded {self.name} to level {self.level}!")

    def info(self):
        return {
            "name": self.name,
            "level": self.level,
            "base_income": self.base_income,
            "income_interval": self.income_interval,
        }

    def to_dict(self):
        return {
            "name": self.name,
            "base_income": self.base_income,
            "income_interval": self.income_interval,
            "level": self.level,
            "last_collected": self.last_collected,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            base_income=data["base_income"],
            income_interval=data["income_interval"],
            level=data["level"],
            last_collected=data.get("last_collected", time.time())
        )


class PythonTycoon:
    def __init__(self):
        self.username = ""
        self.businesses = []
        self.balance = 100
        self.running = True
        self.load_game()
        # Start a thread to listen for incoming P2P connections
        self.listener_thread = threading.Thread(target=self.listen_for_transfers)
        self.listener_thread.daemon = True
        self.listener_thread.start()

    def save_game(self):
        save_data = {
            "username": self.username,
            "balance": self.balance,
            "businesses": [biz.to_dict() for biz in self.businesses]
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(save_data, f)
        print("Game progress saved.")

    def load_game(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                save_data = json.load(f)
                self.username = save_data["username"]
                self.balance = save_data["balance"]
                self.businesses = [Business.from_dict(biz_data) for biz_data in save_data["businesses"]]
            print(f"Loaded saved game progress for player '{self.username}'.")
        else:
            self.username = input("Enter a username to start a new game: ").strip()
            self.businesses = [
                Business("Lemonade Stand", base_income=10, income_interval=5),
                Business("Newspaper Delivery", base_income=50, income_interval=10),
                Business("Car Wash", base_income=200, income_interval=20),
            ]
            print(f"Welcome, {self.username}! Starting a new game.")

    def show_status(self):
        print(f"\n=== {self.username}'s Business Status ===")
        for biz in self.businesses:
            info = biz.info()
            print(f"{info['name']} - Level: {info['level']}, Income: ${info['base_income']:.2f} per {info['income_interval']:.2f} sec")
        print(f"\nBalance: ${self.balance:.2f}\n")

    def collect_all_income(self):
        print("\nCollecting income from all businesses...")
        total_income = 0
        for biz in self.businesses:
            income = biz.collect_income()
            total_income += income
            if income > 0:
                print(f"Collected ${income:.2f} from {biz.name}.")
        self.balance += total_income
        print(f"Total income collected: ${total_income:.2f}")

    def upgrade_business(self, business_index):
        if 0 <= business_index < len(self.businesses):
            biz = self.businesses[business_index]
            upgrade_cost = biz.level * 50
            if self.balance >= upgrade_cost:
                self.balance -= upgrade_cost
                biz.upgrade()
                print(f"Upgraded {biz.name} for ${upgrade_cost:.2f}. Remaining balance: ${self.balance:.2f}")
            else:
                print(f"Not enough balance to upgrade {biz.name}. Upgrade cost: ${upgrade_cost:.2f}")
        else:
            print("Invalid business choice.")

    def peer_send_money(self, recipient_ip, amount):
        """Send money to another player directly via their IP address."""
        if amount > self.balance:
            print("Insufficient balance to send that amount.")
            return

        try:
            with socket.create_connection((recipient_ip, LISTEN_PORT)) as s:
                # Prepare message: username and amount in bytes
                message = f"{self.username}:{amount}".encode()
                s.sendall(message)
            self.balance -= amount
            print(f"Successfully sent ${amount} to {recipient_ip}. Remaining balance: ${self.balance:.2f}")
        except socket.error as e:
            print("Failed to send money due to network error:", e)

    def listen_for_transfers(self):
        """Listen for incoming connections from other players sending money."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", LISTEN_PORT))
            s.listen()
            print(f"Listening for incoming transfers on port {LISTEN_PORT}...")

            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    if data:
                        sender, amount = data.decode().split(":")
                        amount = float(amount)
                        self.balance += amount
                        print(f"\nReceived ${amount:.2f} from {sender}. New balance: ${self.balance:.2f}")

    def main_loop(self):
        print(f"Welcome to Python Tycoon, {self.username}!")
        print("Commands: status, collect, upgrade [number], wait, save, send [recipient_ip] [amount], exit")
        
        while self.running:
            command = input("\nEnter command: ").strip().lower()
            
            if command == "status":
                self.show_status()
            elif command == "collect":
                self.collect_all_income()
            elif command.startswith("upgrade"):
                try:
                    _, index = command.split()
                    self.upgrade_business(int(index) - 1)
                except (ValueError, IndexError):
                    print("Invalid upgrade command. Use 'upgrade [number]'.")
            elif command == "wait":
                print("Waiting... (5 seconds)")
                time.sleep(5)
                self.collect_all_income()
            elif command == "save":
                self.save_game()
            elif command.startswith("send"):
                try:
                    _, recipient_ip, amount = command.split()
                    self.peer_send_money(recipient_ip, float(amount))
                except (ValueError, IndexError):
                    print("Invalid send command. Use 'send [recipient_ip] [amount]'.")
            elif command == "exit":
                save_prompt = input("Do you want to save before exiting? (yes/no): ").strip().lower()
                if save_prompt == "yes":
                    self.save_game()
                print("Exiting Python Tycoon. Thanks for playing!")
                self.running = False
            else:
                print("Unknown command. Available commands: status, collect, upgrade [number], wait, save, send [recipient_ip] [amount], exit")

# Run the game
if __name__ == "__main__":
    game = PythonTycoon()
    game.main_loop()

