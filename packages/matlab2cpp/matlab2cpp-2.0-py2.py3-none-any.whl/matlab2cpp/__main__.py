#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Main executable binding parser together with transpiler."""
try:
    import argcomplete
except ImportError:
    argcomplete = None

from .parser import create_parser


def main(args=None):
    """
    Execute main parser.

    Args:
        args (Optional[List[str]]):
            Argument to be parsed. If omitted, use ``sys.args``.
    """
    parser = create_parser()
    if argcomplete is not None:
        argcomplete.autocomplete(parser)

    args = parser.parse_args(args)

    from matlab2cpp.frontend import execute_parser
    execute_parser(args)


if __name__ == "__main__":
    main()
