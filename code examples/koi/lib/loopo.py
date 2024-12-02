import atexit
import time

__version__ = "1.0.0"
class LOOPO:
    # Dictionary to hold generator objects and their wake-up times
    tasks = {}
    wake_times = {}  # Store wake-up times for tasks
    
    @staticmethod
    def sleep(duration):
        """Public method that users can call to sleep without using a for loop."""
        wake_time = time.monotonic_ns() + duration * 1000000000
        task_id = id(LOOPO._current_task)
        LOOPO.wake_times[task_id] = wake_time

    @staticmethod
    def setup(fn):
        """Decorator to define a setup function."""
        fn()  # Directly execute the setup function
        return fn

    @staticmethod
    def multitask(fn):
        """Decorator to handle multitasking for both loops and threads."""
        def wrapper():
            while True:
                task_id = id(wrapper)
                if LOOPO.wake_times.get(task_id, 0) <= time.monotonic_ns():
                    fn()
                yield  # Return control after each execution
        gen_obj = wrapper()  # Create the generator object
        gen_obj_id = id(gen_obj)
        LOOPO.tasks[gen_obj_id] = gen_obj
        return fn

    # Using the multitask decorator for both loop and thread definitions
    loop = multitask
    thread = multitask

    @staticmethod
    def run():
        """Start the simulated multitasking loop."""
        while True:
            for gen_obj_id, gen_obj in list(LOOPO.tasks.items()):
                if LOOPO.wake_times.get(gen_obj_id, 0) <= time.monotonic_ns():
                    LOOPO._current_task = gen_obj
                    # Run the next step of the task
                    try:
                        next(gen_obj)
                    except StopIteration:
                        del LOOPO.tasks[gen_obj_id]


sleep = LOOPO.sleep
setup = LOOPO.setup
loop = LOOPO.loop
thread = LOOPO.thread
run = LOOPO.run

atexit.register(LOOPO.run)