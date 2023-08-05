# pybcca
Python package for Base Camp Coding Academy helpers

## tui_helper

Pybcca provides a helper function for creating interactive terminal applications.
Is located in the tui_helper module, and can be imported like this:

```python
from pybcca.tui_helper import run
```

`run` has a fairly simple interface. It has four parameters:

```python
def run(init, update, view, rate=None):
```

- `init` is the initial state of the application fun
- `update` is the main transation function for the application. It has two parameters, `key` and `state`, and it returns the next state of the application. `key` will either be the key entered by the user (i.e. `'KEY_UP`, `'a'`, `'r'`) or `'TICK'`. `'TICK'` is only provided on the clock ticks determined by `rate`.
- `view` is a function from the current state to the string that should be used to show it. It has three parameters: `state`, `width`, and `height`.
- `rate` is an optional parameter that specifies the number of times you want the program to "tick" per second. By default, the rate is `None` and the application will
block while waiting for user input.

Press `ctrl+c` to quit a running application.

### Example Application: Count The Spaces

For this application, we just want to show the how many times the user has pressed the space bar. Since we are just counting we can just use an integer for our state, and that integer can start at 0.

So far, we would have a program that looks like this:

```python
from pybcca.tui_helper import run

if __name__ == '__main__':
    run(0, ???, ???)
```

We still need to decide how to update and how to view our application. Let's look at our update function first. If the user presses the spacebar, we want our count to go up, otherwise, our count should stay the same. With this in mind, we can write our update function and end up with something like this:

```python
from pybcca.tui_helper import run

def update(key, state):
    if key == ' ':
        return state + 1
    else:
        return state

if __name__ == '__main__':
    run(0, update, ???)
```

Now, the only thing remaining is the view for our application. We can successfully count spaces, but we don't have a way of viewing the count. Let's show the user
a message like `You have currently entered ??? spaces`. That function is simple enough to write, and we end up with a final program like this:

```python
from pybcca.tui_helper import run

def update(key, state):
    if key == ' ':
        return state + 1
    else:
        return state

def view(state, height, width):
    return 'You have currently entered {} spaces'.format(state)

if __name__ == '__main__':
    run(0, update, view)
```

