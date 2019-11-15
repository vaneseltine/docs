git
###

how does one
============

...delete all traces of a file in a repo?
------------------------------------------

https://stackoverflow.com/questions/2100907/how-to-remove-delete-a-large-file-from-commit-history-in-git-repository



**Interactive rebase**

With a history of::

    $ git lola --name-status
    * f772d66 (HEAD, master) Login page
    | A     login.html
    * cb14efd Remove DVD-rip
    | D     oops.iso
    * ce36c98 Careless
    | A     oops.iso
    | A     other.html
    * 5af4522 Admin page
    | A     admin.html
    * e738b63 Index
      A     index.html

you want to remove `oops.iso` from “Careless”
as though you never added it,
and then “Remove DVD-rip” is useless to you.
Thus, our plan going into an interactive rebase
is to keep “Admin page,” edit “Careless,” and discard “Remove DVD-rip.”

Running `$ git rebase -i 5af4522` starts an editor
with the following contents::

    pick ce36c98 Careless
    pick cb14efd Remove DVD-rip
    pick f772d66 Login page

    # Rebase 5af4522..f772d66 onto 5af4522
    #
    # Commands:
    #  p, pick = use commit
    #  r, reword = use commit, but edit the commit message
    #  e, edit = use commit, but stop for amending
    #  s, squash = use commit, but meld into previous commit
    #  f, fixup = like "squash", but discard this commit's log message
    #  x, exec = run command (the rest of the line) using shell
    #
    # If you remove a line here THAT COMMIT WILL BE LOST.
    # However, if you remove everything, the rebase will be aborted.
    #

Executing our plan, we modify it to::

    edit ce36c98 Careless
    pick f772d66 Login page

    # Rebase 5af4522..f772d66 onto 5af4522
    # ...

That is, we delete the line with “Remove DVD-rip” and
change the operation on “Careless”
to be `edit` rather than `pick`.

Save-quitting the editor drops us at a command prompt
with the following message::

    Stopped at ce36c98... Careless
    You can amend the commit now, with

            git commit --amend

    Once you are satisfied with your changes, run

            git rebase --continue

As the message tells us,
we are on the “Careless” commit we want to edit,
so we run two commands::

    $ git rm --cached oops.iso
    $ git commit --amend -C HEAD
    $ git rebase --continue

The first removes the offending file from the index.
The second modifies or amends “Careless” to be the updated index
and `-C HEAD` instructs git to reuse the old commit message.
Finally, `git rebase --continue` goes ahead with the
rest of the rebase operation.

This gives a history of::

    $ git lola --name-status
    * 93174be (HEAD, master) Login page
    | A     login.html
    * a570198 Careless
    | A     other.html
    * 5af4522 Admin page
    | A     admin.html
    * e738b63 Index
      A     index.html

which is what you want.

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
