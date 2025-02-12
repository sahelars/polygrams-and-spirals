import argparse
import matplotlib.pyplot as plt
from .calculations import plot_star_polygon, plot_logarithmic_spiral
from time import time

parser = argparse.ArgumentParser(
    description="Generate regular star polygons and corresponding logarithmic spirals"
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "--polygrams",
    type=int,
    metavar="N",
    help="plot multiple regular star polygons with N configurations",
)
group.add_argument(
    "--spirals",
    type=int,
    metavar="N",
    help="plot multiple spirals with N configurations",
)
group.add_argument(
    "--polygram",
    type=int,
    metavar="N",
    help="plot a single star polygon with N vertices",
)
group.add_argument(
    "--spiral", type=int, metavar="N", help="plot a single spiral with N vertices"
)
parser.add_argument(
    "--save",
    action="store_true",
    help="save the diagram to the renders folder",
)
args = parser.parse_args()

if args.polygrams and args.polygrams < 6:
    parser.error("number must be 6 or greater")
if args.spirals and args.spirals < 6:
    parser.error("number must be 6 or greater")
if args.polygram and args.polygram < 5:
    parser.error("number must be 5 or greater")
if args.spiral and args.spiral < 5:
    parser.error("number must be 5 or greater")

if args.polygrams:
    length = args.polygrams + 4
elif args.spirals:
    length = args.spirals + 4

polygrams = args.polygrams
spirals = args.spirals
polygram = args.polygram
spiral = args.spiral

if polygrams or spirals:
    configs = []
    for n in range(5, length + 1):
        step = 2
        configs.append((n, step))

    num_plots = len(configs)
    rows = (num_plots + 5) // 6
    dpi = 300 if args.save else 60
    fig = plt.figure(figsize=(18, 3 * rows), dpi=dpi)

    for i, (n, step) in enumerate(configs):
        ax = fig.add_subplot(rows, 6, i + 1)
        if polygrams:
            plot_star_polygon(n, step, ax)
        elif spirals:
            plot_logarithmic_spiral(n, step, ax)
        else:
            parser.print_help()
            parser.exit(1)

    if polygrams:
        name = "Regular Star Polygrams"
        file = "regular_star_polygons.png"
    elif spirals:
        name = "Logarithmic Spirals"
        file = "logarithmic_spirals.png"

    plt.tight_layout()

    if args.save:
        timestamp = int(time())
        plt.savefig(f"generate/renders/{timestamp}_{file}", dpi=300)
        plt.close()

        print(f"\n✨ {name} diagram saved to generate/renders/{timestamp}_{file} 💫\n")
    else:
        plt.gcf().canvas.manager.set_window_title(f"{name}")
        plt.show()

elif polygram or spiral:
    if polygram:
        plot_star_polygon(polygram, 2, plt.gca())
        name = "Regular Star Polygon"
        file = "regular_star_polygon.png"
    elif spiral:
        plot_logarithmic_spiral(spiral, 2, plt.gca())
        name = "Logarithmic Spiral"
        file = "logarithmic_spiral.png"

    plt.tight_layout()

    if args.save:
        timestamp = int(time())
        plt.savefig(f"generate/renders/{timestamp}_{file}", dpi=300)
        plt.close()
        print(f"\n✨ {name} diagram saved to generate/renders/{timestamp}_{file} 💫\n")
    else:
        plt.gcf().canvas.manager.set_window_title(f"{name}")
        plt.show()
