# NoClip
"a relatively simple game engine made because pygame is lowk mid"

## Main Ideas
Everything you create is called a `thing`. The container for a bunch of `thing` is also just a `thing`, in other words the so called [scene](https://docs.godotengine.org/en/stable/getting_started/step_by_step/nodes_and_scenes.html) idea from Godot is also just a `thing` here.

## Main Features
### `thing` class
everything you create is a thing, so we call it a `thing`. each `thing` stores its _name_, _x_, _y_, _shape (or simply image if you prefer)_,  _width_, _height_, and _children_, _update_, _timer_

while most stuff about `thing` will sound intuitive `children` and `update` and `timer` may need more explanation.
#### `children`
`children` variable is a variable that stores a `thing`'s child `thing` inside itself. This allows clean nested structures.
#### `update`
`update` variable is a variable that stores a function that runs every tick of the game for the `thing`. This also makes the code cleaner to write
#### `timer`
`timer` variable is interesting, its a dictionary that stores multiple timers. In reality a timer is really nothing but a integer but it helps for things like doing things after certain time interval without blocking the game loop.
