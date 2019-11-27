"""Plotting class """
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


# print version of packages
print("Import PyPlt:")
from platform import python_version
print("python version: ", python_version())
print("numpy version: ", np.version.version)
print("pandas version: ", pd.__version__)
print("matplotlib version: ", matplotlib.__version__)
print("Seaborn version: ", sns.__version__)


class MyPlt:
    """My python plotter library.
    This does the drawing using matplotlib and/or seaborn
    data (data_x, data_y, data_y2) can be passed in a list, numpy array or
    pandas series with same size.

    # Arguments
        data_x: data for x axis
        data_y: data for y on left y axis
        data_y2: data for y2 on right y axis (optional), default = None
        xlabel, ylabel, y2label = label for x, y ,y2,
            default = None if numpy array or list, or
                      name of data if input data is a pandas series
        xmin, xmax, ymin, ymax, y2min, y2max: min and max of x, y, y2 axis,
            default = min and max of input data
        title: title for figure, default = None
        savefig: save the figure to a png file
            name = title + "png", default = False
        **fig_kw: keywords that are passed to matplotlib.pyplot.plot
    # Date
        20191125
    """

    def __init__(self, data_x, data_y, data_y2=None,
                 xmin=None, xmax=None,
                 ymin=None, ymax=None, y2min=None, y2max=None,
                 xlabel=None, ylabel=None, y2label=None,
                 title=None, savefig=False):



        # check if 2 y axis
        self.double_y = False
        if data_y2 is not None:
            self.double_y = True

        # check dimension of input data
        N = len(data_x)
        assert len(data_y) == N
        if self.double_y:
            assert len(data_y2) == N
        self.data_size = N

        # assign values
        self.x = data_x
        self.y = data_y
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.savefig = savefig

        if self.double_y:
            self.y2 = data_y2
            self.y2min = y2min
            self.y2max = y2max
            self.y2label = y2label

        # convert list to numpy array
        if isinstance(self.x, list):
            self.x = np.array(self.x)
        if isinstance(self.y, list):
            self.y = np.array(self.y)
        if self.double_y and isinstance(self.y2, list):
            self.y2 = np.array(self.y2)

        # set min and max of axis
        if self.xmin is None:
            self.xmin = self.x.min()
        if self.xmax is None:
            self.xmax = self.x.max()
        if self.ymin is None:
            self.ymin = self.y.min()
        if self.ymax is None:
            self.ymax = self.y.max()
        if (self.double_y) and (self.y2min is None):
            self.y2min = self.y2.min()
        if (self.double_y) and (self.y2max is None):
            self.y2max = self.y2.max()

        # set label
        if (isinstance(self.x, pd.Series)) and (self.xlabel is None):
            self.xlabel = self.x.name
        if (isinstance(self.y, pd.Series)) and (self.ylabel is None):
            self.ylabel = self.y.name
        if self.double_y:
            if (isinstance(self.y2, pd.Series)) and (self.y2label is None):
                self.y2label = self.y2.name

        # set tickits
        self.tkw = dict(size=4, width=1.5)

    def scatter_plt(self, hue=None, size=None, style=None,
                    markersize=50, edgecolor='k', legend='brief',
                    **fig_kw):
        """Scatter plot.

        # Arguments
            hue, size, style : grouping variable that produce points with
                different colors, size or style
            markersize: marker size, default = 50. it has no effect if size is
                used.
            edgecolor : color of marks, default = 'k' (black)
            legend : “brief”, “full”, or False, default = 'brief'
            **fig_kw: keywords that are passed to matplotlib.pyplot.plot
        # Example
            fig, ax = plt.subplots(2,1,figsize=(14,16))
            a = PyPlt.MyPlt(x, y, xmin=0.1, xmax=5, ymin=2, ymax=8)
            a.scatter_plt(style=y,marksize=100,edgecolor='red',legend='brief',ax=ax[0])
            a.scatter_plt(hue=x,ax=ax[1])
        # Date
            20191125
    """
        if hue is not None:
            assert len(hue) == self.data_size
        if size is not None:
            assert len(size) == self.data_size
        if style is not None:
            assert len(style) == self.data_size

        plot = sns.scatterplot(self.x, self.y,
                               hue=hue, size=size, style=style,
                               s=markersize, edgecolor=edgecolor,
                               legend=legend, **fig_kw)

        # set x, y limit
        plot.set_xlim(self.xmin, self.xmax)
        plot.set_ylim(self.ymin, self.ymax)

        # set labels
        plot.set_xlabel(self.xlabel)
        plot.set_ylabel(self.ylabel)

        # set ticks
        plot.tick_params(axis='x', **self.tkw)
        plot.tick_params(axis='y', **self.tkw)

        # set title
        if self.title is not None:
            plot.set_title(self.title)

        # save figures
        if self.savefig:
            fig = plot.get_figure()
            if self.title is None:
                file_title = 'scatter_plt'
            else:
                file_title = self.title
            fig.savefig(file_title + ".png", transparent=False,
                        dpi=100, bbox_inches='tight')

    def box_plt(self, hue=None,
                linewidth=2.5, width=0.8,
                markersize=5, boxvalue=True,
                **fig_kw):
        """Box plot.
        For boxplot, min and max from self is different from what shows on
        axis, I decide not to manually set it with set_xlim and set_ylim.

        # Arguments
            hue: grouping variable that produce points with different style
            linewidth: width of gray lines that frame the plot elements,
                default = 2.5
            width: box width, default = 0.8
            markersize: marker size of outlier observations, default = 5.

            **fig_kw: keywords that are passed to matplotlib.pyplot.plot
        # Example
            use sharey here I can still set y(or x) range !!!

            fig, ax = plt.subplots(2,1,figsize=(19,10),sharey=True)
            xmin=-1
            xmax=12
            ymin=0
            ymax=2000
            Eth_r = PyPlt.MyPlt(df_Eth['r']-1, df_Eth['Eth'],
                                xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
            Eth_r.scatter_plt(hue=df_Eth['case'],markersize=10,ax=ax[0])
            Eth_rint = PyPlt.MyPlt(df_Eth['r_int']-1,
                                   df_Eth['Eth'].astype('int64'),
                                   xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
            Eth_rint.box_plt(ax=ax[1], hue=df_Eth['case'], boxvalue=True,
                             linewidth=1, width=0.7)
        # Date
            20191126
    """
        if hue is not None:
            assert len(hue) == self.data_size

        plot = sns.boxplot(self.x, self.y,
                           hue=hue, fliersize=markersize,
                           linewidth=linewidth, width=width,
                           **fig_kw)

        ## set x, y limit
        #if minmax == 'self':
        #    plot.set_xlim=(self.xmin, self.xmax)
        #    plot.set_ylim=(self.ymin, self.ymax)
        #elif minmax == 'auto':
        #    pass
        #else:
        #    print('Unknown mimmax, set minmax to auto')

        # set labels
        plot.set_xlabel(self.xlabel)
        plot.set_ylabel(self.ylabel)

        # set ticks
        plot.tick_params(axis='x', **self.tkw)
        plot.tick_params(axis='y', **self.tkw)

        # set title
        if self.title is not None:
            plot.set_title(self.title)

        # value on box
        if boxvalue:
            axe = plot.axes
            lines = axe.get_lines()
            NumBox = int(np.ceil(len(lines)/6))  # number of box in the figure
            for ibox in range(NumBox):
                # x_l, x_r = position (left and right) of box
                # 25%, 75%, minimum, maximum, median, others
                (x_l, y_25), (x_r, _) = lines[0 + ibox*6].get_xydata()
                (x_l, y_75), (x_r, _) = lines[1 + ibox*6].get_xydata()
                (x_l, y_min), (x_r, _) = lines[2 + ibox*6].get_xydata()
                (x_l, y_max), (x_r, _) = lines[3 + ibox*6].get_xydata()
                (x_l, y_med), (x_r, _) = lines[4 + ibox*6].get_xydata()
                x_center = (x_l + x_r)/2
                # text on box
                axe.text(x_center, y_25, f'{y_25}')
                axe.text(x_center, y_75, f'{y_75}')
                axe.text(x_center, y_min, f'{y_min}')
                axe.text(x_center, y_max, f'{y_max}')
                axe.text(x_center, y_med, f'{y_med}')

        # save figures
        if self.savefig:
            fig = plot.get_figure()
            if self.title is None:
                file_title = 'scatter_plt'
            else:
                file_title = self.title
            fig.savefig(file_title + ".png", transparent=False,
                        dpi=100, bbox_inches='tight')

    def xyy_plt(self, ycolor='blue', y2color='red',
                marker='o', markersize=10, **fig_kw):
        """plot data_y1 (on left y axis) and data_y2
        (on right y axis) with same data_x (on x axis).
        data_x, data_y1, data_y2 are 1-d arrays with same length

        # Arguments
            ycolor, y2color: color of left and right y axis,
                defautl = 'blue', 'red'
            marker: marker of line, default = 'o'
            markersize: marker size, default = 10. 0 means no markers.
            **fig_kw: keywords that are passed to matplotlib.pyplot.plot
        # Example
            fig, ax = plt.subplots(2,1,figsize=(14,16))
            b = PyPlt.MyPlt(df['x'], df['y'], df['y2'], xmin=-1, xmax=5,
                            ymin=0, ymax=10, y2min=3, y2max=10, y2label='y2',
                            savefig=True,title='b title')
            b.xyy_plt(ax=ax[0])
        # Date
            20191125
        """
        ploty = sns.lineplot(self.x, self.y,
                             color=ycolor, label=self.ylabel,
                             legend=False, marker=marker,
                             markersize=markersize,
                             **fig_kw)
        if self.double_y:
            ax_y2 = ploty.twinx()
            ploty2 = sns.lineplot(self.x, self.y2,
                                  color=y2color, label=self.y2label,
                                  legend=False, marker=marker,
                                  markersize=markersize,
                                  ax=ax_y2)

        # set x, y limit
        ploty.set_xlim(self.xmin,  self.xmax)
        ploty.set_ylim(self.ymin, self.ymax)
        if self.double_y:
            ploty2.set_ylim(self.y2min, self.y2max)

        # set labels
        ploty.set_xlabel(self.xlabel)
        ploty.set_ylabel(self.ylabel)
        if self.double_y:
            ploty2.set_ylabel(self.y2label)

        # set axis color
        if self.double_y:
            # Need to use ploty2 here for left and right spines !!
            ploty2.spines['left'].set_color(ploty.get_lines()[0].get_color())
            ploty2.spines['right'].set_color(ploty2.get_lines()[0].get_color())
        else:
            # use ploty if only 1 y axis is used !!
            ploty.spines['left'].set_color(ploty.get_lines()[0].get_color())

        # set color for y labels
        ploty.yaxis.label.set_color(ploty.get_lines()[0].get_color())
        if self.double_y:
            ploty2.yaxis.label.set_color(ploty2.get_lines()[0].get_color())

        # set ticks
        tkw = dict(size=4, width=1.5)
        ploty.tick_params(axis='x', **tkw)
        ploty.tick_params(axis='y',
                          colors=ploty.get_lines()[0].get_color(),
                          **tkw)
        if self.double_y:
            ploty2.tick_params(axis='y',
                               colors=ploty2.get_lines()[0].get_color(),
                               **tkw)

        # set title
        if self.title is not None:
            ploty.set_title(self.title)

        # save figures
        if self.savefig:
            fig = ploty.get_figure()
            if self.title is None:
                file_title = 'xyy_plt'
            else:
                file_title = self.title
            fig.savefig(file_title + ".png", transparent=False,
                        dpi=100, bbox_inches='tight')
