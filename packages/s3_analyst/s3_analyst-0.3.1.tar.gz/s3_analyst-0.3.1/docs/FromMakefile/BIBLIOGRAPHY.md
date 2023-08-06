# Bibliography

Here are some links to understand choices.

## Project tools
- [Structure your python project](https://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/)
    - cookiecutter,
    - virtualenv,
    - git flow,
    - unittest with pytest,
    - doc coverage test,
    - tox,
    - documentation with sphinx,
    - pypi packaging,
    - travisCI,
    - readthedocs CI

- [Understand generated files from cookiecutter and build an opensource CLI](https://stormpath.com/blog/building-simple-cli-interfaces-in-python)
  - cookiecutter,
  - MANIFEST.in,
  - setup.cfg,
  - setup.py,
  - docopts

- [Best practice for using git flow](https://danielkummer.github.io/git-flow-cheatsheet/)
  - git flow

- [Master the use of virtual environments (FR)](http://apprendre-python.com/page-virtualenv-python-environnement-virtuel)

- [Using python 3 inside a virtual environment](https://djangosteps.wordpress.com/2013/09/25/setup-a-virtualenv-for-python3/)

- [Cookiecutter - pypackage](https://github.com/audreyr/cookiecutter-pypackage/)

- [Understanding coverage report](http://www.codemag.com/article/1701081)


## Project style guide

### Pylint
- [Naming convention](http://pylint-messages.wikidot.com/messages:c0103)

### Make lint recipe (from Makefile)
- [Flake8 documentation](http://flake8.pycqa.org/en/latest/)


## Documentation tool - sphinx
- [Using markdown in sphinx (documentation tool) thanks to recommonmark](https://github.com/rtfd/recommonmark)

## Hooks
Because I would automate the update of  docs/FromMakefile [because of `include ../file.md` is missing in markdown, even with recommonmark]
- [git hook add files to commit](https://stackoverflow.com/questions/3284292/can-a-git-hook-automatically-add-files-to-the-commit)
- [git hook example to understand how it works](http://wadmiraal.net/lore/2014/07/14/how-git-hooks-made-me-a-better-and-more-lovable-developer/)
- [useful git hook example](http://codeinthehole.com/tips/tips-for-using-a-git-pre-commit-hook/)


## Versionning tools

### Bumpversion
- [Understand the tool](https://github.com/peritus/bumpversion)

## Python enhancement

### Unittest tools

- **Tox**
    - [Why I keep tox.ini away from setup.cfg](https://github.com/tox-dev/tox/issues/545)

- **Pytest**
    - [Understanding fixture](https://docs.pytest.org/en/latest/fixture.html)

### Logger

- [Official tutorial - basic](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial)
- [Official tutorial - advanced](
https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial)
- [Good logging practices in Python](https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/)


### Miscellanous
- [Using empty list as default argument is dangerous](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values)

## AWS
### Public Datasets
- [aws public datasets](https://aws.amazon.com/fr/public-datasets/)
    - To test the s3_analyst tool with real-world data

### Collections
- [Documentation to filter over collections](http://boto3.readthedocs.io/en/latest/guide/collections.html#filtering)
    - > **Warning**
        > Behind the scenes, the above example will call ListBuckets, ListObjects, and HeadObject many times. If you have a large number of S3 objects then this could incur a significant cost.

### Error handling
- [Boto3 error handling](http://botocore.readthedocs.io/en/latest/client_upgrades.html#error-handling)
