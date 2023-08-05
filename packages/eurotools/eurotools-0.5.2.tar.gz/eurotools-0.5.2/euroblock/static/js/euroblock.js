"use strict";
var STONEBLOCK = {};
(function($){
    $.fn.extend({
        stoneBlock: function(config){
            var config = getDefaultParam(config)
            var elem = createHtml(this, config)
            if(elem){
                var elem_jq = $(this.selector + '_block')
                elem_jq.addClass('stone-loading')
                elem_jq.css(config)
            }
            if (this.selector in STONEBLOCK && !isNaN(STONEBLOCK[this.selector])){
                STONEBLOCK[this.selector] += 1 
            }
            else{
                STONEBLOCK[this.selector] = 1
            }
        },
        stoneUnblock: function(){
            STONEBLOCK[this.selector] -= 1
            if(STONEBLOCK[this.selector] == 0){
                $(this.selector + '_block').remove()
                delete(STONEBLOCK[this.selector])
            }
        },
    });

    var createHtml = function(elem, config){
        if(elem.length > 0){
            var div_el = document.createElement('span')
            if (elem.selector[0] == '#'){
                div_el.id = elem.selector.replace('#', '') + '_block'
            }
            else{
                div_el.className = elem.selector.replace('.', '') + '_block'   
            }
            elem.append(div_el)
            return div_el
        }
        return false;
    }

    var getDefaultParam = function(config){
        var css = {
            
        }
        var result = extendJqueryExtend(css, config)
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
        return config
    }

})(jQuery)