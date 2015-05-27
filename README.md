# Sphinx-Documentation
General Usage of Google style doc strings.  

The module demos the usage of google style documenation generation using
the sphinx 1.3.1 with builtin `Napoleon extention`_.

It also uses Sphinx's autodoc, todo, view code extention.

.. _Napoleon extenstion:
   http://sphinxcontrib-napoleon.readthedocs.org/en/latest/sphinxcontrib.napoleon.html
   
   
Installation Steps:
===================

1. pip install sphinx
2. pip install alabaster(optional)
3. Go to the directory for which the documentation needs be created
4. mkdir docs
5. cd docs
6. sphinx-quickstart
 
It prompts for user input
::
one-piece : (~/workspace/DocIt/GSDoc) >> sphinx-quickstart 
Welcome to the Sphinx 1.3.1 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Enter the root path for documentation.
> Root path for the documentation [.]: 

You have two options for placing the build directory for Sphinx output.
Either, you use a directory "_build" within the root path, or you separate
"source" and "build" directories within the root path.
> Separate source and build directories (y/n) [n]: y

Inside the root directory, two more directories will be created; "_templates"
for custom HTML templates and "_static" for custom stylesheets and other static
files. You can enter another prefix (such as ".") to replace the underscore.
> Name prefix for templates and static dir [_]: 

The project name will occur in several places in the built documentation.
> Project name: Napolean Sphinx Documentation
> Author name(s): Ameet Mamadapur

Sphinx has the notion of a "version" and a "release" for the
software. Each version can have multiple releases. For example, for
Python the version is something like 2.5 or 3.0, while the release is
something like 2.5.1 or 3.0a1.  If you don't need this dual structure,
just set both to the same value.
> Project version: v0.0.1
> Project release [v0.0.1]: rel_0.0.1

If the documents are to be written in a language other than English,
you can select a language here by its language code. Sphinx will then
translate text that it generates into that language.

For a list of supported codes, see
http://sphinx-doc.org/config.html#confval-language.

    one-piece : (~/workspace/DocIt/GSDoc) >> tree
    .
    ├── build
    ├── make.bat
    ├── Makefile
    └── source
        ├── conf.py
        ├── index.rst
        ├── _static
        └── _templates
    
    4 directories, 4 files

    one-piece : (~/workspace/DocIt/GSDoc) >> make html
    one-piece : (~/workspace/DocIt/GSDoc) >> python -m SimpleHttpServer

