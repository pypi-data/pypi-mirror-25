=====
Usage
=====

To use taxydromikilib in a project:

.. code-block:: python

    from taxydromikilib import Taxydromiki
    taxydromiki = Taxydromiki()
    states = server.search(VALID_PACKAGE_NUMBER)

    for state in states:
        if state.is_final:
            print('This state concludes the delivery of the packet')
        print(state.status)
        print(state.location)
        print(state.date)
        print(state.time)
