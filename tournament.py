import pygame
import sys, os, shutil, math, random
from bracket import Bracket

from settings import *

os.makedirs(winners_dir, exist_ok=True)


# Initialize Pygame
pygame.init()
surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH = surface.get_width()
SCREEN_HEIGHT = surface.get_height()
pygame.display.set_caption("Meme Tournament")

# Set the font and font size
font = pygame.font.Font(None, 30)
winner_font = pygame.font.Font(None, 120)

# Define colors
BG = (40, 40, 40)
BLACK = (0, 0, 0)
SELECT = (0, 235, 235)
TEXT = (240, 240, 240)

# Load images
path = "."
filenames = next(os.walk("./" + images_dir), (None, None, []))[2]
if ".DS_Store" in filenames:
    filenames.remove(".DS_Store")
filenames = ["./" + images_dir + "/" + fn for fn in filenames]
for path in filenames:
    # print(path)
    pygame.image.load(path)
images = [pygame.image.load(path) for path in filenames]

n_competitors = len(images)
n_slots = 2 ** math.ceil(math.log2(n_competitors)) if n_competitors > 1 else 2
n_byes = n_slots - n_competitors
images += [None] * n_byes
filenames += [None] * n_byes
n_competitions = n_slots // 2
paired = list(zip(images, filenames))
random.shuffle(paired)
images, filenames = map(list, zip(*paired))
print(f"{n_competitors} competitors, {n_byes} byes, {n_competitions} first-round brackets")
battle_screen = False
selected_image = "left"
chosen_image = None
chosen_file = None
tournament_winner = None
tournament_winner_fn = None

Bracket.initialize_brackets(n_competitions, SCREEN_WIDTH, SCREEN_HEIGHT)
Bracket.set_bracket_memes(images, filenames)

for i, bracket in enumerate(Bracket.round_brackets[1]):
    if bracket.meme1 is None and bracket.meme2 is not None:
        winner, winner_fn = bracket.meme2, bracket.meme2_fn
    elif bracket.meme2 is None and bracket.meme1 is not None:
        winner, winner_fn = bracket.meme1, bracket.meme1_fn
    else:
        continue
    try:
        if i % 2 == 0:
            bracket.next_bracket.meme1 = winner
            bracket.next_bracket.meme1_fn = winner_fn
        else:
            bracket.next_bracket.meme2 = winner
            bracket.next_bracket.meme2_fn = winner_fn
    except AttributeError:
        pass

prev_bracket = -1
selected_bracket = 0
current_bracket = Bracket.brackets[0]
current_bracket.selected = True

def find_bracket_location(bracket):
    for round_i, brackets in Bracket.round_brackets.items():
        for bracket_i, b in enumerate(brackets):
            if b is bracket:
                return round_i, bracket_i
    return None, None

def resize_image(pygame_image):
    original_width = pygame_image.get_width()
    original_height = pygame_image.get_height()

    # Calculate the aspect ratio
    aspect_ratio = original_width / original_height

    # Calculate the new height based on the desired width and aspect ratio
    new_width = SCREEN_WIDTH // 2
    new_height = int(new_width / aspect_ratio)

    if new_height > SCREEN_HEIGHT:
        new_height = SCREEN_HEIGHT
        new_width = int(aspect_ratio * new_height)

    return new_width, new_height

def save_winner(fn):
    base = fn.split("/")[-1]
    shutil.copyfile(fn, winners_dir + "/WINNER_" + base)
    print(f"Winner: {base}")

def output_last_filenames():
    print("Final 4:")
    for i in range(len(Bracket.brackets)-1, len(Bracket.brackets) - 3, -1):
        # print(i)
        print(Bracket.brackets[i].meme1_fn)
        print(Bracket.brackets[i].meme2_fn)
        print(Bracket.brackets[i].meme1_fn.split("/")[-1])
        print(Bracket.brackets[i].meme2_fn.split("/")[-1])
        shutil.copyfile(Bracket.brackets[i].meme1_fn, winners_dir + "/" + Bracket.brackets[i].meme1_fn.split("/")[-1])
        shutil.copyfile(Bracket.brackets[i].meme2_fn, winners_dir + "/" + Bracket.brackets[i].meme2_fn.split("/")[-1])


# Main game loop
while True:
    # try:
    surface.fill(BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            output_last_filenames()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if battle_screen: 
                    try:
                        if selected_bracket % 2 == 0:
                            current_bracket.next_bracket.meme1 = chosen_image
                            current_bracket.next_bracket.meme1_fn = chosen_file
                        else:
                            current_bracket.next_bracket.meme2 = chosen_image
                            current_bracket.next_bracket.meme2_fn = chosen_file
                    except AttributeError:
                        tournament_winner = chosen_image
                        tournament_winner_fn = chosen_file
                        save_winner(chosen_file)

                    # Switch to tournament screen
                    battle_screen = False
                else:
                    if current_bracket.meme1 is not None and current_bracket.meme2 is not None:
                        battle_screen = True

            if battle_screen:
                if event.key == pygame.K_LEFT:
                    selected_image = "left"
                elif event.key == pygame.K_RIGHT:
                    selected_image = "right"

            elif not battle_screen:
                if event.key == pygame.K_LEFT:
                    prev_bracket = selected_bracket
                    selected_bracket -= 1
                elif event.key == pygame.K_RIGHT:
                    prev_bracket = selected_bracket
                    selected_bracket += 1
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    round_i, bracket_i = find_bracket_location(current_bracket)
                    if round_i is not None:
                        is_final = not hasattr(current_bracket, 'next_bracket')
                        if is_final:
                            target_round = round_i - 1
                            target_index = 0 if event.key == pygame.K_UP else 1
                        elif current_bracket.upways:
                            if event.key == pygame.K_DOWN:
                                target_round, target_index = round_i + 1, bracket_i // 2
                            else:
                                target_round, target_index = round_i - 1, bracket_i * 2
                        else:
                            if event.key == pygame.K_UP:
                                target_round, target_index = round_i + 1, bracket_i // 2
                            else:
                                target_round, target_index = round_i - 1, bracket_i * 2
                        if target_round in Bracket.round_brackets:
                            rbs = Bracket.round_brackets[target_round]
                            target_index = max(0, min(target_index, len(rbs) - 1))
                            target_bracket = rbs[target_index]
                            new_index = Bracket.brackets.index(target_bracket)
                            Bracket.update_current_bracket(selected_bracket, new_index)
                            prev_bracket = selected_bracket
                            selected_bracket = new_index
                            current_bracket = Bracket.current_bracket

                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    try:
                        Bracket.update_current_bracket(prev_bracket, selected_bracket)
                        current_bracket = Bracket.current_bracket
                    except:
                        output_last_filenames()

    if battle_screen:
        # Draw battle screen
        # Resize images, preserve aspect ratio
        if current_bracket.meme1 != None and current_bracket.meme2 != None:
            meme1 = pygame.transform.scale(current_bracket.meme1, resize_image(current_bracket.meme1))
            meme2 = pygame.transform.scale(current_bracket.meme2, resize_image(current_bracket.meme2))
            meme1_fn = current_bracket.meme1_fn
            meme2_fn = current_bracket.meme2_fn

            left_image_rect = meme1.get_rect()
            left_image_rect.topleft = (0, 0)
            right_image_rect = meme2.get_rect()
            right_image_rect.topleft = (SCREEN_WIDTH // 2, 0)

            # Draw images with outlines
            surface.blit(meme1, left_image_rect)
            surface.blit(meme2, right_image_rect)

            # Display image names
            meme1_text = meme1_fn.split(images_dir + '/')[1].split('_')[0].title()
            meme2_text = meme2_fn.split(images_dir + '/')[1].split('_')[0].title()

            # Render the left and right titles
            left_title_surface = font.render(meme1_text, True, TEXT)
            right_title_surface = font.render(meme2_text, True, TEXT)

            # Get the dimensions of the title surfaces
            left_title_width, left_title_height = left_title_surface.get_size()
            right_title_width, right_title_height = right_title_surface.get_size()


            # Draw the left and right titles on the screen
            surface.blit(left_title_surface, ((SCREEN_WIDTH // 4) - (left_title_width // 2), SCREEN_HEIGHT - left_title_height))
            surface.blit(right_title_surface, ((SCREEN_WIDTH * 3 // 4) - (right_title_width // 2), SCREEN_HEIGHT - right_title_height))



            if selected_image == "left":
                pygame.draw.rect(surface, SELECT, left_image_rect, 10)
                chosen_image = meme1
                chosen_file = meme1_fn
            elif selected_image == "right":
                pygame.draw.rect(surface, SELECT, right_image_rect, 10)
                chosen_image = meme2
                chosen_file = meme2_fn
    
    elif not battle_screen:
        Bracket.draw_brackets(surface)
        if tournament_winner is not None:
            orig_w, orig_h = tournament_winner.get_width(), tournament_winner.get_height()
            aspect = orig_w / orig_h
            w = min(SCREEN_WIDTH, int(SCREEN_HEIGHT * aspect))
            h = min(SCREEN_HEIGHT, int(SCREEN_WIDTH / aspect))
            winner_scaled = pygame.transform.scale(tournament_winner, (w, h))
            winner_rect = winner_scaled.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            surface.blit(winner_scaled, winner_rect)
            label = winner_font.render("WINNER!", True, SELECT)
            surface.blit(label, label.get_rect(center=(SCREEN_WIDTH // 2, 60)))
    
    pygame.display.flip()
