This is a work in progress
==========================

Introduction
============

This is a scaffolding engine. It uses extensions for everything, so you
can customize the experience.

You get, by default:
~~~~~~~~~~~~~~~~~~~~

-  A microservice architecture
-  Django backend
-  Next.js (with react/redux) frontend
-  Optional user authentication
-  Model, view, component, and api, scaffolding

Extensible
~~~~~~~~~~

-  Install an extension or change any of the default ones.
-  New extensions can be generated with a single command
   ``reactjo extend``
-  Deploying an extension is as easy as pushing it to a github repo.

zero-weight
~~~~~~~~~~~

You don't need reactjo in production, it can be uninstalled after it's
done building. Or just .gitignore the reactjorc directory which holds
all the extensions and their bulk.

Interactive, intelligent
~~~~~~~~~~~~~~~~~~~~~~~~

This is not a boilerplate repo, that just gives you a starting point and
leaves you hanging.

Reactjo takes you through a series of questions to determine what you
need, and even gives you the available options so you don't need to need
to endlessly ask docs "what was that mandatory field I need to pass
in..."

After you generate the project, Reactjo can continue to be used to
scaffold more pieces of the project in the future.

Requirements:
=============

-  `Python 3 <https://www.python.org/downloads/>`__ (Ideally 3.6.x or
   newer)
-  `pip3 <https://pip.pypa.io/en/stable/installing/>`__
-  `node and npm <https://nodejs.org/en/download/>`__
-  `git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`__

5 minute Django + React project.
================================

Open up your command line

.. code:: bash

    # Setup stuff. This should be obvious
    > mkdir my_project            # Create a directory.
    > cd my_project               # Enter directory.
    > python3 -m venv env         # Or python -m venv env (windows).
    > source env/bin/activate     # Or just env/Scripts/activate (window).
    > pip install reactjo         # Installs the core engine that runs everything.

    # Finally we use reactjo.
    > reactjo init                # Creates reactjorc/, downloads default extensions.
    > reactjo new                 # It asks some questions and starts building.

    # Wait 5 minutes for npm to finish installing packages...

    # Test drive your new site
    > cd frontend
    > npm run start

    # Open a new terminal tab
    > cd backend/path
    > python manage.py runserver 3001

There are now two servers running: - http://localhost:3000 The frontend
NodeJS server (for visual, react stuff) - http://localhost:3001 The
backend Django dev server (creates an api for the DB)

What next?
----------

In a browser, go to http://localhost:3000

Now click "signup" and create an account. React just made an ajax
request to the django server, which stored the user in it's database,
and responded with a token.

Now every time you visit a page that requires you to be logged in, the
frontend app sends the token to the backend app to authenticate you.

User Auth
---------

One of the questions asked during ``reactjo new`` is "Do you need user
authentication"

If you answer "yes", then you will automatically get: - Login page -
Logout button - Signup page - Users list page at /users - User profile
page at /user/:id

Adding content
--------------

.. code:: bash

    reactjo content               # Start the scaffolding wizard

This command starts a series of questions to determine what you need.
After you're done, it creates: - The database model, - An API for it -
List and detail pages, - Create, Update, Delete options.

Why microservices?
------------------

In theory, you could create more frontends, like a mobile app. As long
as they make ajax calls to the same endpoints, they should seamlessly
integrate with the existing database. Just remember to update the
allowed hosts in django.

Alternately, you could create a different backend.

Larger companies may find benefit in separating staff, having dedicated
frontend javascript devs and dedicated backend python devs, instead of
having javascript everywhere and expecting everyone to be full stack.

That said, the frontend app still has it's own Node.js server, it just
doesn't deal with models or databases aside from making API calls.

Working with extensions
=======================

Extensions are just git repos that reactjo downloads. They respond to
certain reactjo commands and do most of the work.

To install a new extension: - Open reactjorc/config.json - Add the entry
- In a terminal, run ``reactjo update`` to reinstall all extensions.

Note that reactjo update overwrites any existing extensions, which is
why you should never make changes to existing extensions in your project
or you'll lose all the changes.

Creating a new extension
========================

.. code:: bash

    ...
    pip install reactjo         # Install Reactjo
    reactjo extend              # Creates an extension template

This creates a skeleton of an extension. Check the README.md file for
more help.

Put it in a github repo, and it can immediately be used as an extension
by following the install steps above.

By default, it responds to the ``reactjo new`` command with a "hello
world". You can make it listen for any ``reactjo _____`` commands you
want by editing the entry.py file.

The template comes with several helper modules which make it absurdly
easy to build out the extension.
