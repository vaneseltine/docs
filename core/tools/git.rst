git
###

how does one
============

...find and restore an old deleted file?
----------------------------------------

https://stackoverflow.com/questions/7203515/git-how-to-find-a-deleted-file-in-the-project-commit-history

.. pull-quote::

    If you do not know the exact path you may use

    ``git log --all --full-history -- "**/thefile.*"``

    If you know the path the file was at, you can do this:

    ``git log --all --full-history -- <path-to-file>``

    This should show a list of commits in all branches which touched that file. Then, you can find the version of the file you want, and display it with...

    ``git show <SHA> -- <path-to-file>``

    Or restore it into your working copy with:

    ``git checkout <SHA>^ -- <path-to-file>``

    Note the caret symbol (^), which gets the checkout prior to the one identified, because at the moment of <SHA> commit the file is deleted, we need to look at the previous commit to get the deleted file's contents
