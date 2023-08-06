from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pickle

from matplotlib.backend_bases import FigureManagerBase, FigureCanvasBase
from matplotlib.figure import Figure


########################################################################
#
# The following functions and classes are for pylab and implement
# window/figure managers, etc...
#
########################################################################

def new_figure_manager(num, *args, **kwargs):
    """
    Create a new figure manager instance
    """
    # if a main-level app must be created, this (and
    # new_figure_manager_given_figure) is the usual place to
    # do it -- see backend_wx, backend_wxagg and backend_tkagg for
    # examples.  Not all GUIs require explicit instantiation of a
    # main-level app (egg backend_gtk, backend_gtkagg) for pylab
    FigureClass = kwargs.pop('FigureClass', Figure)
    thisFig = FigureClass(*args, **kwargs)
    return new_figure_manager_given_figure(num, thisFig)


def new_figure_manager_given_figure(num, figure):
    """
    Create a new figure manager instance for the given figure.
    """
    canvas = FigureCanvasPickle(figure)
    manager = FigureManagerPickle(canvas, num)
    return manager


class FigureCanvasPickle(FigureCanvasBase):
    """
    The canvas the figure renders into. Not applicable.

    Attributes
    ----------
    figure : `matplotlib.figure.Figure`
        A high-level Figure instance

    """

    def draw(self):
        pass

    filetypes = {}
    filetypes['pkl'] = 'Python pickle format'
    filetypes['pickle'] = 'Python pickle format'

    def print_pkl(self, filename, *args, **kwargs):
        pickle.dump(self.figure, open(filename, 'wb'))

    print_pickle = print_pkl

    def get_default_filetype(self):
        return 'pkl'


class FigureManagerPickle(FigureManagerBase):
    """
    Wrap everything up into a window for the pylab interface

    For non interactive backends, the base class does all the work
    """
    pass

########################################################################
#
# Now just provide the standard names that backend.__init__ is expecting
#
########################################################################


FigureCanvas = FigureCanvasPickle
FigureManager = FigureManagerPickle
