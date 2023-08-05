To make a new release::

    $ tox
    $ bumpversion {major,minor,patch}
    $ make release
    $ make -C docs latexpdf

Then update the docs in Bitbucket Downloads page.

To update the courtana feedstock, edit the recipe with the new version
and `sha256` (from warehouse -> Download files -> .tar.gz).
