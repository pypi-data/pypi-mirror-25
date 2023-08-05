keyman
======

Keyman is a utility for storing and managing your passwords locally.

Features
--------

The manager can store an account with following terms recorded ("*" marked term
is required):

- title (*): title of the account, e.g. weibo, wechat, facebook
- username: your username
- description: description of the account
- password: your password
- phone: the phone number bound to the account
- email: the email address related to the account
- secret: some secret information

where passwords and secrets are stored in encrypted forms.

**IMPORTANT:** In spite that encryption procedure is involved, since keyman
*doesn't require any certification* before it is used to manage (including
exhibit and edit) your account records, it is recommended that you store the
keywords that can remind you of your password and secret info, rather than the
"raw" keywords and secret messages.

Installation
------------

Simply use:

.. code-block:: bash

    $ pip install keyman

If you are using Anaconda, problems may arise when pip is trying to install
pycrypto_, which is required by keyman. To deal with this problem, you can use

.. code-block:: bash

    $ conda install pycrypto

and then use

.. code-block:: bash

    $ pip install keyman

as usual.

.. _pycrypto: https://pypi.python.org/pypi/pycrypto/

Usage
-----

Below are what can be done with keyman:

- Create a new account record:

    .. code-block:: bash

        $ keyman insert

    Then follow the instructions to record the account.

- Remove an existing account (accounts):

    .. code-block:: bash

        $ keyman remove --id IDS_TO_BE_REMOVED

    If ``--nontrash`` flag is not given, the record(s) will be moved into trash;
    Otherwise they will be deleted from the database completely.

- Recover an account (accounts) from trash:

    .. code-block:: bash

        $ keyman recover --id IDS_TO_BE_RECOVERED


- Search accounts according to given conditions:

    #. search by id's:

        .. code-block:: bash

            $ keyman search --id IDS_TO_SEARCH

    #. or search by sub-strings in title and description [#]_:

        .. code-block:: bash

            $ keyman search --title STR_IN_TITLE --description STR_IN_DESC

    If ``--show-all`` flag is given, the records found in trash will also be
    listed out.

    .. [#] The logical relation between arguments ``--title`` and ``--description`` is "AND".

- List out all the accounts in certain range [#]_:

    .. code-block:: bash

        $ keyman list --all | --trash | --normal

    .. [#] The three flags are not mutually exclusive. ``--all`` will overwrite the rest two flags, and ``--trash --normal`` is equivalent to ``--all``.

- Update an existing account by editing its information:

    .. code-block:: bash

        $ keyman updata --id ID_TO_BE_UPDATED

    Then follow the instructions to update the account.

For command ``keyman`` or any sub-command, use ``--help`` to get the related
help message.
