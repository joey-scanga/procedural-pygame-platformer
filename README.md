# A basic example of platformer physics using pygame and pymunk!

[![Demo](https://github.com/joey-scanga/procedural-pygame-platformer/blob/main/demo.gif)

Also contains some basic level generation using a simple [random walk](https://en.wikipedia.org/wiki/Random_walk) variation, where there are a few "drunk walkers"
at different parts of the map.

If there are any contributions, ideas, or thoughts you'd like to add to this 
project, please don't hesitate to make an issue or pull request and I'll take
a look at it. 

To run:

```
git clone https://www.github.com/joey-scanga/procedural-pygame-platformer
cd procedural-pygame-platformer
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cd src/
python3 game.py
```

Controls:

```
L/R arrow keys: move
Spacebar: jump
R: respawn from top of map
Enter: regenerate map
```




