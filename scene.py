from manim import *
from manim.utils.color import Colors

# Cool colour scheme
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

def collatz(x):
    return (3*x) + 1 if x % 2 == 1 else x//2

memo = {}
def apply_collatz_n_times_recursive(n, x):
    global memo

    print(n,x)

    if (n,x) in memo:
        return memo[(n,x)]
    else:
        if n == 0:
            new_x = x
        else:
            new_x = collatz(apply_collatz_n_times_recursive(n-1, x))

        memo[(n,x)] = new_x

        return new_x

def apply_collatz_n_times(n, x):
    for i in range(int(n)+1):
        x = collatz(x)

    return x

class Collatz2d(Scene):

    def construct(self):
        grid = Axes(
            x_range=[0,20,1],
            y_range=[0,1500,1],
            y_length=12
        )

        graphs = VGroup()
        for n in np.arange(1,250,1):
            col = PLPLOT_CMAP0[n%len(PLPLOT_CMAP0)]
            graphs += grid.get_graph(
                lambda t: apply_collatz_n_times(t, n),
                color=col
            )

        self.add(graphs)

class Collatz3d(ThreeDScene):

    def __init__(self):
        self._current_z = 0
        super().__init__()

    def get_x_and_y(self, t, n):
        x = t
        y = apply_collatz_n_times_recursive(t,n)
        return x,y

    def right_angle_parm_eq(self, t, n):
        x,y = self.get_x_and_y(t,n)

        if t != 1:
            val_before = apply_collatz_n_times_recursive(t, n-1)
            if y > val_before:
                self._current_z += 1
            else:
                self._current_z -= 1

        return np.array([x,y,self._current_z])

    def thirty_deg_param_eq(self, t, n):
        x,y = self.get_x_and_y(t,n)

        if t != 1:
            val_before = apply_collatz_n_times_recursive(t, n-1)

            p = np.sqrt(((y-val_before)**2) + 1)

            if y > val_before:
                self._current_z += np.tan(30) * p
            else:
                self._current_z -= np.tan(30) * p

        return np.array([x,y,self._current_z])


    def construct(self):
        grid = ThreeDAxes(
            x_range=(0,20,1),
            y_range=(0,1500,1),
            z_range=(-100,100,1)
        )
        self.set_camera_orientation(phi=-90*DEGREES, theta=0*DEGREES)

        graphs = VGroup()
        for n in np.arange(1,250,1):
            self._current_z = 0
            col = PLPLOT_CMAP0[n%len(PLPLOT_CMAP0)]
            graphs += grid.get_parametric_curve(
                lambda t: self.thirty_deg_param_eq(t,n),
                t_range=[0, 20, 1],
                color=col
            )

        self.add(graphs)

        self.wait()
        self.begin_ambient_camera_rotation(rate=1)
        self.wait(10)
        self.stop_ambient_camera_rotation()
