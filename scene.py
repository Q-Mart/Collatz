from manim import *
from manim.utils.color import Colors
import random

PLPLOT_CMAP0=[
    '#ff0000',
    '#ffff00',
    '#00ff00',
    '#7fffd4',
    '#ffc0cb',
    '#f5deb3',
    '#bebebe',
    '#a52a2a',
    '#0000ff',
    '#8a2be2',
    '#00ffff',
    '#40e0d0',
    '#ff00ff',
    '#fa8072',
    '#ffffff'
]

class Collatz2d(Scene):
    def collatz(self, x):
        return (3*x) + 1 if x % 2 == 1 else x//2

    def apply_collatz_n_times(self, n, x):
        for i in range(int(n)+1):
            x = self.collatz(x)

        return x


    def construct(self):
        grid = Axes(
            x_range=[0,20,1],
            y_range=[0,1500,1],
            y_length=12
        )

        colours = list(Colors)
        random.shuffle(colours)

        graphs = VGroup()
        for n in np.arange(1,250,1):
            col = PLPLOT_CMAP0[n%len(PLPLOT_CMAP0)]
            graphs += grid.get_graph(
                lambda t: self.apply_collatz_n_times(t, n),
                color=col
            )

        self.add(graphs)
