import random

def print_centered(text, width=50):
    print(text.center(width))

def show_intro():
    print_centered("FATHER")
    print_centered("CREATIVE COMPUTING")
    print_centered("MORRISTOWN, NEW JERSEY")
    print('\n' * 3)
    print("WANT TO HAVE A DEBATE WITH YOUR FATHER, EH??")
    
def show_instructions():
    print("YOU ARE GOING TO PLAY IN A GAME IN WHICH YOU WILL DISCUSS")
    print("A PROBLEM WITH YOUR FATHER AND ATTEMPT TO GET HIM TO")
    print("AGREE WITH YOU IN THREE TRIES.")
    print()
    print("FOR EACH STATEMENT YOU MAKE, I WILL TELL YOU WHAT")
    print("YOUR FATHER REPLIED.")
    print()
    print("YOU MUST SELECT YOUR STATEMENT FROM ONE")
    print("OF THE FOLLOWING SIX.")

def show_statements():
    print("**********")
    print("1.     O.K. I WILL STAY HOME.")
    print("2.     BUT I'D REALLY LIKE TO GO. ALL MY FRIENDS ARE GOING.")
    print("3.     IF ALL MY WORK IS DONE, I SHOULD BE ABLE TO GO.")
    print("4.     IF YOU LET ME GO OUT I'LL BABYSIT ALL NEXT WEEK")
    print("5.     YOU NEVER LET ME DO WHAT I WANT TO DO.")
    print("6.     I'M GOING ANYWAY!")
    print("**********")
    print()

def get_valid_input(prompt, valid_range):
    while True:
        try:
            response = int(input(prompt))
            if response in valid_range:
                return response
            else:
                print("INVALID RESPONSE. PLEASE CHOOSE A NUMBER BETWEEN 1 AND 6.")
        except ValueError:
            print("INVALID INPUT. PLEASE ENTER A NUMBER.")

def play_game():
    points = 0
    attempts = 0
    responses = [
        "NO, YOU CAN'T GO OUT ON A DATE SAT. NITE AND THAT'S THAT.",
        "I DON'T THINK YOU DESERVE TO GO OUT SAT. NITE.",
        "NO, I'M SORRY, BUT YOU REALLY DON'T DESERVE TO GO SAT. NIGHT.",
        "WELL, MAYBE, BUT I DON'T THINK YOU SHOULD GO.",
        "O.K. IF YOU DO THAT YOU CAN GO OUT SAT. NIGHT."
    ]

    points_dict = {1: -1, 2: 2, 3: -1, 4: 2, 5: -1, 6: -2}

    print(responses[0])

    for attempt in range(3):
        attempts += 1
        response = get_valid_input("WHAT WOULD YOU SAY FIRST (CHOOSE 1-6): ", range(1, 7))
        
        points += points_dict[response]
        
        if response == 1:
            print("AGREEMENT REACHED")
            break
        else:
            print("YOUR FATHER SAID:")
            if response == 2:
                print(responses[1])
            elif response in [3, 4]:
                print(responses[3])
            elif response == 5:
                print(responses[0])
            elif response == 6:
                print(responses[0])
            
            print(f"YOUR SCORE IS NOW {points} POINTS.")

    print(f"ON A SCALE OF -7 TO 4, YOUR SCORE WAS {points} POINTS.")
    return points

def final_decision(points):
    print("IT IS NOW SAT. NIGHT, WHICH DO YOU DO?")
    print("1. GO OUT.")
    print("2. STAY HOME.")
    decision = get_valid_input("", [1, 2])

    if decision == 1:
        if random.random() > 0.5:
            print("YOUR FATHER CHECKED UP ON YOU.")
        else:
            print("YOUR FATHER DIDN'T CHECK UP ON YOU.")

    if points >= 2:
        print("WELL DONE!")
    elif points > -4:
        print("YOU CONVINCED YOUR FATHER BUT IT TOOK TOO MANY TRIES.")
    else:
        print("YOU DIDN'T SUCCEED IN CONVINCING YOUR FATHER.")

def main():
    show_intro()
    if input("DO YOU WANT INSTRUCTIONS (YES/NO): ").upper() == "YES":
        show_instructions()
        show_statements()
    
    score = play_game()
    final_decision(score)

    while input("WOULD YOU LIKE TO TRY AGAIN (YES/NO): ").upper() == "YES":
        score = play_game()
        final_decision(score)

if __name__ == "__main__":
    main()
