Tornado Cookiecutter template
===

[Cookiecutter](https://github.com/audreyr/cookiecutter) template for a eVision Python Web Service project.

This is my cookiecutter template to build a simple, fast and rock solid website based upon
the Tornado framework. There are quite many Tornado template projects out there,
but I wanted to start something from scratch, that fits my needs and evolves out
of years of experiences (positive and negative alike) with other Python based webframeworks like Turbogears and Django.

Of course this template is not designed for larger data structures. The main
focus is on scalability, fast data access and small library dependencies.

Features
---
* Configurable as a Cookiecutter template
* pytest and tox for testing
* Vagrant and Docker support
* Basic [HTML5 Boilerplate](https://html5boilerplate.com/)
* SASS for CSS generation
* Choice of various licenses.
* (Optional) [Bumpversion](https://github.com/peritus/bumpversion) for updating version information

Requirements
---

Projects using this template have these minimal dependencies:

- [Cookiecutter](https://github.com/audreyr/cookiecutter) - just for creating the project
- [Tox](https://tox.readthedocs.io/en/latest/) - for running the tests
- [Tornado](https://github.com/tornadoweb/tornado) - Web framework based
- [eVision-Lib](https://github.com/evision-ai/evision-lib) - eVision common python library

Installation and options
---

Install Cookiecutter

    $ pip install cookiecutter

Initialize the project with cookiecutter and answer some questions for the newly started project:

    $ cookiecutter https://github.com/evision-ai/cookiecutter-tornado

You will be asked for these fields:

| Field | Default | Description |
|:-----:|:-----:|:-----|
| `project_name` | eVision Awesome Service | Verbose project name, used in headings (docs, readme, etc). |
| `repo_name` | evision-awesome-service | Repository name on GitHub (and project's root directory name). |
| `project_slug` | awesome | Python package namespace name (whatever you would import). |
| `author_name` | `Your name` | Main author of this library or application (used in ``AUTHORS.rst`` and ``setup.py``). |
| `email` | `Your e-mail` | Contact email of the author (used in ``AUTHORS.rst`` and ``setup.py``). |
| `repo_hosting` | github.com | Use ``"no"`` for no hosting (various links will disappear). You can also use ``"gitlab.com"`` and such but various things will be broken. |
| `repo_hosting_domain` | github.com | Domain of VCS. |
| `repo_username` | `evision-ai` | GitHub user name of this project (used for GitHub link). |
| `description` | `A short description of the project.` | One line description of the project (used in ``README.rst`` and ``setup.py``). |
| `version` | `0.1.0` | Release version (see ``.bumpversion.cfg`` and in Sphinx ``conf.py``). |
| `use_docker` | `y` | Add docker configuration or not |
| `open_source_license` | Not open source | License to use. Available options: MIT, BSD, GPLv3, ASL2, Not open source |


Testing
---
All test files will be added to the ``tests`` directory. To run the tests, simply call:

    $ python setup.py test
    
or 

    $ pytest

Start the server
---

To start the final application, just run the following fabric command:

    $ fab devserver

This will tell Tornado to start the application with the default port 8888. If
you want to use another port, just type:

    $ fab devserver:port=8000

In addition to that, see the fabfile.py Script for other parameters and
commands.

Docker
---

To run the application within Docker, you need to build and then run the image:

    $ sudo docker build --tag=tornado-app --rm=true .
    $ sudo docker run -p 8000:8000 -t -i tornado-app:latest

You can now access your application via `http://localhost:8000`
