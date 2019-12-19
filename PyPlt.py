"""Plotting class """
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from platform import python_version

# print version of packages
print("Import PyPlt:")
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
        xlabel, ylabel, y2label: label for data_x, data_y , data_y2,
            default = None if numpy array or list, or
                      name of data if input data is a pandas series
        fonts, fontm, fontl: font size small, medium, large
        xmin, xmax, ymin, ymax, y2min, y2max: min and max of x, y, y2 axis,
            default = min and max of input data
        xpadding, ypadding:
            effective only when xmin, xmax, ymin, or ymax is none (default),
            use paddig to add more space above/below the max and min of data
            add (x.max-x.min)*xpadding to the x.min or x.max
            add (y.max-y.min)*ypadding to the y.min or y.max
        legend_pos, legend_loc, legend_pad:
            legend position, location and pad
            for example, legend_pos=(1.04,1) and legend_loc="upper left"
            means to place the legend outside the axes, such that the
            "upper left" corner of the legend is at position (1.04,1)
            in axes coordinates.
            legend_loc can be:
                'best','right','center'
                'upper left', 'upper right'
                'lower left', 'lower right',
                'center left', 'center right',
                'lower center', 'upper center',
            legend_pad is the pad between the axes and legend border.
        title: title for figure, default = None
        savefig: save the figure to a png file
            name = title + "png", default = False
        **fig_kw: keywords that are passed to matplotlib.pyplot.plot
    # Date
        20191218
    """

    def __init__(self, data_x, data_y, data_y2=None,
                 xmin=None, xmax=None,
                 ymin=None, ymax=None, y2min=None, y2max=None,
                 xpadding=0.1, ypadding=0.1,
                 xlabel=None, ylabel=None, y2label=None,
                 fonts=14, fontm=16, fontl=18,
                 legend_pos=(1, 1), legend_loc='upper right',
                 legend_pad=0.5,
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
        self.fonts = fonts
        self.fontm = fontm
        self.fontl = fontl
        self.legend_pos = legend_pos
        self.legend_loc = legend_loc
        self.legend_pad = legend_pad

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
        padding_x = abs(self.x.max() - self.x.min())*xpadding
        if self.xmin is None:
            self.xmin = self.x.min() - padding_x
        if self.xmax is None:
            self.xmax = self.x.max() + padding_x

        padding_y = abs(self.y.max() - self.y.min())*ypadding
        if self.ymin is None:
            self.ymin = self.y.min() - padding_y
        if self.ymax is None:
            self.ymax = self.y.max() + padding_y

        if (self.double_y) and (self.y2min is None):
            padding_y = abs(self.y2.max() - self.y2.min())*ypadding
            self.y2min = self.y2.min() - padding_y
        if (self.double_y) and (self.y2max is None):
            padding_y = abs(self.y2.max() - self.y2.min())*ypadding
            self.y2max = self.y2.max() + padding_y

        # size of font
        plt.rc('font', size=self.fonts)          # controls default text sizes
        plt.rc('axes', titlesize=self.fonts)     # fontsize of the axes title
        plt.rc('axes', labelsize=self.fontm)     # fontsize of the x, y labels
        plt.rc('xtick', labelsize=self.fonts)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=self.fonts)    # fontsize of the tick labels
        plt.rc('legend', fontsize=self.fonts)    # legend fontsize
        plt.rc('figure', titlesize=self.fontl)   # fontsize of the figure title

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
                    set_ylabel=None,
                    markersize=50, edgecolor='k', legend='brief',
                    **fig_kw):
        """Scatter plot.

        # Arguments
            hue, size, style : grouping variable that produce points with
                different colors, size or style
            markersize: marker size, default = 50. it has no effect if size is
                used.
            edgecolor : color of marks, default = 'k' (black)
            set_ylabel: used for set_ylabel to set label for y axis
                None: don't set_ylabel, default
                'self': use set_ylabel(self.ylabel)
                other string: use set_ylabel(set_ylabel)
            legend : “brief”, “full”, or False, default = 'brief'
            **fig_kw: keywords that are passed to matplotlib.pyplot.plot
        # Example
            (1)
            fig, ax = plt.subplots(2,1,figsize=(14,16))
            a = PyPlt.MyPlt(x, y, xmin=0.1, xmax=5, ymin=2, ymax=8)
            a.scatter_plt(style=y,marksize=100,edgecolor='red',legend='brief',ax=ax[0])
            a.scatter_plt(hue=x,ax=ax[1])

            (2) 2 scatter plots on 1 figure
            fig, ax = plt.subplots(5,1,figsize=(8,16))
            a = PyPlt.MyPlt(x, y, xmin=0.1, xmax=5, ymin=2, ymax=18,
                            xlabel='x', ylabel='y ylabel', title='a title')
            a.scatter_plt(markersize=100, edgecolor='red', legend='brief',
                          ax=ax[0])
            a = PyPlt.MyPlt(x, y2, xmin=0.1, xmax=5, ymin=2, ymax=18,
                            xlabel='x', ylabel='y2 ylabel', title='a title')
            a.scatter_plt(markersize=100, edgecolor='blue', legend='brief',
                          ax=ax[0])
        # Date
            20191127
    """
        plot_ylabel = self.ylabel

        if hue is not None:
            assert len(hue) == self.data_size
            plot_ylabel = None
        if size is not None:
            assert len(size) == self.data_size
            plot_ylabel = None
        if style is not None:
            assert len(style) == self.data_size
            plot_ylabel = None

        # lebel here will be shown in legend
        plot = sns.scatterplot(self.x, self.y,
                               hue=hue, size=size, style=style,
                               s=markersize, edgecolor=edgecolor,
                               legend=legend, label=plot_ylabel,
                               **fig_kw)

        # set x, y limit
        plot.set_xlim(self.xmin, self.xmax)
        plot.set_ylim(self.ymin, self.ymax)

        # set labels, shown on axis
        plot.set_xlabel(self.xlabel)

        if set_ylabel is None:
            plot.set_ylabel('')
        elif set_ylabel == 'self':
            plot.set_ylabel(self.ylabel)
        else:
            plot.set_ylabel(set_ylabel)

        # set ticks
        plot.tick_params(axis='x', **self.tkw)
        plot.tick_params(axis='y', **self.tkw)

        # set title
        if self.title is not None:
            plot.set_title(self.title)

        # set legend
        plot.legend(bbox_to_anchor=self.legend_pos,
                    loc=self.legend_loc,
                    borderaxespad=self.legend_pad)

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
            20191127
    """
        if hue is not None:
            assert len(hue) == self.data_size

        plot = sns.boxplot(self.x, self.y,
                           hue=hue, fliersize=markersize,
                           linewidth=linewidth, width=width,
                           **fig_kw)

        # set labels, shown on axis
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

        # set legend
        plot.legend(bbox_to_anchor=self.legend_pos,
                    loc=self.legend_loc,
                    borderaxespad=self.legend_pad)

        # save figures
        if self.savefig:
            fig = plot.get_figure()
            if self.title is None:
                file_title = 'box_plt'
            else:
                file_title = self.title
            fig.savefig(file_title + ".png", transparent=False,
                        dpi=100, bbox_inches='tight')

    def xyy_plt(self, ycolor='blue', y2color='red', legend='brief',
                marker='o', markersize=10,
                set_ylabel=None, set_y2label=None,
                **fig_kw):
        """plot data_y1 (on left y axis) and data_y2
        (on right y axis) with same data_x (on x axis).
        data_x, data_y1, data_y2 are 1-d arrays with same length

        # Arguments
            ycolor, y2color: color of left and right y axis,
                defautl = 'blue', 'red'
                use None to allow multiple lines with different colors in
                a single figure.
            marker: marker of line, default = 'o'
            markersize: marker size, default = 10. 0 means no markers.
            legend : “brief”, “full”, or False, default = 'brief'
            set_ylabel, set_y2label: for set_ylabel to set label for y axis
                None: don't set_ylabel, default
                'self': use set_ylabel(self.ylabel)
                other string: use set_ylabel(set_ylabel)
            **fig_kw: keywords that are passed to matplotlib.pyplot.plot
        # Example
            (1) x and 2 y axis (left and right):
            b = PyPlt.MyPlt(df['x'], df['y'], df['y2'],
                            xmin=-1, xmax=5, ymin=0, ymax=10,
                            y2min=3, y2max=10, title='b title')
            b.xyy_plt(legend=False, set_ylabel='its y', set_y2label='its y2',
                      ax=ax[1])

            (2) multiple data on left y axis
            c = PyPlt.MyPlt(df['x'], df['y'], ylabel='y',xmin=0.1, xmax=5,
                            ymin=2, ymax=12)
            c.xyy_plt(marker='v',ax=ax[2])
            c = PyPlt.MyPlt(df['x'], df['y2'],ylabel='y2',xmin=0.1, xmax=5,
                            ymin=2, ymax=12)
            c.xyy_plt(marker='o',ax=ax[2],set_ylabel='Data')
        # Date
            20191127
        """

        plot_ylabel = self.ylabel
        # lebel here will be shown in legend
        ploty = sns.lineplot(self.x, self.y,
                             color=ycolor, label=plot_ylabel,
                             legend=legend, marker=marker,
                             markersize=markersize,
                             **fig_kw)

        if self.double_y:
            plot_y2label = self.y2label
            ax_y2 = ploty.twinx()
            ploty2 = sns.lineplot(self.x, self.y2,
                                  color=y2color, label=plot_y2label,
                                  legend=legend, marker=marker,
                                  markersize=markersize,
                                  ax=ax_y2)

        # set x, y limit
        ploty.set_xlim(self.xmin,  self.xmax)
        ploty.set_ylim(self.ymin, self.ymax)
        if self.double_y:
            ploty2.set_ylim(self.y2min, self.y2max)

        # set labels, shown on axis
        ploty.set_xlabel(self.xlabel)

        if set_ylabel is None:
            ploty.set_ylabel('')
        elif set_ylabel == 'self':
            ploty.set_ylabel(self.ylabel)
        else:
            ploty.set_ylabel(set_ylabel)

        if self.double_y:
            if set_y2label is None:
                ploty2.set_ylabel('')
            elif set_y2label == 'self':
                ploty2.set_ylabel(self.y2label)
            else:
                ploty2.set_ylabel(set_y2label)

        # set axis color
        if self.double_y:
            # Need to use ploty2 here for left and right spines !!
            ploty2.spines['left'].set_color(ploty.get_lines()[0].get_color())
            ploty2.spines['right'].set_color(ploty2.get_lines()[0].get_color())
        else:
            # use ploty if only 1 y axis is used !!
            # ploty.spines['left'].set_color(ploty.get_lines()[0].get_color())
            ploty.spines['left'].set_color('black')

        # set color for y labels
        if self.double_y:
            ploty.yaxis.label.set_color(ploty.get_lines()[0].get_color())
            ploty2.yaxis.label.set_color(ploty2.get_lines()[0].get_color())
        else:
            ploty.yaxis.label.set_color('black')

        # set ticks
        tkw = dict(size=4, width=1.5)
        ploty.tick_params(axis='x', **tkw)
        if self.double_y:
            ploty.tick_params(axis='y',
                              colors=ploty.get_lines()[0].get_color(),
                              **tkw)
            ploty2.tick_params(axis='y',
                               colors=ploty2.get_lines()[0].get_color(),
                               **tkw)
        else:
            ploty.tick_params(axis='y',
                              colors='black',
                              **tkw)

        # set title
        if self.title is not None:
            ploty.set_title(self.title)

        # set legend
        ploty.legend(bbox_to_anchor=self.legend_pos,
                     loc=self.legend_loc,
                     borderaxespad=self.legend_pad)

        # save figures
        if self.savefig:
            fig = ploty.get_figure()
            if self.title is None:
                file_title = 'xyy_plt'
            else:
                file_title = self.title
            fig.savefig(file_title + ".png", transparent=False,
                        dpi=100, bbox_inches='tight')

    def bar_plt(self, hue=None, orient='v',
                order=None, hue_order=None, ci=None, edgecolor='k',
                linewidth=1,
                set_ylabel='self', **fig_kw):
        """Show point estimates and confidence intervals as rectangular bars.

        A bar plot represents an estimate of central tendency for a numeric
        variable with the height of each rectangle and provides some indication
        of the uncertainty around that estimate using error bars. Bar plots
        include 0 in the quantitative axis range, and they are a good choice
        when 0 is a meaningful value for the quantitative variable, and you
        want to make comparisons against it.

        It is also important to keep in mind that a bar plot shows only the
        mean (or other estimator) value, but in many cases it may be more
        informative to show the distribution of values at each level of the
        categorical variables. In that case, other approaches such as a box or
        violin plot may be more appropriate.

        # Arguments
            x, y, hue : Inputs for plotting long-form data.
            orient: orientation of the plot (vertical 'v' or horizontal 'h'),
                sometimes we need to change orient and switch x, y to make it
                work.
            set_ylabel: used for set_ylabel to set label for y axis
                None: don't set_ylabel
                'self': use set_ylabel(self.ylabel), default
                other string: use set_ylabel(set_ylabel)
            order, hue_order : lists of strings, optional
                Order to plot the categorical levels in, otherwise the levels
                are inferred from the data objects.
                x, y limit is not working here, but we can use order to add
                space to the plot (for legend).
            ci: float, 'sd', or None(default),
                size of confidence intervals to draw around estimated values.
                If “sd”, skip bootstrapping and draw the standard deviation of
                the observations.
                If None, no bootstrapping will be performed, and error bars
                will not be drawn.
            edgecolor: color of bar, default = 'k' (black).
            linewidth: width of edge of bar, default = 1.
            **fig_kw: keywords that are passed to matplotlib.pyplot.plot

        # Example
            fig, ax = plt.subplots(1,1,figsize=(4,4),sharey=True)
            var_pre = PyPlt.MyPlt(df_1d['mt'],df_1d[var])
            var_pre.bar_plt(hue=df_1d['wb?'],order=[10.0,20.0,40.0,'',''],
                            hue_order=[14.0,2.0])
            ('' in order to add space for legend)
        # Date
            20191219
        """

        plot = sns.barplot(self.x, self.y, hue=hue, orient=orient,
                           order=order, hue_order=hue_order, ci=ci,
                           linewidth=linewidth, edgecolor=edgecolor,
                           **fig_kw)

        # only show legend if hue is used.
        if hue is not None:
            # set tile in legend
            if (isinstance(hue, pd.Series)):
                legend_title = hue.name
            # set legend
            plot.legend(bbox_to_anchor=self.legend_pos,
                        loc=self.legend_loc,
                        borderaxespad=self.legend_pad,
                        title=legend_title)

        # set labels, shown on axis
        plot.set_xlabel(self.xlabel)

        if set_ylabel is None:
            plot.set_ylabel('')
        elif set_ylabel == 'self':
            plot.set_ylabel(self.ylabel)
        else:
            plot.set_ylabel(set_ylabel)

        # set title
        if self.title is not None:
            plot.set_title(self.title)

        # save figures
        if self.savefig:
            fig = plot.get_figure()
            if self.title is None:
                file_title = 'bar_plt'
            else:
                file_title = self.title
            fig.savefig(file_title + ".png", transparent=False,
                        dpi=100, bbox_inches='tight')
