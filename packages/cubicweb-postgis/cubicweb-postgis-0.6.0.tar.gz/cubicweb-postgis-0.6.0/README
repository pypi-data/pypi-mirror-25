Summary
-------

Add types and functions to work with geometric attributes that are stored in a
Postgis database (that is a PostgreSQL database with Postgis extension
enabled).

The present cube supports only version *2.0 and later* of Postgis.

It introduces one new type when defining attributes in the data model schema:

* a ``Geometry`` type. Additionally, you should give the following elements
  along with a `Geometry` attribute:

  * ``geom_type``. The Postgis type of geometries that this attribute will
    accept, for example ``POINT``, ``MULTILINESTRING`` or ``POLYGON``,

  * ``srid``. The spatial reference system the geometry coordinates will live
    in. This is an integer and a foreign key that must match the ``srid`` key
    in the ``spatial_ref_sys`` table. Most of the time, it will be the same as
    the spatial system EPSG code,

  * ``coord_dimension``. The number of dimensions used by geometries. Defaults
    to 2.

* a ``Geography`` type (see the description_).

.. _description: https://postgis.net/docs/using_postgis_dbmanagement.html#PostGIS_Geography


Then you can also use geometric functions like ``ST_INTERSECTS``, ``ST_WITHIN``
or ``ST_UNION`` to work with this new type.

See `Postgis manual`_ for reference documentation about Postgis.

.. _Postgis manual: http://postgis.net/docs/


Example
-------

In ``schema.py``, one can declare a ``City`` entity like the following.

.. code-block:: python

    class City(EntityType):
        name = String(required=True)
        geometry = Geometry(geom_type='POLYGON', srid=4326)

You may then make queries like:

.. code-block:: python

   # get all cities in a given bounding box
   rql('City C WHERE C geometry G HAVING(ST_WITHIN(G, ST_MAKEENVELOPE('
       '%(left)s, %(bottom)s, %(right)s, %(top)s, 4326)) = TRUE)',
	   {'left': 2.2,
	   'right': 2.6,
	   'top': 49,
	   'bottom': 48})

   # get all cities at a given distance from a point, sorted by distance
   rql('Any C, ST_DISTANCE(G, ST_SETSRID(ST_MAKEPOINT(2.2, 48.4), 4326)) '
       'ORDERBY 5 WHERE '
	   'C geometry G HAVING ('
	   ' ST_DWITHIN(G, ST_SETSRID(ST_MAKEPOINT(2.2, 48.4), 4326), 0.1) = TRUE)')
