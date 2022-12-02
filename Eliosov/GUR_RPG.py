from enum import Enum
import random


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class FirstScene(Enum):
    entered = 0
    sewer = 1
    wall = 2
    gate = 3


class SecondSceneSewer(Enum):
    entered = 0
    exited = 1


class SecondSceneCourtyard(Enum):
    entered = 0
    tower = 1
    hall = 2


class ThirdSceneFromCourtyard(Enum):
    entered = 0
    exited = 1


class ThirdSceneFromSewer(Enum):
    entered = 0
    exited = 1


class FourthScene(Enum):
    entered = 0
    exited = 1


class FifthScene(Enum):
    entered = 0
    won = 1


class Decision(Enum):
    think = 0
    attack = 1
    defend = 2
    heal = 3


class Player(object):
    def __init__(self):
        self.health_points = 5
        self.turns = 0
        self.current_location = [5, 1]
        self.first_scene = FirstScene.entered
        self.second_scene_courtyard = SecondSceneCourtyard.entered
        self.second_scene_sewer = SecondSceneSewer.entered
        self.third_scene_from_courtyard = ThirdSceneFromCourtyard.entered
        self.third_scene_from_sewer = ThirdSceneFromSewer.entered
        self.fourth_scene = FourthScene.entered
        self.fifth_scene = FifthScene.entered
        self.boss_fight_initiated = False
        self.defence_stance = False
        self.analysis_done = False

    def health_handler(self, delta):
        if delta > 0:
            delta = min(5-self.health_points, delta)
        if not self.defence_stance:
            self.health_points += delta
        if self.health_points <= 0:
            print("\nYou feel your body fail as your consciousness fades. The last chance to save the world is gone\n(This is one of the bad endings. There are other paths)")
            exit()
        elif (delta > 0):
            print(f'\nYou heal {delta} health points')
        elif self.boss_fight_initiated:
            if self.defence_stance:
                self.defence_stance = False
                print("You dodge the shots, but lose coordination")
            else:
                print(
                    f'One of the shots hits you. You lose {abs(delta)} health points')
        else:
            print(f'\nYou lose {abs(delta)} health points')

    def turn_handler(self, delta=1):
        self.turns += delta
        if (self.turns-delta < 10 and self.turns >= 10):
            print("\nThe radio buzzes with new information. The missile silos are being prepared for launch.\nThere is not much time")
        elif (self.turns >= 25):
            print("\nYou feel the earth shaking as distant silos release their payload. There's nothing anyone can do now\n(This is one of the bad endings. There are other paths)")
            exit()

    def maze_handler(self, maze, command):
        x = self.current_location[0]
        y = self.current_location[1]
        if "left" in command:
            if y == 0 or maze[x][y-1] == 0:
                print("You hit a wall")
            elif maze[x][y-1] == "O":
                print("You exit the sewers")
                self.turn_handler()
                self.second_scene_sewer = SecondSceneSewer.exited
            else:
                print("You move left")
                self.turn_handler()
                self.current_location = [x, y-1]
        elif "up" in command:
            if x == 0 or maze[x-1][y] == 0:
                print("You hit a wall")
            elif maze[x-1][y] == "O":
                print("You exit the sewers")
                self.turn_handler()
                self.second_scene_sewer = SecondSceneSewer.exited
            else:
                print("You move up")
                self.turn_handler()
                self.current_location = [x-1, y]
        elif "right" in command:
            if self.turns >= 20 and y == 0 and x+1 == 1:
                print("\nThe world shatters before your eyes. You are blinded by the light\nYou hear an annoyed voice you recognize as your commander's\n'This simulator cost us a billion and you broke it on the first try'\n(This is the secret ending. You have wrestled the game to its knees. There are other paths)")
                exit()
            elif y == 4 or maze[x][y+1] == 0:
                print("You hit a wall")
            elif maze[x][y+1] == "O":
                print("You exit the sewers")
                self.turn_handler()
                self.second_scene_sewer = SecondSceneSewer.exited
            else:
                print("You move right")
                self.turn_handler()
                self.current_location = [x, y+1]
        elif "down" in command:
            if x == 5 or maze[x+1][y] == 0:
                print("You hit a wall")
            elif maze[x+1][y] == "O":
                print("You exit the sewers")
                self.turn_handler()
                self.second_scene_sewer = SecondSceneSewer.exited
            else:
                print("You move down")
                self.turn_handler()
                self.current_location = [x+1, y]

    def elevator_code_guessing(self):
        while self.third_scene_from_courtyard == ThirdSceneFromCourtyard.entered:
            command = input(">>> ")
            if "stop" in command:
                print("You go back to the lobby")
                break
            elif command == "1991":
                print("The elevator carries you swiftly to the final floor")
                self.turn_handler()
                self.third_scene_from_courtyard = ThirdSceneFromCourtyard.exited
            elif command == "1917":
                print("Good guess, but no")
            elif command == "2022" or command == "2023":
                print("Wrong century")
            elif len(command) != 4 or not command.isdigit():
                print("That's not a valid code")
            else:
                print(
                    f"Wrong code. Try another or input {Color.RED}stop{Color.END} to stop trying")


class Dictator(object):
    def __init__(self):
        self.health_points = 5
        self.next_decision = Decision.think
        self.defence_stance = True

    def health_handler(self, delta, player):
        if delta > 0:
            delta = min(5-self.health_points, delta)
        self.health_points += delta
        if self.health_points <= 0:
            print("putin's corpse lies among the broken turrets. You notice a passage behind his desk and rush through it")
            player.fourth_scene = FourthScene.exited
        elif (delta > 0):
            print(f'putin heals {delta} health points')
        elif (delta < 0) and not self.defence_stance:
            print(f'putin loses {abs(delta)} health points')
        else:
            self.defence_stance = False
            print("putin defends the attack, but his shield is broken")

    def decision_makes(self):
        roll = random.random()
        if roll <= 0.5:
            self.next_decision = Decision.attack
        else:
            if self.health_points < 5:
                self.next_decision = Decision.heal
            else:
                if not self.defence_stance:
                    self.next_decision = Decision.defend
                else:
                    self.next_decision = Decision.attack

    def act(self, player):
        if self.next_decision == Decision.defend:
            self.defence_stance = True
            print("putin has restored his shield")
        elif self.next_decision == Decision.attack:
            print("The turrets open fire")
            player.health_handler(-1)
        elif self.next_decision == Decision.heal:
            self.health_handler(1, player)
        else:
            print("putin seems to be pondering his next move")

    def decision_string(self):
        if self.next_decision == Decision.defend:
            return "defend"
        elif self.next_decision == Decision.attack:
            return "attack"
        elif self.next_decision == Decision.heal:
            return "heal"
        else:
            return "think"


def main():
    maze = ([1, 1, 0, "O", 0], [1, 0, 0, 1, 1], [1, 1, 0, 0, 1],
            [1, 0, 0, 1, 1], [1, 1, 1, 1, 0], [1, 1, 1, 1, 0])
    player = Player()
    putin = Dictator()
    print("You are a top secret agent of GUR. Intelligence reports that the Russians are preparing a nuclear launch.\nYour task is to infltrate the Kremlin and take control of the control room\n")
    print("You must decide how to approach. You have a radio, a Fort-17 pistol and a grappling hook")
    while player.first_scene == FirstScene.entered:
        command = input(">>> ")
        if "options" in command:
            print("sewer", "main gate", "wall", "look around", sep=", ")
        elif "sewer" in command:
            print(
                "You enter the sewers through a nearby grate. The stench is overwhelming and you throw up")
            player.health_handler(-1)
            player.turn_handler()
            player.first_scene = FirstScene.sewer
        elif "wall" in command:
            print(
                "You scale the wall using your grappling hook. It breaks, but you are now standing in the courtyard")
            player.turn_handler()
            player.first_scene = FirstScene.wall
        elif "main gate" in command:
            print("You try a direct approach and rush the gate. After the machinegun fire ceases, your body is unrecognisable.\nWhat did you think would happen?")
            player.health_handler(-5)
            player.first_scene = FirstScene.gate
        elif "look around" in command:
            print("The Kremlin towers above you. The walls are well-built, but largerly deserted.\nThe main gate is still well manned despite the clear manpower issues. You can see a sewer grate besides you")
        else:
            print(
                f"Unknown command. Input {Color.RED}options{Color.END} for help")
    while player.first_scene == FirstScene.sewer and player.second_scene_sewer == SecondSceneSewer.entered:
        command = input(">>> ")
        if "options" in command:
            print("left", "up", "right", "down", "look around", sep=", ")
        elif "left" in command or "up" in command or "right" in command or "down" in command:
            player.maze_handler(maze, command)
        elif "look around" in command:
            print("The sewers are a maze")
        else:
            print(
                f"Unknown command. Input {Color.RED}options{Color.END} for help")
    while player.first_scene == FirstScene.wall and player.second_scene_courtyard == SecondSceneCourtyard.entered:
        command = input(">>> ")
        if "options" in command:
            print("tower", "hall", "look around", sep=", ")
        elif "tower" in command:
            print("Climbing the tower will take some time. Are you sure (Y/N)?")
            command = input(">>> ")
            if command == "Y":
                print(
                    "You climb the tower. The staircase is long and winding")
                player.turn_handler(10)
                player.second_scene_courtyard = SecondSceneCourtyard.tower
            else:
                print("You decide against it")
        elif "hall" in command:
            print(
                "You run to the hall. The snipers notice you and dutifully open fire. A few shots connect before you breach the door")
            player.health_handler(-2)
            player.turn_handler()
            player.second_scene_courtyard = SecondSceneCourtyard.hall
        elif "look around" in command:
            print(
                "A large hall is to your right. A nearby sniper tower covers the approach")
        else:
            print(
                f"Unknown command. Input {Color.RED}options{Color.END} for help")
    while player.first_scene == FirstScene.wall and player.second_scene_courtyard == SecondSceneCourtyard.tower:
        command = input(">>> ")
        if "options" in command:
            print("choke", "shoot", "look around", sep=", ")
        elif "choke" in command:
            print(
                "You quietly choke the guards one after another. The way is now open and you rush to the hall")
            player.turn_handler()
            player.second_scene_courtyard = SecondSceneCourtyard.hall
        elif "shoot" in command:
            print(
                "You shoot one of the guards. The other manages to a shot off before you take him out\nThe way is now open and you rush to the hall")
            player.health_handler(-1)
            player.turn_handler()
            player.second_scene_courtyard = SecondSceneCourtyard.hall
        elif "look around" in command:
            print(
                "You have reached the top of the tower. There are two snipers looking outside. Their backs are turned")
        else:
            print(
                f"Unknown command. Input {Color.RED}options{Color.END} for help")
    while player.second_scene_sewer == SecondSceneSewer.exited and player.third_scene_from_sewer == ThirdSceneFromSewer.entered:
        command = input(">>> ")
        if "options" in command:
            print("vent", "door", "look around", sep=", ")
        elif "door" in command:
            print("The door looks flimsy. You could break it, but it will hurt (Y/N)")
            command = input(">>> ")
            if command == "Y":
                print(
                    "You rush at the door. It swings open, but your entire body is sore")
                player.turn_handler()
                player.health_handler(-1)
                player.second_scene_courtyard = SecondSceneCourtyard.hall  # Awkward transition
                break
            else:
                print("You decide against it")
        elif "vent" in command:
            print(
                "Climbing through the vents will take some time. Do you persist regardless? (Y/N)")
            command = input(">>> ")
            if command == "Y":
                print(
                    "The vents are clean and safe. You are bored rather than tired when you emerge")
                player.turn_handler(5)
                player.third_scene_from_sewer = ThirdSceneFromSewer.exited
            else:
                print("You decide against it")
        elif "look around" in command:
            print(
                "You are in a utility room. There are many machine you do not recognize, but you notice the vent openings")
        else:
            print(
                f"Unknown command. Input {Color.RED}options{Color.END} for help")
    while player.second_scene_courtyard == SecondSceneCourtyard.hall and player.third_scene_from_courtyard == ThirdSceneFromCourtyard.entered:
        command = input(">>> ")
        if "options" in command:
            print("elevator", "stairs", "look around", sep=", ")
        elif "elevator" in command:
            print("The elevator requires a four digit code. A note is pinned to the keypad:\n'The greatest geopolitical catastrophe of the 20th century'")
            player.elevator_code_guessing()
        elif "stairs" in command:
            print(
                "There are many floors to climb. Are you sure you have the time?(Y/N)")
            command = input(">>> ")
            if command == "Y":
                print(
                    "You cannot feel your legs by the time you reach the fifteenth floor. Do you take some time to rest?(Y/N)")
                command = input(">>> ")
                if command == "Y":
                    print(
                        "The warm carpet feels so nice. You feel refreshed and ready to take on anything")
                    player.turn_handler(10)
                    player.health_handler(1)
                    player.third_scene_from_courtyard = ThirdSceneFromCourtyard.exited
                else:
                    print("You decide against it. Your body does not appreciate it")
                    player.turn_handler(5)
                    player.health_handler(-1)
                    player.third_scene_from_courtyard = ThirdSceneFromCourtyard.exited
            else:
                print("You decide against it")
        elif "look around" in command:
            print(
                "You are standing in a luxurious lobby. This must be the main building\nYou can see an elevator and a set of stairs")
        else:
            print(
                f"Unknown command. Input {Color.RED}options{Color.END} for help")
    while (player.third_scene_from_sewer == ThirdSceneFromSewer.exited or player.third_scene_from_courtyard == ThirdSceneFromCourtyard.exited) and player.fourth_scene == FourthScene.entered:
        if not player.boss_fight_initiated:
            print("\n\nYou have entered putin's lair. Noticing you, he looks up from his desk.\nTwin turrets drop from the ceiling and a shield rises up before the dictator\nThis is what you've trained for!")
            player.boss_fight_initiated = True
        print(
            f'\nYou have {player.health_points} health points. Putin has {putin.health_points} health points')
        if player.analysis_done:
            print(f"putin is intending to {putin.decision_string()}")
        command = input(">>> ")
        if "options" in command:
            print("attack", "defend", "analyze", "look around", sep=", ")
        elif "attack" in command:
            print("You open fire")
            putin.health_handler(-1, player)
        elif "defend" in command:
            print("You take cover")
            player.defence_stance = True
        elif "analyze" in command:
            print("You try to figure out what putin is planning")
            if random.random() >= 0.5:
                print("His next moves are clear as the morning air to you")
                player.analysis_done = True
            else:
                print("putin's strategy is either inscrutable or absent")
        elif "look around" in command:
            print(
                "There's no time to waste by looking around!")
        else:
            print(
                f"Unknown command. Input {Color.RED}options{Color.END} for help")
        if putin.health_points > 0:
            putin.act(player)
            putin.decision_makes()
    while player.fourth_scene == FourthScene.exited:
        command = input(">>> ")
        if "options" in command:
            print("console", "look around", sep=", ")
        elif "console" in command:
            print("The terminal is unlocked. putin was clearly confident this room would never be breached.\nThe abort button is unmistakable. Do you press it (Y/N)?")
            command = input(">>> ")
            while command:
                if command == "Y":
                    print("\nYou can see the missiles self-destruct one by one. The world is safe, thanks to your actions today\n(This is the good ending. There are other paths)")
                    exit()
                elif command == "N":
                    print(
                        "\n...Why?\n(This is the evil ending. There are other paths)")
                    exit()
                else:
                    print("Stop fooling around. There's not a moment to waste")
                    command = input(">>> ")
        elif "look around" in command:
            print(
                "A massive supercomputer the size of a room is before you\nA thousand screens are showing trajectories, impact projections and casualty estimates\n\nYou have reached your goal at last")
        else:
            print(
                f"Unknown command. Input {Color.RED}options{Color.END} for help")


if __name__ == "__main__":
    main()
