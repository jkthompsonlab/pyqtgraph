# -*- coding: utf-8 -*-
"""
MultiPlotItem.py -  Graphics item used for displaying an array of PlotItems
Copyright 2010  Luke Campagnola
Distributed under MIT/X11 license. See license.txt for more information.
"""
from . import GraphicsLayout
from ..metaarray import *

__all__ = ['MultiPlotItem']


class MultiPlotItem(GraphicsLayout.GraphicsLayout):
    """
    :class:`~pyqtgraph.GraphicsLayout` that automatically generates a grid of
    plots from a MetaArray.

    .. seealso:: :class:`~pyqtgraph.MultiPlotWidget`: Widget containing a MultiPlotItem
    """

    def __init__(self, *args, **kwds):
        GraphicsLayout.GraphicsLayout.__init__(self, *args, **kwds)
        self.plots = []

    def plot(self, data, **plotArgs):
        """Plot the data from a MetaArray with each array column as a separate
        :class:`~pyqtgraph.PlotItem`.

        Axis labels are automatically extracted from the array info.

        ``plotArgs`` are passed to :meth:`PlotItem.plot
        <pyqtgraph.PlotItem.plot>`.
        """
        #self.layout.clear()

        if hasattr(data, 'implements') and data.implements('MetaArray'):
            if not ((data.ndim != 2) != (data.ndim != 3)):
                raise Exception("MultiPlot currently only accepts 2D or 3D MetaArray.")
            ic = data.infoCopy()
            if data.ndim < 3:
                ax = 0
                for i in [0, 1]:
                    if 'cols' in ic[i]:
                        ax = i
                        break
                #print "Plotting using axis %d as columns (%d plots)" % (ax, data.shape[ax])
                for i in range(data.shape[ax]):
                    pi = self.addPlot()
                    self.nextRow()
                    sl = [slice(None)] * 2
                    sl[ax] = i
                    pi.plot(data[tuple(sl)], **plotArgs)
                    #self.layout.addItem(pi, i, 0)
                    self.plots.append((pi, i, 0))
                    info = ic[ax]['cols'][i]
                    title = info.get('title', info.get('name', None))
                    units = info.get('units', None)
                    pi.setLabel('left', text=title, units=units)
                info = ic[1-ax]
                title = info.get('title', info.get('name', None))
                units = info.get('units', None)
                pi.setLabel('bottom', text=title, units=units)
            elif data.ndim == 3:
                ax_rows = 1
                ax_traces = 0
                ax_data = 2
                colors = ["#d9d9d9bb","#ff333399"]
                symbols = ["x","-"]
                if not (('cols' in ic[ax_rows]) and ('cols' in ic[ax_traces])):
                    raise Exception(""" 3D MultiPlot needs 3D MetaArray with first dimension: 
                                    different data traces/runs to be plotted on top of each 
                                    other, second dimension: different data traces/runs to 
                                        be plotted below each other, third dimension: data. """)
                #print "Plotting using axis %d as columns (%d plots)" % (ax, data.shape[ax])
                for i in range(data.shape[ax_rows]):
                    pi = self.addPlot()
                    self.nextRow()
                    for trace_idx in range(data.shape[ax_traces]):
                        sl = [slice(None)] * 3
                        sl[ax_rows] = i
                        sl[ax_traces] = trace_idx
                        #print(data[tuple(sl)])
                        pi.plot(data[tuple(sl)], pen=colors[trace_idx], symbol=symbols[trace_idx] **plotArgs)
                    #self.layout.addItem(pi, i, 0)
                    self.plots.append((pi, i, 0))
                    info = ic[ax_rows]['cols'][i]
                    title = info.get('title', info.get('name', None))
                    units = info.get('units', None)
                    pi.setLabel('left', text=title, units=units)
                info = ic[ax_data]
                title = info.get('title', info.get('name', None))
                units = info.get('units', None)
                pi.setLabel('bottom', text=title, units=units)
        else:
            raise Exception("Data type %s not (yet?) supported for MultiPlot." % type(data))

    def close(self):
        for p in self.plots:
            p[0].close()
        self.plots = None
        self.clear()
