periscope-downloader
=========

*A command line tool to download periscope charts, and save the snapshot of the
chart with a timestamp to a local file. Allows for historical data to be
archived so that trends can be analyzed.*

Install:
* from pip:
  * `sudo easy_install pip`
  * `pip install pdown`
* from tarball:
  * `gunzip -c pdown-X.Y.Z.tar.gz | tar xopf -`
  * `python setup.py install`
  * (optional) `export PATH=/usr/local/bin:$PATH`

To build:
* change directories to pdown dir
    * `$ cd periscope-downloader/dir`
* run the setup script
    * `python setup.py develop`

To push to PyPi:
* `$ cd periscope-downloader`
* `python setup.py sdist`
* `twine upload dist/pdown-X.Y.Z.tar.gz` 
  
