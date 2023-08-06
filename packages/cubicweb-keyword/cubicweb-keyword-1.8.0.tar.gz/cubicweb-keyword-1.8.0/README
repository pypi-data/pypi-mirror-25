Summary
-------
The `keyword` cube provides classification by using hierarchies of keywords to
classify content.

Each classification is represented using a `Classification` entity, which will
hold a keywords tree.

There is two types of keywords:

- `Keyword` which contains a description,

- `CodeKeyword` which contains the keyword description and the associated code.

In order to link an entity to a keyword, you have to add a relation
 `applied_to` in the schema.

Each keyword has the `subkeyword_of` relation definition. This allows to
navigate in the classification without a Modified Preorder Tree Traversal
representation of the data.

Some methods are defined in order to get parents and children or get the status
of a keyword (leaf or root).

See also `cubicweb-tag`_ as another (simpler) way to classify content.

.. _`cubicweb-tag`: http://www.cubicweb.org/project/cubicweb-tag