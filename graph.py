import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
import util

def filter_intermediate_flatlines(x, y):
    new_y = [y[0]]
    new_x = [x[0]]
    before_y = y[0]
    for i in range(1, len(y)-1):
        if y[i] == before_y:
            continue
        else:
            new_x.append(x[i])
            new_y.append(y[i])
            before_y = y[i]
    new_x.append(x[-1])
    new_y.append(y[-1])
    return (new_x, new_y)

def graph(races, ranks, startval=0, title="Ranks", exclude=[], output_file=None):
    mpl.style.use('bmh')
    mpl.rcParams['axes.prop_cycle'] = cycler(linestyle=['-', '--', '-.']) * mpl.rcParams['axes.prop_cycle']
    plt.figure(figsize=(19,10))
    for player in [x[1] for x in util.byscore(ranks[-1]) if x[1] not in exclude]:
        y = [ranks[r].get(player, startval) for r in range(len(ranks)) if r == 0 or not races[r-1].get("incomplete", False) or player in util.finishers(races[r-1]) or player in races[r-1]["forfeits"]]
        x = range(len(y))
        (x, y) = filter_intermediate_flatlines(x,y)
        plt.plot(x, y, label=player, lw=1.5)
    plt.legend(loc='best', frameon=False)
    plt.title(title)
    if output_file is None:
        plt.show()
    else:
        plt.savefig(output_file)
