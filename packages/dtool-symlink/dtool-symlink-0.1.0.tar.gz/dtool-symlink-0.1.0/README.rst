README
======

Add ability to create dataset where data directory is a symlink.

Installing this package provides the dtool command line client with a storage
broker named ``symlink``. This is useful if one wants to mark up files in a
directory as a dataset without having to re-organise their structure on disk.
For example if one wants to mark up some Next Generation Sequencing data that
has arrived on an external hard disk as a dataset before copying the resulting
dataset to some other form of storage.

If one wants to make use of the
``dtool_symlink.storagebroker.SymLinkStorageBroker`` class programatically one
needs to create a function that returns the data directory to be symbolically
linked. This function is then passed into the
``SymLinkStorageBroker.create_structure()`` method. For example::

    from dtool_symlink.storagebroker import SymLinkStorageBroker

    def get_data_dir():
        return "/my/path/with/data"

    symlink_storage_broker = SymLinkStorageBroker("/path/to/dataset")
    symlink_storage_broker.create_structure(get_data_dir)



Installation
------------

To install the dtool-symlink package.

.. code-block:: bash

    cd dtool-symlink
    python setup.py install
