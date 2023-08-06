pobo
====

Usage
-----

.. code:: python

    from pobo import Parser

    parser = Parser("file.obo")

    parser.headers.get("format-version")
    parser.headers.get("...")

    for stanza in parser:
        stanza.name
        stanza.tags

        for tag, value in stanza.tags.items():
            ...


include modifiers
-----------------

.. code:: python

    parser = Parser("file.obo", include_modifiers=True)

    ...

    for tag, value in stanza.tags.items():
        value.value
        value.modifiers



