ezdashboard
===========

1 - Overview
------------

| **ezdashboard** stands for easy dashboard.
| The purpose of this module is to enable fast creation of good looking
  dashboards from several raw HTML contents.

-  Each tile contains and display an HTML+JS+CSS content
-  IMPORTANT: The HTML and JS must be written so as to avoid collision
   inter-tiles

   -  No scope is added by this module
   -  Content is pasted as-is

-  In this demo the tile contents are just some text and a background
   color - but could be anything.
-  The content can be created in any way but for a Python user I
   recommend:

   -  *`matplotlib <https://matplotlib.org/>`__* for static graphs of
      artitrary complexity. See the
      `gallery <https://matplotlib.org/gallery.html>`__ for inspiration
   -  *`ezhc <https://github.com/oscar6echo/ezhc>`__* (thin wrapper
      around `highcharts <https://www.highcharts.com/demo>`__) for 2D
      graphs
   -  *`ezvis3d <https://github.com/oscar6echo/ezvis3d>`__* (thin
      wrapper around
      `visjs/graph3d <http://visjs.org/graph3d_examples.html>`__) for 3D
      graphs
   -  *`toyplot/tables <https://toyplot.readthedocs.io/en/stable/table-coordinates.html>`__*
      for tables

.. figure:: img/ezdashboard_snapshot.gif
   :alt: 

*Mouse or keyboard navigation across tab* ## 2 - Install

From command line:

::

    pip install ezdashboard

3 - Notebook
------------

Read the userguide and run a demo in the `demo
notebook <http://nbviewer.jupyter.org/urls/gitlab.com/oscar6echo/ezdashboard/raw/master/demo_ezdashboard.ipynb>`__.

Open the `demo
dashboard <https://gitlab.com/oscar6echo/ezdashboard/blob/master/sample/index_sample.html>`__
produced (standalone HTML file) in your browser - similar to the
animated gif above.

.. raw:: html

   <!-- pandoc --from=markdown --to=rst --output=README.rst README.md -->
