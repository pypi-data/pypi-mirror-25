=====
Usage
=====

To use ``mutaprops`` in a project::

    from mutaprops import *

Decorating classes
------------------

``mutaprops`` are created by decorating classes with some custom decorators,
much like the usage of the `@property`_ decorator. Those decorators enable the
property manager to see the properties and track their state.

@mutaprop_class [:func:`~mutaprops.decorators.mutaprop_class`]
    is the mandatory class decorator which enable objects instantiated from the
    decorated classes to be tracked by the property manager.

@mutaproperty [:func:`~mutaprops.decorators.mutaproperty`]
    is the basic decorator. Any attribute decorated with ``@mutaproperty``
    becomes visible in the UI. The arguments of ``@mutaproperty`` allow to define
    the type of the parameter (that defines the UI widget), it's display name,
    numerical ranges, the position/category in the UI etc.

    The docstring of the attribute is displayed as help in the UI. Any change
    to this attribute during run-time is reflected in the UI. Any change in the
    UI causes change of the attribute's value.

    Same as with usual properties, ``@mutaproperty`` can be read only, either by
    not defining a setter function, or by explicitly setting it to
    ``read_only``.

    Most parameters of the ``@mutaproperty`` can be assigned as a constant, or
    as a reference to another ``@mutaproperty`` or ``@mutasource``. Change of a
    referred ``@mutaproperty`` then causes UI update of the referee.

    All optional parameters can be specified either in getter or in setter
    decorator, it doesn't matter which.

@mutaprop_action [:func:`~mutaprops.decorators.mutaprop_action`]
    is basically a simplified version of ``@mutaproperty``. It's represented as
    a button on UI level, and causes direct function call of the decorated
    function when the button is pressed.

@mutasource [:func:`~mutaprops.decorators.mutasource`]
    is best described as a "hidden mutaproperty". ``@mutasource`` is not
    directly visible, but it's changes are propagated to the UI. It can be used
    to implement some controller (as in MVC) functionality which would be hard
    to do with ``@mutaproperty`` alone.

All above-mentioned decorators wrap the original class implementation and add
some extra functionality. None of it is used, however, if the instantiated
objects are not registered with the UI manager. One therefore doesn't need to be
concerned about the functionality/performance impact of the decorators
on the original class.


Setting up an UI manager
------------------------

:class:`~mutaprops.managers.HttpMutaManager` does all the heavy-lifting,
providing data from registered object to the UI front-end and tracking
the object changes and user actions. It runs on aiohttp_.

UI manager is basically a REST service (the UI front-end is a HTML5 app) with
additional websocket component.

Apart of the bi-directional object data update, the manager is also responsible
for forwarding the registered logger messages to the front-end, and also serving
static files (the HTML5 app blob and custom user data).

Using external Asyncio loop
+++++++++++++++++++++++++++

By default, the manager would create a new loop upon start. If the application
is using :mod:`asyncio` as well, manager can be specified to use the
application's loop.

.. code-block:: python

    import asyncio
    from mutaprops import *

    loop = asyncio.get_event_loop()

    # Some nice async code

    man = HttpMutaManager("Some manager", loop=loop)

Custom static files
+++++++++++++++++++

UI manager can serve a custom static files as well. This can be utilized
in several ways:

* providing image files for the auto-documentation
* providing logos and custom stylesheets for the UI customization

All custom files must be placed in one directory structure, the path to this
directory can be specified as the ``local_dir`` argument.

.. code-block:: python

    from mutaprops import *

    man = HttpMutaManager("Some manager", loop=loop,
                          local_dir="path/to/custom/dir")

The contents of the ``local_dir`` will be served in the path ``/local``.

Custom style modification
+++++++++++++++++++++++++

To modify the UI look-and feel, one can produce a custom stylesheet and override
the stylesheet in ``mutaprops/web_ui/dist/base.css``.

This stylesheet must be called ``custom.css`` and must be placed in the
``local_dir``. Any additional asset files (logos, images etc.) must be placed
there as well.


UI self-documentation and help files
++++++++++++++++++++++++++++++++++++

Each parameter is documented with its own docstring (ReST_ can be used for
formatting).

On top of that, an additional help text can be displayed in the help window
(activated by the help link in the menu bar).
This text is specified as the ``help_doc`` argument, the content must be a
string containing HTML code.

To translate a ReST_ text into suitable ``help_doc``,
the :func:`mutaprops.utils.rest_to_html` can be used.

.. code-block:: python

    from mutaprops import *
    from mutaprops.utils import rest_to_html

    help = """
    Help-less
    ---------

    This help is of *NO USE* at all!
    """

    man = HttpMutaManager("Some manager", loop=loop,
                          local_dir="path/to/custom/dir",
                          help_doc=rest_to_html(help))

Log forwarding
++++++++++++++

UI manager is capable of forwarding the :mod:`logging` messages to the HTML UI.
In order to do so, a logger has to be registered with the manager using the
``proxy_log`` argument.

.. code-block:: python

    from mutaprops import *
    import logging

    logger = logging.getLogger(__name__)

    man = HttpMutaManager("Some manager", loop=loop,
                          local_dir="path/to/custom/dir",
                          proxy_log=logger)

By default, all log messages are forwarded. The log level can be further
specified by the ``log_level`` argument.

Manager clustering and chaining
+++++++++++++++++++++++++++++++

Several running UI manager instances can be connected into one *master* manager.
This feature can be used for example to create a joint UI console for
several headless machines (e.g. RPi's) that are used in a cluster,
each running it's mutaprops UI.

Furthermore, such clusters can be chained (a master manager connects to another,
higher-level master manager). There is no fixed limit for such chains, however
in practice the latencies will increase with each chain link.


.. code-block:: python

    # Running on machine 192.168.1.1
    from mutaprops import *

    man = HttpMutaManager("Some master manager")
    dead_parrot = SomeDecoratedClass()
    dead_parrot.muta_init("Parrot #1")
    man.add_object(dead_parrot)
    man.run(port=9000)


.. code-block:: python

    # Running on machine 192.168.1.2
    from mutaprops import *

    man = HttpMutaManager("Some slave manager",
                          master='http://192.168.1.1:9000')
    dead_parrot = SomeDecoratedClass()
    dead_parrot.muta_init("Parrot #2")
    man.add_object(dead_parrot)
    man.run(port=9000)

In the above example, the ``Parrot #2`` will appear in the UI served at
``http://192.168.1.1:9000``, alongside the ``Parrot #1``

At the same time, it will be also accessible from it's own UI served at
``http://192.168.1.2:9000``. Any change on any of those UI's will be reflected
on the other UI as well.


Registering and unregistering objects with UI manager
-----------------------------------------------------

Once an object is instantiated from the muta-decorated class, there is nothing
special going on with it until the mutaproperties are initialized and registered
with the UI manager.

To initialize the mutaproperties,
the :meth:`~mutaprops.mutaprops.MutaPropClass.muta_init` must be called.
During this initialization process, an ID (UI-visible name) is assigned to
a given object.

.. code-block:: python

    from mutaprops import *

    dead_parrot = SomeDecoratedClass()
    dead_parrot.muta_init("Parrot #1")  # ID is assigined to the dead_parrot instance.

After mutaproperties are initialized, the object can be added to an existing
UI manager using :meth:`~mutaprops.managers.HttpMutaManager.add_object`.

.. code-block:: python

    man = HttpMutaManager("Some master manager")
    man.add_object(dead_parrot)

The whole process can be simplified by initializing the mutaproperties when
adding the object to the manager

.. code-block:: python

    dead_parrot = SomeDecoratedClass()
    man = HttpMutaManager("Some master manager")
    man.add_object(dead_parrot, "Parrot #1")  # Mutaproperties initialized while adding

Objects that were once added to the manager can be removed in the similar
fashion using the :meth:`~mutaprops.managers.HttpMutaManager.add_object`.

.. code-block:: python

    man.remove_object(dead_parrot)

Running the manager
-------------------

UI manager is basically just a server, and need to be run. In case of
asyncio-based application, this is very simple, just as starting any sort of
server.

.. code-block:: python

    # Continuing the example above

    man.run(port=9000)

In case the rest of your application is not asyncio based and there are other
tasks which has to be run alongside the user-initiated actions, it's possible to
run the UI manager in a separate thread.

.. code-block:: python

    # Continuing the example above

    man.run_in_thread(port=9000)


This feature is not very well tested, and by definition opens all sort of
synchronization problems which needs to be dealt with by the implementator.
*Use at your own risk!*.

Run parameters
++++++++++++++

UI manager is built on the top of the aiohttp_ server, it's therefore possible
to use any parameters used in the `aiohttp.run_app()`_ method.


Using the UI
------------

The UI itself is just a simple HTML5 application. Change of any property causes
immediate change of the corresponding attribute of the underlying object.

Conversely, any change of underlying object's state causes immediate update
of the UI state.

There is some color coding to help making sense of those transitions:

*Orange code* - value is being changed by the user
    Orange label/background of the widget singalizes that the UI is currently
    being changed by the user and it's state does not correspond
    with the underlying object's state. The value on the label shows the value
    which is currently set on the object.

    As soon as user stops changing the property value (widget looses
    it's focus), the value is set to the underlying object and the orange code
    disappears.

.. image:: ../docs/img/change-orange.png

*Blue code* - value changed by the underlying object
    Blue code signalizes user that the underlying object's state has changed
    without user's interaction. Blue label shows the last value before this
    change.

    Blue label dissapears when the value is changed by the user.

.. image:: ../docs/img/change-blue.png

*Azure code* - value changed by another user session
    Since UI manager supports multiple parallel sessions (=multi-user), this
    mechanism signalizes the changes caused by another users. Azure label
    shows the last value before this change.

.. image:: ../docs/img/change-azure.png

*Red code* - value could not be updated
    Red background on the widget signalizes that the user change on the UI could
    not be set to the underlying object. Usually because the connection to the
    UI manager was lost etc.

.. image:: ../docs/img/change-red.png



.. _`@property`: http://stackabuse.com/python-properties/
.. _aiohttp: http://aiohttp.readthedocs.io/en/stable/
.. _ReST: http://docutils.sourceforge.net/rst.html
.. _`aiohttp.run_app()`: http://aiohttp.readthedocs.io/en/stable/web_reference.html#aiohttp.web.run_app
