# KM3Astro

[](https://readthedocs.org/projects/km3astro/badge/?version=latest)

## About

KM3Astro is a collection astronomy utils, like coordinate transformations.

## Install

This is developed on python >=3.5. Lower versions (especially py2)
might or might not work.

Install the dependencies

* numpy 
* pandas
* astropy

In your python env, do

  pip install git+http://git.km3net.de/km3py/km3astro.git

or just clone the git repository and install via ``pip install .``

## Docs (local)

Clone the git repo, and <pre>
pip install -Ur requirements.txt       # needed to run examples
pip install -Ur doc-requirements.txt   # (sphinx etc).
</pre>
Then go to `doc` and `make html`. Docs are in `_build/html/index.html`.
