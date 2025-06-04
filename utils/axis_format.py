import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime

class AxisFormatter:
    def __init__(self, ax, ax_width=1.5, labelsize=12,
                 scale='linear', xmin=None, xmax=None, ymin=None, ymax=None):
        self.ax = ax
        self.ax_width = ax_width
        self.labelsize = labelsize
        self.scale = scale
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def format_common_axis(self):
        ax = self.ax
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_linewidth(self.ax_width)
        ax.spines['left'].set_linewidth(self.ax_width)
        # ax.minorticks_on()
        ax.tick_params(axis='both', which='major', width=self.ax_width, labelsize=self.labelsize)
        #ax.tick_params(axis='both', which='minor', width=self.ax_width)

        if self.scale == 'xlog':
            ax.set_xscale('log')
        elif self.scale == 'ylog':
            ax.set_yscale('log')
        elif self.scale == 'loglog':
            ax.set_xscale('log')
            ax.set_yscale('log')

        if self.xmin is not None and self.xmax is not None:
            ax.set_xlim(self.xmin, self.xmax)
        if self.ymin is not None and self.ymax is not None:
            ax.set_ylim(self.ymin, self.ymax)

    def ax_setting_numeric(self, minor_locator=None):
        self.format_common_axis()
        self.ax.minorticks_on()
        self.ax.tick_params(axis='both', which='minor', width=self.ax_width)
        if minor_locator is not None:
            self.ax.xaxis.set_minor_locator(minor_locator)
        self.ax.grid(True, which='major', linewidth=0.5, color='k', alpha=0.2, zorder=0)
        self.ax.grid(True, which='minor', linewidth=0.3, color='k', alpha=0.2, zorder=0)

    def ax_setting_date(self):#, date_minor_days=15
        self.format_common_axis()
        self.ax.xaxis.set_major_locator(mdates.MonthLocator())
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        #self.ax.xaxis.set_minor_locator(mdates.DayLocator(interval=date_minor_days))
        self.ax.grid(True, which='major', linewidth=0.5, color='k', alpha=0.2, zorder=0)
        self.ax.grid(True, which='minor', linewidth=0.3, color='k', alpha=0.2, zorder=0)

# if __name__ == '__main__':
#     import pandas as pd
#     import matplotlib.dates as mdates
#     import matplotlib.pyplot as plt
#     import datetime
    
#     data = pd.read_csv("sagadani_temp_data.csv")
#     data['date'] = pd.to_datetime(data['date'])
    
#     fig, ax = plt.subplots(figsize=(10, 4))


#     sxmin='2023-07-01'
#     sxmax='2023-12-01'
#     xmin = datetime.datetime.strptime(sxmin, '%Y-%m-%d')
#     xmax = datetime.datetime.strptime(sxmax, '%Y-%m-%d')

#     formatter = AxisFormatter(ax, xmin=xmin, xmax=xmax, ymin=0, ymax=35)
#     #formatter.ax_setting_numeric()

#     formatter.ax_setting_date()

#     line_color = ['grey', 'blue']
#     line_width = 1
#     ax_width = 1.5
    
#     for i in range(len(data.columns)-1):
#         # データをプロット
#         ax.plot(data.iloc[:, 0], data.iloc[:, i+1], linestyle='solid', color=line_color[i], linewidth=line_width)

#     plt.show()