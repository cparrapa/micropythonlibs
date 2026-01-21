import update_library

manager = update_library.UpdateLibraryManager()
if manager.should_update():
    try:
        manager.update()
    except Exception:
        manager.cleanup(False)
