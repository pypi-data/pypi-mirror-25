"use strict";
var STONEGRIDS = {};
(function($){
    $.fn.extend({
        /**
         * Creates a grid.
         *
         * @param      {<dict>}  config  The configuration
         */
        createGrid: function(config){
            config = getDefaultConfigGrid(config)
            if ('footer' in config){
                if(config['footer']){
                    var footer = createFooter(config['columns'])
                    $(this).append(footer)
                }
            }
            STONEGRIDS[this[0].id] = {};
            STONEGRIDS[this[0].id]['config'] = config;
            STONEGRIDS[this[0].id]['gridmethods'] = this.DataTable(config);
            changeStyleButtons(this)
            STONEGRIDS[this[0].id]['itablecounter'] = 1;
        },
        /**
         * Update data of grid
         *
         * @param      {<list of lists>}  datas   The new rows
         */
        updateData: function(datas, footer){
            STONEGRIDS[this[0].id]['datas'] = datas
            STONEGRIDS[this[0].id]['footer'] = footer
            STONEGRIDS[this[0].id]['gridmethods'].clear()
            STONEGRIDS[this[0].id]['gridmethods'].rows.add(datas)
            // Remove previous draw events detection
            STONEGRIDS[this[0].id]['gridmethods'].off('draw.dt');
            STONEGRIDS[this[0].id]['gridmethods'].draw()
            if(typeof(footer) != 'undefined'){
                this.updateFooter(footer)
            }
            $('.DTFC_RightWrapper').hide()
        },

        setTitleFileExport: function(title){
            STONEGRIDS[this[0].id]['gridmethods'].destroy()
            var config = STONEGRIDS[this[0].id]['config']
            var new_buttons = []
            $.each(config['buttons'], function(index, value){
                value['title'] = title
                new_buttons.push(value)
            })
            config['buttons'] = new_buttons
            STONEGRIDS[this[0].id]['gridmethods'] = this.DataTable(config);
            this.updateData(STONEGRIDS[this[0].id]['datas'], STONEGRIDS[this[0].id]['footer'])
            this.hideColumns(STONEGRIDS[this[0].id]['hideColumns'])
            changeStyleButtons(this)
        },
        /**
         * Resize teh grid
         */
        resizeColumns: function(){
          STONEGRIDS[this[0].id]['gridmethods'].columns.adjust();
          STONEGRIDS[this[0].id]['gridmethods'].draw(true)
        },
        /**
         * Hides the columns.
         *
         * @param      {<list of number of columns>}  hideColumns  The hide columns
         */
        hideColumns: function(hideColumns){
            STONEGRIDS[this[0].id]['hideColumns'] = hideColumns
            STONEGRIDS[this[0].id]['gridmethods'].columns().visible(true)
            STONEGRIDS[this[0].id]['gridmethods'].columns(hideColumns).visible(false)
            STONEGRIDS[this[0].id]['gridmethods'].draw()
        },
        /**
         * Update footer data
         *
         * @param      {<dict>}  data    The data
         */
        updateFooter: function(data){
            var id_grid = this[0].id
            var api = STONEGRIDS[id_grid]
            var ya = false;
            $.each(data, function(name, value){
                var column_num = getColumnIndex(id_grid, name)
                if (column_num != -1){
                    var footer = api['gridmethods'].columns(column_num).footer()
                    $(footer).html(value)
                }
                $(footer).html(value)
            });
        },
        /**
         * Gets column name fnding by id.
         *
         * @param      {<int>}  column_index   The column index
         * @return     {<str>}  the column name
         */
        getColumnName: function(column_index){
            return STONEGRIDS[this[0].id]['gridmethods'].column(column_index).dataSrc();
        },
        /**
         * Gets cell data finding by row and column ids.
         *
         * @param      {<int>}  row_index      The row index
         * @param      {<int>}  column_index   The column index
         * @return     {<str>}  the cell data
         */
        getCellData: function(row_index, column_index){
            return STONEGRIDS[this[0].id]['gridmethods'].cell(row_index, column_index).data();
        },
        /**
         * Gets row data finding by id.
         *
         * @param      {<int>}  row_index      The row index
         * @return     {<str>}  the row data
         */
        getRowData: function(row_index){
            return STONEGRIDS[this[0].id]['gridmethods'].row(row_index).data();
        },
        addDrill: function(drillColumns, callbackFunction){
            var oTable = STONEGRIDS[this[0].id];

            // Check if table is empty
            if (oTable['gridmethods'].rows().count()){
                var columns_positions = [];
                var i = 1;

                // Get columns position
                var visible_columns = oTable['gridmethods'].columns().visible();
                $.each(oTable['gridmethods'].columns().dataSrc(), function(index, value){
                    if (visible_columns[index]){
                        if(drillColumns.indexOf(value) != -1){
                            columns_positions.push(i);
                        }
                        i++;
                    }
                })

                var grid_id = this[0].id;
                manageDrill(grid_id, columns_positions, callbackFunction, true);

                $('#'+grid_id).on('draw.dt', function(){
                    manageDrill(grid_id, columns_positions, callbackFunction, false);
                })
            }
        },
    });

    var manageDrill = function(grid_id, columns_positions, callbackFunction, resize){
        var oTable = STONEGRIDS[grid_id];
        // Add drill icon
        $('#'+grid_id+' > tbody > tr').each(function(){
            for (var i=0 ; i<columns_positions.length; i++){
                var td = $(this).children("td:nth-child("+columns_positions[i]+")")
                if(!td.children('img').hasClass('drill-icon') && !td.children('div').hasClass('slider') && !td.hasClass('dataTables_empty')){
                    td.html('<img class="drill-icon" src="https://image.flaticon.com/icons/png/128/118/118740.png">'+td.html());
                }
            }
        });

        // Resize columns after adding drill icon
        if(resize){
            $('#'+grid_id).resizeColumns();
        }

        // Remove previous drill functionality
        $('#'+grid_id+' > tbody > tr > td > img').off('click');
        // Add drill functionality
        $('#'+grid_id+' > tbody > tr > td > img').on('click', function () {
            var tr = $(this).closest('tr');
            var td = $(this).closest('td');
            var row = oTable['gridmethods'].row(tr);
            var table_id = $(this).closest('table')[0].id;

            if (td.hasClass('shown')) {
                // This row is already open - close it
                this.src = "https://image.flaticon.com/icons/png/128/118/118740.png";
                row.child.hide();
                tr.removeClass('shown');
                td.removeClass('shown');
            }
            else {
                // Open this row
                if (row.child.isShown()){
                    // This row is already open by another column - close it
                    row.child.hide();
                    tr.removeClass('shown');
                    var last_td = tr.children("td.shown");
                    last_td.removeClass('shown');
                    last_td.children("img")[0].src = "https://image.flaticon.com/icons/png/128/118/118740.png";
                }
                this.src = "https://image.flaticon.com/icons/png/128/118/118738.png";

                var subgrid_id = table_id+"_"+oTable['itablecounter'];

                // Set subgrid class (table row) in order to have differences among subgrids
                var class_name = 'drill-odd'
                if($(this).parents('table').length % 2 == 0){
                   class_name = 'drill-even';
                }
                row.child(fnFormatDetails(subgrid_id, $('#'+table_id).width()-30), class_name).show();

                // $("#"+subgrid_id).DataTable();
                tr.addClass('shown');
                td.addClass('shown');
                oTable['itablecounter'] += 1

                var row_index = oTable['gridmethods'].row(tr).index();
                var row_column = oTable['gridmethods'].column(td).index();
                callbackFunction(table_id, subgrid_id, row_index, row_column);
            }

            // Resize columns after clicking drill icon
            $('#'+table_id).resizeColumns();
        });
    }

    var changeStyleButtons = function(element){
        var buttons = $('#'+element[0].id+'_wrapper .dt-buttons a')
        if (buttons.length>0){
            buttons.removeClass('dt-button buttons-excel buttons-html5 buttons-csv')
        }
    }

    function fnFormatDetails(table_id, width) {
        var sOut = "<div class=\"slider\"><table id=\"" + table_id + "\" width=\"" + width + "\">";
        sOut += "</table></div>";
        return sOut;
    }

    var createFooter = function(columns){
        var html_footer = ''
        for(var i = 0 ; i< columns.length; i++){
            var colname = columns[i]['data']//.replace(/\s+/g, '');
            html_footer+="<td id='" + colname + "_footer'></td>"
        }
        html_footer = '<tfoot><tr>' + html_footer + '</tfoot></tr>'
        return html_footer;
    }
    /**
     * Gets the default configuration grid.
     *
     * @param      {<dict>}    config  The configuration
     * @return     {<dict>}    The default configuration grid.
     */
    var getDefaultConfigGrid = function(config){
        var dataSet = [
            {
                "Tipo":       "Tiger Nixon",
                "Tarj":   "System Architect",
                "Traf":     "$3,120",
                "Benef": "2011/04/25",
                "office":     "Edinburgh",
                "extn":       "5421"
            },
            {
                "Tipo":       "Garrett Winters",
                "Tarj":   "Director",
                "Traf":     "$5,300",
                "Benef": "2011/07/25",
                "office":     "Edinburgh",
                "extn":       "8422"
            }
        ];
        var default_config = {
            data: dataSet,
            searching: false,
            paging: true,
            scrollY: 100,
            deferRender:    true,
            scroller:       true,
            scrollX: true,
            footer: false,
            // fixedColumns:   {
            //     leftColumns: 1,
            // },
            // dom: 'Bfrtip',
            // buttons: [
            //     {
            //         extend: 'excelHtml5',
            //         exportOptions: {
            //             columns: ':visible'
            //         }
            //     }, 
            //     {
            //         extend: 'pdfHtml5',
            //         exportOptions: {
            //             columns: ':visible'
            //         }
            //     }, 
            //     {
            //         extend: 'csvHtml5',
            //         exportOptions: {
            //             columns: ':visible'
            //         }
            //     }, 
            // ],
            columns: [
                { title: "Tipo" , data: "Tipo" },
                { title: "Tarj", data: "Tarj", render: $.fn.dataTable.render.number( '.', ',', 0) }, // thousand separator, decimal separator, floating point precision, prefix string (op), postfirx string (op)
                { title: "Traf", data: "Traf", render: $.fn.dataTable.render.number( '.', ',', 2) },
                { title: "Benef", data: "Benef", render: $.fn.dataTable.render.number( '.', ',', 2) },
            ],
        }
        var result = extendJqueryExtend(default_config, config)
        result = normalizerConfig(result)
        return result;
    }

    /**
     * { function_description }
     *
     * @param      {<type>}  config  The configuration
     */
    var normalizerConfig = function(config){
        config = searchBoolean(config)
        config['columns'] = normalizeColumns(config['columns'])
        return config
    }

    var normalizeColumns = function(columnConfig){
        var new_columns = []
        $.each(columnConfig, function(index, value){
            if(Object.keys(value).includes('render')){
                if(typeof(value['render'].includes)=='undefined'){
                    value['render'] = fillRender(value['render'])
                }
            }
            new_columns.push(value)
        })
        return new_columns
    }

    var fillRender = function(render){
        render = renderNumber(render['thousands'], render['decimal'], render['round'], render['prefix'], render['postfix'], render['mod'], render['number'])
        return render
    }

    var renderNumber = function(thousands, decimal, precision, prefix, postfix, operator, num){
        return {
                display: function ( d ) {
                    if (operator != ''){
                        if (operator == 'mul'){
                            var flo = parseFloat(d);
                            if (!isNaN(flo)){
                                d = d * num;
                            }
                        }
                    }
                    // dataTable.render.number function is called in order to avoid using __htmlEscapeEntities
                    return $.fn.dataTable.render.number(thousands, decimal, precision, prefix, postfix).display(d);
                }
            };
    }


    /**
     * Gets the grid columns.
     *
     * @param      {<str>}    grid_id  The grid id
     * @return     {<array>}  List of columns
     */
    var getGridColumns = function(grid_id){

        var grid = STONEGRIDS[grid_id];
        var api = grid.gridmethods.columns();
        var n_columns = api.count();
        var columns = new Array();

        for(var i=0;i<n_columns;i++){
            // Check which columns are visible
            // if (grid.gridmethods.columns().column(i).visible()){
            columns.push(grid.gridmethods.column(i).dataSrc());
            // }
        }
        return columns;
    }


    /**
     * Gets the column index.
     *
     * @param      {<str>}    grid_id  The grid id
     * @param      {<str>}    column_name  The internal column name
     * @return     {<int>}    the column index
     */
    var getColumnIndex = function(grid_id, column_name){
        return getGridColumns(grid_id).indexOf(column_name);
    }

})(jQuery)