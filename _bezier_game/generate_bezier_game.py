import os
from random import shuffle, sample
import datetime

'''
Bézier Game
by Ryan Bugden
'''


# ======================= EDIT THE FOLLOWING! ======================= #


# Title
school_name = "Typographics"  # Line 1 of title
event_name = "Type Lab 2023"  # Line 2 of title

# I highly encourage you to customize your team name
team_1_name = "TEAM ONE" 
team_2_name = "TEAM TWO"


# ======================= MAYBE EDIT THE FOLLOWING! ======================= #

# Glyphs you're to feature in the game. This influences difficulty.
g_lib = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "?", "!", "@", "$", "%", "&", "(", "}", "~", ";"]

# Decrease the dot radius to increase difficulty (have to be more accurate)
dot_radius = 24  

# Whether or not you want to include the overlaps page with each letter. For this to make sense, the fonts need to be generated with overlaps
overlaps = False  

# For showing what font is on each page (e.g. if a font is poorly drawn or converted to cubic and has too many points, you'll know which to remove from the font folder)
test_mode = True  


# ======================= SHOULDN’T NEED TO EDIT THE FOLLOWING! ======================= #


# page dimensions
w = 2240 
h = 1680

margin_title = 50
margin_name = 20

# Letters
letter_size = 1000
letter_posY = 30
margin_letter = 160

header_font = 'Helvetica'  # Path to font you want to use for headers
header_font_sz = 30  # Header font size

name_font = 'Helvetica-Bold'
name_font_sz = 80

scoreboard_h = 150  # Scoreboard height
scoreboard_ind = 450  # Scoreboard indent

board_stroke_width = 3

path = './_place_fonts_here/'  # Path to the folder with all the fonts you want to plug into the game

g_lib *= 1000
shuffle(g_lib)

def make_blank_page():
    newPage(w,h)
    
    if black_or_white_board == 'white':        
        fill(1) 
    else:
        fill(0)
        
    rect(0,0,w,h)
    
def make_instruction_page():
    instr_sz = 60
    instructions = f'''Welcome to the Bézier Game, a competitive point-plotting game\nin which you must balance accuracy and speed! \n\n\nHere’s how to play:\n
1.\t\tProject upon a {black_or_white_board}board.\n
2.\t\tLine up two teams, single file, on either side of the board.\n
3.\t\tSummon a contestant from each team. Advance the slide.\n
4.\t\tThe first person who’s confident they’ve finished should shout “Done!”,\n\t\t\tat which point both players put down their plotting instruments.\n
5.\t\tReveal the answers on the next slide. If the solution is not perfect, go back\n\t\t\tto the previous slide, resume play, and repeat until there’s a winner.\n
6.\t\tTally the score on the top-right of each side.\n
7.\t\tPlay until the score of your choice.'''
    make_blank_page()
    if black_or_white_board == 'white':        
        fill(0) 
    else:
        fill(1)
    font(header_font)
    fontSize(instr_sz)
    textBox(instructions, (margin_title, margin_title, w - margin_title*2, h - margin_title*2), align="left")
    
def write_team_name(name, pos):
    name = name.upper()
    name_w, name_h = scoreboard_ind - margin_name*2, scoreboard_h - margin_name*2
    
    if black_or_white_board == 'white':        
        name_fill = 0 
    else:
        name_fill = 1
    
    # Figuring out the best font size for the team names
    overflow = "overflow"
    scaled_name_font_size = name_font_sz
    while overflow:
        team_name_fs  = FormattedString()
        team_name_fs.append(name, font=name_font, fontSize=scaled_name_font_size, lineHeight=scaled_name_font_size*0.95, fill=None)
        overflow = textBox(team_name_fs, (w+10, h+10, name_w, name_h), align='left')
        scaled_name_font_size -= 1
    
    
    team_name_fs  = FormattedString()
    team_name_fs.append(name, font=name_font, fontSize=scaled_name_font_size, lineHeight=scaled_name_font_size*0.95, fill=name_fill)
    textBox(team_name_fs, (*pos, name_w, name_h), align='left')
    

def make_game_page():
    make_blank_page()
    
    if black_or_white_board == 'white':        
        stroke(0) 
    else:
        stroke(1)
        
    strokeWidth(board_stroke_width)
    line((w/2,0),(w/2,h))
    
    # Scoreboard
    fill(None)
    rect(-10, h - scoreboard_h, w + 20, scoreboard_h + 10)
    line((scoreboard_ind, h - scoreboard_h), (scoreboard_ind, h))
    line((w/2 + scoreboard_ind, h - scoreboard_h), (w/2 + scoreboard_ind, h))
    font(header_font, header_font_sz)
    
    stroke(None)
    if black_or_white_board == 'white':        
        fill(0) 
    else:
        fill(1)
        
    # Write "SCORE"
    for x in [0, w/2]:
        with savedState():
            score_margin = 25
            translate(75)
            rotate(90, (x + scoreboard_ind, h-scoreboard_h))
            text("SCORE", (x + scoreboard_ind + score_margin, h-scoreboard_h + score_margin), align="left")
    
    # Add the team names
    write_team_name(team_1_name, (margin_name, h-scoreboard_h+margin_name))
    write_team_name(team_2_name, (w/2 + margin_name, h-scoreboard_h+margin_name))
    
   
# Walk the font folder and its subfolders, find any and all fonts
fonts = []
for (dir_path, dir_names, file_names) in os.walk(path):
    for file_name in file_names:
        # Only accepting OTFs, because it’s more likely to only get fonts with sensible cubic point structure
        if file_name.endswith('.otf'):  
            fonts.append(os.path.join(dir_path, file_name))
fonts *= 2
shuffle(fonts)
stages = len(fonts)

for black_or_white_board in ['black', 'white']:
    newDrawing()
    
    # Title page
    make_blank_page()
    with savedState():
        if black_or_white_board == 'white':        
            image("_assets/title_page-white.pdf", (0,0))
            fill(0)
        else:
            image("_assets/title_page.pdf", (0,0))
            fill(1)
        font(header_font, header_font_sz)
        lineHeight(header_font_sz*1.3)
        text(school_name.upper(), (margin_title, margin_title + header_font_sz*1.4), align='left')
        text(event_name.upper(), (margin_title, margin_title), align='left')
        this_year = datetime.date.today().strftime("%Y")
        text(f"© RYAN BUGDEN", (w-margin_title, margin_title), align='right')
    
    # Instruction page
    make_instruction_page()

    # Game pages
    for stage in range(stages):
    
        def draw_game_letters(opacity, dots=False, the_stroke=False):
            game_letter_1 = BezierPath()
            game_letter_2 = BezierPath()
        
            try:
                page_font = fonts[stage]
            except:
                page_font = header_font
        
            if black_or_white_board == 'white':        
                fill(0,0,0,opacity/100) 
            else:
                fill(1,1,1,opacity/100)
        
            # Create letter as BezierPath, and default to header font if there are issues with the chosen font
            try:
                game_letter_1.text(g_lib[stage], (w/4, h/3), align='center', font=fonts[stage], fontSize=letter_size)
                game_letter_2.text(g_lib[stage], (3/4*w, h/3), align='center', font=fonts[stage], fontSize=letter_size)
            except:
                game_letter_1.text(g_lib[stage], (w/4, h/3), align='center', font=header_font, fontSize=letter_size)
                game_letter_2.text(g_lib[stage], (3/4*w, h/3), align='center', font=header_font, fontSize=letter_size)
        
            # Calculate the width and height of the path
            min1x, min1y, max1x, max1y = game_letter_1.bounds()
            min2x, min2y, max2x, max2y = game_letter_2.bounds()
            _1w = max1x - min1x
            _1h = max1y - min1y
            _2w = max2x - min2x
            _2h = max2y - min2y
            vert_marg1_fix = ((h - scoreboard_h) - (min1y+max1y)) / 2
            vert_marg2_fix = ((h - scoreboard_h) - (min2y+max2y)) / 2
            horiz_marg1_fix = ((w/2) - (min1x+max1x)) / 2
            horiz_marg2_fix = ((w/2) - (min2x+max2x)) / 2
            # Calculate the box in which we want to draw the path
            box_width  = (w/2) - (margin_letter * 2)
            box_height = (h - (margin_letter * 2)) - (h/5)
            # Calculate a scale based on the given path bounds and the box
            s1 = min([box_width / float(_1w), box_height / float(_1h)])
            s2 = min([box_width / float(_2w), box_height / float(_2h)])
            new_1radius = dot_radius * (1/s1)
            new_2radius = dot_radius * (1/s2)
        
            if the_stroke == True:
                if black_or_white_board == 'white':        
                    stroke(0) 
                else:
                    stroke(1)
                
            # Set the scale
            with savedState():
                translate(horiz_marg1_fix, vert_marg1_fix)
                scale(s1, center=(w/4, h/2))
                drawPath(game_letter_1)
                if dots == True:
                    for x, y in game_letter_1.onCurvePoints:
                        if black_or_white_board == 'white':        
                            fill(0) 
                        else:
                            fill(1)
                        oval(x-new_1radius, y-new_1radius, new_1radius*2, new_1radius*2)
            
            with savedState():
                translate(horiz_marg1_fix, vert_marg2_fix)
                scale(s2, center=((3/4)*w, h/2))
                drawPath(game_letter_2)
                if dots == True:
                    for x, y in game_letter_2.onCurvePoints:
                        if black_or_white_board == 'white':        
                            fill(0) 
                        else:
                            fill(1)
                        oval(x-new_2radius, y-new_2radius, new_2radius*2, new_2radius*2)
                    
            if test_mode == False:
                font(header_font, header_font_sz)
                if black_or_white_board == 'white':        
                    fill(0) 
                else:
                    fill(1)
                stroke(None)
                tracking(0)
                text(str(fonts[stage]).split("/")[-1], (margin_title, margin_title), align='left')
        
        make_game_page()
        fontSize(100)
        rotate_range = 15
        rotation = randint(-rotate_range, rotate_range)
        mult = 1
        for x in [w/4, 3*w/4]:
            with savedState():
                rotate(mult*rotation, (x, h/2 - scoreboard_h/2))
                text("GET READY!", (x, h/2 - scoreboard_h/2), align="center")
            mult = -1
        make_game_page()
        draw_game_letters(100)
        make_game_page()       
        draw_game_letters(30, dots=True)
    
        # The next two lines represent the game page that calls for teammates to draw overlaps. This is normally not as competitive. It's subjective, so it should be a relaxing way to chill out from the previous slide. It's also a new addition, and not completely necessary.
        if overlaps == True:
            make_game_page()       
            draw_game_letters(0, the_stroke=True)
    
    saveImage(f"_output/Bezier_Game-{black_or_white_board}board.pdf")  
    