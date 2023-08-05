import curses
import time


def run(init, update, view, rate=None, quit_when=None, final_view=None):
    '''(State, (String, State) -> State, (State, Int, Int) -> String, Int) -> None

    Helper inspired by The Elm Architecture for running simple terminal applications.
    `init` is the initial state of the application.
    `update` is a transition function from the current state
        to the next state when given an input character.
    `view` returns the string that should be printed for the current state of the application
        given the width and height of the curses window.
    `rate` is the number of times per second 'TICK` will be provided to update. By default,
        `rate` is none, and the application will block on input. If `rate` is provided,
        the application will not block on input.

    For example, a simple counter application might look like:

    def update(key, state):
        return state + 1
    
    def view(state, width, height):
        return 'The current number is: {}'.format(state)

    if __name__ == '__main__':
        run(0, update, view)
    '''

    def helper(stdscr):
        state = init
        y, x = stdscr.getmaxyx()
        stdscr.addstr(0, 0, view(state, x, y))
        if not (rate is None):
            stdscr.nodelay(1)
            wait = 1 / rate
            previous_tick = time.time()
        while True:
            if quit_when is not None and quit_when(state):
                if final_view is not None:
                    stdscr.addstr(0, 0, final_view(state, x, y))
                else:
                    stdscr.addstr(0, 0, view(state, x, y))
                stdscr.getkey()
            else:
                if not (rate is None) and time.time() - previous_tick > wait:
                    previous_tick = time.time()
                    state = update('TICK', state)
                    y, x = stdscr.getmaxyx()
                    stdscr.addstr(0, 0, view(state, x, y))
                try:
                    key = stdscr.getkey()
                except KeyboardInterrupt:
                    return
                except:
                    pass
                else:
                    stdscr.clear()
                    state = update(key, state)
                    y, x = stdscr.getmaxyx()
                    stdscr.addstr(0, 0, view(state, x, y))

    curses.wrapper(helper)
