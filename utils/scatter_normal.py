import numpy as np
from scipy import stats
from matplotlib.ticker import MultipleLocator, LogLocator

class PlotManager:
    def __init__(self, ax, fontsize=12, fontsize_s=10, linewidth=1.5, scale='linear',
                 xmin=None, xmax=None, ymin=None, ymax=None):
        self.ax = ax
        self.fontsize = fontsize
        self.fontsize_s = fontsize_s
        self.linewidth = linewidth
        self.scale = scale
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def ax_setting(self, minor=True, minor_locator=None):
        ax = self.ax
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_linewidth(self.linewidth)
        ax.spines['left'].set_linewidth(self.linewidth)
        ax.minorticks_on()
        ax.grid(which="both")
        ax.tick_params(axis='both', which='major', width=self.linewidth, labelsize=self.fontsize)
        ax.tick_params(axis='both', which='minor', width=self.linewidth)

        if self.xmin is not None and self.xmax is not None:
            ax.set_xlim(self.xmin, self.xmax)
        if self.ymin is not None and self.ymax is not None:
            ax.set_ylim(self.ymin, self.ymax)

        if self.scale == 'xlog':
            ax.set_xscale('log')
        elif self.scale == 'ylog':
            ax.set_yscale('log')
        elif self.scale == 'loglog':
            ax.set_xscale('log')
            ax.set_yscale('log')

        ax.grid(True, which='major', linewidth=0.5, color='k', alpha=0.2, zorder=0)
        ax.grid(True, which='minor', linewidth=0.3, color='k', alpha=0.2, zorder=0)
    
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def scatter_plot(self, x, y, color):
        self.ax.scatter(x, y, color=color)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def plot_regression_with_ci(self, x, y, color='blue', force_intercept_zero=False, text_loc=(0.95, 0.95)):
        # 回帰計算
        if force_intercept_zero:
            a = np.sum(x * y) / np.sum(x ** 2)
            y_pred = a * x
            r2 = np.sum((a * x) ** 2) / np.sum(y ** 2)
            b = 0
        else:
            a, b = np.polyfit(x, y, 1)
            y_pred = a * x + b
            r = np.corrcoef(x, y)[0, 1]
            r2 = r ** 2

        # 回帰直線描画用データ
        x_line = np.linspace(np.min(x), np.max(x), 100)
        if force_intercept_zero:
            y_line = a * x_line
        else:
            y_line = a * x_line + b

        # 信頼区間の計算
        n = len(x)
        dof = n - (1 if force_intercept_zero else 2)
        tval = stats.t.ppf(0.975, dof)

        y_fit = a * x + (0 if force_intercept_zero else b)
        se = np.sqrt(np.sum((y - y_fit) ** 2) / dof)
        mean_x = np.mean(x)
        s_xx = np.sum((x - mean_x) ** 2) if not force_intercept_zero else np.sum(x ** 2)

        ci = tval * se * np.sqrt(1 / n + (x_line - (0 if force_intercept_zero else mean_x)) ** 2 / s_xx)

        # 描画
        self.ax.fill_between(x_line, y_line - ci, y_line + ci, color=color, alpha=0.2, label="95% CI")
        self.ax.plot(x_line, y_line, color=color, linewidth=self.linewidth, label='回帰直線')

        # 式とR^2の表示
        if force_intercept_zero:
            formula = f"$y = {a:.2f}x$\n$R^2 = {r2:.2f}$"
        else:
            formula = f"$y = {a:.2f}x + {b:.2f}$\n$R^2 = {r2:.2f}$"

        self.ax.text(text_loc[0], text_loc[1], formula, transform=self.ax.transAxes,
                fontsize=self.fontsize_s, ha='right', va='top',
                fontdict={"math_fontfamily": "cm"})
        pass

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np

    plt.rc('font', family='serif')
    plt.rc('font', serif='CMU Serif')   

    # サンプルデータ
    x = np.linspace(1, 10, 20)
    y = 2 * x + np.random.normal(0, 2, len(x))

    # プロット
    fig, ax = plt.subplots()
    pm = PlotManager(ax, fontsize=12, scale='linear', xmin=0, xmax=12)
    pm.ax_setting()
    pm.scatter_plot(x, y, color='red')
    pm.plot_regression_with_ci(x, y, color='red')
    plt.show()


