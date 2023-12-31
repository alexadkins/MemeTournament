import pygame
import sys, os, shutil
from bracket import Bracket

section = "001/"

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
surface = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Meme Tournament")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SELECT = (0, 235, 235)

# Load images
path = "."
filenames = next(os.walk("./images"), (None, None, []))[2]
filenames = ["./images/" + fn for fn in filenames]
images = [pygame.image.load(path) for path in filenames]

n_competitors = len(images)
n_competitions = len(images)//2
# n_competitors = 16
battle_screen = False
selected_image = "left"
chosen_image = None
chosen_file = None

Bracket.initialize_brackets(n_competitions, SCREEN_WIDTH, SCREEN_HEIGHT)
Bracket.set_bracket_memes(images, filenames)

# Bracket.brackets[50].set_memes(images[0], images[2])
for bracket in Bracket.brackets:
    bracket.set_memes(images[0], images[1])
    bracket.set_filenames(filenames[0], filenames[1])

prev_bracket = -1
selected_bracket = 0
current_bracket = Bracket.brackets[0]
current_bracket.selected = True

def resize_image(pygame_image):
    original_width = pygame_image.get_width()
    original_height = pygame_image.get_height()

    # Calculate the aspect ratio
    aspect_ratio = original_width / original_height

    # Calculate the new height based on the desired width and aspect ratio
    new_width = SCREEN_WIDTH // 2
    new_height = int(new_width / aspect_ratio)

    return new_width, new_height

def output_last_filenames():
    print("Final 4:")
    for i in range(len(Bracket.brackets)-1, len(Bracket.brackets) - 3, -1):
        # print(i)
        print(Bracket.brackets[i].meme1_fn)
        print(Bracket.brackets[i].meme2_fn)
        shutil.copyfile(Bracket.brackets[i].meme1_fn, section + Bracket.brackets[i].meme1_fn)
        shutil.copyfile(Bracket.brackets[i].meme2_fn, section + Bracket.brackets[i].meme2_fn)


# Main game loop
while True:
    # try:
    surface.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("What")
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
                    except:
                        pass

                    # Switch to tournament screen
                    battle_screen = False
                else:
                    # Switch to battle screen 
                    battle_screen = True

            if battle_screen:
                if event.key == pygame.K_LEFT:
                    selected_image = "left"
                elif event.key == pygame.K_RIGHT:
                    selected_image = "right"

            elif not battle_screen:
                if event.key == pygame.K_LEFT:
                    # Move left in the bracket
                    prev_bracket = selected_bracket
                    selected_bracket -= 1
                elif event.key == pygame.K_RIGHT:
                    # Move right in the bracket
                    prev_bracket = selected_bracket
                    selected_bracket += 1
                
                Bracket.update_current_bracket(prev_bracket, selected_bracket)
                current_bracket = Bracket.current_bracket

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
    
    pygame.display.flip()
    # except:
    #     output_last_filenames()

print("what")
