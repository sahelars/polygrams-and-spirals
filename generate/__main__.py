import argparse
import matplotlib.pyplot as plt
from .calculations import plot_star_polygon, plot_logarithmic_spiral
from time import time

parser = argparse.ArgumentParser(
    description="Generate regular star polygons and corresponding logarithmic spirals"
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "--polygrams", action="store_true", help="plot regular star polygons"
)
group.add_argument("--spirals", action="store_true", help="plot spirals")
parser.add_argument(
    "n",
    type=int,
    nargs="?",
    default=30,
    help="number for total configurations",
)
args = parser.parse_args()

if args.n <= 0:
    parser.error("number must be greater than 0")

length = args.n + 4

polygrams = args.polygrams
spirals = args.spirals

configs = []
for n in range(5, length + 1):
    step = 2
    configs.append((n, step))

num_plots = len(configs)
rows = (num_plots + 5) // 6
fig = plt.figure(figsize=(18, 3 * rows), dpi=300)

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
    name = "Polygrams"
    file = "regular_star_polygons.png"
elif spirals:
    name = "Spirals"
    file = "logarithmic_spirals.png"

timestamp = int(time())
plt.tight_layout()
plt.savefig(f"generate/renders/{timestamp}_{file}", dpi=300)
plt.close()

print(f"\n✨ {name} diagram saved to generate/renders/{file} 💫\n")
