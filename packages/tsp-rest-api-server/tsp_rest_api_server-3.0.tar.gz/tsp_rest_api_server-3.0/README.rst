.. image:: https://raw.githubusercontent.com/caputomarcos/tsp-rest-api-server/master/logotipo-pickngo.png



tsp-rest-api-server
===================


TSP Rest Api Server - Rest Api Server using Dijsktra's algorithm applied to travelling salesman problem.


License
-------
Licensed under the MIT License.


Install
-------

Follow the steps below to get everything up and running.


pip
---


1. Create project folder:

   .. code-block:: bash

        $ mkdir tsp-rest-api-server && cd tsp-rest-api-server

2. Create virtualenv in the normal way:

   .. code-block:: bash

        $ virtualenv env --python=python

3. Active your new virtualenv:

   .. code-block:: bash

        $ source env/bin/activate


4. Install tsp-rest-api-server:

   .. code-block:: bash

        $ pip install tsp-rest-api-server


5. Create setting file:

   .. code-block:: bash

        $ tsp_rest_api_server settings

6. Run tsp rest api server:

   .. code-block:: bash

        $ tsp_rest_api_server runserver



Git
----

1. Clone repository:

   .. code-block:: bash

        $ git clone git@github.com:caputomarcos/tsp_rest_api_server.git

2. Go to tsp_rest_api_server source folder:

   .. code-block:: bash

        $ cd tsp-rest-api-server/

3. Create virtualenv in the normal way:

   .. code-block:: bash

        $ virtualenv env --python=python

4. Active your new virtualenv:

   .. code-block:: bash

        $ source env/bin/activate


5. Create dev environment:

   .. code-block:: bash

        $ make develop


Usage
------

1. Create routes:

   .. code-block:: bash

        $ curl -d "@map.json"  -H "Content-Type: application/json" -X POST http://0.0.0.0:5000/maps

        or

        $ curl -d '{ "title":"Sao Paulo", "routes":[{"origin":"A","destiny":"B","distance":10},{"origin":"B","destiny":"D","distance":15},{"origin":"A","destiny":"C","distance":20},{"origin":"C","destiny":"D","distance":30},{"origin":"B","destiny":"E","distance":50},{"origin":"D","destiny":"E","distance":30}]}' -H "Content-Type: application/json" -X POST http://0.0.0.0:5000/maps


3. Search shortest route:

   .. code-block:: bash

        $ curl 'http://0.0.0.0:5000/maps/shortest?map=Sao%20Paulo&origin=A&destiny=D&price=2.50&autonomy=10'

        {
          "data": [
            {
              "Path": "['A', 'B', 'D']"
            },
            {
              "Total KM": "25.00"
            },
            {
              "Cost": "6.25"
            }
          ]
        }


Links
-----

* `DIJKSTRA'S SHORTEST PATH ALGORITHM  <http://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php>`_


