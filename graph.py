import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
import util

def graph(races, ranks, startval=0, title="Ranks", exclude=[], output_file=None):
    mpl.style.use('bmh')
    mpl.rcParams['axes.prop_cycle'] = cycler(linestyle=['-', '--', '-.']) * mpl.rcParams['axes.prop_cycle']
    plt.figure(figsize=(19,10))
    for player in [x[1] for x in util.byscore(ranks[-1]) if x[1] not in exclude]:
        x = range(len(ranks))
        y = [r.get(player, startval) for r in ranks]
        plt.plot(x, y, label=player)
    plt.legend()
    plt.title(title)
    if output_file is None:
        plt.show()
    else:
        plt.savefig(output_file)
