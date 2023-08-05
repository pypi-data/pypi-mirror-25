.. image:: https://media.quantopian.com/logos/open_source/qgrid-logo-03.png
    :target: https://qgrid.readthedocs.io
    :width: 190px
    :align: center
    :alt: qgrid

=====
qgrid
=====
Qgrid is an Jupyter notebook widget which uses `SlickGrid <https://github.com/mleibman/SlickGrid>`_ to render pandas
DataFrames within a Jupyter notebook. This allows you to explore your DataFrames with intuitive scrolling, sorting, and
filtering controls, as well as edit your DataFrames by double clicking a cell.

We originally developed qgrid for use in `Quantopian's hosted research environment
<https://www.quantopian.com/research?utm_source=github&utm_medium=web&utm_campaign=qgrid-repo>`_, but had to put it
on the backburner for a while so we could focus on higher priority projects (like developing the research environment
in which qgrid would be deployed, and adding the ability to share notebooks from that environment to the
`Quantopian forums <https://www.quantopian.com?utm_source=github&utm_medium=web&utm_campaign=qgrid-repo>`_).  So after
being initially released on github in `October of 2014
<https://twitter.com/Tim_Shawver/status/521092342162681857>`_, this project has not gotten significant attention by
Quantopian engineers, other than for the purposes of fixing critical bugs or reviewing PRs from the community.

That changed a bit in summer 2017, when we started a major refactoring project to allow qgrid to take advantage
of the latest advances in ipywidgets.  As a part of this refactoring we also moved qgrid's sorting, and filtering
logic from the client (javascript) to the server (python).


See the `\*\*\* Introducing qgrid 1.0.0 \*\*\*`_
section below for more details.

Demo
----
See the demo by viewing `qgrid_demo.ipynb
<http://nbviewer.jupyter.org/gist/TimShawver/8fcef51dd3c222ed25306c002ab89b60>`_ in nbviewer.

API Documentation
-----------------
API documentation is hosted on `readthedocs <http://qgrid.readthedocs.org/en/latest/>`_.

Installation
------------

**Python Dependencies:**

Qgrid runs on `Python 2 or 3 <https://www.python.org/downloads/>`_.  You'll also need
`pip <https://pypi.python.org/pypi/pip>`_ for the installation steps below.

Qgrid depends on the following five Python packages:

    `Jupyter notebook <https://github.com/jupyter/notebook>`_
      This is the interactive Python environment in which qgrid runs.

    `ipywidgets <https://github.com/ipython/ipywidgets>`_
      In order for Jupyter notebooks to be able to run widgets, you have to also install this ipywidgets package.
      It's maintained by the Jupyter organization, the same people who created Jupyter notebook.

    `Pandas <http://pandas.pydata.org/>`_
      A powerful data analysis / manipulation library for Python.  Qgrid requires that the data to be rendered as an
      interactive grid be provided in the form of a pandas DataFrame.

    `Semver <https://github.com/k-bx/python-semver>`_
      A Python module for semantic versioning. Simplifies comparing versions.

These are listed in `requirements.txt <https://github.com/quantopian/qgrid/blob/master/requirements.txt>`_
and will be automatically installed (if necessary) when qgrid is installed via pip.
Iv9kkfO9Kzjt8&0KbK$@sMuYDcV0euA7
**Compatibility:**

=================  ===========================  ==============================
 qgrid             IPython / Jupyter notebook   ipywidgets
=================  ===========================  ==============================
 0.2.0             2.x                          N/A
 0.3.x             3.x                          N/A
 0.3.x             4.0                          4.0.x
 0.3.x             4.1                          4.1.x
 0.3.2             4.2                          5.x
 0.3.3             5.x                          6.x
 1.0.0b0           5.x                          7.x
=================  ===========================  ==============================

**Installing from PyPI:**

Qgrid is on `PyPI <https://pypi.python.org/pypi>`_ and can be installed like this::

    # this will give you the latest beta
    pip install qgrid --pre

    # enable qgrid in your local jupyter notebook installation
    jupyter nbextension enable --py --sys-prefix qgrid

If you don't care about the new features such as handling millions of rows and using qgrid in jupyterlab,
you can install the latest stable version like this::

    # to get the latest stable version, 0.3.3
    pip install qgrid

If you need to install a specific version of qgrid, pip allows you to specify it like this::

    pip install qgrid==0.2.0

See the `Releases <https://github.com/quantopian/qgrid/releases>`_ page for more details about the versions that
are available.

**Installing from GitHub:**

The latest release on PyPI is often out of date, and might not contain the latest bug fixes and features that you
want.  To run the latest code that is on master, install qgrid from GitHub instead of PyPI::

    pip install git+https://github.com/quantopian/qgrid

\*\*\* Introducing the qgrid 1.0.0 \*\*\*
--------------------------------------------------
A new project is underway (it's merged to master, so we're currently in the beta phase) to refactor qgrid to be able
to handle displaying much larger DataFrames. By only sending the rows of the DataFrame that are currently in view and
requesting more rows from the notebook server as the user scrolls, the amount of data qgrid can display is now only
limited by the memory constraints of your server, rather than by the memory constraints of a browser tab.

To achieve the "virtual scrolling" described above while still allowing the user to sort and filter qgrid, the sorting
and filtering logic had to be moved to the server (since that's the only place where we have a copy of the entire
DataFrame). This change had the nice side effect of enabling us to keep the DataFrame that was passed in to qgrid in
sync with the sorting and filtering settings in the UI.

Also contained in this project is a bunch of work to reorganize the qgrid repository to match the latest best practices
for widget deployment and distribution (as outlined by the awesome `widget-cookiecutter <https://github.com/jupyter-widgets/widget-cookiecutter>`_
template project).  This work also simplifies qgrid's installation steps, and enables it to be used in more contexts such
as jupyterhub and jupyterlab.

To try out the latest alpha, run the following to install and enable qgrid::

  pip install qgrid --pre
  jupyter nbextension enable --py --sys-prefix qgrid

  OR

  conda install -c tim_shawver/label/dev qgrid==1.0.0a11

If you haven't enabled the ipywidgets nbextension yet, you'll need to also run this command::

  jupyter nbextension enable --py --sys-prefix widgetsnbextension

At this point you should be able to run a notebook and use qgrid as you normally would.  The only change in the API is
that the **nbinstall function no longer exists, and is now unnecessary**.  Also there are a couple of features that
are currently broken:

- Searching for a string in the text filter dropdown is broken
- Date filter is broken
- Slider filter can't reopen after setting a filter on a numpy int64 column.
- Exporting to html appears to be broken.  This was working at one point.

Other than those issues, everything else should be working though so feel free to log issues for any other problems
you find in the alpha.

To try qgrid out on Jupyterlab, run the following commands::

  pip install jupyterlab==0.25.2
  jupyter labextension install @jupyter-widgets/jupyterlab-manager@0.24.3
  jupyter labextension enable @jupyter-widgets/jupyterlab-manager
  jupyter labextension install qgrid-jupyterlab@1.0.0-dev.12
  jupyter labextension enable qgrid-jupyterlab
  jupyter lab

I don't have exporting to static html working in ipywidgets 7 yet but the
following combination of packages should work:

  notebook==5.0.0
  ipywidgets==6.0.0
  qgrid==1.0.0a0

Running the demo notebook locally
---------------------------------

The qgrid repository includes a demo notebook which will help you get familiar with the functionality that qgrid
provides.  This demo notebook doesn't get downloaded to your machine when you install qgrid with pip, so you'll need
to clone the qgrid repository to get it.  Here are the steps to clone the repository and run the demo notebook:

#. Clone the repository from GitHub::

    git clone https://github.com/quantopian/qgrid.git

#. Go to the top-level directory of the qgrid repository and run the notebook::

    cd qgrid
    jupyter notebook

   The advantage of running the notebook from the top-level directoy of the qgrid repository is the sample notebook
   that comes with qgrid will be available on the first page that appears when the web browser launches.  Here's what
   you can expect that page to look like:

     .. figure:: docs/images/home_screen.png
         :align: left
         :target: docs/images/home_screen.png
         :width: 800px

         The "notebook dashboard" for the jupyter notebook which shows all the files in the current directory.

#. Click on qgrid_demo.ipynb to open it.  Here's what that should like:

     .. figure:: docs/images/notebook_screen.png
         :align: left
         :target: docs/images/notebook_screen.png
         :width: 800px

         The demo notebook, qgrid_demo.ipynb, rendered by a locally-running Jupyter notebook.

#. Click the "Cell" menu at the top of the notebook and click "Run All" to run all the cells in the notebook and
   render a few sample qgrids.

        .. figure:: docs/images/qgrid_screen.png
         :align: left
         :target: docs/images/qgrid_screen.png
         :width: 800px

         A sample qgrid, as seen in the demo notebook, qgrid_demo.ipynb.


Running from source
-------------------

If you'd like to contribute to qgrid, or just want to be able to modify the source code for your own purposes, you'll
want to clone this repository and run qgrid from your local copy of the repository.  The following steps explain how
to do this.

#. Clone the repository from GitHub and ``cd`` into the top-level directory::

    git clone https://github.com/quantopian/qgrid.git
    cd qgrid

#. Install the current project in `editable <https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs>`_
   mode::

    pip install -e .

#. Install the node packages that qgrid depends on and build qgrid's javascript using webpack::

    cd js && npm install .

#. Install and enable qgrid's javascript in your local jupyter notebook environment::

    jupyter nbextension install --py --symlink --sys-prefix qgrid && jupyter nbextension enable --py --sys-prefix qgrid

#. Run the notebook as you normally would with the following command::

    jupyter notebook

#. If the code you need to change is in qgrid's python code, then restart the kernel of the notebook you're in and
   rerun any qgrid cells to see your changes take effect.

#. If the code you need to change is in qgrid's javascript code, repeat step 3 to rebuild qgrid's javascript, then
   refresh the browser tab where you're viewing your notebook to see your changes take effect.

Publishing a new version
------------------------

The pypi package. Change the version in _version.py and qgrid.widget.js, then run::

  python setup.py sdist
  pip install twine
  twine upload dist/qgrid-<version>.tar.gz

The npm package. Change the version in js/package.json and grid.py, then run::

  cd js && npm publish --tag next

To create a tarball locally before publishing::
Ï
  cd js && npm pack

The conda package.

  cd anaconda-recipes

Building sphinx docs
--------------------

pip install
pip install sphinx_rtd_theme
cd docs
make html
