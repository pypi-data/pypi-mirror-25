Hivemind Plus
=============

Hivemind Plus is a Python library to assist with the creation of
instances and processing of results on the Hivemind platform. Before you
use this library you will need to register for an API key via the
website.

Installation
------------

.. code:: sh

    $ pip install hivemind-plus

Usage
-----

In order to use Hivemind Plus you must create an instance configuration,
a result configuration or both. Each type of configuration ships with a
``ConfigBuilder`` class which helps you to assemble your configuration.

Instance Configuration
~~~~~~~~~~~~~~~~~~~~~~


.. code:: python

    from hivemindplus import instance

    instance_config = (
        instance.ConfigBuilder()
            .with_connection_string('DRIVER={SQL Server};SERVER=localhost;DATABASE=DB;') # ODBC style connection string 
            .with_query('SELECT PeopleId, FullName FROM dbo.People') # Query to drive instances
            .with_key('PeopleId') # Column name to use as unique identifier for an instance 
            .with_name('FullName') # Column name to use as a human readable identifier
            .with_tags(['FullName']) # (Optional) Columns to tag instances with
            .with_instructions('instructions.md', ['FullName']) # (Optional) Template markdown file and values
            .with_schema('schema.json', ['Id', 'FullName']) # (Optional) Schema template json file and values
            .with_qualifications_query('SELECT PeopleId, Qualification FROM dbo.Qualifications') # (Optional) Query for qualifications
            .build()
    )

Result Configuration
~~~~~~~~~~~~~~~~~~~~


.. code:: python

    from hivemindplus import result

    # Executed for every agreed upon result
    def output_fn(res):
        print('Output function')
        print(str(res))


    # Custom agreement function that compares two results
    def agreement_fn(a, b):
        return a['data'] == b['data']


    result_config = (
        result.ConfigBuilder()
            .with_connection_string('DRIVER={SQL Server};SERVER=localhost;DATABASE=DB;') # ODBC style connection string
            .with_instance_table('dbo.InstanceResults') # (Optional) Override default name of instance results table
            .with_iteration_table('dbo.IterationResults') # (Optional) Override default name of iteration results table
            .with_output_function(output_fn) # (Optional) Function to execute on agreed upon result
            .with_agreement_function(agreement_fn, 0.51) # (Optional) Function to determine agreement
            .with_feedback_function(feedback_fn) # (Optional) Function executed with instance/iteration results for integration of feedback
            .with_max_iterations(5) # (Optional) Max number of iterations to retry agreement checking with
            .build()
    )

Workflow Configuration
~~~~~~~~~~~~~~~~~~~~~~


.. code:: python

    from hivemindplus import workflow

    flow = (
        workflow.Builder()
            .with_api_url('https://client.sandbox.hvmd.io') # URL of the API without a trailing /
            .with_api_key('API-KEY') # Personal API key
            .with_task_id(0) # Task that you want to manage
            .with_instance_config(instance_config) # (Optional) instance configuration
            .with_result_config(result_config) # (Optional) result configuration
            .with_auto_submission() # (Optional) submit task if not already submitted
            .build()
    )

    # Start the workflow
    flow.start()

Examples
--------

A full set of examples can be found in the ``/examples`` directory.

Development
-----------

To begin development, you will need to install all the required
development packages.

.. code:: sh

    $ pip install .[test]

All the source code resides within the ``/hivemindplus`` directory and
the tests can be ran from the project root directory as shown below.

.. code:: sh

    python -m pytest

