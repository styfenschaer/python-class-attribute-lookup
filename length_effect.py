import pathlib
import timeit
from time import perf_counter_ns

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

LOG_LENGTHS = range(11)
NUMBER = 100_000
REPEAT = 20

ROOT = pathlib.Path('themes')
# THEME = 'light.mplstyle'
# THEME = 'dark.mplstyle'
# THEME = 'light_notex.mplstyle'
THEME = 'dark_notex.mplstyle'
BOX_FACECOLOR = '#BB86FC' 
# BOX_FACECOLOR = 'lightblue' 
SAVEFIG = False
FILENAME = 'boxplot_attrlen_vs_lookuptime.png'


def eval_lookup_time(num_chars):
    class MyBlog:
        ...

    attr_name = 'a' * num_chars
    setattr(MyBlog, attr_name, None)
    stmt = f'MyBlog.{attr_name}'

    timings = timeit.repeat(stmt, timer=perf_counter_ns,
                            repeat=REPEAT, number=NUMBER,
                            globals=dict(MyBlog=MyBlog))

    return np.asarray(timings) / NUMBER


def main():
    lenghts = [2**exp for exp in LOG_LENGTHS]
    recordings = [eval_lookup_time(l) for l in lenghts]
    labels = [r'$2^{{{}}}$'.format(i) for i in LOG_LENGTHS]

    with plt.style.context(ROOT / THEME):
        fig, ax = plt.subplots(1, 1)
        bplot = ax.boxplot(recordings, labels=labels)

        for i, patch in enumerate(bplot['boxes']):
            patch.set_facecolor(BOX_FACECOLOR)

            if i % 2 != 0:
                box = [Rectangle((i+0.5, 0), 1, 1e4)]
                pc = PatchCollection(box, alpha=0.1)
                ax.add_collection(pc)

        ax.set_xlim(0.5, len(recordings)+0.5)
        ax.set_xlabel('number of characters')
        ax.set_ylabel('lookup time [ns]')

        if SAVEFIG:
            plt.savefig(FILENAME)
        plt.show()


if __name__ == '__main__':
    main()
