import copy
import re
import sys


# Please implement this function according to Section "Read Configuration File"
def load_config_file(filepath):
    # It should return width, height, waters, woods, foods, golds based on the file
    # Complete the test driver of this function in file_loading_test.py
    width, height = 0, 0
    waters, woods, foods, golds = [], [], [], []  # list of position tuples
    resources_list = []  # list of all resources position tuples
    desert_area = []  # positions which should not be occupied with resources or water
    try:
        with open(filepath, "r") as f:
            config = f.read()
    except FileNotFoundError:
        raise FileNotFoundError
    # Use regular expressions to determine the structure
    if not re.match(r"^Frame: .*\nWater: .*\nWood: .*\nFood: .*\nGold: .*", config):
        raise SyntaxError("Invalid Configuration File: format error!")

    config = config.split("\n")
    # Verification format
    if not re.match(r"^Frame: \d+x\d+$", config[0]):
        raise SyntaxError("Invalid Configuration File: frame should be in format widthxheight!")

    width, height = re.findall(r"\d+", config[0])
    width, height = int(width), int(height)

    if width not in range(5, 8) or height not in range(5, 8):
        raise ArithmeticError("Invalid Configuration File: width and height should range from 5 to 7!")

    for content in config[1:]:
        content = content.split(" ")
        line_name = content[0][:-1]
        num_list = content[1:]

        if len(num_list) != 1 or num_list[0] != "":  # Prevent the situation of ['']
            for i in num_list:  # Check character format
                if not i.isdigit():
                    raise ValueError(f"Invalid Configuration File: {line_name} contains non integer characters!")

            if len(num_list) % 2 != 0:  # Check the character length
                raise SyntaxError(f"Invalid Configuration File: {line_name} has an odd number of elements!")

            for i in range(0, len(num_list), 2):
                position_x, position_y = int(num_list[i]), int(num_list[i + 1])
                if position_x >= width or position_y >= height:  # Check if it is out of bounds
                    raise ArithmeticError(
                        f"Invalid Configuration File: {line_name} contains a position that is out of map.")
                if line_name == "Water":
                    waters.append((position_x, position_y))
                elif line_name == "Wood":
                    woods.append((position_x, position_y))
                elif line_name == "Food":
                    foods.append((position_x, position_y))
                elif line_name == "Gold":
                    golds.append((position_x, position_y))
                # Add the location to the total resource list every time
                # Facilitate repeated inspections in the next step
                resources_list.append((position_x, position_y))

    desert_area = [(1, 1), (width - 2, height - 2), (0, 1),
                   (1, 0), (2, 1), (1, 2), (width - 3, height - 2),
                   (width - 2, height - 3), (width - 1, height - 2),
                   (width - 2, height - 1)
                   ]  # positions which should not be occupied with resources or water

    check_list = []  # Create a checklist, record the data that has occurred
    for res in resources_list:
        if res not in desert_area:
            if res not in check_list:
                check_list.append(res)
            else:  # Appears stating that the position is duplicated
                x, y = res
                raise SyntaxError(f"Invalid Configuration File: Duplicate position ({x}, {y})!")
        else:  # The location can no longer be in and around the base
            raise ValueError(
                "Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")

    print(f"Configuration file {filepath} was loaded.")
    return width, height, waters, woods, foods, golds


# ============================================================================================#

def create_init_database(map_width, map_height, map_waters, map_woods, map_foods, map_golds, player_1_pos,
                         player_2_pos):
    """
    The function used to create the initial map, use the height and width to create a two-dimensional list
    equal to the size of the map, and pass in the basic resources.
    Call it only once
    :param map_width: (int) Incoming map width
    :param map_height: (int) Incoming map height
    :param map_waters: (List) Contains a list of waters coordinates
    :param map_woods: (List) Contains a list of woods coordinates
    :param map_foods: (List) Contains a list of foods coordinates
    :param map_golds: (List) Contains a list of golds coordinates
    :param player_1_pos: (Player) Player one's object
    :param player_2_pos: (Player) Player two's object
    :return: None
    """
    map_data = [["" for _ in range(map_width)] for _ in range(map_height)]
    # print(map_data)
    # Because a vertical list structure reads the vertical lines first and then the horizontal lines
    # The human reading order is x, y = 4, 2, but the list operation is 2, 4,
    # and the x and y axes need to be exchanged to read the data
    # [[0,0,0, 0],
    #  [0,0,0,hi],
    #  [0,0,0, 0]]
    # Generate the corresponding object according to the coordinates
    for x, y in map_waters:
        map_data[y][x] = Water(x, y)
    for x, y in map_woods:
        map_data[y][x] = Wood(x, y)
    for x, y in map_foods:
        map_data[y][x] = Food(x, y)
    for x, y in map_golds:
        map_data[y][x] = Gold(x, y)
    map_data[player_1_pos.position_y][player_1_pos.position_x] = player_1_pos  # Put the player object in the list
    map_data[player_2_pos.position_y][player_2_pos.position_x] = player_2_pos
    return map_data


def show_game_map(data_list):
    """
    Generate a map based on the database list
    :param data_list: (List) The list which saves the data of the field
    :return: None
    """
    print("Please check the battlefield, commander.")
    map_height, map_width = len(data_list), len(data_list[1])
    print(f"  X{' '.join(str(i).zfill(2) for i in range(0, map_width))}X")
    print(f" Y+{'-'.join('--' for _ in range(0, map_width))}+")
    for i in range(map_height):
        print(f"{str(i).zfill(2)}|{'|'.join(value.name if value else '  ' for value in data_list[i])}|")
    print(f" Y+{'-'.join('--' for _ in range(0, map_width))}+")
    return


def recruit_price():
    """
    Printing cost
    :return: None
    """
    print('''Recruit Prices:
  Spearman (S) - 1W, 1F
  Archer (A) - 1W, 1G
  Knight (K) - 1F, 1G
  Scout (T) - 1W, 1F, 1G''')


YEAR = 617  # Initial time, Global variable


def main():
    """
    The main game program, which controls the sequence of players and the round mechanism of the game.
    :return: None
    """
    print("Game Started: Little Battle! (enter QUIT to quit the game)\n")
    show_game_map(data)
    print("(enter DIS to display the map)\n")
    recruit_price()
    print("(enter PRIS to display the price list)\n")
    global YEAR
    while True:
        print(f"-Year {YEAR}-\n")
        print("+++Player 1's Stage: Recruit Armies+++\n")
        player_1.recruit_armies(data)
        print("\n===Player 1's Stage: Move Armies===")
        move_stage(player_1, data)
        print(f"-Year {YEAR}-\n")
        print("+++Player 2's Stage: Recruit Armies+++\n")
        player_2.recruit_armies(data)
        print("\n===Player 2's Stage: Move Armies===")
        move_stage(player_2, data)
        YEAR += 1


def generating_conditions(player, map_data) -> bool:
    """
    Used to verify whether the amount of resources consumed by the army generated by the player is sufficient
    and to verify whether there is an open space around the player's base
    :param player: (Player) Player object
    :param map_data: (List) Database of maps
    :return: bool
    """
    if (player.resources["W"] - 1 >= 0 and player.resources["F"] - 1 >= 0) or \
            (player.resources["W"] - 1 >= 0 and player.resources["G"] - 1 >= 0) or \
            (player.resources["F"] - 1 >= 0 and player.resources["G"] - 1 >= 0):
        if map_data[player.position_y - 1][player.position_x] == "" or \
                map_data[player.position_y + 1][player.position_x] == "" or \
                map_data[player.position_y][player.position_x + 1] == "" or \
                map_data[player.position_y][player.position_x - 1] == "":
            return True

        else:
            print("No place to recruit new armies.")
            return False

    else:
        print("No resources to recruit any armies.")
        return False


WIN = False  # When it becomes True, means victory


def move_stage(player, map_data):
    global WIN, YEAR
    counter_list = copy.copy(
        player.counter_list)  # The player’s existing army list, make a copy to avoid being affected
    armies_counter = player.armies_counter  # The number of the player's army
    moved_armies_list = []  # Save the list of moved armies
    while True:
        print()
        if armies_counter == 0:
            print("No Army to Move: next turn.\n")  # 5f
            return

        armies_to_move(counter_list)
        while True:
            position = input("Enter four integers as a format ‘x0 y0 x1 y1’ to represent move "
                             "unit from (x0, y0) to (x1, y1) or ‘NO’ to end this turn.\n")
            if position == "NO":
                print()
                return
            elif position == "DIS":
                show_game_map(map_data)
                break
            elif position == "PRIS":
                recruit_price()
                break
            elif position == "QUIT":
                exit()
            elif not re.match(r"^\d+ \d+ \d+ \d+$", position):
                print("Invalid move. Try again.")
                break
            x0, y0, x1, y1 = map(lambda x: int(x), re.findall(r"\d+", position))

            if (x0 == x1 and y0 == y1) \
                    or not (0 <= x0 < len(map_data[0]) and 0 <= x1 < len(map_data[0])) \
                    or not (0 <= y0 < len(map_data) and 0 <= y1 < len(map_data)) \
                    or not isinstance(map_data[y0][x0], Army) \
                    or player.camp != map_data[y0][x0].camp \
                    or map_data[y0][x0] in moved_armies_list \
                    or (not isinstance(map_data[y1][x1], str) and map_data[y1][x1].camp == player.camp):
                # do not step in place
                # Select the coordinates in the chessboard
                # The coordinates of the landing point are in the chessboard
                # make sure that the army is selected to move,
                # and that it is player own pawn
                # Determine whether the army has moved
                # Ensure that the landing is not player own army
                print("Invalid move. Try again.")
                break

            original_army = map_data[y0][x0]
            # Objects are stored in the list, and the objects (armies) that can be selected have the move method
            if not map_data[y0][x0].move(x1, y1, map_data):
                print("Invalid move. Try again.")
                player.broadcast = ""  # Invalid move, clear broadcast message
                # Return to the previous loop, continue to ask for user input
                break

            print(f"\nYou have moved {original_army.TYPE_NAME} from ({x0}, {y0}) to ({x1}, {y1}).")
            if player.broadcast:
                print(player.broadcast.rstrip())
                # Print message: The wood was collected, the enemy was defeated...
            player.broadcast = ""  # Empty broadcast
            if WIN:
                print()
                name = input("What’s your name, commander?\n")
                print(f"\n***Congratulation! Emperor {name} unified the country in {YEAR}.***")
                exit()
            counter_list.remove(original_army)  # Remove the soldier from the copied list, indicating that it has moved
            armies_counter -= 1
            # Throw the new memory address of this element to the one that has been moved.
            moved_armies_list.append(original_army)
            break


class Player(object):
    def __init__(self, camp: str, position_x: int, position_y: int):
        self.camp = camp  # player's camp
        self.position_x = position_x
        self.position_y = position_y
        self.type = "H"
        self.armies_counter = 0  # Save the number of armies on the field
        self.__resources = {"W": 2, "F": 2, "G": 2}  # Initial resources
        self.counter_list = []  # Save the army objects on the field
        self.broadcast = ""

    @property
    def resources(self):
        return self.__resources

    def set_resources(self, type_of_recruit, mode="verify") -> bool:
        """
        Verify that the number of resources is sufficient to recruit the army or reduce resources
        :param type_of_recruit: (Army) army object
        :param mode: String "verify" or "update"
        :return: bool
        """
        if mode == "verify":  # Verify the number of resources
            for c in type_of_recruit.COST:
                if self.__resources[c] - 1 < 0:
                    print("Insufficient resources. Try again.")
                    return False
            return True
        elif mode == "update":
            for c in type_of_recruit.COST:  # Traverse minus recruitment cost
                self.__resources[c] -= 1
            return True

    @property
    def name(self):
        return self.type + self.camp

    def recruit_armies(self, map_data):
        while True:
            print(f"[Your Asset: Wood - {self.resources['W']} Food "
                  f"- {self.resources['F']} Gold - {self.resources['G']}]")
            round_of_generation = True
            while round_of_generation:
                if not generating_conditions(self,
                                             map_data):  # Does not meet the generation conditions, return directly
                    return
                while True:
                    choose = input("\nWhich type of army to recruit, (enter) ‘S’, ‘A’, ‘K’, or ‘T’? Enter"
                                   " ‘NO’ to end this stage.\n")  # spec 5d - i
                    ask_position = False
                    type_of_recruit = ""
                    if choose == "S":
                        # class Spearman
                        type_of_recruit = Spearman
                        ask_position = True
                    elif choose == "A":
                        # class Archer
                        type_of_recruit = Archer
                        ask_position = True
                    elif choose == "K":
                        # class Knight
                        type_of_recruit = Knight
                        ask_position = True
                    elif choose == "T":
                        # class Scout
                        type_of_recruit = Scout
                        ask_position = True
                    elif choose == "NO":
                        return
                    elif choose == "QUIT":
                        exit()
                    elif choose == "DIS":
                        show_game_map(map_data)
                        break
                    elif choose == "PRIS":
                        recruit_price()
                        break
                    else:
                        print("Sorry, invalid input. Try again.")
                        break

                    if ask_position:
                        if not self.set_resources(type_of_recruit):
                            # Insufficient resources, break to back to the military position
                            break
                        while True:
                            army_create_position = input(
                                f"\nYou want to recruit a {type_of_recruit.TYPE_NAME}. Enter two integers as format ‘x y’ to place your army.\n")
                            if army_create_position == "QUIT":
                                exit()
                            elif army_create_position == "DIS":
                                show_game_map(map_data)
                                continue
                            elif army_create_position == "PRIS":
                                recruit_price()
                                continue
                            elif not re.match(r"^\d \d$", army_create_position):
                                print("Sorry, invalid input. Try again.")
                                continue
                            x, y = army_create_position.split(" ")
                            x, y = int(x), int(y)

                            if (x, y) not in [(self.position_x + 1, self.position_y),
                                              (self.position_x - 1, self.position_y),
                                              (self.position_x, self.position_y + 1),
                                              (self.position_x, self.position_y - 1)
                                              ] or map_data[y][x]:
                                # Determine if it is around the base
                                # Or is it occupied (map_data[y][x]-> object-> True)
                                print(
                                    "You must place your newly recruited unit in an unoccupied position next to your home base. Try again.")
                                continue
                            self.set_resources(type_of_recruit, mode="update")
                            map_data[y][x] = type_of_recruit(self, x, y)
                            print(f"\nYou has recruited a {type_of_recruit.TYPE_NAME}.\n")
                            round_of_generation = False  # Return to the position where the selected pawn spawned
                            # print recourse list
                            break  # end inner loop
                    break  # End the training cycle and reprint the resource list


def armies_to_move(counter_list):
    """
    Generate movable army segments.
    :param counter_list: (List) Incoming the list of movable armies of the current player
    :return: None
    """
    spearman_counter_list, archer_counter_list, knight_counter_list, scout_counter_list = [], [], [], []
    # Classify the army objects in the list
    for i in counter_list:
        if isinstance(i, Spearman):
            spearman_counter_list.append((i.position_x, i.position_y))
        elif isinstance(i, Archer):
            archer_counter_list.append((i.position_x, i.position_y))
        elif isinstance(i, Knight):
            knight_counter_list.append((i.position_x, i.position_y))
        elif isinstance(i, Scout):
            scout_counter_list.append((i.position_x, i.position_y))
    print("Armies to Move:")
    # Only output if there is army in the list
    if spearman_counter_list:
        print("  Spearman: " + ", ".join([f"({x}, {y})" for x, y in spearman_counter_list]))
    if archer_counter_list:
        print("  Archer: " + ", ".join([f"({x}, {y})" for x, y in archer_counter_list]))
    if knight_counter_list:
        print("  Knight: " + ", ".join([f"({x}, {y})" for x, y in knight_counter_list]))
    if scout_counter_list:
        print("  Scout: " + ", ".join([f"({x}, {y})" for x, y in scout_counter_list]))
    print()


class Army(object):
    COST = []
    TYPE_NAME = "Army"

    def __init__(self, player, position_x, position_y):
        self.camp = player.camp  # The chess piece camp is the player’s class attribute camp
        self.position_x = position_x
        self.position_y = position_y
        self.type = ""
        self.player = player  # Save the address of the player to which the army belongs

    def move(self, move_horizontal, move_vertical, map_data) -> bool:
        global WIN
        move_horizontal, move_vertical = move_horizontal - self.position_x, move_vertical - self.position_y
        max_step = max(abs(move_horizontal), abs(move_vertical))
        if not (
                (move_vertical == 0 and move_horizontal != 0 and 0 < abs(move_horizontal) <= max_step)
                or (move_vertical != 0 and move_horizontal == 0 and 0 < abs(move_vertical) <= max_step)
        ):  # Determine whether the horizontal and vertical movement is within the range
            return False
        elif self.type != "T" and max_step != 1:  # Limit the number of movement steps other than T
            return False
        # The movement is divided into multiple steps to walk, for example, two steps are [(1,0),(1,0)]
        if max(move_horizontal, move_vertical) == 0:
            if move_horizontal > move_vertical:
                ls = [(0, -1) for _ in range(-1, move_vertical - 1, -1)]
            else:
                ls = [(-1, 0) for _ in range(-1, move_horizontal - 1, -1)]
        else:
            if move_horizontal > move_vertical:
                ls = [(1, 0) for _ in range(1, move_horizontal + 1)]
            else:
                ls = [(0, 1) for _ in range(1, move_vertical + 1)]

        count = 0
        cache = 0
        # If there are two steps and there is one's own army in between, temporarily store T in the cache
        for move_x, move_y in ls:
            new_y = self.position_y + move_y
            new_x = self.position_x + move_x  # New x and y
            target_position = map_data[new_y][new_x]  # The object corresponding to the new coordinate
            if isinstance(target_position, str):  # If the next step is a string, directly replace it (blank position)
                if not cache:
                    # The memory on the old coordinates is directly given to the new coordinates
                    map_data[new_y][new_x] = map_data[self.position_y][self.position_x]
                    map_data[self.position_y][self.position_x] = ""  # Reset old coordinates
                else:
                    map_data[new_y][new_x] = cache
                self.position_x, self.position_y = new_x, new_y  # Update the old coordinates in the class to the new coordinates

            elif isinstance(target_position, Resources):  # If the target location is a resource
                if isinstance(target_position, Wood):  # The target is wood
                    self.player.broadcast += "Good. We collected 2 Wood.\n"
                    self.player.resources["W"] += 2

                elif isinstance(target_position, Food):  # The target is food
                    self.player.broadcast += "Good. We collected 2 Food.\n"
                    self.player.resources["F"] += 2

                elif isinstance(target_position, Gold):  # target is gold
                    self.player.broadcast += "Good. We collected 2 Gold.\n"
                    self.player.resources["G"] += 2

                if cache:
                    map_data[new_y][new_x] = cache  # Replace the memory address in the cache with the new address
                    self.position_x, self.position_y = new_x, new_y  # Coordinate update in class memory
                else:
                    map_data[new_y][new_x] = map_data[self.position_y][self.position_x]  # Update memory to new location
                    map_data[self.position_y][self.position_x] = ""  # Clear the original memory
                    self.position_x, self.position_y = new_x, new_y  # Coordinate update in class memory

            elif isinstance(target_position, Water):  # If it is water
                self.player.broadcast += f"We lost the army {self.TYPE_NAME} due to your command!\n"
                if not cache:
                    self.die_out(map_data)  # self die
                else:
                    self.player.armies_counter -= 1  # Number of player armies - 1
                    self.player.counter_list.remove(self)  # Remove the army from the player object list
                return True

            elif target_position.type == self.type:  # When the same type of army meets, both lose
                self.player.broadcast += f"We destroyed the enemy {target_position.TYPE_NAME} with massive loss!\n"
                if not cache:
                    self.die_out(map_data)  # self die
                else:
                    # If it is in the cache, there is no need to consider deleting the data in the map database.
                    self.player.armies_counter -= 1  # Number of player armies - 1
                    self.player.counter_list.remove(self)  # Remove the army from the player object list
                target_position.die_out(map_data)  # The target also die
                return True

            # If the target belongs to the army or base camp
            elif isinstance(target_position, Army) or isinstance(target_position, Player):
                # Determine whether the target's camp is the same as your own camp, it is the situation of the same camp
                if target_position.camp == self.camp:
                    if len(ls) == 1:  # If it is 1, it means that this is may not a T
                        return False  # Can't kill each other of the same type

                    elif count == 1:  # The second step is to come here, go first else
                        # In fact, there will be no situation where the second step is still the same camp,
                        # because it has been judged before.
                        map_data[new_y - move_vertical][new_x - move_horizontal] = cache
                        self.position_x, self.position_y = new_x - move_horizontal, new_y - move_vertical
                        return False

                    else:  # Gave the scout a chance to take two steps
                        cache = map_data[self.position_y][self.position_x]
                        map_data[self.position_y][self.position_x] = ""  # Clear the original location
                        # Because it cannot be overwritten, it must be stored in the cache
                        # If in the same camp or own base camp, update the new coordinates first
                        self.position_x, self.position_y = new_x, new_y

                else:  # Not in the same camp
                    if isinstance(target_position, Player):  # If this position is the base camp, player will win
                        self.player.broadcast += f"The army {self.TYPE_NAME} captured the enemy’s capital."
                        WIN = True
                        return True
                    if isinstance(self, Spearman):  # If "self" are a spearman
                        # If it weren't for knights and scout, they would not be able to fight
                        if not isinstance(target_position, Knight) and not isinstance(target_position, Scout):
                            self.player.broadcast += f"We lost the army {self.TYPE_NAME} due to your command!\n"
                            self.die_out(map_data)
                            return True

                    elif isinstance(self, Archer):  # If "self" are a Archer
                        if not isinstance(target_position, Spearman) and not isinstance(target_position, Scout):
                            self.player.broadcast += f"We lost the army {self.TYPE_NAME} due to your command!\n"
                            self.die_out(map_data)
                            return True

                    elif isinstance(self, Knight):  # If "self" are a Knight
                        if not isinstance(target_position, Archer) and not isinstance(target_position, Scout):
                            self.player.broadcast += f"We lost the army {self.TYPE_NAME} due to your command!\n"
                            self.die_out(map_data)
                            return True

                    elif isinstance(self, Scout):  # Spearman, "self" will die if whatever meet anyone
                        self.player.broadcast += f"We lost the army {self.TYPE_NAME} due to your command!\n"
                        if not cache:
                            self.die_out(map_data)  # self die
                        else:  # Die in the cache
                            self.player.armies_counter -= 1
                            self.player.counter_list.remove(self)
                        return True

                    # The rest is the case of winning(Defeat the enemy)
                    self.player.broadcast += f"Great! We defeated the enemy {target_position.TYPE_NAME}!\n"
                    target_position.die_out(map_data)  # target die
                    map_data[new_y][new_x] = map_data[self.position_y][self.position_x]  # Move self to a new position
                    map_data[self.position_y][self.position_x] = ""  # Clear the original address
                    self.position_x, self.position_y = new_x, new_y  # Update the memory address in its own class
                    return True
            if count == len(ls) - 1:
                return True
            count += 1

    def die_out(self, map_data):
        map_data[self.position_y][self.position_x] = ""  # Clear the original address
        self.player.armies_counter -= 1  # Number of player armies - 1
        self.player.counter_list.remove(self)
        return

    @property
    def name(self):
        return self.type + self.camp


# The following are all built resource classes
# Inherit the method of the parent class Army
class Spearman(Army):
    COST = ["W", "F"]
    TYPE_NAME = "Spearman"

    def __init__(self, player, position_x, position_y):
        super().__init__(player, position_x, position_y)
        self.type = "S"
        player.armies_counter += 1  # Total number of player armies + 1
        self.player.counter_list.append(self)  # Add self to the player's army class list


class Knight(Army):
    COST = ["F", "G"]
    TYPE_NAME = "Knight"

    def __init__(self, player, position_x, position_y):
        super().__init__(player, position_x, position_y)
        self.type = "K"
        player.armies_counter += 1
        self.player.counter_list.append(self)


class Archer(Army):
    COST = ["W", "G"]
    TYPE_NAME = "Archer"

    def __init__(self, player, position_x, position_y):
        super().__init__(player, position_x, position_y)
        self.type = "A"
        player.armies_counter += 1
        self.player.counter_list.append(self)


class Scout(Army):
    COST = ["W", "F", "G"]
    TYPE_NAME = "Scout"

    def __init__(self, player, position_x, position_y):
        super().__init__(player, position_x, position_y)
        self.type = "T"
        player.armies_counter += 1
        self.player.counter_list.append(self)


class Water(object):
    def __init__(self, position_x, position_y):
        self.type = "~~"
        self.camp = ""
        self.position_x = position_x
        self.position_y = position_y

    @property
    def name(self):
        return self.type


class Resources(object):
    def __init__(self, position_x, position_y):
        self.type = ""
        self.camp = ""
        self.position_x = position_x
        self.position_y = position_y

    @property
    def name(self):
        return self.type


class Wood(Resources):
    def __init__(self, position_x, position_y):
        super().__init__(position_x, position_y)
        self.type = "WW"


class Food(Resources):
    def __init__(self, position_x, position_y):
        super().__init__(position_x, position_y)
        self.type = "FF"


class Gold(Resources):
    def __init__(self, position_x, position_y):
        super().__init__(position_x, position_y)
        self.type = "GG"


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 little_battle.py <filepath>")
        sys.exit()
    width, height, waters, woods, foods, golds = load_config_file(sys.argv[1])
    # ============================================================================================#
    player_1 = Player("1", 1, 1)
    player_2 = Player("2", width - 2, height - 2)
    data = create_init_database(width, height, waters, woods, foods, golds, player_1, player_2)
    main()
