import pygame
from inspect import signature
from time import sleep, clock
from datetime import datetime

# ADJUSTABLE VALUES ------------------------
fps_polling_interval = 0.3
logging_level = 0
# ------------------------------------------

_pr_framerate_cap = 60
_pr_frame_interval = 1 / _pr_framerate_cap

capped_framerate = _pr_framerate_cap
potential_framerate = 0
delta_time = 0
_function_pool = {"setup":[], "draw": [], "event":[]}

def log(msg, level):
    """
    Simple logging function.
    """
    
    if logging_level > level: return
    timestamp = datetime.now().strftime("%H:%M:%S")
    if level is 0: # trace
        print(f"[{timestamp}] TRACE: {msg}")
    if level is 1: # info
        print(f"[{timestamp}] INFO: {msg}")
    if level is 2: # warning
        print(f"[{timestamp}] WARN: {msg}")
    if level is 3: # error
        print(f"[{timestamp}] ERROR: {msg}")
        
def prioritySort(e): return e[1]
def pool(name, priority):
    """
    Adds a function to the given function pool.

    The setup pool runs at the start of the application.
    The event pool runs each frame when the event list is not empty.
    The draw pool runs every frame after the event pool.

    The priority changes the order in which the functions are executed.
    
    Functions part of the setup and draw pools do not take any arguments,
    functions part of the event pool take 1 argument containing the event
    list.
    """
    global _function_pool
    def wrapper(f):
        params = len(signature(f).parameters)
        if not name in _function_pool: raise Exception(f"Pool {name} doesn't exist.")
        if name == "event":
            if params != 1: 
                log(f"Failed to add function '{f.__name__}()' to {name} pool; {name} functions should take exactly 1 argument. (raised by kernel.pool.wrapper)", 3)
                raise Exception(f"Functions in pool {name} take 1 argument.")
        else:    
            if params != 0: 
                log(f"Failed to add function '{f.__name__}()' to {name} pool; {name} functions should take 0 arguments. (raised by kernel.pool.wrapper)", 3)
                raise Exception(f"Functions in pool {name} should take 0 arguments.")
        _function_pool[name].append((f, priority))
        _function_pool[name].sort(key=prioritySort)
        log(f"Added function '{f.__name__}()' to the {name} pool.",0)
        return f
    return wrapper
def run():
    """
    Starts the kernel loop.
    This function should be called at the end of your main script.
    """
    global potential_framerate, capped_framerate, delta_time
    
    running = True
    time_since_fps_poll = 0
    
    log("Running setup pool...", 0)
    for f in _function_pool["setup"]: f[0]()

    log("Started kernel loop.", 1)
    while running:
        t0 = clock()
        
        e = pygame.event.get()
        if len(e) > 0:
            for event in e:
                if event.type == pygame.QUIT: running = False
            
            for f in _function_pool["event"]: f[0](e)
        
        for f in _function_pool["draw"]: f[0]()
        
        pygame.display.flip()

        t1 = clock()

        delta_time = t1 - t0
        inv_delta_time = 1 / delta_time

        if delta_time < _pr_frame_interval: 
            sleep(_pr_frame_interval - delta_time)
            time_since_fps_poll += _pr_frame_interval
        else: time_since_fps_poll += delta_time

        # Framerate Updates
        if time_since_fps_poll > fps_polling_interval:
            time_since_fps_poll = 0
            if delta_time < _pr_frame_interval:
                capped_framerate = _pr_framerate_cap
                
            else: capped_framerate = inv_delta_time

            potential_framerate = inv_delta_time

    
    pygame.quit()
