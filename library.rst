library
###############

notes
=====================

https://news.ycombinator.com/item?id=13021722

https://hugotunius.se/2016/01/10/the-one-cent-blog.html

https://github.com/yoloseem/awesome-sphinxdoc

todo
=====================

improve genindex
--------------------------------

https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#index-generating-markup

update
--------------------------------

- download the file attached to each key (from bucket)
- generate a key for each file (from current repo)
- upload files with no keys
- delete keys with no files
- for intersection, check diff; update as needed

infrastructure
--------------------------------

::

    [X] rst -> html (Sphinx)
    [X] html -> s3 (boto3)
    [X] s3 -> website (aws)
    [X] ssl
    [ ] www ->  www.misterdoubt.com -> https://misterdoubt.com
    [X] mrdoubt.com -> https://misterdoubt.com
    [ ] www.mrdoubt.com -> https://misterdoubt.com
    [X] http://misterdoubt.com -> https://misterdoubt.com
    [ ] http://www.misterdoubt.com -> https://misterdoubt.com
    [ ] minimize file duplication (https://console.aws.amazon.com/billing/home?#/freetier)

new theme?
------------

- https://github.com/snide/sphinx_rtd_theme
- https://github.com/ryan-roemer/sphinx-bootstrap-theme
- https://github.com/guzzle/guzzle_sphinx_theme
- https://sphinx-themes.org/html/murray/murray/index.html
- https://sphinx-themes.org/html/oe-sphinx-theme/oe_sphinx/basic.html
- https://sphinx-themes.org/html/sphinx-fossasia-theme/sphinx_fossasia_theme/basic.html
- https://nameko.readthedocs.io/en/stable/

misc
---------

- https://sphinx-git.readthedocs.io/en/stable/using.html#git-changelog-directive
