"use strict";
var STONEDATE = {};
(function($){
    var start_moment = moment().subtract(29, 'days');
    var end_moment = moment();
    $.fn.extend({
        createDate: function(config){
            var id_elem = this[0].id
            config = getDefaultParam(config)
            var elem = createHtml(this, config)
            $('#' + elem.id).daterangepicker(config)
            STONEDATE[id_elem] = config
            if (config['eventModified']){
                $('#' + elem.id).on('show.daterangepicker', function(ev, picker){
                    STONEDATE[id_elem]['last_value'] = $('#' + elem.id).val()
                });
                $('#' + elem.id).on('hide.daterangepicker', function(ev, picker){
                    if($('#' + elem.id).val() != STONEDATE[id_elem]['last_value']){
                        $('#' + id_elem).trigger( "modified:daterangepicker");
                        STONEDATE[id_elem]['last_selected'] = picker.chosenLabel
                    }
                });
            }
        }, 
        clearDate: function(config){
            config = STONEDATE[this[0].id]
            $('#' + this[0].id + '_range').data('daterangepicker').setStartDate(config['startDate']);
            $('#' + this[0].id + '_range').data('daterangepicker').setEndDate(config['endDate']);
        },
        getVal: function(config){
            return $('#' + this[0].id + '_range').serialize()
        },
        getSelection: function(config){
            return STONEDATE[this[0].id].date_ranges_map[STONEDATE[this[0].id].last_selected]
        }
    });

    function cb(start, end, elem, format) {
        elem.html(start.format(format) + ' - ' + end.format(format));
    }

    var createHtml = function(elem, config){
        var class_input = 'col-md-12'
        if(config['icon']){
            var span_el = document.createElement('span')
            span_el.setAttribute('class', 'add-on col-md-2')
            span_el.onclick = function(){$('#' + input_el.id).trigger('click')}
            var i_el = document.createElement('i')
            i_el.setAttribute('class', 'glyphicon glyphicon-calendar')
            i_el.id = 'cal'
            span_el.appendChild(i_el)
            elem.append(span_el)
            class_input = 'col-md-10'
        }
        class_input += ' text-center';
        var input_el = document.createElement('input')
        input_el.id = elem[0].id + '_range' 
        input_el.type = 'text'
        input_el.name = 'daterange'
        input_el.setAttribute('class', class_input)
        if(config['icon'] && !config['input']){
            input_el.style = 'visibility:hidden;width:0px'
        }
        elem.append(input_el)
        return input_el
    }

    var getDefaultParam = function(config){
        var dafult = {
            "eventModified":true,
            "icon": false,
            "input": true,
            "singleDatePicker": false,
            "showDropdowns": true,
            "showWeekNumbers": false,
            "showISOWeekNumbers": false,
            "timePicker": true,
            "timePicker24Hour": true,
            "timePickerSeconds": true,
            "autoApply": true,
            // "dateLimit": {
            //     "days": 7
            // },
            "ranges": {
                // "Today": [
                //     "2016-10-05 00:00:00",
                //     "2016-10-05 12:29:59",
                // ],
                // "Yesterday": [
                //     "2016-10-04 00:00:00",
                //     "2016-10-04 23:59:59",
                // ],
                // "Last 7 Days": [
                //     "2016-09-28 00:00:00",
                //     "2016-10-05 23:59:59",
                // ],
                // "Last 30 Days": [
                //     "2016-09-05 00:00:00",
                //     "2016-10-05 23:59:59",
                // ],
                // "This Month": [
                //     "2016-10-01 00:00:00",
                //     "2016-10-05 23:59:59",
                // ],
                // "Last Month": [
                //     "2016-09-01 00:00:00",
                //     "2016-09-30 23:59:59",
                // ]
            },

            "locale": {
                "format": "YYYY-MM-DD HH:mm:ss",
                "separator": " - ",
                "applyLabel": "Apply",
                "cancelLabel": "Cancel",
                "fromLabel": "From",
                "toLabel": "To",
                "customRangeLabel": "Custom",
                "weekLabel": "W",
                "daysOfWeek": [
                    "Su",
                    "Mo",
                    "Tu",
                    "We",
                    "Th",
                    "Fr",
                    "Sa"
                ],
                "monthNames": [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December"
                ],
                "firstDay": 1
            },
            "alwaysShowCalendars": false,
            "startDate": "2016-10-04",
            "endDate": "2016-10-04"
        }
        config = checkRanges(config)
        var result = extendJqueryExtend(dafult, config)
        result = normalizerConfig(result)
        return result;
    }
    var checkRanges = function(config){
        if('ranges' in config){
            var ranges = {}
            $.each(config['ranges'], function(index, item){
                $.each(item, function(key, value){
                    ranges[key] = value;
                })    
            })
            config['ranges'] = ranges
        }
        return config
    }

    /**
     * { function_description }
     *
     * @param      {<type>}  config  The configuration
     */
    var normalizerConfig = function(config){
        config = searchBoolean(config)
        return config
    }
})(jQuery)
