import argparse, pathlib, sys
from .lexer import Lexer
from .parser import Parser
from .runtime import Interpreter
from .errors import FarxError

def main(argv=None):
    p=argparse.ArgumentParser(prog="farx",description="FARX NEXUS interpreter")
    p.add_argument("file",help="Path to .farx source file")
    args=p.parse_args(argv)
    path=pathlib.Path(args.file)
    try:
        source=path.read_text(encoding="utf-8")
        program=Parser(Lexer(source).tokens()).parse()
        Interpreter().run(program)
        return 0
    except (OSError,FarxError) as e:
        print(f"FARX ERROR: {e}",file=sys.stderr)
        return 1
