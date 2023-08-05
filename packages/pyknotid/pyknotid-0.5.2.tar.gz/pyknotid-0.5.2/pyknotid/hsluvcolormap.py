
from matplotlib.colors import Colormap
from hsluv import hsluv_to_rgb

class HsluvColormap(Colormap):
    def __getitem__(self, index):
        return hsluv_to_rgb(360*index, 100, 65)

from matplotlib.cm import register_cmap
register_cmap(name='hsluv', cmap=HsluvColormap('hsluv'))
