*django-geoexplorer* allows you to use `GeoExplorer <http://opengeo.org>`_
in your `Django <https://www.djangoproject.com>`_ projects.

This is just packaging work for the boundless suite client sdk.

The releases will be done loosely based on the suite releases but the minor version numbers may not match.

=======
INSTALL
=======

::

    pip install django-geoexplorer

=====
USAGE
=====

* Add ``geoexplorer`` to your ``INSTALLED_APPS``


=======
AUTHORS
=======

* Ariel Núñez <http://ingenieroariel.com>

==========
DEVELOPERS
==========

::

    git clone http://github.com/GeoNode/suite.git
    cd suite
    git submodule update --init
    cd ../
    git clone http://github.com/GeoNode/django-geoxplorer.git
    cp -R suite/geoexplorer/target/geoexplorer/WEB-INF/app/static/* django-geoexplorer/geoexplorer/static/
    cd django-geoexplorer
    git add geoexplorer/static
    vim setup.py  # update the version number
    git add setup.py
    git commit -m "Commit committed, a new release was needed because the other one was old."
    git push origin master
    python setup.py sdist upload


===================
GeoExplorer Sources
===================

::

    git clone https://github.com/geosolutions-it/geoexplorer.git
    cd geoexplorer
    git checkout geonode-geoexplorer
    ant war
    cp -R suite/geoexplorer/target/geoexplorer/WEB-INF/app/static/* django-geoexplorer/geoexplorer/static/


=======
LICENSE
=======

* Lesser GNU Public License
* OpenGeo Suite License - GPL
