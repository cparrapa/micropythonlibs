# boot.py v0.1.1 18.5.26 new app
import update_library
import os
import json

def initialize_lock_file():
    try:
        os.stat('lock.json')
        return
    except OSError:
        pass

    try:
        from lock_data import DATA
        with open('lock.json', 'w') as f:
            json.dump(DATA, f)
    except ImportError:
        pass
    except Exception:
        pass


initialize_lock_file()

manager = update_library.UpdateLibraryManager()
if manager.should_update():
    try:
        manager.update()
    except Exception:
        manager.cleanup(False)