from __future__ import absolute_import, division, print_function

import os
import sys
import traceback
from collections import OrderedDict
import numpy as np
import larray as la

from qtpy.QtWidgets import QApplication, QMainWindow
from larray.viewer.view import Figure, FigureCanvas, PlotDialog

__all__ = ['view', 'edit', 'compare', 'REOPEN_LAST_FILE', 'animate', 'animate_barh']


def animate(arr, x_axis=-2, time_axis=-1, repeat=False, interval=200, repeat_delay=None, filepath=None,
            writer='ffmpeg', fps=5, metadata=None, bitrate=None):
    import matplotlib.animation as animation

    if arr.ndim < 2:
        raise ValueError('array should have at least 2 dimensions')

    _app = QApplication.instance()
    if _app is None:
        _app = qapplication()
        parent = None
    else:
        parent = _app.activeWindow()

    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    x_axis = arr.axes[x_axis]
    time_axis = arr.axes[time_axis]
    xdata = np.arange(len(x_axis))
    if arr.ndim == 2:
        arr = arr.expand(la.Axis('dummy', 1))
    arr = arr.transpose(x_axis)
    arr = arr.combine_axes(arr.axes - [time_axis, x_axis], sep=' ')
    initial_data = arr[time_axis.i[0]]
    lines = [ax.plot(xdata, initial_data[row].data, lw=2, label=str(row))[0]
             for row in initial_data.axes[1]]
    # TODO: to stack bars, we need to compute bottom value for each bar (use cumsum(stack_dim))
    # xdata = xdata + 0.5
    # bars = ax.barh(xdata, initial_data[initial_data.axes[1].i[0]].data)

    ax.grid()
    ax.set_ylim(arr.min(), arr.max() * 1.05)
    # set x axis
    ax.set_xlabel(x_axis.name)
    ax.set_xlim(0, len(x_axis) - 1)
    # we need to do that because matplotlib is smart enough to
    # not show all ticks but a selection. However, that selection
    # may include ticks outside the range of x axis
    xticks = [t for t in ax.get_xticks().astype(int) if t <= len(x_axis.labels) - 1]
    xticklabels = [x_axis.labels[j] for j in xticks]
    ax.set_xticklabels(xticklabels)
    ax.legend()
    ax.set_title(str(time_axis.i[0]))

    def run(y):
        data = arr[y].data
        for line, line_data in zip(lines, data.T):
            line.set_data(xdata, line_data)
        ax.set_title(str(y))
        return lines
        # data = arr[y, initial_data.axes[1].i[0]].data
        # for bar, height in zip(bars, data):
        #     bar.set_height(height)
        # ax.set_title(str(y))
        # return bars

    ani = animation.FuncAnimation(fig, run, arr.axes[time_axis], blit=False, interval=interval, repeat=repeat,
                                  repeat_delay=repeat_delay)
    if filepath is None:
        dlg = PlotDialog(canvas, parent)
        if parent:
            dlg.show()
        else:
            dlg.exec_()
    else:
        print("Writing animation to", filepath, '...', end=' ')
        sys.stdout.flush()
        if '.htm' in os.path.splitext(filepath)[1]:
            content = '<html>{}</html>'.format(ani.to_html5_video())
            with open(filepath, mode='w', encoding='utf8') as f:
                f.write(content)
        else:
            Writer = animation.writers[writer]
            writer = Writer(fps=fps, metadata=metadata, bitrate=bitrate)
            ani.save(filepath, writer=writer)
        print("done.")
        return ani


def animate_barh(arr, x_axis=-2, time_axis=-1, title=None, repeat=False, interval=200, repeat_delay=None, filepath=None,
                 writer='ffmpeg', fps=5, metadata=None, bitrate=None):
    import matplotlib.animation as animation

    if arr.ndim < 2:
        raise ValueError('array should have at least 2 dimensions')

    _app = QApplication.instance()
    if _app is None:
        _app = qapplication()
        parent = None
    else:
        parent = _app.activeWindow()

    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    if title is not None:
        # fig.suptitle(title, y=1.05, fontsize=18)
        ax.set_title(title, fontsize=16)

    x_axis = arr.axes[x_axis]
    time_axis = arr.axes[time_axis]
    xdata = np.arange(len(x_axis)) + 0.5
    assert 2 <= arr.ndim <= 3
    if arr.ndim == 2:
        arr = arr.expand(la.Axis('dummy', 1))
    gender_axis = (arr.axes - [time_axis, x_axis])[0]
    arr = arr.transpose(gender_axis, x_axis, time_axis)
    initial_data = arr[time_axis.i[0]]
    nd_bars = []
    for g in gender_axis:
        data = initial_data[g]
        if any(data < 0):
            left = data
        else:
            left = 0
        nd_bars.append(ax.barh(xdata, data.data, left=left, label=str(g)))

    # ax.grid()
    amax = abs(arr).max() * 1.05
    # set x axis
    ax.set_xlim(-amax, amax)
    ax.set_xticklabels([abs(v) for v in ax.get_xticks()])

    # set y axis
    ax.set_ylabel(x_axis.name)
    ax.set_ylim(0, len(x_axis))
    # we need to do that because matplotlib is smart enough to
    # not show all ticks but a selection. However, that selection
    # may include ticks outside the range of x axis
    yticks = [t for t in ax.get_yticks().astype(int) if t <= len(x_axis.labels) - 1]
    yticklabels = [x_axis.labels[j] for j in yticks]
    ax.set_yticks([yt + 0.5 for yt in yticks])
    ax.set_yticklabels(yticklabels)

    ax.legend()
    # ax.set_title(str(time_axis.i[0]))

    def run(y):
        artists = []
        for nd_bar, c in zip(nd_bars, arr.axes[0]):
            data = arr[y, c]
            for bar, width in zip(nd_bar, data):
                if width < 0:
                    bar.set_width(-width)
                    bar.set_x(width)
                else:
                    bar.set_width(width)
            artists.extend(nd_bar)
        if filepath is None:
            artists.append(ax.annotate(str(y), (0.03, 0.92), xycoords='axes fraction', fontsize=16, color=(.2, .2, .2)))
        else:
            ax.set_title('{} ({})'.format(title, str(y)))
        return artists

    def init():
        return run(time_axis.i[0])

    ani = animation.FuncAnimation(fig, run, arr.axes[time_axis], init_func=init, blit=filepath is None,
                                  interval=interval, repeat=repeat, repeat_delay=repeat_delay)
    if filepath is None:
        dlg = PlotDialog(canvas, parent)
        if parent:
            dlg.show()
        else:
            dlg.exec_()
    else:
        print("Writing animation to", filepath, '...', end=' ')
        sys.stdout.flush()
        if '.htm' in os.path.splitext(filepath)[1]:
            content = '<html>{}</html>'.format(ani.to_html5_video())
            with open(filepath, mode='w', encoding='utf8') as f:
                f.write(content)
        else:
            Writer = animation.writers[writer]
            writer = Writer(fps=fps, metadata=metadata, bitrate=bitrate)
            ani.save(filepath, writer=writer)
        print("done.")
        return ani
