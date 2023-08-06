# Jupyter ProgressBar

Wrap generators and iterators with a ProgressBar in Jupyter Notebooks. Get an early educated guess on the running time
if you want to

 * process several files by wrapping `os.listdir`: `for file in ProgressBar(os.listdir(...)):`
 * process a generator of iterator: `for x in ProgressBar((... some generator ...), size=90):`
 * even if you are clueless about the size:  `for x in ProgressBar((... some generator ...)):`

If the size is unknown, `size == 2` is assumed until the `size+1`-th element is returned, then `size` is doubled. The
size is also doubled when it was known via `__len__` or specified via `size`, but exceeded while looping.


![ProgressBar example](example.png?raw=true "Example ProgressBar")

## Installation

Via pip

    pip install jupyter-progressbar

From git

    git clone git@github.com:prinsherbert/jupyter-progressbar.git
    cd jupyter-progressbar
    python setup.py install

## Example

    from jupyter_progressbar import ProgressBar
    import time
    import random
    for i in ProgressBar(range(100)):
        time.sleep(0.1 + random.random()*0.1)

