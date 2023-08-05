Azkaban Orchestrator
====================

An Orchestrator for Azkaban pipelines

Quick Start
----------
.. code-block:: console

    pip install azkaban-orchestrator

Define Orchestration logic
--------------------------
Create a file and define the dependencies between pipelines using the following notation.

* Pipeline name is a project name in Azkaban. Project and flow name of a pipeline should be the same.
* use '->' for **hard dependency** between two pipelines. A -> B means B runs if A runs successfully.
* use '.>' for **soft dependency** between two pipelines. A .> B means B runs after A despite A runs successfully or not.
* if pipeline has some **parameters** put them in parentheses by the pipeline name like A(status=1|date). use vertical bar '|' to separate the parameters.
* to define **clusters** use colon ':' e.g. S: A,B,C means cluster S includes pipelines A,B and C. to move from one cluster all the pipelines within the cluster should run successfully.

Sample 1
--------

.. code-block:: console

    ----------
    |  a  b  | s1
    ----------
        |
        v
    ----------
    |  c  d  | s2
    ----------
        |
        v
        e

Sample1 diagram file

.. code-block:: console

    s1 : a, b
    s2 : c, d
    s1 -> s2
    s2 -> e

     
Sample 2
--------

.. code-block:: console

    a -> b -> d(date)
    |     ___/|
    |    |    |
    v    v    v
    c -> e <- f(status=1)
    |
    v
    f(status=2)

Sample2 diagram file

.. code-block:: console

    a -> b
    b -> d(date)
    d(date) -> f(status=1)
    d(date) -> e
    f(status=1) -> e
    a -> c
    c -> e
    c -> f(status=2)


Usage
-----
To run the orchestrator

.. code:: python

    import logging
    from azkaban_orchestrator import orchestrator

    client = orchestrator.Client(
        diagram_file_name='/path/to/diargam_file',
        host='azkaban_host',
        username='azkaban_username',
        password='azkaban_passwpord',
        logger=logging.getLogger(__name__)
    )

    # define the parameters need to pass to the orchestrator
    params = {'date':'20171202'}

    # define the initial pipeline
    # if you need to start orchestration from a specific pipeline
    initial = None

    client.run(initial, params)

To draw the diagram

.. code:: python

    from azkaban_orchestrator import diagram

    d = diagram.Diagram('test diagram', 'path/to/diagram_file')
    d.show()
