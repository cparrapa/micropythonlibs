import os
files = os.listdir()
for file in files:
    try:
        os.remove(file)
    except OSError:
        pass
