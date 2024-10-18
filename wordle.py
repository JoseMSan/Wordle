import csv
import random
import pygame
import sys

pygame.init()

# DIMENSIONS AND TITLE =============>
WIDTH, HEIGHT = 500, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle Game Team 1")

# COLORS (CODES) ==================>
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# SELECT FONTS ====>
FONT = pygame.font.SysFont("Arial", 40)
MINI_FONT = pygame.font.SysFont("Montserrat", 30)

# IMPORT OUR DATA BASE =============>
with open('RANDOM_WORDS - Hoja 1.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    WORDS = [row for row in reader]
    
# SELECT LANGUAGE ==================>
def select_language():
    WINDOW.fill(BLACK)
    # SET UP OF THE FIRST PAGE
    welcome = FONT.render("Welcome player", True, WHITE)
    title = FONT.render("Select Language", True, WHITE)
    spanish_option = MINI_FONT.render("1. Spanish", True, RED)
    english_option = MINI_FONT.render("2. English", True, GREEN)
    # DISPLAY IT ON THE SCREEN
    WINDOW.blit(welcome, (80, 50))
    WINDOW.blit(title, (80, 80))
    WINDOW.blit(spanish_option, (120, 180))
    WINDOW.blit(english_option, (120, 220))
    # THIS UPDATES OUR SCREEN ==>
    pygame.display.update()
    # LANGUAGE SELECTION ======>
    lang = 0
    while lang == 0:
        # GET PYGAME EVENT (ANY)
        for event in pygame.event.get():
            # DETECT IF THE USER QUITS THE GAME
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # DETECT IF THE USER CLICKS THE KEYBOARD
            if event.type == pygame.KEYDOWN:
                # DETECT IF THE USER CLICKS 1
                if event.key == pygame.K_1:
                    lang = 1
                # DETECT IF THE USER CLICKS 2
                elif event.key == pygame.K_2:
                    lang = 2
    
    return lang

# INSTRUCTIONS FUNCTION ============>
def show_instructions(lang):
    WINDOW.fill(BLACK)
    # FROM SELECT LANGUAGE, DETECT WHICH ARRAY WE WILL USE
    if lang == 1:
        instructions = [
            "======== REGLAS ============",
            "Empieza a escribir una palabra de 5 letras.",
            "Solo tendrás 5 intentos.",
            "Verde: letra y posición correcta",
            "Amarillo: letra correcta, posición incorrecta",
            "Rojo: letra y posición incorrecta"
        ]
    else:
        instructions = [
            "======== RULES ============",
            "Start typing a 5-letter word.",
            "You will have 5 attempts.",
            "Green: correct letter and position",
            "Yellow: correct letter, wrong position",
            "Red: wrong letter and position"
        ]
    # INITIAL Y COORD
    y_coord = 50
    # FOR EACH ELEMENT IN OUR ARRAY
    for line in instructions:
        # RENDER EACH LINE
        text = MINI_FONT.render(line, True, WHITE)
        # DISPLAY EACH LINE
        WINDOW.blit(text, (20, y_coord))
        # INCREASE Y COORD ADDING SPACE BETWEEN THEM
        y_coord += 50
    # UPLOAD SCREEN ===>
    pygame.display.update()

# DRAW BOARD FOR GAME ==============>
def draw_board(guessed_words, score):
    WINDOW.fill(BLACK)
    # DYNAMIC SPACE IN Y AXIS
    y_coord = 50
    # GUESSED WORDS IS AN ARRAY, IT WILL READ EACH ELEMENT
    # SO IT WILL READ EACH LETTER ONE BY ONE.
    for i in guessed_words:
        # FOR EACH LETTER IN THE WORD
        guessed_word = i[0]
        # DYNAMIC COLOR PICKER FOR EACH WORD.
        colors = i[1]
        # IT MAKES THE WORDS APPEAR IN THE SCREEN
        # ITERATING THE POSITION FROM OUR ARRAY GUESSED_WORDS
        # TAKEN BY THE GAME FUNCTION
        # ACCESS EACH LETTER
        for j, letter in enumerate(guessed_word):
            # RENDERS EACH LETTER OF OUR GUESSED WORD-
            text = FONT.render(letter, True, colors[j])
            WINDOW.blit(text, (50 + j * 60, y_coord))
        y_coord += 60
    score_text = MINI_FONT.render(f"Score: {score}", True, WHITE)
    WINDOW.blit(score_text, (20, HEIGHT - 50))  # Adjust position as needed
    pygame.display.update()

# SCORE SYSTEM ======>
def score_system(guessed_words):
    # DETERMINE THE SCORE OF HOW MANY WORDS WERE GUESSED
    # BEFORE THE WON IS TRUE
    score = 0
    score_reader = len(guessed_words)
    if score_reader == 0:
        score = 100
    elif score_reader == 1:
        score = 90
    elif score_reader == 2:
        score = 80
    elif score_reader == 3:
        score = 70
    elif score_reader == 4:
        score = 60
    elif score_reader == 5:
        score = 50
    else:
        score = 0
    return score

# COLOR FUNCTIONS ====================>
# RECEIVES THE WORD AND ALSO RECEIVES THE
# SPECIFIC WORD, THIS FUNCTION IS TO MAKE A DYNAMIC COLOR
# EACH ELEMENT OF OUR GUESS
def check_guess(word, guess):
    # COLOR ARRAYS
    colors = []
    # ACCESS EACH LETTER OF OUR GUESSED WORD.
    for i, letter in enumerate(guess):
        # IF THEY ARE THE SAME, IT ADDS TO THE COLORS ARRAY GREEN
        if letter == word[i]:
            colors.append(GREEN)
        # IF THE LETTER IS INSIDE, IT ADDS TO THE COLOR ARRAY YELLOW
        elif letter in word:
            colors.append(YELLOW)
        else:
        # IF IT IS NOT FOUND, ADD RED
            colors.append(RED)
    # RETURN AN ARRAY WITH THE COLOR VALUE
    return colors

# GAME FUNCTION =======>
def game(lang, word):
    # ATTEMPTS NUMBER
    attempts = 5
    # GUESSED WORDS ARRAY IN ORDER TO ACCESS EACH LETTER
    guessed_words = []
    # MATRIX CREATION
    final_colors  = []
    # EVENT HANDLER
    won = False

    while len(guessed_words) < attempts and not won:
        current_guess = ""
        input_active = True
        current_score = 100
        # KEEP ASKING THE USER
        while input_active:
            # QUICK VERIFICATION
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # IF USER PRESSES ANY KEY
                if event.type == pygame.KEYDOWN:
                    # THE 'ENTER' KEY, THEN THE WORD IS STORED
                    if event.key == pygame.K_RETURN:
                        # CURRENT GUESS IS OUR NEW ARRAY
                        # CHECKS IF IT HAS 5 LETTERS
                        if len(current_guess) == 5:
                            # MAKE THEM UPPER, FOR DESIGN ONLY
                            current_guess = current_guess.upper()
                            # CHECK EVERY LETTER OF OUR CURRENT GUESS
                            # GIVES EVERY LETTER A COLOR AND SAVE THEM IN AN ARRAY
                            colors = check_guess(word, current_guess)
                            # IT CREATES AN ARRAY WITH THE WORD AND ANOTHER ARRAY WITH
                            # COLOR OF EACH LETTER OF THE GUESSED WORD.
                            row = [current_guess, colors]
                            guessed_words.append(row)
                            # APPEND TO THE MATRIX
                            final_colors.append(colors)
                            print(f'User current guess: ', ''.join(current_guess))
                            print("Final colors matrix:")
                            for i in final_colors:
                                print(i)
                            print(' ')                          
                            # FUNCTION OF DRAWING EACH LETTER ON THE BOARD
                            # GUESSED WORDS IS AN ARRAY WITH 'WORD' AND THE COLORS OF EACH LETTER
                            # CHECK FOR THE SCORE FOR EACH ITERATION
                            current_score = score_system(guessed_words)
                            print(f'Current Score: {current_score}')  # Print for debugging
                            draw_board(guessed_words, current_score)
                            # STRINGIFY THE ARRAY
                            if "".join(current_guess) == word:
                                # CHECK IF IT'S THE SAME
                                print("You guessed the correct word!")
                                input_active = False
                                won = True
                            # CHECK IF THE USER ALREADY HAS AN ARRAY OF 5 ELEMENTS
                            # SO THEY CAN'T GUESS AGAIN AND LOSE
                            if len(guessed_words) >= attempts:
                                input_active = False
                                print("You lost!")
                            # IF THEY DIDN'T LOSE OR GUESS
                            # THE WORD, THEY CAN GUESS AGAIN
                            current_guess = "" 
                        # IF THE USER DIDN'T PUT A 5 LETTER WORD
                        else:
                            print("Introduce a 5-letter word.")
                    # CAPACITY TO ERASE
                    elif event.key == pygame.K_BACKSPACE:
                        # IF THE USER PRESSES THE 'BACKSPACE' KEY
                        # IT ERASES THE LAST LETTER OF THE CURRENT GUESS
                        current_guess = current_guess[:-1]
                    else:
                        if len(current_guess) < 5:
                            current_guess += event.unicode.upper()
            draw_board(guessed_words, current_score)
            pygame.display.set_caption(f"Wordle - Current Guess: {current_guess}")

    # SHOW ALL THE WORDS IN COLORS
    display_guessed_words(final_colors, word, current_score)

# MATRIX HERE !!! ====>>
def display_guessed_words(final_colors, correct_word, score):
    WINDOW.fill(BLACK)
    y_coord = 100
    result_title = MINI_FONT.render("Game resume:", True, WHITE)
    WINDOW.blit(result_title, (20, y_coord))
    y_coord += 50

    for word in final_colors:
        x_offset = 20
        for color in word:
            # GENERATE SQUARES THAT REPRESENT THE COLOR
            pygame.draw.rect(WINDOW, color, (x_offset, y_coord, 30, 30))
            # ADD SPACING
            x_offset += 50
        # ADD SPACING IN EACH ITERATION
        y_coord += 40

    # FINAL CORRECT WORD AT THE END
    correct_text = MINI_FONT.render(f"Correct word: {correct_word}", True, GREEN)
    WINDOW.blit(correct_text, (20, y_coord))
    y_coord += 50  # Move down for the score display

    # DISPLAY FINAL SCORE
    score_text = MINI_FONT.render(f"Final Score: {score}", True, WHITE)
    WINDOW.blit(score_text, (20, y_coord))

    pygame.display.update()
    
    # QUIT EVENT HANDLES
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# CALLING ALL THE FUNCTIONS
def main():
    lang = select_language()

    random_word = random.choice(WORDS)
    if lang == 1:
        word = random_word['SPANISH'].upper()
    elif lang == 2:
        word = random_word['ENGLISH'].upper()

    show_instructions(lang)

    pygame.time.delay(3000)

    game(lang, word)

main()