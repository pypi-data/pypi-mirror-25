BreezeBlocks
============

BreezeBlocks is a query abstraction layer that takes advantage of some of the
features of the Python language more than DBAPI 2.0 modules, but provides
more lightweight result objects and more flexible querying than many ORMs for
the language.

BreezeBlocks is currently a very-early stage product. More information will
come as the codebase is developed further, but for now you can read through
the overview of the the ideas behind BreezeBlocks.

* Wanting to use a database via Python doesn't imply wanting to manage that
  database via python.
* There's not always a 1:1 matchup of the fields in the output data and the
  fields in tables.
* Information that is relevant to SQL is not always relevant in the same way
  in Python

These ideas are realized in the design of the package in these ways.

* BreezeBlocks is focused on querying. It will likely grow to handle
  insertion, updating, and deletion.
  Operations at the row-level are within the scope of the project, but
  operations at the table level and above are not.
* Query syntax does not revolve around tables. Querying is not a method on
  Table-like objects.
* Tables do not need to be fully-defined in order to be used, just defined
  enough to contain all the structural information the application needs.
* Data types and constraint information are not known on the python side.
