# The Bézier Game

The Bézier Game, and educational materials about curves

## How to set up your own game:
1. Save/clone this whole repository.
2. Open `generate_bezier_game.py` in [DrawBot](https://www.drawbot.com/index.html)
3. Set up the title page; change `school_name` and `event_name`
4. Choose your 2 team names; have fun with it!

> *Optional: Change the list of glyphs that might show up in the game. The more obscure or complicated, the more difficult the drawing (usually).*

> *Optional: Decrease the `dot_radius` to increase necessary-accuracy and therefore difficulty.*

5. Drop a bunch of fonts in the folder called `_place_fonts_here`. Be careful to only drop in fonts the drawings of which you trust to be sensible and simple. You don’t want to have to deal with weird point structures! 

> *Note: If you generate the game and there are some glyphs with funky drawings, you can change `test_mode` to `True`, find the problem fonts, remove the files from your folder, and regenerate.*

6. Run the script, and check the `_output` folder for PDFs.

## How to play:
1. Project upon a blackboard or whiteboard. Choose the corresponding PDF.
2. Line up two teams, single file, on either side of the board.
3. Summon a contestant from each team. Advance the slide.
4. The first person who’s confident they’ve finished should shout “Done!” or the keyword of your choice, at which point both players put down their plotting instruments.
5. Reveal the answers on the next slide. If neither solution is perfect, go back to the previous slide, resume play, and repeat until there’s a winner. *Dots must fall within the highlighted circles!*
6. Tally the score on the top-right of each side.
7. Play until the score of your choice. *Suggestion: Roughly the amount of total contestants.*

### — Ryan Bugden