# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/tofull/devops-coding-challenge/issues.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

S3_analyst could always use more documentation, whether as part of the
official S3_analyst docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/tofull/devops-coding-challenge/issues.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `s3_analyst` for local development.

1. Fork the `s3_analyst` repo on GitHub.
2. Clone your fork locally::

    ```sh
    $ git clone git@github.com:tofull/devops-coding-challenge.git
    ```
3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:

    For python2: `$ mkvirtualenv devops-coding-challenge-python2`
    or for python3:
    `$ mkvirtualenv --python=/usr/bin/python3 devops-coding-challenge-python3`

    Then install all the requirements:

    ```sh
    $ cd devops-coding-challenge/
    $ pip install -r requirements_dev.txt
    $ python setup.py develop
    ```
    You're now ready to make magic with programming.

4. Install the hooks to keep the documentation updated:
    ```sh
    $ ln -s ../../hooks/pre-commit .git/hooks/pre-commit
    $ ln -s ../../hooks/post-commit .git/hooks/post-commit
    ```

5. Create a branch for local development::

    ```sh
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox:

    ```sh
    $ flake8 s3_analyst tests
    $ python setup.py test or py.test
    $ tox
    ```

   To get flake8 and tox, just pip install them into your virtualenv.

7. Commit your changes and push your branch to GitHub::

    ```sh
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

8. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.7 and 3.5, and for PyPy. Check
   https://travis-ci.org/tofull/s3_analyst/pull_requests
   and make sure that the tests pass for all supported Python versions.

## Tips

To run a subset of tests:

```sh
$ py.test tests.test_s3_analyst
```
