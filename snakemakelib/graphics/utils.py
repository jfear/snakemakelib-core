# Copyright (C) 2015 by Per Unneberg
"""
Helper functions for graphics with bokeh
"""
from snakemakelib.log import LoggerManager

smllogger = LoggerManager().getLogger(__name__)

__all__ = ['create_bokeh_fig']


def _import_bokeh():
    try:
        import bokeh.plotting as plt
    except:
        raise ImportError("bokeh is not found.")

    return plt


def create_bokeh_fig(fig=None, plot_height=None, plot_width=None, **kw):
    if fig is None:
        plt = _import_bokeh()
        try:
            if plot_height is None or plot_width is None:
                smllogger.warning("plot_height and/or plot_width is None; figure will be initialized but not drawn")
            fig = plt.figure(plot_height=plot_height, plot_width=plot_width, **kw)
        except:
            raise
    return fig


FIGURE_ATTRIBUTES = {'x_range', 'y_range', 'x_axis_type', 'y_axis_type',
                     'x_minor_ticks', 'y_minor_ticks', 'x_axis_location',
                     'y_axis_location', 'x_axis_label', 'y_axis_label',
                     'tools'}


def fig_args(kwargs, keys=FIGURE_ATTRIBUTES):
    return dict([ (k, kwargs.pop(k, None)) for k in keys if k in kwargs ])
    
