|buildstatus|\ |Coverage Status|

pyarxiv
=======

pyarxiv is a wrapper for the API of `Cornell University's famous
repository <http://arxiv.org>`__ for scientific papers.

Supports Python 2.7, 3.3-3.6+

Installation
------------

.. code:: sh

    # TODO

Features
--------

-  Query the arXiv API (atom feed) in your code
-  Use enums for arXiv categories
-  Download papers in your code as PDF TODO - Do the above in the
   commandline

Usage
-----

CLI
~~~

.. code:: sh

    pyarxiv-cli download -h
    pyarxiv-cli query -h
    # will download a couple of papers with given ids to folder /home/user, name them according to their titles,
    # append their arxiv ids, and do not give progress feedback when each paper is downloaded
    pyarxiv-cli download 1703.00001 1703.00002v1 ... --target-folder=/home/user --use-title-for-filename --append-id --silent

.. code:: sh

    # Queries for papers with "Lorem" in them, maximally gets 5 papers (default 100), authors Einstein and Zweistein
    # Other potential arguments are --abstract, --journalref and manualmode with --querystring
    pyarxiv-cli query --title="Lorem" --max-results=5 --authors="A Einstein, B Zweistein"

You can also chain commands:

.. code:: sh

    pyarxiv-cli download $(pyarxiv-cli query --title="WaveNet") --use-title-for-filename --append-id

Python
~~~~~~

.. code:: python

    from pyarxiv import query, download_entries
    from pyarxiv.arxiv_categories import ArxivCategory, arxiv_category_map
    #query(max_results=100, ids=[], categories=[],
    #                title='', authors='', abstract='', journal_ref='',
    #                querystring='')
    entries = query(title='WaveNet') 
    titles = map(lambda x: x['title'], entries)
    print(list(titles))


    #download_entries(entries_or_ids_or_uris=[], target_folder='.',
    #                     use_title_for_filename=False, append_id=False,
    #                     progress_callback=(lambda x, y: id))
    download_entries(entries)


    entries_with_category = query([ArxivCategory.cs_AI])
    print(arxiv_category_map(ArxivCategory.cs_AI))

.. |buildstatus| image:: https://travis-ci.org/culshoefer/pyarxiv.svg?branch=master
   :target: https://travis-ci.org/culshoefer/pyarxiv
.. |Coverage Status| image:: https://coveralls.io/repos/github/culshoefer/pyarxiv/badge.svg?branch=master
   :target: https://coveralls.io/github/culshoefer/pyarxiv?branch=master
