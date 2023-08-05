/*
*stoneSelect2.js
*Version: 1.0
*Author: Antonio  Palomo <antonio.palomo@stoneworksolutions.net>

*Copyright (c) 2016 StoneWorkSolutions. All rights reserved.
*/

var eurofiltersIU = function (config_data_out, callbackFunction, stoneselectDB){
	/**
	* Private vars
	* 
	* config_data = {							// Save all config
	* 	prefix:'ob', 							// Set at the end of all filter names
	* 	container:'ob',							// ID or class of a html element where filters go
	* 	automatic: true,						// If true all events invoke the function 
	* 	local: true,							// If true all filters load the local data 
	* }
	* callbackSelect2 = callbackFunction;		// Function which is invoked when automatic is true
	* filters_names = [] 						// 
	* options = {};								//
	* self = this;								//
	*/
	var self = this;
	self.config_data = {
		prefix:'ob',
		noneSelectedText: '------------',
		placeholder: 'Select options',
		container:'ob',
		automatic: true,
		staticdata: false,
		clientdata: false,
		local: true,
		setCategories: true,
		action: 'multiFilters',
		width: '',
		width_class: 'col-md-12 center-block',
		preload: false,
		search_input: true,
		mark_selected: true,
		min_width: '170px',
		request_type: 'GET',
	}
	self.callbackSelect2 = callbackFunction;
	self.filters_names = [] 
	self.stoneselectDB = stoneselectDB;
	self.options = {};
	self.lastClicked = ''
	self.filtersObjects = {}
	self.neededLaunchEvent = false
	self.selectBeforeOpen = {}
	self.numSelected = 0;
	self.waiting = false;
	self.children_id_infix = '__';
	self.actions = [];
	self.action_buttons = {}

	/** 
	* This is the constructor, merge the dict of config with the default values.
	*
	* @param {config_data_out} -- taked dict.
	* @return {}
	*/
	var eurofiltersIU = function(config_data_out){
		config_data_out = searchBoolean(config_data_out)
		$.each(self.config_data, function(key, value){
			if(value=='ob'){
				if(! key in config_data_out){
					console.log('El campo '+key+' es obligatorio.')
					return false;
				}
			}

		});

		$.each(config_data_out, function(key, value){
			self.config_data[key] = value
		});

		if(typeof(self.stoneselectDB)!='undefined'){
			self.stoneselectDB.addMessageFunction(self.config_data['prefix'], returnDataFromDB);
		}
	}

	var createSelectTag = function (name){
		var selectbox = document.createElement("select");
		selectbox.classList.add(self.configData(name, 'prefix')+name);
		selectbox.name = name;
		selectbox.multiple = 'multiple';
		
		
		var div_general = document.createElement('div');
		div_general.classList.add(self.configData(name, 'prefix')+name+'-container');

		if (self.configData(name, 'width_class')) {
			style_classes = self.configData(name, 'width_class').split(' ')
			style_classes.forEach(function(el){
					if (el != ""){
						div_general.classList.add(el);
					}
				}
			)
		}
		else{
			width = self.configData(name, 'width')
			div_general.style.cssText = "display:inline-block;margin:1px;width:"+width;
		}
		div_general.appendChild(selectbox);
		return div_general;
	};

	var createFieldsetTag = function (name, fieldset_id){
		var fieldset = document.createElement("fieldset");
		fieldset.id = fieldset_id;
		fieldset.classList.add('form-control');

		var legend = document.createElement("legend");
		legend.textContent = self.options[name]['fieldset']['placeholder'];
		legend.classList.add('ui-widget');

		fieldset.appendChild(legend);
		return fieldset;
	};

	self.configData = function(name_filter, option_name){
		option = typeof self.options[name_filter][option_name] !== 'undefined' ? self.options[name_filter][option_name] : self.config_data[option_name];
		return option
	}

	var automaticSelectUnselect = function(name_event, event_data, data_serialize, name_filter){
		if(name_event=='closing'){
			$('.select2-search').css({'display': 'none'})
			if(isNeedLaunchEvent(name_filter)){
				if(self.configData(name_filter,'automatic')){
					self.callbackSelect2('unselect', event_data, data_serialize, name_filter)	
				}
				else{
					self.callbackSelect2('waiting', event_data, data_serialize)
					self.waiting = true;
				}
			}
		}
	}

	self.isWaiting = function(){
		return self.waiting;
	}

	var loadData = function(name_event, event_data, name_filter, data_serialize){
		if(name_event == 'opening'){
				self.lockFilters()
				if(!self.configData(name_filter, 'staticdata')){
					if(!self.configData(name_filter, 'clientdata')){
						if(!self.configData(name_filter, 'local')|| self.stoneselectDB.filters.indexOf(self.options[name_filter]['db']) == -1){
							params = self.callbackSelect2('getParams')
							data = self.callbackSelect2('getRequestData')
							self.makeRequest(name_filter, params, data)
							self.callbackSelect2(name_event, event_data, data_serialize)
						}
						else{
							loadLocalDataSingle(self.options[name_filter]['db'], name_filter)
						}
					}
					else{
						name_filter_callback = name_filter
						if('dynamic_field' in self.options[name_filter]){
							name_filter_callback = self.options[name_filter]['dynamic_field']
						}
						data = self.callbackSelect2('getData', event_data, data_serialize, name_filter_callback)
						self.updateFilterData(name_filter, data)
					}
				}else{
					data =  self.options[name_filter]['data']
					if(typeof(self.options[name_filter]['data']) == 'undefined'){
						 data = []
					}
					self.updateFilterData(name_filter, data)
				}
		}
	}

	var launchEvent = function(name_event, event_data, name_filter){
		data_serialize = self.serializeStr()
		automaticSelectUnselect(name_event, event_data, data_serialize, name_filter)
		loadData(name_event, event_data, name_filter, data_serialize)
		styleFilters(name_filter)
	}

	var returnDataFromDB = function(message, data, prefix){
		if(prefix == self.config_data['prefix'] || prefix == 'ALL'){
			$.each(data, function(key, value){
				self.updateFilterData(key, value)
			});
		}
		if (message=='checkVersion'){
			self.unlockFilters()
		}
	}

	var loadLocalDataSingle = function(db, name){
		self.stoneselectDB.getData(db, self.configData(name, 'prefix'), name);
	}

	self.loadLocalData = function(){
		$.each(self.filters_names, function(index, val){
			loadLocalDataSingle(val)
		});
	}

	self.makeRequest = function(name, params, data){
		url = self.configData(name, 'url')+params+self.getFiltersNames()+self.getTypes()+self.getFilterSelected();
		$.ajax({
			type: self.configData(name, 'request_type'),
			url: url,
			data: data,
			dataType: 'json',
			// async: false,
			success: function(data){
				self.updateFilterData(name, data)
			},
			error: function(jqXHR, textStatus, errorThrown){
				self.updateFilterData(name, [])
				console.log(textStatus, errorThrown);
			}
		});
	}


	var addHtmlToContainer = function(name){
		var container = self.configData(name, 'container');
		if(self.options[name]['fieldset']){
			var fieldset_id = self.configData(name, 'prefix')+self.options[name]['fieldset']['name']+'-fieldset';
			if($(self.configData(name, 'container')+' '+'#'+fieldset_id).length == 0){
				var fieldset = createFieldsetTag(name, fieldset_id);
				$(self.configData(name, 'container')).append(fieldset);
			}
			container += ' #'+fieldset_id;
		}
		if( $(container+' '+'#'+self.configData(name, 'prefix')+name).length == 0 ){
			var selectbox = createSelectTag(name, self.options[name])
			self.html = selectbox;
			$(container).append(selectbox);
		}
	}

	var aplyConfigSelect2 = function(name, selected){
		opts = jQuery.extend({}, self.options[name])

		self.filtersObjects[name] = $('.' + self.configData(name, 'prefix') + name).multiselect(opts);

		if (self.configData(name, 'search_input'))
		{
			self.filtersObjects[name].multiselectfilter({'label': ''});
		}

		styleFilters(name)
		$('.ui-multiselect-menu').hide()
	}

	var styleFilters = function(name){
		$('.ui-multiselect-menu.ui-widget.ui-widget-content.ui-corner-all').css({'min-width': self.configData(name, 'min_width')})
		// float_style = 'right'
		// width = self.config_data['width']+'px'
		// if(self.config_data['width']==135){
		// 	if('placeholder' in self.options[name]){
		// 		if(!self.options[name]['placeholder']){
		// 			float_style = 'left'
		// 			width = '100%'
		// 		}
		// 	}
		// }

		// $('.'+self.config_data['prefix']+name+'-container button.ui-multiselect').css({'float': float_style, 'width': width})
		 
		// $('.'+self.config_data['prefix']+name+'-container button.ui-multiselect').classList.add('col-sm-6')
	}

	var updateConfigFilter = function(name, data, selected){
		opts = jQuery.extend({}, self.options[name])
		self.filtersObjects[name].multiselect(opts)
		setOptions(name, data, selected)
	}

	self.refreshFilter = function(name){
		self.filtersObjects[name].multiselect('refresh')
	}

	self.refreshAll = function(){
		$.each(self.filters_names, function(index, val){
			self.refreshFilter(val)
			styleFilters(val)
		})
	}

	self.addArrayData = function(name, data, selected_local){
		self.numSelected = 0;
		html = ''
		categories = [];
		// html += addOneData(name, {'id':0, 'text': self.config_data['placeholder']}, [])
		$.each(data, function(index, value){
			if('children' in value){
				html += addGroup(name, value)
				$.each(value['children'], function(index2, value2){
					element = addOneData(name, value2, selected_local, value)
					if (element){
						html += element
					}
				})
				html += closeGroup(name)
				// Avoid adding Selected category to internal filter categories
				if(value['text'] != 'Selected'){
					categories.push(value['id']);
				}

			}else{
				element = addOneData(name, value, selected_local, null)
				if (element){
					html += element
				}
			}
		})
		self.filtersObjects[name][0].innerHTML = html

		if(typeof(self.options[name]['categories']) == 'undefined'){
			self.options[name]['categories'] = categories;
		}
	}

	var addGroup = function(name, group){
		//{'id':12, 'text': 'adad', children :[]}
		return "<optgroup label='" + group['text'] + "'>"
	}

	var closeGroup = function(name){
		return "</optgroup>"
	}

	var addOneData = function(name, option, selected, optgroup){
		//{'id':12, 'text': 'adad', disabled:true, selected:true}
		id_option = option['id']
		text_option = option['text']
		disable = ''
		style = ''
		if ('disable' in option){
			disable = "disabled='disabled'"
		}
		if(option['id'] != null){
			if((selected.indexOf(parseInt(option['id']))!=-1)||(selected.indexOf(option['id'])!=-1)||(selected.indexOf(option['id'].toString())!=-1)){
				if((self.options[name]['max']==0) || (self.numSelected < self.options[name]['max'])){
					selected_attr = "selected='selected'"
					self.numSelected += 1;
				}
			}else{
				selected_attr = ""
			}
			class_value = ''
			if('active' in option){
				if(!option['active']){
					class_value = "class='non-active-option'"
				}
			}
			if('class' in option){
				class_value = "class='" + option['class'] + "'"
			}
			// Concatenate optgroup id to every option id if anyone has been selected
			if(optgroup && selected.length == 0){
				id_option = optgroup['id'] + self.children_id_infix + id_option;
			}
			action_buttons = ''
			self.actions.forEach(function(element){
				action_buttons += " button-"+element+"='"+self.action_buttons[element]+"'"
			})
			option = "<option value='"+ id_option +"' "+ disable +" "+selected_attr+" "+class_value+" actions="+self.actions.join(" ")+action_buttons+">" + text_option + "</option>"
			return option
		}
		else{
			return false
		}
	}

	self.addAction = function(action, button){
		self.actions.push(action)
		self.action_buttons[action] = button
	}

	var addFilter = function (name){
		addHtmlToContainer(name)
		aplyConfigSelect2(name)
	}

	var addFilterOne = function(name, id, opts){
		var selectbox = createSelectTag(name, opts)
		self.html = selectbox;
		$('#'+id).append(selectbox);	

		opts = jQuery.extend({}, opts)
		$('.'+self.configData(name, 'prefix')+name).multiselect(opts).multiselectfilter();

		styleFilters(name)
		$('.ui-multiselect-menu').hide()

	}

	self.removeNoActives = function(){
		$.each(self.filters_names, function(index, val){
			$('.'+self.configData(val, 'prefix')+val).next().css({'border-color': '#444'})
			styleFilters(val)
		})
		self.waiting = false;
	}

	var isNeedLaunchEvent = function(name){
		selectedBeforeOpen = self.selectBeforeOpen[name]
		selectedNow = self.serializeListIds()[name]
		if(selectedBeforeOpen.length != selectedNow.length){
			return true;
		}
		else{
			if(selectedNow.length==0){
				return false;
			}
			different = false;
			count = 0;
			while(!different && count<selectedNow.length){
				if(selectedBeforeOpen.indexOf(selectedNow[count]) == -1 ){
					return true;
				}
				count += 1;
			}
			return different;
		}
	}

	var styleOpen = function(name){
		// Check the device to focus on the input or not
		if(!( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))) {
			$('.ui-multiselect-menu .ui-multiselect-filter input').focus()
			$('.ui-multiselect-menu .ui-multiselect-filter input').keydown(function(e) {
				switch (e.which) {
	                 case 27:
	                 		self.close(name)
	                 	break;
	                 case 40:
							$(this).parent().parent().next().children().filter('li:visible').find('label')[0].focus()
							$($(this).parent().parent().next().children().filter('li:visible').find('label')[0]).addClass('ui-state-hover')
						break;
	             }
			});
		}
		if(self.options[name]['max']!=0){
			$('.ui-multiselect-all').addClass('ui-state-disabled');
		}
		else{
			$('.ui-multiselect-all').removeClass('ui-state-disabled');
		}
	}

	var getDefaultParam = function(name){
		opts_default = {header: true ,selectedList : 3, position: {my: 'left top',at: 'left bottom'} , max: 0, maxShow: 3, maxLetters: 3, numToShow: 10, multiple:true,checkAllText:'', uncheckAllText:'', noneSelectedText:self.config_data['noneSelectedText'], fieldset:null, width_class: self.config_data['width_class'],/*show: ["bounce", 200],hide: ["bounce", 1000],*/
			click: function(event, ui){
				name = event.target.getAttribute('class').replace(self.configData(name, 'prefix'),'')
				launchEvent('select', event, name)
				if(self.options[self.lastClicked]['max'] > 0){
					if ($(this).multiselect("widget").find("input:checked").length > self.options[self.lastClicked]['max'] && self.options[self.lastClicked]['max'] > 0){
							$(this).multiselect("widget").find("input:checked").each(function(num, x){
								if (x != event.currentTarget){
									$(x).attr("checked", false);
								}
							});
					} else {
							console.log('check a fex boxes' );
					}
					if(self.options[self.lastClicked]['max'] == 1){
						self.close(name)
					}
				}else {
				   		console.log('check a fex boxes' );
				}
				if(self.options[self.lastClicked]['min'] > 0){

				}

			},
			beforeopen: function(event){
				self.removeMessage()
				self.selectBeforeOpen = self.serializeListIds()
				name = event.target.getAttribute('class').replace(self.configData(name, 'prefix'),'')
				self.selectBeforeOpen[name] = self.serializeListIds()[name]
				self.lastClicked = name
				launchEvent('opening', event, name)
			},
			open: function(event){
				name = event.target.getAttribute('class').replace(self.configData(name, 'prefix'),'')
				launchEvent('open', event, name)
				styleOpen(name)
			},
			beforeclose: function(event){
				self.neededLaunchEvent = isNeedLaunchEvent(name)
				name = event.target.getAttribute('class').replace(self.configData(name, 'prefix'),'')
				launchEvent('closing', event, name)
				if((!self.configData(self.lastClicked, 'automatic') || self.configData(self.lastClicked, 'mark_selected'))&& self.neededLaunchEvent){
					$('.'+self.configData(name, 'prefix')+self.lastClicked).next().css({'border-color': '#0b93d5'})
				}
			},
			close: function(event){
				name = event.target.getAttribute('class').replace(self.configData(name, 'prefix'),'')
				launchEvent('close', event, name)
				//remove input text area
				$('.ui-multiselect-filter input').val('')
				$('.ui-multiselect-menu').hide()
			},
			checkAll: function(event){
				name = event.target.getAttribute('class').replace(self.configData(name, 'prefix'),'')
				launchEvent('select', event, name)
			},
			uncheckAll: function(event){
				name = event.target.getAttribute('class').replace(self.configData(name, 'prefix'),'')
				launchEvent('unselect', event, name)
			},
			beforeoptgrouptoggle: function(event, elements){
				if (elements['label']=='Selected')
				{
					return true
				}else{
					if (self.options[self.lastClicked]['max'] != 0 && (elements['inputs'].length + $(this).multiselect("widget").find("input:checked").length) > self.options[self.lastClicked]['max'])
					{
						if (self.options[self.lastClicked]['max'] == 1){
							message = self.options[self.lastClicked]['max'] + ' option max.'
						}
						else{
							message = self.options[self.lastClicked]['max'] + ' options max.'	
						}
						self.showMessage(message)
						return false
					}
				}
			},
			optgrouptoggle: function(event, ui){
			  var values = $.map(ui.inputs, function(checkbox){
			     return checkbox.value;
			  }).join(", ");
				  
			},selectedText: function(numChecked, numTotal, checkedItems){
				$('.' + self.configData(name, 'prefix') + self.lastClicked).next().children()[1].removeAttribute('title')
				var filter_name = self.options[self.lastClicked]['noneSelectedText'];
				if (filter_name.length>5){
					filter_name = filter_name.substr(0,5)
				}
				filter_name +=  ' : '
				if(checkedItems.length == 1){
					if(checkedItems[0].title.length>self.options[self.lastClicked]['numToShow']){
						result = filter_name + checkedItems[0].title.substring(0,self.options[self.lastClicked]['numToShow']-3)+'...'

						$('.' + self.configData(name, 'prefix') + self.lastClicked).next().children()[1].title = checkedItems[0].title
						class_name = $('select[name*="'+self.lastClicked+'"] option[value*="'+checkedItems[0].value+'"]').attr('class')
						$('.' + self.configData(name, 'prefix') + self.lastClicked).next().children()[1].className = class_name
					}
					else{
						result = filter_name + checkedItems[0].title	
					}
				}
				else if (checkedItems.length <= self.options[self.lastClicked]['maxShow']){
					result = ''
					for(i=0;i<checkedItems.length;i++){
						result += checkedItems[i].title.substring(0,self.options[self.lastClicked]['maxLetters']) + ','
					}
					result = filter_name + result.substring(0,result.length-1);
				}
				else{
					if (self.configData(name, 'preload')){
						result = filter_name + numChecked + ' selected';
					}
					else{
						result = filter_name + numChecked + ' of ' + numTotal/* + ' checked'*/;
					}
				}
				return result;
		   }
		}
		return opts_default;
	}

	var mergeOptions = function(options, index){
		opts_pos = searchBoolean(options[index])
		opts_default = getDefaultParam(opts_pos['name'])

		
		if(!('db' in opts_pos)){
			opts_pos['db'] = opts_pos['name']
		}

		opts_keys = Object.keys(opts_pos)
		$.each(opts_keys, function(index, val){
			opts_default[val] = opts_pos[val]
		})

		/*Used multiple like simple */
		if(!opts_default['multiple']){
			opts_default['max'] = 1
			opts_default['multiple'] = true
		}

		opts_default['noneSelectedText'] = opts_default['placeholder']
		return opts_default
	}

	/** 
	* Take one dict with one or more keys between ['automatic','local'], to change his initial value
	*
	* @param {data} -- dict with keys to change his value.
	* @return {}
	*/
	self.updateConfig = function(data){
		changed_fields = ['automatic', 'local', 'clientdata', 'staticdata', 'preload']
		$.each(data, function(key, value){
			if(changed_fields.indexOf(key) >= 0){
				self.config_data[key] = value
			}
			else{
				console.log('The field '+key+' is not available to update or not exists.')
			}
		})
	}

	var setOptionCategory = function(selected, selected_category, another_category, value){
		try{
			if((selected.indexOf(parseInt(value['id']))!=-1)||(selected.indexOf(value['id'])!=-1)||(selected.indexOf(value['id'].toString())!=-1)){
				selected_category[0]['children'].push(value)
			}else{
				another_category['children'].push(value)
			}
		}catch(err){
			another_category['children'].push(value)
		}
	}

	var setCategories = function(name, data, selected){
		// data.push({'id':1, 'text': 'guayaba', 'children':[{'id':12, 'text': 'guayaba1'}, {'id':13, 'text': 'guayaba2'}, {'id':14, 'text': 'guayaba4'}, {'id':15, 'text': 'guayaba4'}]})
		if(self.options[name]['multiple']){
			if(self.configData(name, 'setCategories') && (selected.length > 0) ){
				selected_options = [{'id':1, 'text': 'Selected', 'children': []}]
				options = [{'id':1, 'text': 'Options', 'children': []}]
				ohters = []
				others_categories = []
				other_category = {}
				$.each(data, function(index, val){
					if('children' in val){
						other_category = {'id':val['id'], 'text': val['text'], 'children': []}
						$.each(val['children'], function(index2, val2){
							// Concatenate optgroup id to every option id if there are different categories
							val_id = val['id'] + self.children_id_infix + val2['id'];
							var option = $.extend({}, val2);
							option['id'] =  val_id; 
							option['text'] = val2['text'];
							setOptionCategory(selected, selected_options, other_category, option)
						});
					}
					else{
						setOptionCategory(selected, selected_options, options[0], val)
					}

					if(Object.keys(other_category).length > 0){
						others_categories.push(other_category)
						other_category = {}
					}

				});
				if(options[0]['children'].length==0){
					options = []
				}

				return selected_options.concat(options).concat(others_categories)
			}
		}
		return data
	}

	/**
	* Gets selected ids with correct id format (category is concatenated to option_id).
	*
	* @param {data} -- dict with new values
	* @param {selected_ge} -- list with ids of selected options
	* @return {selected_ids} -- A list with formatted ids of selected options
	*/
	var getSelectedIds = function(data, selected_ge){
		var selected_list = [];
		$.each(selected_ge, function(index, value){
			selected_list.push(value.toString());
		})
		var selected_ids = [];
		$.each(data, function(index, value){
			if('children' in value){
				$.each(value['children'], function(index2, value2){
					// Concatenate optgroup id to option id
					val_id = value['id'] + self.children_id_infix + value2['id'];
					if(selected_list.indexOf(value2['id'].toString()) != -1 || selected_list.indexOf(val_id.toString()) != -1){
						selected_ids.push(val_id);
					}
				})
			} else {
				if(selected_list.indexOf(value['id'].toString()) != -1){
					selected_ids.push(value['id']);
				}
			}
		})
		return selected_ids;
	}

	/** 
	* Take a name of a filter and one dict of new values to be selected.
	*
	* @param {name} -- string which represent a name of a filter
	* @param {data} -- dict with new values.
	* @return {}
	*/
	self.updateFilterData = function(name, data, selected_ge){
		if(typeof(selected_ge)!='undefined'){
			self.lastClicked = name
		}
		selected_ge = typeof selected_ge !== 'undefined' ? getSelectedIds(data, selected_ge) : self.serializeListIds()[name];
		selected_dict = self.serializeDict()[name];
		self.options[name]['data'] = data;
		data = setCategories(name, data, selected_ge)
		self.addArrayData(name, data, selected_ge)
		self.refreshFilter(name)
		options_to_add = checkSelected(name, selected_dict)
		self.unlockFilters()
		styleFilters(name)
	}

	var checkSelected = function(name, selected_dict_old){
		selected_ids = self.serializeListIds()[name];
		options_to_add = []
		$.each(selected_dict_old, function(index, val){
			if(selected_ids.indexOf(val['id'])==-1 && selected_ids.indexOf(parseInt(val['id']))==-1 && selected_ids.indexOf(val['id'].toString())==-1){
				options_to_add.push(val)
				selected_ids.push(val['id'])
			}
		})
		if(options_to_add.length>0){
			data = self.options[name]['data']
			data = data.concat(options_to_add)
			data = setCategories(name, data, selected_ids)
			self.addArrayData(name, data, selected_ids)
			self.refreshFilter(name)
		}
		return options_to_add
	}
	/** 
	* Take a name of a filter and one dict with the new options.
	*
	* @param {name} -- string which represent a name of a filter
	* @param {opts_local} -- dict with new self.options.
	* @return {}
	*/
	self.updateFilterConfig = function(name, opts_local){
		selected_ge = self.serializeListIds()[name]
		self.clearOne(name)
		$.each(opts_local, function(key, val){
			self.options[name][key] = val
		})
		self.options[name] = searchBoolean(self.options[name])
		updateConfigFilter(name, [], selected_ge);
	}

	/** 
	* Create the filters in the html elemt indicated
	*
	* @param {self.options_l} -- A dict with the self.options of each filter. Example with the defaults values : {placeholder: config_data['prefix_placeholder']+filter.replace(config_data['remove_from_name'], ''),multiple: false,placeholder:true, data:[], closeOnSelect: true,allowClear: true, width: '100%' }
	* @return {}
	*/

	self.createFilters = function(options_l){
		self.lockFilters()
		$.each(options_l, function(index, val){
			self.options[val['name']] = mergeOptions(options_l, index)
			addFilter(val['name']);
			self.filters_names.push(val['name'])
		})
		self.unlockFilters()
	}


	/** 
	* Create the filter in the html elemt indicated
	*
	* @param {self.options_l} -- A dict with the self.options of each filter. Example with the defaults values : {placeholder: config_data['prefix_placeholder']+filter.replace(config_data['remove_from_name'], ''),multiple: false,placeholder:true, data:[], closeOnSelect: true,allowClear: true, width: '100%' }
	* @return {}
	*/

	self.createFilter = function(id, options_l, data){
		self.lockFilters()
		$.each(options_l, function(index, val){
			opts = mergeOptions(options_l, index)
			addFilter(val['name']);
		})
		self.unlockFilters()
	}

	/** 
	* Open the self.options of a filter
	*
	* @param {name} -- string which represent a name of a filter
	* @return {}
	*/
	self.open = function (name){
		self.filtersObjects[name].multiselect('open')
	}

	var closeAllExclude = function(name_filter){
		$.each(self.filters_names, function(index, val){
			if(name_filter!=val){
				self.close(val)
			}
		})
	}

	/** 
	* Close the self.options of a filter
	*
	* @param {name} -- string which represent a name of a filter
	* @return {}
	*/
	self.close = function (name){
		self.filtersObjects[name].multiselect('close')
	}

	/** 
	* Delete all the self.options of one filter
	*
	* @param {name} -- string which represent a name of a filter
	* @return {}
	*/
	self.clearOne = function (name){
		self.filtersObjects[name][0].innerHTML = ''
	}

	/** 
	* Delete all the self.options of all filters
	*
	* @return {}
	*/
	self.clearAll = function (){
		$.each(self.filters_names, function(index, val){
			self.clearOne(val)
			styleFilters(val)
		})
		self.refreshAll()
	}
	
	/** 
	* This method return a the selected values of all filters 
	*
	* @return {serialize_str} -- A string with the selected values in all filters. Example: "&nameFilter=id1,id"
	*/
	self.serializeStr = function(){
		serialize_str = "";
		$.each(self.filters_names, function(index, name){
			ids = self.filtersObjects[name].multiselect('getChecked')
			texts = self.filtersObjects[name].multiselect('getChecked').next()
			categories = self.options[name]['categories'];
			if(!categories){
				categories = [];
			}
			selected_str = ""
			$.each(ids, function(index, val){
				val = ids[index].value
				// It's necessary to remove category if it is concatenated to option id
				values = val.split(self.children_id_infix);
				if(values.length > 1 && categories.indexOf(values[0]) != -1){
					val = values[1];
				}
				selected_str += ','+val;

			})
			selected_str = selected_str.substring(1, selected_str.length)
			if(selected_str==""){
				selected_str = "NULL"
			}
			if('dynamic_field' in self.options[name]){
				serialize_str += '&'+self.options[name]['dynamic_field']+'='+selected_str
			}else{
				serialize_str += '&'+name+'='+selected_str
			}
		})
		
		return serialize_str
	}

	/**
	* This method returns the selected values of all filters group by categories if are specified (optgroup)
	*
	* @return {serialize_str} -- A string with the selected values in all filters (optgroup). Example: "&nameChildren1=id1,id2&nameChildren2=id3"
	*/
	self.serializeStrByGroup = function(){
		serialize_str = "";
		$.each(self.filters_names, function(index, name){
			ids = self.filtersObjects[name].multiselect('getChecked');
			texts = self.filtersObjects[name].multiselect('getChecked').next();
			categories = self.options[name]['categories'];

			if('dynamic_field' in self.options[name]){
				filter_name = self.options[name]['dynamic_field'];
			}else{
				filter_name = name;
			}

			if(!categories){
				categories = [];
				field_name_list = [filter_name];
			} else {
				field_name_list = categories.slice(0);
			}

			fields_dict = {}
			$.each(ids, function(index, val){
				val = ids[index].value;
				// It's necessary to remove category if it is concatenated to option id
				values = val.split(self.children_id_infix);
				if(categories && values.length > 1 && categories.indexOf(values[0]) != -1){
					field_name = values[0];
					val = values[1];
				} else {
					field_name = filter_name;
				}
				if(field_name in fields_dict){
					fields_dict[field_name] += ',' + val;
				} else {
					fields_dict[field_name] = val.toString();
				}
			})

			// If filter has categories and there are options that aren't belonged to any category
			if(categories && filter_name in fields_dict){
				field_name_list.push(filter_name);
			}

			$.each(field_name_list, function(index, field_name){
				if(field_name in fields_dict){
					selected_str = fields_dict[field_name];
				} else {
					selected_str = "NULL";
				}
				serialize_str += '&'+field_name+'='+selected_str;
			})
		})

		return serialize_str
	}

	self.getFiltersNames = function(){
		result_local = ''
		$.each(self.filters_names, function(index, val){
			if('dynamic_field' in self.options[val]){
				name = self.options[val]['dynamic_field']
				result_local += name+',';
			}else{
				result_local += val+',';
			}
		})
		return '&filters_names='+result_local
	}

	self.getTypes = function(){
		filter_selected = ''
		if(self.lastClicked!=''){
			if('dynamic_field' in self.options[self.lastClicked]){
				filter_selected = self.options[self.lastClicked]['dynamic_field']
				return '&types='+filter_selected;
			}
			else{
				return '&types='+self.lastClicked;
			}
		}
		
	}

	self.getFilterSelected = function(){
		filter_selected = ''
		if(self.lastClicked!=''){
			if('dynamic_field' in self.options[self.lastClicked]){
				filter_selected = self.options[self.lastClicked]['dynamic_field']
				return '&filter_selected='+filter_selected;
			}
			else{
				return '&filter_selected='+self.lastClicked;
			}
		}
		
	}

	self.getFilterSelectedName = function(){

		filter_selected = ''
		if(self.lastClicked!=''){
			if('dynamic_field' in self.options[self.lastClicked]){
				filter_selected = self.options[self.lastClicked]['dynamic_field']
				return filter_selected;
			}
			else{
				return self.lastClicked;
			}
		}
		
	}
	/** 
	* This method return a dict of dicts with the selected values of all filters
	*
	* @return {serialize_str} -- A string whith the selected values in all filters. Example: {nameFilter: [{id:id1, text:value1}, {id:id2, text:value2}]
	*/
	self.serializeDict = function (exclude_category){
		serialize_list_dicts = {};
		$.each(self.filters_names, function(index, name){
			ids = self.filtersObjects[name].multiselect('getChecked')
			texts = self.filtersObjects[name].multiselect('getChecked').next()
			if(exclude_category && self.options[name]['categories']){
				categories = self.options[name]['categories'];
			} else {
				categories = [];
			}
			selected_dict = []
			$.each(ids, function(index, val){
				val = ids[index].value
				if(categories){
					// It's necessary to remove category if it is concatenated to option id
					values = val.split(self.children_id_infix);
					if(values.length > 1 && categories.indexOf(values[0]) != -1){
						val = values[1];
					}
				}
				text = texts[index].textContent
				selected_dict.push({'id':val, 'text': text})
			})
			serialize_list_dicts[name] = selected_dict
		})
		return serialize_list_dicts;
	}

	/** 
	* This method return a dict of list with the selected values of all filters
	*
	* @return {serialize_str} -- A string whith the selected values in all filters. Example: {nameFilter: [id1, id2]
	*/
	self.serializeListIds = function (exclude_category){
		serialize_list_ids = {};
		$.each(self.filters_names, function(index, name){
			try {
			    ids = self.filtersObjects[name].multiselect('getChecked')
			}catch(err) {
				self.filtersObjects[name].multiselect(self.options[name])
				ids = self.filtersObjects[name].multiselect('getChecked')
			}
			texts = self.filtersObjects[name].multiselect('getChecked').next()
			if(exclude_category && self.options[name]['categories']){
				categories = self.options[name]['categories'];
			} else {
				categories = [];
			}
			selected_list = []
			$.each(ids, function(index, val){
				val = ids[index].value
				if(categories){
					// It's necessary to remove category if it is concatenated to option id
					values = val.split(self.children_id_infix);
					if(values.length > 1 && categories.indexOf(values[0]) != -1){
						val = values[1];
					}
				}
				selected_list.push(val)
			})
			serialize_list_ids[name] = selected_list
		})
		return serialize_list_ids;
	}

	self.serializeJson = function(serialize_by_category){
		serialize_json = {};
		$.each(self.filters_names, function(index, name){
			ids = self.filtersObjects[name].multiselect('getChecked');
			texts = self.filtersObjects[name].multiselect('getChecked').next();
			categories = self.options[name]['categories'];

			if('dynamic_field' in self.options[name]){
				filter_name = self.options[name]['dynamic_field'];
			}else{
				filter_name = name;
			}

			if(!categories){
				categories = [];
				field_name_list = [filter_name];
			} else {
				field_name_list = categories.slice(0);
			}

			fields_dict = {}
			$.each(ids, function(index, val){
				val = ids[index].value;
				// It's necessary to remove category if it is concatenated to option id
				values = val.split(self.children_id_infix);
				if(categories && values.length > 1 && categories.indexOf(values[0]) != -1){
					if(serialize_by_category){
						field_name = values[0];
					} else {
						field_name = filter_name;
					}
					val = values[1];
				} else {
					field_name = filter_name;
				}
				if(field_name in fields_dict){
					fields_dict[field_name].push(val.toString());
				} else {
					fields_dict[field_name] = [val.toString()];
				}
			})

			// If filter has categories and there are options that aren't belonged to any category
			if(categories && filter_name in fields_dict){
				field_name_list.push(filter_name);
			}

			$.each(field_name_list, function(index, field_name){
				if(field_name in fields_dict){
					selected = fields_dict[field_name];
				} else {
					selected = "NULL";
				}
				serialize_json[field_name] = selected;
			})
		})

		return JSON.stringify(serialize_json)
	}

	/** 
	* Lock all the filters
	*
	* @return {}
	*/
	self.lockFilters = function(){
		position = $(self.config_data['container']).css('position')
		if(self.config_data['local']){
			// $('.ui-multiselect-menu').block({'message':'<h2>Loading local data...</h2>'})
			$('.ui-multiselect-menu').stoneBlock({'background-size': '30%'})
		}
		else{
			// $('.ui-multiselect-menu').block({'message':'<h2>Loading server data...</h2>'})
			$('.ui-multiselect-menu').stoneBlock({'background-size': '30%'})
		}
	}

	/** 
	* Unlock all the filters
	*
	* @return {}
	*/
	self.unlockFilters = function(){
		// $(self.config_data['container']).unblock()
		// $('.ui-multiselect-menu').unblock()
		$('.ui-multiselect-menu').stoneUnblock()
	}

	self.hideFilter= function(name){
		$('.'+self.configData(name, 'prefix')+name+'-container').hide()
	}

	self.showFilter= function(name){
		$('.'+self.configData(name, 'prefix')+name+'-container').show()
	}

	self.showMessage = function(message){
		self.removeMessage()
		var liData = '<li class="messages_multiselect_jquery" style="display:none; margin: 4px; text-align: center;"></li>';
		$(liData).appendTo('.ui-multiselect-header').fadeIn('slow');
		jQuery('.messages_multiselect_jquery').html(message, 500);
	}

	self.removeMessage = function(){
		ele = jQuery('.messages_multiselect_jquery')
		if (ele.length!=0){ele.hide('slow', function(){ ele.remove(); });}
	}

	eurofiltersIU(config_data_out);
	return self;
	
}
