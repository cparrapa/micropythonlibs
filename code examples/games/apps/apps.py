# apps.py — List your apps here (label, module_name)
# Each module must expose:  def run(shared_i2c): ...  and handle long-press to exit.

APPS_CONFIG = [
    ("Calculator",     "calculator"),
    ("TVM Calculator",     "tvm"),
    ("Snake",     "game1"),
    ("Space Invaders",     "game2"),
]

# Tip: To add a new app, create myapp.py with a run(shared_i2c) function,
# then append ("My App Name", "myapp") here. Done.
