import sys
from argparse import ArgumentParser

from cowsay import cowsay, list_cows


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-e", default="oo", help="Select the appearance of the "\
         "cow's eyes,", type=str)
    parser.add_argument("-f", default="default", help="Specifies a particular "\
         "cow picture file ('cowfile') to use", type=str)
    parser.add_argument("-l", action="store_true", help="If it is specified, "\
         "list all cowfiles on the current COWPATH")
    parser.add_argument("-n", action="store_false", help="If it is specified, "\
         "the given message will not be word-wrapped")
    parser.add_argument("-T", default="", help="Tongue string, "\
         "it must be two characters and does not appear by default", type=str)
    parser.add_argument("-W", default=40, help="Where the message should be "\
         "wrapped", type=int)

    parser.add_argument("-b", action="store_true", help="")
    parser.add_argument("-d", action="store_true", help="")
    parser.add_argument("-g", action="store_true", help="")
    parser.add_argument("-p", action="store_true", help="")
    parser.add_argument("-s", action="store_true", help="")
    parser.add_argument("-t", action="store_true", help="")
    parser.add_argument("-w", action="store_true", help="")
    parser.add_argument("-y", action="store_true", help="")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    message = None

    if args.l:
        message = list_cows()
    else:
        rows = [row.strip() for row in sys.stdin]

        for val in "bdgpstwy":
            preset = getattr(args, val, None)
            if preset is not None:
                preset = val
                break

        message = cowsay(
             message="\n".join(rows),
             cow=args.f,
             preset=preset,
             eyes=args.e[:2],
             tongue=args.T,
             width=args.W,
             wrap_text=args.n,
        )

    print(message, file=sys.stdout)
