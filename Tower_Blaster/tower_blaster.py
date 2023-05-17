import random


def setup_bricks():
    '''
    This function sets up the numbers included in the main_pile
    and creates a discard_pile for further discard bricks.

    This function returns both lists with the main pile as the first item
    and the discard pile as the second.
    '''

    main_pile = [i for i in range(1, 61)]
    discard_pile = []
    return main_pile, discard_pile


def shuffle_bricks(bricks):
    '''
    This function shuffles the given bricks.

    This function does not return anything.
    '''
    random.shuffle(bricks)


def check_bricks(main_pile, discard_pile):
    '''
    This function checks if there are any bricks left in the given main_pile of bricks.
    If not, shuffle the discard_pile and move the bricks into the main_pile.
    Then it turns over the top brick back to the discard_pile.

    This function does not return anything.
    '''

    if len(main_pile) == 0:
        shuffle_bricks(discard_pile)
        # add discard_pile to main_pile
        main_pile.extend(discard_pile)
        #clean the discard_pile
        discard_pile.clear()
        # turn over the top brick to be the start of the new discard pile
        discard_pile.append(main_pile[0])
        main_pile.pop(0)


def check_tower_blaster(tower):
    '''
    This function checks if the tower is completed with an ascending order.

    This function returns a boolean value.
    '''

    check_tower = tower.copy()
    check_tower.sort()
    # check the completeness of the tower
    if tower == check_tower:
        return True
    else:
        return False


def get_top_brick(brick_pile):
    '''
    This function returns the top brick of any given tower or pile.
    '''

    return brick_pile.pop(0)


def deal_initial_bricks(main_pile):
    '''
    This function distributes the top 20 bricks in turn to computer and player.

    This function returns two lists, first for the computer, second for the player.
    '''
    # computer first
    initial_computer = []
    # player second
    initial_player = []

    for i in range(10):
        # append the bricks to the end of the lists
        initial_computer.append(get_top_brick(main_pile))
        initial_player.append((get_top_brick(main_pile)))

    # reverse the lists to get the correct order
    initial_computer.reverse()
    initial_player.reverse()

    return initial_computer, initial_player


def add_brick_to_discard(brick, discard_pile):
    '''
    This function inserts the given brick to the top of the discard_pile.

    This function does not return anything.
    '''
    discard_pile.insert(0, brick)


def find_and_replace(new_brick, brick_to_be_replaced, tower, discard_pile):
    '''
    This function is used to replace the brick in the tower by the new_brick chosen.

    This function returns true if the bricks to be replaced can be found in the tower;
    and returns false if the bricks cannot be found.
    '''

    try:
        # find the index of the brick to be replaced
        replace_index = tower.index(brick_to_be_replaced)
        # replace it with the new_brick
        tower[replace_index] = new_brick
        # place the brick being replaced to the top of the discard_pile
        discard_pile.insert(0, brick_to_be_replaced)
        return True

    # check the brick to be replaced is indeed the brick in the tower
    except ValueError:
        print("Invalid number, please enter again.")
        return False


def computer_play(tower, main_pile, discard_pile):
    '''
    This is the function considering the strategy that the computer adopts.

    Regardless of the current tower that the computer has, just stick to the following switch rules:

    1. Divide the tower into 10 positions, and since the range for the bricks is 1-60,
    so each level will be assigned 6 numbers.

    e.g. top: 1-6; bottom: 55-60

    2. When getting the bricks from the top of the discard_pile,
    check if in its range, there is already another number positioned in the level.

    e.g. discard_pile top: 10 --> it should be placed in level 2 (7-12);
    if there is no other numbers, say 11 (range 7 to 12), in level 2, take the brick
    and replace it with the level 2 brick.

    3. If there is another number in the level that is within the range of the
    discard_pile brick, choose the mystery brick from the top of the main_pile.

    4. Repeat step 2 and swap the brick if it satisfies the rule.

    5. If not 4, meaning that there is already a brick within the level,
    choose to skip the current turn and change nothing.

    '''

    current_discard_top = discard_pile[0]
    # locate the position to be checked
    cdt_index = current_discard_top // 6

    # handle the bound issue regarding tower[cdt_index]
    if cdt_index == 10:
        cdt_index -= 1

    if (cdt_index * 6 < tower[cdt_index] <= (cdt_index + 1) * 6):
        current_main_top = main_pile[0]
        cmt_index = current_main_top // 6
        if cmt_index == 10:
            cmt_index -= 1

        if (cmt_index * 6 < tower[cmt_index] <= (cmt_index + 1) * 6):
            # will not take the brick and skip the turn
            print("Computer chooses to skip the turn.")
            print("Computer's Tower: ", tower)
            print()

        else:
            brick_to_be_removed = tower[cmt_index]
            find_and_replace(get_top_brick(main_pile), brick_to_be_removed, tower, discard_pile)
            print("The computer picked {} from the main brick".format(current_main_top))
            print("Computer's Tower: ", tower)
            print()
    else:
        brick_to_be_removed = tower[cdt_index]
        find_and_replace(get_top_brick(discard_pile), brick_to_be_removed, tower, discard_pile)
        print("The computer picked {} from the discard brick".format(current_discard_top))
        print("Computer's Tower: ", tower)
        print()

    return tower


def intro():
    # print instructions and start the game
    print("-" * 50)
    print("----------Welcome to Tower Blaster Game!----------")
    print("-" * 50)
    print("Here are the rules:")
    print("--A Tower Blaster game starts with a main pile of 60 bricks,"
          "each numbered from 1 to 60.")
    print("--The computer and you will each be given 10 random bricks from the main pile.")
    print("--In each turn, the computer and you will be asked if to replace a brick or not.")
    print("--Computer will move first and you the second.")
    print("--Try to arrange your tower with 10 bricks in ascending order as fast as possible.")
    print("Now let's get started!")
    print("")


def player_play(tower, main_pile, discard_pile):
    while True:
        # ask the first question when the top of the discard_pile is shown to the player
        decision1 = input("Type 'D' to take the discard brick, 'M' for a mystery brick, "
                          "or 'H' for help")
        if (decision1[0] == 'D' or decision1[0] == 'd'):
            # do not use get_top_brick() function to avoid the over pop() issue
            top_brick = discard_pile[0]
            print("You picked {} from the discard brick.".format(top_brick))

            while True:
                try:
                    decision2 = int(
                        input("Where do you want to place this brick? Type a brick number to replace in your tower."))
                    if find_and_replace(discard_pile[0], decision2, tower, discard_pile):
                        print("Your Tower after the swap: ", tower)

                        break
                    else:
                        print("The brick you entered is not in your tower."
                              "Please enter again.")
                        continue
                # if player types in things other than int, start over the previous question
                except ValueError:
                    print("The number you entered is not an integer."
                          "Please enter a valid brick number again.")

        elif (decision1[0] == 'M' or decision1[0] == 'm'):
            move_in_main = main_pile[0]
            print("You picked {} from main pile.".format(move_in_main))

            flag2 = True
            while flag2:
                try:
                    decision3 = input("Do you want to use this brick? "
                                      "Type 'Y' for yes or 'N' to skip turn")
                    if (decision3[0] == 'Y' or decision3[0] =='y'):
                        while True:
                            move_out_player = int(input("Where do you want to place this brick? Type a brick number "
                                                        "to replace in your tower."))
                            if find_and_replace(main_pile[0], move_out_player, tower, discard_pile):
                                # now can use get_top_brick() to pop the top brick from the main_pile
                                get_top_brick(main_pile)
                                print("Your Tower after the swap: ", tower)
                                flag2 = False
                                break
                            else:
                                print("The brick you entered is not in your tower."
                                      "Please enter again.")
                                continue
                    # the player chooses not to use the brick
                    elif (decision3[0] == 'N' or decision3[0] == 'n'):
                        break

                except ValueError:
                    print("The input you entered is invalid."
                          "Please enter again.")
                    continue
        elif (decision1[0] == 'H' or decision1[0] == 'h'):
            print("Please refer to the instruction and enter again.")
            continue

        else:
            continue
        break


def main():
    # set up the main_pile and discard_pile and prepare the game
    main_pile = setup_bricks()[0]
    discard_pile = setup_bricks()[1]
    # shuffle the bricks in main_pile
    shuffle_bricks(main_pile)

    # distribute bricks from the main_pile in turn to both computer and player
    initial_bricks = deal_initial_bricks(main_pile)
    computer_tower = initial_bricks[0]
    player_tower = initial_bricks[1]

    # turn over the top brick from the main_pile to the discard_pile
    add_brick_to_discard(get_top_brick(main_pile), discard_pile)

    intro()
    print("Your Tower: ", player_tower)
    print("Computer's Tower: ", computer_tower)
    print()

    while (check_tower_blaster(computer_tower) == False and check_tower_blaster(player_tower) == False):

        check_bricks(main_pile, discard_pile)
        # computer's move
        print("Computer starts the round: ")
        print("Computer's Tower: ", computer_tower)
        # print("Computer's Tower: [*, *, *, *, *, *, *, *, *, *]", )
        print("The top brick on the discard pile is: ", discard_pile[0])
        computer_play(computer_tower, main_pile, discard_pile)
        print("Computer finished the round.")
        print()

        check_bricks(main_pile, discard_pile)
        # player's move
        print("Now is your turn: ")
        print("Your Tower: ", player_tower)
        print("The top brick on the discard pile is: ", discard_pile[0])
        player_play(player_tower, main_pile, discard_pile)
        print("Your turn finish.")
        print()

        # check if the computer wins the game
        if check_tower_blaster(computer_tower):
            print("Computer wins the game.")
            print("Your unfinished tower is: ", player_tower )
            break

        # check if the player wins the game
        if check_tower_blaster(player_tower):
            print("You win the game!")
            print("The computer's unfinished tower is: ", computer_tower)
            break




if __name__ == "__main__":
    main()
