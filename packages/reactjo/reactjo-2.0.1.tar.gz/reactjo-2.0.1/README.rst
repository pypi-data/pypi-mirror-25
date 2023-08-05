# This is a work in progress

# Introduction
This is a scaffolding engine. It uses extensions for everything, so you can customize the experience. 

The default extension is meant for django projects with a react.js frontend. But you can easily throw in other extensions for (theoretically) any web framework(s), database(s), server(s), frontend(s), language(s). etc.

# 10 minute django + react message board, from nothing.
Open up your command line
```bash
# Setup stuff. This should be obvious
> mkdir my_project            # Create a directory
> cd my_project               # Enter directory
> virtualenv env              # Create virtual environment
> source env/bin/activate     # Activate virtual environment

> pip install reactjo         # Core, plus react-django extension by default
> reactjo init                # Creates a reactjorc directory.
> reactjo new                 # Some questions and starts building
"Name your project: " 
> www
> cd www
> python manage.py runserver  # Start the server
```

Now open your web browser and go to localhost:8000
You should be looking at a simple landing page using react components, and a django backend. But who cares about "Hello World"'s? Let's move on.

Back in command line
```bash
> <ctrl> + c                  # cancels the server
> reactjo users               # scaffolds users
```
Boom! There's now a login/signup button on every page, or a logout button if you're logged in.

But what good are users if you don't have anything for them to do? Let's have some fun.

```bash
> reactjo app               # Create a django app, with react frontend
"Name this app: " 
> Forum

> reactjo models             # Starts the interactive wizard which asks some Qs
"... Lists all apps ..."
"To which app is this model associated? " 
> Forum
"Name this model: " 
> Post

"Add a new field to 'Post'? (y/n): " 
> y

"Name this field: " 
> title

"... Available field types ..."
"Pick a field type for 'title': " 
> charfield

"Give title a max_length (default: 250): " 
> 120

"Do you need to add any other options to title? (y/n)" 
> n

"Add a new field to 'Post'? (y/n): " 
> y

"Name this field: " 
> author

"... Available field types ..."
"Pick a field type for 'title': " 
> foreignkey

"... Available models ..."
"Which model is it related to?" 
> Users

"Do you need to add any other options to title? (y/n)" 
> n

"Add a new field to 'Post'? (y/n): " 
> n

"Will you need a 'create' view for 'Post'? (y/n)" 
> y

"Will you need a 'list' view for 'Post'? (y/n)" 
> y

"Will you need a 'details' view for 'Post'? (y/n)" 
> y

"Usergroups: 'admin', 'authenticated', 'everyone'"
"Who can create instances of 'Post'?" 
> authenticated

"Done :-)"

python manage.py runserver
```

Ok, now go back to localhost:8000. You can sign up, create posts, and have them posted to the site. And everything uses react components, so you can customize it however you want.

With a bit more work you could turn this into a full featured message board forum.

# Basic Usage:

1. Install
-----------
```
> pip install reactjo
```

2. Create reactjorc
--------------------
```
> reactjo init
```

3. Create an app
-----------------
```
> reactjo app
```

4. Create models and views
---------------------------
```
> reactjo models
> reactjo views
```

Depending on the answers you gave, you now automatically have react components rendering 
the list/detail/etc views for your models, as well as a static react component for the index page. 

The components themselves are intentionally kept extremely minimalistic. It's up to you to
build them into something pretty and functional! Alternately, use an extension that makes them prettier.

