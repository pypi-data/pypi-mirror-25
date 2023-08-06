json-graph-repl
===============

Extensible command-line REPL for interacting with JSON graphs containing
business objects.

The JSON format is based on the ``json-graph`` specification at:
https://github.com/jsongraph/json-graph-specification

Several additional assumptions are made:

-  We assume that the graph contains no cycles
-  We treat node IDs as case-insensitive
-  There are certain ``metadata`` fields that some aspects of the tool
   depend on (but none of these are mandatory)

Sample graphs are provided in the ``tests`` directory.

To use from the command line, just point the ``jgrepl`` tool to your
JSON graph:

::

    $ ./jgrepl/jgrepl.py tests/food-graph.json 

Once in the REPL, type ``help`` for the list of available commands. Use
``ctrl-d`` to exit.

Here is a sample session using the "food" graph:

::

    *** Loading graph from 'tests/food-graph.json'...
    JSON Graph REPL v.0.1.2
    /> info         // The `info` command displays information about the current node or graph
    CURRENT GRAPH: Sample Food Graph ('tests/food-graph.json')
    GRAPH TYPE: food graph
    NODES: 14
    EDGES: 11
    {                     // All metadata is shown here:
        "version": "1.0"  
    }

    /> ls -l
    CAT1 category Vegetables
    CAT2 category Fruits
    CAT3 category Sweets

    /> cd CAT3          // Change to a new path. Note the prompt changes to reflect your location. 
    /CAT3> info
    NODE ID: cat3
    NODE TYPE: category
    NODE LABEL: Sweets
    {
        "available_from": "2017-07-18",
        "available_to": "2017-11-18"
    }

    /CAT3> find food8  // Print all paths to this node ID
    /CAT3/CAT32/FOOD8

    /CAT3> cd $    // Switch to the last shown path
    /CAT3/CAT32/FOOD8> 


