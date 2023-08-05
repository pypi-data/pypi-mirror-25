Simple AWS Lambda Maker
=======================

This is a super simple tool for creating/modifying multiple lambda functions.

It was built for the purpose of deploying our Alexa skills across multiple
regions in the same account.

Installation
------------

Just use pip::

  $ pip install simple-aws-lambda-maker

Then create a ``salm.yml`` with something like:

.. code-block:: yaml

  ---

  function_defaults:
    filepath: "{config_root}/lambda_function.py"
    runtime: "python2.7"
    role: "arn:aws:iam::1234567890:role/lambda_basic_execution"
    timeout: 8
    handler: "lambda_function.lambda_handler"

  functions:
    - name: test
      region: us-east-1
      description: "Test function"
      env:
        ONE: "1"
        TWO: "2"
      tags:
        three: "four"

    - name: test2
      region: us-east-1
      description: "Test function 2"
      env:
        ONE: "3"
        TWO: "4"
      tags:
        three: "four"

Here we are creating two functions, one called test and another called test2.
They are both put into ``us-east-1`` and have different values for the ``ONE``
and ``TWO`` environment variables.

Both also have the options in the ``function_defaults`` block, which includes
a reference to a file relative to this file called ``./lambda_function.py``

For example:

.. code-block:: python

  import os
  def lambda_handler(event, context):
      return "{0} - {1}".format(os.environ["ONE"], os.environ["TWO"])

We can then determine if anything will be created or changed by going into that
directory and saying::

  $ salm deploy --dry-run

And then to actually apply those changes::

  $ salm deploy
