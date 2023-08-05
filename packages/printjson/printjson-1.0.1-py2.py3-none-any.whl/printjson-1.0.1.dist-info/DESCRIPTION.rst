Utility for pretty JSON output
==============================

Simple python utility for using in shell scripts.

Features
--------

- Print colorized JSON
- Minimized and formatted output
- Output elements by keys and indexes
- Check JSON for correctness
- Automatically disabling color sequences, when prints to pipeline, file or other non-tty output

Examples
--------

- test.json

.. code-block:: json

        {
          "arr": [
            123,
            "λάμβδα ラムダ lambda",
            [
              "1",
              "2"
            ]
          ],
          "test": "test"
        } 

- Colorized indented

.. code-block:: bash

        printjson test.json

- Minimized monochrome

.. code-block:: bash

        printjson -om test.json

Result:

.. code-block:: json

        {"test":"test","arr":[123,"λάμβδα ラムダ lambda",["1","2"]]}

- Print third entry of "arr" array, using "__" as delimiter

.. code-block:: bash

        printjson -k 'arr__2' -d '__' test.json

Result:

.. code-block:: json

        [
          "1",
          "2"
        ]





