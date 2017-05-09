Design Considerations
=====================


2017-05-09
----------

Initially starting with a very loose data structure to try to accommodate for very different structures across different data sets. Once we have more data stored we can decide if and what we need to structure more definitively.

There 'may' be a user need for an administrator or superuser to to define necessary attributes across different data types without the need for application development/release.

Each attribute should have a data type.

There will most likely be a need to search/filter on attributes for each Item.

Items may need to link to other items in many-to-many, one-to-many, many-to-one and one-to-one relationships.

Item Types (eg Software, API etc.) may need to be nested in a tree structure. (Other option is a flat list of tags)

An 'Owner' can be considered to be someone who is a user of the system and will therefore have a user account or one will be created.
