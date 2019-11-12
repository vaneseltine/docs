graphviz
########

https://graphviz.gitlab.io/documentation/

https://graphviz.gitlab.io/gallery/


sphinx integration
==================

Happily, :ref:`Sphinx` comes with graphviz batteries included.

.. graphviz::

    digraph graphname {
        graph [rankdir=LR, bgcolor="transparent"]
        a -> b
        b -> c -> d
        b -> e -> f -> g
        d -> g
    }
