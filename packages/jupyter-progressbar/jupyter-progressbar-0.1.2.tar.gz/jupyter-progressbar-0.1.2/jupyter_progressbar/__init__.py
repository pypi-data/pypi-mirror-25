from IPython.display import display
import ipywidgets as widgets
import time
import humanize
from math import sqrt


__version__ = '0.1.2'
__author__ = 'Herbert Kruitbosch'


def ProgressBar(iter, size=None):
    progress = widgets.FloatProgress(value=0.0, min=0.0, max=1.0)
    text = widgets.HTML(
        value="<b>0</b>s passed",
        placeholder='0%',
        description='',
    )
    text2 = widgets.HTML(
        value="<b>0</b>% or <b>0</b> of <b>0</b> done",
        placeholder='0%',
        description='',
    )
    display(widgets.VBox([widgets.HBox([progress, text]), text2]))
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
        text.value = "<b>{}</b> &plusmn; <b>{}</b> left".format(left, std)
        text2.value = "<b>{}</b>% or <b>{}</b> of <b>{}</b> done".format(round(100 * p), i, size)
    text.value = ''
    text2.value = "took <b>{}</b> to process <b>{}</b> items".format(humanize.naturaldelta(t), i)
    progress.value = 100
