CADBIOM (Computer Aided Design of Biological Models) is an open source modelling software.
Based on Guarded transition semantic, it gives a formal framework to help the modelling of
biological systems such as cell signaling network.

Official website: [link](http://cadbiom.genouest.org/)


# Installation

## System requirements

CADBIOM is mainly developed in Python 2.7.
Before running Cadbiom, the following system packages have to be installed from
the distribution packages library (or similar, depending on your operating system):

* python2.7-dev
* libxml2-dev
* libxslt1-dev
* libgraphviz-dev (Networkx layouts)
* pkg-config (Fix errors when installing pygraphviz and when config is not loaded)
* libpng12-dev (Matplotlib)
* libfreetype6-dev (Matplotlib)
* python-glade2 (GUI)
* python-gtk2 (GUI)
* python-gtksourceview2 (GUI)
* python-tk (GUI)


Fix errors when installing pygraphviz and when config is not loaded:

* pkg-config

For Matplotlib installation:

* libpng12-dev
* libfreetype6-dev

You can install these dependencies with the following command (on Debian-like systems):

    sudo apt-get install python-gtksourceview2 python2.7-dev libxml2-dev libxslt1-dev \
    libxslt1-dev libgraphviz-dev pkg-config python-glade2 python-gtk2 python-tk libpng12-dev libfreetype6-dev

PS: Most of these packages are already installed on basic Debian-like systems.

## Python requirements

When `cadbiom` library is installed, the following Python packages
will be installed from pypi repository:

* lxml
* networkx
* pygraphviz
* matplotlib
* numpy
* pycryptosat


### Virtual environment

This is not a mandatory step but it is a good practice to use virtual environments
to separate projects from each other.

* Install virtualenvwrapper:

    pip install virtualenvwrapper


* Edit your .bashrc or .zshrc file to source the virtualenvwrapper.sh script with these lines:

    export WORKON_HOME=~/.virtualenvs
    mkdir -p $WORKON_HOME
    source /usr/bin/virtualenvwrapper.sh

The location of this script may vary depending on your Linux distro


* Restart your terminal or run:

    source /usr/bin/virtualenvwrapper.sh


* Create your virtualenv:

    mkvirtualenv cadbiom -p /usr/bin/python2.7


* Later if you want to reactivate the virtualenv:

    workon cadbiom


### SAT solver

Cadbiom software requires a SAT solver which is
proposed as a Python wrapper by an independant library (pycryptosat).

*For now, an non official version of pycryptosat is on pypi and it is used by packages;

Source of the fork if you want to compile it manually:
[Cryptominisat repository](https://github.com/msoos/cryptominisat/tree/5.0.1)*

Here you will find the installation commands of the pycryptosat package:

    git clone --branch 5.0.1_cmake_dev git@gitlab.irisa.fr:0000B8EG/pycryptosat.git
    cd pycryptosat
    mkdir build && cd build && cmake ../
    make python_interface_install


### Cadbiom

If you want to install from pypi, just do:

    pip install cadbiom-cmd
    pip install cadbiom-gui


If you want to install the library with its GUI, and command line in one command,
after the git clone step, just do:

    make install

---

For the library itself:

* From Python Package Index:

    pip install cadbiom_cmd


* From the current repository

    cd library && make install


For the command line tool:


* From Python Package Index:

    pip install cadbiom_cmd


* From the current repository

    cd library && make install
    cd ../command_line && make install


For the GUI:

* From Python Package Index:

    pip install cadbiom_gui


* From the current repository

    cd library && make install
    cd ../gui && make install


# Structure of packages

The library contains the cadbiom folder with 4 modules:

    antlr3 (folder)
    bio_models (folder)
    models (folder)

The command line tool exposes the command `cadbiom_cmd` to the current context.

The gui package exposes the command `cadbiom` to the current context.


# Utilization

## Command line

### General:

    $ cadbiom_cmd -h

    usage: cadbiom_cmd [-h] [-vv [VERBOSE]]
                        {compute_macs,sort_solutions,parse_trajectories,merge_cams}
                        ...

    optional arguments:
    -h, --help            show this help message and exit
    -vv [VERBOSE], --verbose [VERBOSE]

    subcommands:
    {compute_macs,sort_solutions,parse_trajectories,merge_cams}
        compute_macs        Parse arguments and launch Cadbiom search of MACs
                            (Minimal Activation Conditions). - If there is no
                            input file, there will be only one process. - If an
                            input file is given, there will be 1 process per line
                            (per logical formula on each line). - all_macs: Solver
                            will try to search all macs with 0 to the maximum of
                            steps allowed. - continue: If there is a mac file from
                            a previous work, last frontier places will be
                            reloaded.
        sort_solutions      Parse a solution file and sort all frontier places in
                            alphabetical order.
        parse_trajectories  Parse a complete solution file and make a
                            representation of trajectories.
                            The output is in graphml file format and is exported
                            in 'graphs' directory. .. note:: Requires the
                            model file.
        merge_cams          Merge solutions to a csv file. .. note:: CSV file:
                            <Final property formula>;<cam>
        model_comp          Model consistency checking. Check if the 2 given
                            models have the same topology, nodes & edges
                            attributes/roles. .. note:: You can export a graphml
                            file for the 2 models.
        model_infos         Model informations. Get number of nodes, edges,
                            centralities (degree, closeness, betweenness). ..
                            note:: You can export a graphml file for model.


### compute_macs:

    usage: cadbiom_cmd compute_macs [-h] [--input_file [INPUT_FILE]]
                                    [--combinations] [--steps [STEPS]]
                                    [--all_macs] [--continue]
                                    [--start_prop [START_PROP]]
                                    [--inv_prop [INV_PROP]] [--output [OUTPUT]]
                                    chart_file [final_prop]

    positional arguments:
    chart_file
    final_prop

    optional arguments:
    -h, --help            show this help message and exit
    --input_file [INPUT_FILE]
    --combinations
    --steps [STEPS]
    --all_macs
    --continue
    --start_prop [START_PROP]
    --inv_prop [INV_PROP]
    --output [OUTPUT]


### parse_trajectories:

    usage: cadbiom_cmd parse_trajectories [-h] chart_file sol_file

    positional arguments:
    chart_file
    sol_file

<br>
* Result:

[image](examples/graph_example_with_legend.png)

* Cytoscape styles:

[file](examples/cytoscape_styles.xml)


### sort_solutions:

    usage: cadbiom_cmd sort_solutions [-h] sol_file

    positional arguments:
    sol_file


### merge_cams:

    usage: cadbiom_cmd merge_cams [-h] [--output [OUTPUT]] [solutions_directory]

    positional arguments:
    solutions_directory


### model_comp:

    usage: cadbiom_cmd model_comp [-h] [--make_graphs] model_file_1 model_file_2

    positional arguments:
    model_file_1
    model_file_2

    optional arguments:
    -h, --help     show this help message and exit
    --graphs
    --json
    --output [OUTPUT]

<br>

Usage in scripts:

    >>> from cadbiom_cmd.solution_repr import graph_isomorph_test
    >>> print(graph_isomorph_test('test.bcx', 'test2.bcx', output_dir='graphs/',
        make_graphs=False, make_json=False))
    INFO: 3 transitions loaded
    INFO: 3 transitions loaded
    INFO: BUILD GRAPH FOR SOL: Connexin_32_0 Connexin_26_0
    INFO: BUILD GRAPH FOR SOL: Connexin_32_0 Connexin_26_0
    INFO: Topology checking: True
    INFO: Nodes checking: True
    INFO: Edges checking: True
    {u'nodes': True, u'edges': True, u'topology': True}


### model_infos

    usage: cadbiom_cmd model_infos [-h] [--graph] [--json] [--output [OUTPUT]]
                                model_file

    positional arguments:
    model_file

    optional arguments:
    -h, --help         show this help message and exit
    --graph
    --json
    --output [OUTPUT]


## Graphical User Interface

Usage:

    $ cadbiom


## Logging

Logs are stored in the system temporary dictory:

* On Windows, the directories C:\TEMP, C:\TMP, \TEMP, and \TMP, in that order.
* On all other platforms, the directories /tmp, /var/tmp, and /usr/tmp, in that order.
* As a last resort, the current working directory.


# License

CADBIOM is freely available on cadbiom.genouest.org,
and distributed under the terms of the GNU General Public License.
