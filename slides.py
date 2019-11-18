#!/usr/bin/env python3
from __future__ import annotations

import inspect
import os.path
import sys
import time
from contextlib import contextmanager
from inspect import getdoc
from pathlib import Path
from shutil import get_terminal_size
from subprocess import PIPE, run
from typing import cast

from boxing import boxing
from IPython import start_ipython
from mistletoe import markdown
from mistletoe.base_renderer import BaseRenderer
from pygments import highlight
from pygments.formatters import TerminalTrueColorFormatter
from pygments.lexers import Python3Lexer, get_lexer_by_name
from pygments.style import Style
from pygments.token import Token
from traitlets.config import Config

FILE = sys.argv[0]
NAME = os.path.basename(FILE)
WIDTH, _ = get_terminal_size()

config = Config()
config.TerminalInteractiveShell.confirm_exit = False
config.TerminalIPythonApp.display_banner = False


def bash() -> None:
    run(["bash", "-i"])


def ipython(locals=None, /) -> None:
    start_ipython(config=config, user_ns=locals)


def wait() -> None:
    try:
        input("\x1b[30m>\x1b[0m ")
    except EOFError:
        pass


class Kalgykai(Style):
    styles = {
        Token.Comment: "#6b6d68",
        Token.Comment.Hashbang: "italic #c8742a",
        Token.Keyword: "bold #c81f1f",
        Token.Keyword.Constant: "nobold #06989a",
        Token.Name.Decorator: "#4e9a06",
        Token.Name.Function: "#4e9a06",
        Token.Name.Variable: "#4e9a06",
        Token.Number: "#386cb0",
        Token.Operator.Word: "#c81f1f",
        Token.String: "#c4a800",
        Token.String.Interpol: "italic #c8742a",
        Token.String.Escape: "italic #c81f1f",
    }


class TerminalRenderer(BaseRenderer):
    def render_strong(self, token):
        return f"\x1b[1m{self.render_inner(token)}\x1b[22m"

    def render_emphasis(self, token):
        return f"\x1b[3m{self.render_inner(token)}\x1b[23m"

    def render_inline_code(self, token):
        return f"\x1b[33m{self.render_inner(token)}\x1b[39m".format(
            self.render_inner(token)
        )

    def render_raw_text(self, token, escape=True):
        return token.content

    def render_strikethrough(self, token):
        return f"\x1b[9m{self.render_inner(token)}\x1b[29m"

    def render_image(self, token):
        return f"[{token.src}]"

    def render_link(self, token):
        return f"\x1b[34;4m\x1b]8;;{token.target}\x1b\\{self.render_inner(token)}\x1b]8;;\x1b\\\x1b[39;24m"

    def render_auto_link(self, token):
        return f"\x1b[34;4m{token.target}\x1b[39;24m"

    def render_escape_sequence(self, token):
        return self.render_inner(token)

    def render_heading(self, token):
        if token.level == 1:
            return f"\n\x1b[1m{self.render_inner(token):^{WIDTH}}\x1b[22m\n\n"
        elif token.level == 2:
            return f"\x1b[35;1m{self.render_inner(token)}\x1b[39;22m\n\n"

    def render_quote(self, token):
        return f"\x1b[90m{self.render_inner(token)}\x1b[99m"

    def render_paragraph(self, token):
        return f"{self.render_inner(token)}\n\n"

    def render_block_code(self, token):
        code = self.render_inner(token)
        if token.language:
            lexer = get_lexer_by_name(token.language)
            formatter = TerminalTrueColorFormatter(style=Kalgykai)
            code = highlight(code, lexer, formatter)
        return boxing(code, style="double-single", padding=0).lstrip("\n") + "\n"

    def render_list(self, token):
        return f"{self.render_inner(token)}\n"

    def render_list_item(self, token):
        inner = self.render_inner(token).rstrip("\n")
        return f"  • {inner}\n"

    def render_table(self, token):
        return self.render_inner(token)

    def render_table_row(self, token):
        return self.render_inner(token)

    def render_table_cell(self, token):
        return self.render_inner(token)

    @staticmethod
    def render_thematic_break(token):
        return "\\hrulefill\n"

    @staticmethod
    def render_line_break(token):
        return "\n" if token.soft else "\\newline\n"

    def render_document(self, token):
        return self.render_inner(token)


def format_slide(content: str) -> str:
    return markdown(content, TerminalRenderer)


slides = []


def slide(func) -> None:
    docstring = getdoc(func)
    assert docstring is not None
    content = format_slide("# " + docstring)
    slides.append((content, func))
    return func


@contextmanager
def flair():
    print("Slides START!!")
    try:
        yield
    except KeyboardInterrupt:
        print()
        print("Slides CANCEL!!!")
    except Exception:
        print("Slides FAIL!!!")
        raise
    else:
        print("Slides END!!!")


def display_slides() -> None:
    for n, (content, func) in enumerate(slides, start=1):
        run(["clear", "-x"])
        slidename = f"{NAME}.{func.__name__}"
        progress = f"[{n}/{len(slides)}]"
        print(f"\x1b[30m{slidename:<{WIDTH - 10}}{progress:>10}\x1b[0m")
        print(content, end="")
        start = time.monotonic()
        func()
        if time.monotonic() - start < 0.5:
            wait()


