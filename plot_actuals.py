import normfit
import races
from scipy import asarray as ar
import scipy.stats
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

def plot_race(race, label, fn):
    time_secs = [normfit.time_to_seconds(t) for t in race["times"]]
    ts_arr = ar(time_secs)
    n = fn(*fn.fit(ts_arr))
    fig, ax = plt.subplots(1,1)
    ax.xaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: (datetime.datetime.min + datetime.timedelta(seconds=x)).strftime("%H:%M:%S")))
    ax.plot(ts_arr, n.pdf(ts_arr), 'k-', lw=2, alpha=0.6, label='norm pdf')
    ax.hist(ts_arr, density=True, alpha=0.2)
    ax.legend(loc='best', frameon=False)
    plt.title(label)
    plt.show()

if __name__ == "__main__":
    for r in range(len(races.races)):
        plot_race(races.races[r], "Race " + str(r+1), scipy.stats.skewnorm)
