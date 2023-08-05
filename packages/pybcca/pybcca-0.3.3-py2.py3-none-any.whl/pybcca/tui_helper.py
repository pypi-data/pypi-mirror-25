from threading import Thread
from queue import Queue
import curses
import time


def listen_to_ticks(rate, input_queue):
    if rate is not None:
        while True:
            input_queue.put('TICK')
            time.sleep(1 / rate)


def listen_to_keys(input_queue, get_input):
    while True:
        try:
            input_queue.put(get_input())
        except curses.error:
            pass
        finally:
            time.sleep(.1)


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
        def clear_and_draw(s):
            stdscr.clear()
            stdscr.addstr(0, 0, s)

        y, x = stdscr.getmaxyx()
        stdscr.nodelay(1)

        input_queue = Queue()

        Thread(
            target=listen_to_ticks, args=(rate, input_queue),
            daemon=True).start()
        Thread(
            target=listen_to_keys,
            args=(input_queue, stdscr.getkey),
            daemon=True).start()

        state = init
        while True:
            clear_and_draw(view(state, x, y))
            state = update(input_queue.get(), state)
            if quit_when is not None and quit_when(state):
                break
        if final_view is not None:
            clear_and_draw(final_view(state, x, y))

    try:
        curses.wrapper(helper)
    except KeyboardInterrupt:
        return
