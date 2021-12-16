import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
import util

def graph(races, ranks, startval=0, title="Ranks", exclude=[], output_file=None):
    mpl.style.use('bmh')
    mpl.rcParams['axes.prop_cycle'] = cycler(linestyle=['-', '--', '-.']) * mpl.rcParams['axes.prop_cycle']
    plt.figure(figsize=(19,10))
    for player in [x[1] for x in util.byscore(ranks[-1]) if x[1] not in exclude]:
        y = [ranks[r].get(player, startval) for r in range(len(ranks)) if r == 0 or not races[r-1].get("incomplete", False) or player in util.finishers(races[r-1]) or player in races[r-1]["forfeits"]]
        x = range(len(y))
        plt.plot(x, y, label=player, lw=1.5)
    plt.legend(loc='best', frameon=False)
    plt.title(title)
    if output_file is None:
        plt.show()
    else:
        plt.savefig(output_file)
