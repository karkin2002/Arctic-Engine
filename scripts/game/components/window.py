from pygame import display as pygame_display, RESIZABLE, SCALED, transform as pygame_transform, FULLSCREEN
from pygame import Vector2, Surface
import scripts.utility.glob as glob
glob.init()


class Window:
    def __init__(self,
                 dim: tuple[int, int],
                 background: str | None = None,
                 flags = (FULLSCREEN | SCALED),
                 vsync: bool = True):

        self.dim = Vector2(dim)
        self.center = Vector2(0, 0)
        self.win: Surface | None = None

        self.vsync = vsync
        self.flags = flags

        self.set_win(self.dim)
        self.background = background

    def set_win(self, win_dim: Vector2):
        """Creates a new window.

        Args:
            win_dim (tuple[int, int]): Window (<width>, <height>).
        """

        self.win = pygame_display.set_mode(
            win_dim,
            self.flags,
            vsync=1 if self.vsync else 0
        )

        self.resize()

    def resize(self):
        """
        Handles the event upon which the window is resized.
        """
        self.dim.update(self.win.get_size())
        self.center.update(round(self.dim[0] / 2), round(self.dim[1] / 2))

    def draw(self):

        self.win.blit(self.win, (0, 0))

        pygame_display.flip()

    def draw_background(self):
        if self.background is not None:
            self.win.fill(glob.get_colour(self.background))

    def set_flags(self, flags: int):
        self.flags = flags
        self.set_win(self.dim)

    def add_flags(self, flags: int):
        self.flags |= flags
        self.set_win(self.dim)

    def remove_flags(self, flags: int):
        self.flags &= ~flags
        self.set_win(self.dim)

    def set_vsync(self, vsync: bool):
        if self.vsync != vsync:
            self.vsync = vsync

            self.set_win(self.dim)