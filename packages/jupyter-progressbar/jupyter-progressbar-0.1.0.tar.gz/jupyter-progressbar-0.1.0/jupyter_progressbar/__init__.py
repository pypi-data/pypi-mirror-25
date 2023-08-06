from IPython.display import display
import ipywidgets as widgets
import time
import humanize
from math import sqrt


__version__ = '0.1.0'


def ProgressBar(iter, size=None):
    progress = widgets.FloatProgress(value=0.0, min=0.0, max=1.0)
    text = widgets.HTML(
        value="<b>0</b>% <b>0</b>s passed",
        placeholder='0%',
        description='',
    )
    display(widgets.HBox([progress, text]))
    if size is None and hasattr(iter, '__len__'):
        size = len(iter)
    if size is None:
        size = 2
    t = 0
    tsq = 0
    for i, item in enumerate(iter, start=1):
        while i > size:
            size = size * 2
        t0 = time.time()
        yield item
        t0 = time.time() - t0
        t += t0
        tsq += t0 ** 2
        p = i / size
        progress.value = p
        std = humanize.naturaldelta((size - i) * sqrt((tsq / i) - (t / i) ** 2))
        left = humanize.naturaldelta((1 - p) / p * t if p > 0 else 0)
        text.value = "<b>{}</b>% <b>{}</b> &plusmn; <b>{}</b> left".format(round(100 * p), left, std)

    progress.value = 100
