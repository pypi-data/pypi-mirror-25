************* 
eurotools
*************

.. image:: http://gitlab.stonework.net/stoneworksolutions/eurotools/badges/master/build.svg
     :target: http://gitlab.stonework.net/stoneworksolutions/eurotools/

.. image:: http://gitlab.stonework.net/stoneworksolutions/eurotools/badges/master/coverage.svg
     :target: http://gitlab.stonework.net/stoneworksolutions/eurotools/

Comienzo rapido
---------------

1. Agregar la aplicacion deseada a INSTALLED_APPS::

     INSTALLED_APPS = (
         ...
         "euroblock",
         "eurocharts",
         "eurocube",
         "eurodate",
         "eurodecorators",
         "eurofilters",
         "eurogrids",
         "europlugin",
     )

2. Importar los estaticos:

TBD

    <!-- jQuery UI -->
    <script src="{{STATIC_URL}}plugins/jquery-ui-1.12.1/jquery-ui.min.js"></script>
    <link href="{{STATIC_URL}}plugins/jquery-ui-1.12.1/jquery-ui.min.css" rel="stylesheet">
    <link href="{{STATIC_URL}}plugins/jquery-ui-1.12.1/jquery-ui.theme.min.css" rel="stylesheet">
    <link href="{{STATIC_URL}}plugins/jquery-ui-1.12.1/jquery-ui.structure.min.css" rel="stylesheet">


    <!-- MULTISELECT-->
    <link href="{{ STATIC_URL }}css/euromultiselect.css" rel="stylesheet"/>
    <script src="{{ STATIC_URL }}js/euromultiselect.js" type="text/javascript"></script>
    <script src="{{ STATIC_URL }}js/eurofilters_localdb.js" type="text/javascript"></script>
    <script src="{{ STATIC_URL }}lib/jquery-multiselect/src/jquery.multiselect.min.js" type="text/javascript"></script>
    <script src="{{ STATIC_URL }}lib/jquery-multiselect/src/jquery.multiselect.filter.min.js" type="text/javascript"></script>

    <!-- Add stoneplugins  -->
    <script src="{{STATIC_URL}}js/euroutils.js"></script>

    <!-- BLOCKUI -->
    <script src="{{ STATIC_URL }}js/euroblock.js" type="text/javascript"></script>


3. Ejemplo de uso:


    euroselect = new eurofiltersIU(config, cb)
    euroselect.createFilters(filters);

************* 
euroblock
*************

Libreria client y server side que proporciona filtros avanzados basados en componentes html _select_

************* 
eurocharts
*************

Libreria cliente que proporciona integracion con HighCharts

************* 
eurocube
*************

Libreria server side que proporciona compatibilidad con bases de datos multidimensionales Microsoft Analysis Services

************* 
eurodate
*************

Libreria client side que proporciona filtros de fecha avanzados basados en componentes Bootstrap

************* 
eurodecorators
*************

Libreria server side que proporciona filtros avanzados basados en componentes html _select_

************* 
eurofilters
*************

Libreria client y server side que proporciona filtros avanzados basados en componentes html _select_

************* 
eurogrids
*************

Libreria client y server side que proporciona filtros avanzados basados en componentes html _select_

************* 
europlugin
*************

Libreria client y server side que proporciona filtros avanzados basados en componentes html _select_
