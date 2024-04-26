import pygame

BLACK = (0, 0, 0)
SELECT = (0, 235, 235)

class Bracket():

    # ----- Class Code -----

    # Default bracket width & height
    width = None
    height = None
    weight = 3

    brackets = []
    round_quants = {}
    round_brackets = {}

    def set_default_size(screen_width, screen_height, n_competitors, rounds):
        Bracket.width = int(screen_width/n_competitors*2)
        # TODO: dynamically set height
        Bracket.height = int(screen_height/rounds/2)

    def get_total_brackets(n_competitors, round=0):
        while n_competitors > 0:
            Bracket.round_quants[round + 1] = n_competitors
            Bracket.round_brackets[round + 1] = []
            brackets_so_far, round = Bracket.get_total_brackets(n_competitors//2, round + 1)
            return n_competitors + brackets_so_far, round
        return 0, round

    def create_brackets(n_competitors, total_brackets, screen_height):
        y = 0
        upways = True

        bracket_tracker = 0  #keeps track of how many brackets seen in round so far
        half_bracket_tracker = 0  #keeps track of brackets, resets every half
        num_brackets_per_round_summed = n_competitors  #increases each round by new round num of competitors
        round_competitors = n_competitors  #decreases each round to match round's num of competitors
        round_tracker = 0   #keeps track of which round we're on, starts at 0
        width = Bracket.width
        for i in range(1, total_brackets):
            # Start a new round of brackets
            if i > num_brackets_per_round_summed:
                num_brackets_per_round_summed += round_competitors // 2
                round_competitors = round_competitors // 2
                bracket_tracker = 0
                half_bracket_tracker = 0
                round_tracker += 1
                y = Bracket.height * round_tracker
                upways = True
                width *= 2

            # Reached halfway point of brackets
            if bracket_tracker >= round_competitors // 2 and upways:
                half_bracket_tracker = 0
                y = screen_height - Bracket.height * (round_tracker + 1)
                upways = False
            
            new_bracket = Bracket(half_bracket_tracker * width, y, width, Bracket.height, upways)
            Bracket.brackets.append(new_bracket)
            Bracket.round_brackets[round_tracker + 1].append(new_bracket)
            bracket_tracker += 1
            half_bracket_tracker += 1

    def set_next_brackets(rounds):
        for round_i in range(1, rounds - 1):
            for bracket_i in range(len(Bracket.round_brackets[round_i])):
                current_bracket = Bracket.round_brackets[round_i][bracket_i]
                next_bracket = Bracket.round_brackets[round_i + 1][bracket_i // 2]
                current_bracket.set_next_bracket(next_bracket)

    def initialize_brackets(n_competitors, screen_width, screen_height):
        total_brackets, rounds = Bracket.get_total_brackets(n_competitors)
        Bracket.set_default_size(screen_width, screen_height, n_competitors, rounds)
        Bracket.create_brackets(n_competitors, total_brackets, screen_height)
        Bracket.set_next_brackets(rounds)

    def set_bracket_memes(memes, filenames):
        i = 0
        for meme_i in range(0, len(memes), 2):
            Bracket.brackets[meme_i//2].set_memes(memes[meme_i], memes[meme_i + 1])
            Bracket.brackets[meme_i//2].set_filenames(filenames[meme_i], filenames[meme_i + 1])

        
    def draw_brackets(surface):
        for bracket in Bracket.brackets:
            bracket.draw(surface)

    def update_current_bracket(previous_index, selected_index):
        # TODO: error correction for going out of bracket range
        Bracket.brackets[previous_index].selected = False
        Bracket.brackets[selected_index].selected = True
        Bracket.current_bracket = Bracket.brackets[selected_index]

    # ----- Instance Code ----- 

    def __init__(self, x, y, width, height, upways):
        self.meme1 = None
        self.meme2 = None
        self.meme1_fn = None
        self.meme2_fn = None

        self.selected = False

        self.x = x
        self.y = y
        self.w = width
        self.h = height

        self.weight = Bracket.weight
        self.upways = upways

        self.set_rect()
    
    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def set_next_bracket(self, next_bracket):
        self.next_bracket = next_bracket

    def set_memes(self, meme1, meme2):
        self.meme1 = meme1
        self.meme2 = meme2

    def set_filenames(self, fn1, fn2):
        self.meme1_fn = fn1
        self.meme2_fn = fn2


    def draw(self, surface):
        if self.upways:
            line1 = [self.x + self.w * .25, self.y, self.x + self.w * .25, self.y + self.h * .5]
            line2 = [self.x + self.w * .75, self.y, self.x + self.w * .75, self.y + self.h * .5]
            line3 = [self.x + self.w * .25, self.y + self.h * .5, self.x + self.w * .75, self.y + self.h * .5]
            line4 = [self.x + self.w * .5, self.y + self.h * .5, self.x + self.w * .5, self.y + self.h]

            self.meme1_pos = (self.x, self.y)
            self.meme2_pos = (self.x + self.w * .5, self.y)
        else:
            line1 = [self.x + self.w * .25, self.y + self.h * .5, self.x + self.w * .25, self.y + self.h]
            line2 = [self.x + self.w * .75, self.y + self.h * .5, self.x + self.w * .75, self.y + self.h]
            line3 = [self.x + self.w * .25, self.y + self.h * .5, self.x + self.w * .75, self.y + self.h * .5]
            line4 = [self.x + self.w * .5, self.y, self.x + self.w * .5, self.y + self.h * .5]

            self.meme1_pos = (self.x, self.y)
            self.meme2_pos = (self.x + self.w * .5, self.y)

        pygame.draw.line(surface, BLACK, [line1[0], line1[1]], [line1[2], line1[3]], self.weight)
        pygame.draw.line(surface, BLACK, [line2[0], line2[1]], [line2[2], line2[3]], self.weight)
        pygame.draw.line(surface, BLACK, [line3[0], line3[1]], [line3[2], line3[3]], self.weight)
        pygame.draw.line(surface, BLACK, [line4[0], line4[1]], [line4[2], line4[3]], self.weight)

        if self.meme1 != None:
            meme1 = self.meme1
            meme1 = pygame.transform.scale(meme1, (self.w/2, self.h))
            surface.blit(meme1, self.meme1_pos)

        if self.meme2 != None:
            meme2 = self.meme2
            meme2 = pygame.transform.scale(meme2, (self.w/2, self.h))
            surface.blit(meme2, self.meme2_pos)

        if self.selected:
            pygame.draw.rect(surface, SELECT, self.rect, Bracket.weight)

    