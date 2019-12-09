import pygame
from inspect import signature
from time import sleep, clock

pr_framerate = 60
current_fps = 0
logging_level = 1
def log(msg, level):
    if logging_level > level: return
    if level is 0: # trace
        print(f"TRACE: {msg}")
    if level is 1: # info
        print(f"INFO: {msg}")
    if level is 2: # warning
        print(f"WARN: {msg}")
    if level is 3: # error
        print(f"ERROR: {msg}")
function_pool = {"setup":[], "draw": [], "event":[]}
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
    global function_pool
    def wrapper(f):
        params = len(signature(f).parameters)
        if not name in function_pool: raise Exception(f"Pool {name} doesn't exist.")
        if name == "event":
            if params != 1: raise Exception("Functions in pool {name} take 1 argument.")
        else:    
            if params != 0: raise Exception("Functions in pool {name} take 0 arguments.")
        function_pool[name].append((f, priority))
        function_pool[name].sort(key=prioritySort)
        log(f"Added function '{f.__name__}()' to the {name} pool.",0)
        return f
    return wrapper
def run():
    global current_fps
    for f in function_pool["setup"]: f[0]()
    running = True
    while running:
        t0 = clock()
        e = pygame.event.get()
        if len(e) > 0:
            for event in e:
                if event.type == pygame.QUIT: running = False
        for f in function_pool["event"]: f[0](e)
        for f in function_pool["draw"]: f[0]()
        pygame.display.flip()
        t1 = clock()
        if t1 - t0 < 1./pr_framerate:
            current_fps = pr_framerate
            sleep((1./pr_framerate)-t0+t1)
        else: current_fps = 1./(t1-t0)