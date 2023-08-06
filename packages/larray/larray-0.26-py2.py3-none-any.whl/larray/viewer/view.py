

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
    # bars = ax.bar(xdata, initial_data[initial_data.axes[1].i[0]].data)

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
        Writer = animation.writers[writer]
        writer = Writer(fps=fps, metadata=metadata, bitrate=bitrate)
        ani.save(filepath, writer=writer)
        # content = '<html>{}</html>'.format(ani.to_html5_video())
        # with open('test.html', mode='w', encoding='utf8') as f:
        #     f.write(content)
        return ani



