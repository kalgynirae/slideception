# slideception

A Python library for creating interactive presentations in Linux terminals.

## Requirements

* Python 3.8 or newer
* Linux (unless you avoid the Linux-specific stuff)

## Usage

Here's a quick example:

```python3
#!/usr/bin/env python3
from slideception import display_slides, ipython, slide

@slide
def context_managers():
    """Context Managers

    A **context manager** is a thing that can be used in a `with` block.

    ```python3
    with record_time() as timer:
        stuff()
    print(f"stuff took {timer.elapsed} seconds")
    ```

    It lets you factor out pieces of code that *surround* other code.
    """
    # Now jump into an intepreter for a quick demo
    ipython()


display_slides()
```

### Presentation Boilerplate

At a minimum, you'll need to import `display_slides` and `slide` and call
`display_slides()` at the bottom of your script.

```python3
#!/usr/bin/env python3
from slideception import display_slides, slide

…

display_slides()
```

### Defining Slides

**@slide**

This decorator registers a function as a slide. The docstring of the function
becomes the slide's content, and the body of the function is executed after the
content is displayed. The docstring is parsed as CommonMark and then rendered
for display in a terminal.

### Helpers

*   **bash(*history=None, init=None*)**

    This function starts a Bash shell which can be used to demo shell scripting
    and command-line programs.

    The `history` parameter accepts a list of commands which will be preloaded
    into the shell's history; this lets you simply press **Up** to recall those
    commands instead of typing them from scratch.

    The `init` parameter accepts a list of commands which will be executed
    after the shell loads your `.bashrc` file. This can be used to `cd` to a
    specific directory, create files, etc.

*   **ipython()**

    This function starts an iPython interpreter which can be used to demo Python
    code.

*   **python()**

    This function starts a Python interpreter which can be used to demo Python
    code. You should definitely prefer to use `ipython()` if possible.
