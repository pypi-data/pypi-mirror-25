var eurofiltersIndexedDB = function (filters, partition, unique_exec_id){

	var BROWSERS_PARTIALLY_SUPPORTED = ['safari', 'explorer']
	var BROWSERS_DICT = {
		'Chrome': 'chrome',
		'MSIE': 'explorer',
		'Trident': 'explorer',
		'Firefox': 'firefox',
		'Safari': 'safari',
		'Opera': 'opera'
	}
	var messageFunction = [];
	var prefixes = [];
	var self = this;
	var db;
	var _partition = partition;
	var url_static_filters = '/international/eurofilters/check/';
	self.checkVersionFinished = false;
	self.delete_older = false;
	self.filters;

	self.addMessageFunction = function(prefix, newFunction){
		messageFunction.push(newFunction);
		prefixes.push(prefix)
	}

	var setConfig = function(filters){
		self.filters = filters;
	}
	
	var getBrowserName = function (){
		for(browser in BROWSERS_DICT){
			if(navigator.userAgent.indexOf(browser) != -1){
				return BROWSERS_DICT[browser];
			}
		}
		return '';
	}

	var initVersionData = function (filters){
		filters.forEach(function(element){
			var request = self.db.transaction("filters_version", "readwrite").objectStore("filters_version").add({ id: element, version: 0 });
			request = self.db.transaction("filters_value", "readwrite").objectStore("filters_value").add({ id: element, value: 0 });
		})
	};

	var deletekeys = function(filters){
		filters.forEach(function(element){
			var request = self.db.transaction("filters_version", "readwrite").objectStore("filters_version").delete(element);
			request = self.db.transaction("filters_value", "readwrite").objectStore("filters_value").delete(element);
		})
	}

	var notin = function(dbfilters, serverfilters){
		notinFilters = []
		dbfilters.forEach(function(element){
			if(!serverfilters.includes(element)){
				notinFilters.push(element)
			}
		})
		return notinFilters
	}

	var deleteOlder = function(){
		filters_result = []
		var deferred = $.Deferred()
		connection(deferred)
		deferred.done(function(event_type, event){
			var transaction = self.db.transaction('filters_value', "readwrite");
			var objectStore = transaction.objectStore("filters_value");
			var request_local = objectStore.openCursor();
			var value = {}
			request_local.onsuccess = function(event){
				cursor = request_local.result;
				if(cursor){
					filters_result.push(cursor.value.id)
					cursor.continue();
				}
				else{
					return
				}
			}
			request_local.onerror = function(){
				console.log('error request update data')
				return
			}
			transaction.oncomplete = function(){
				to_delete = notin(filters_result, self.filters)
				if (to_delete.length > 0){
					deletekeys(to_delete)
				}
				return
			}
			transaction.onerror = function(){
				console.log('error update data')
				return
			}
		});
	};

	var cleanOldFilters = function(){

	}

	var endCheckVersion = function(data){
		self.checkVersionFinished = true;
		sendNotifications('checkVersion', data, 'ALL')
	}

	var updateDBFilter = function(response){
		response = JSON.parse(response)
		if(Object.keys(response).length > 0){
			updateVersions(response)
			updateData(response)	
		}
		else{
			endCheckVersion(response)
		}
		
	};

	var sendNotifications = function(message, data, prefix){
			$.each(messageFunction, function(index, val){
					val(message, data, prefix)
			})
	}

	var updateVersions = function(response){
		var transaction = self.db.transaction('filters_version', "readwrite");
		var objectStore = transaction.objectStore("filters_version");
		var request_local = objectStore.openCursor();
		var value = {}
		request_local.onsuccess = function(event){
			cursor = request_local.result;
			if(cursor){
				if (cursor.value.id+'__version' in response){
					cursor.value.version = response[cursor.value.id+'__version']
					cursor.update(cursor.value);
				}
				cursor.continue();
			}
			else{
				return
			}
		}
		transaction.oncomplete = function(){
			return
		}
	};

	var connectEventSource = function(unique_exec_id){
		console.log('connecting to filters event source...')
		// Listen messages
		filter_eventsource = new EventSource('/stoneFilterMessages/'+unique_exec_id+'/');

		// Before leaving the page (i.e.: reload page) the event message is closed in order to prevent event message disconnection error
		window.onbeforeunload = function() {
			filter_eventsource.close();
		}

		filter_eventsource.addEventListener('open', function(e) {
			if (e.readyState == EventSource.CLOSED) {
				console.log('Connection to filter stream closed!')
			}
			console.log('Connection to filter stream opened!')
		}, false);


		filter_eventsource.onerror = function(e){
			console.log('ERROR connection channel')
		}

		filter_eventsource.addEventListener("updateVersion", function(e) {
			console.log('Received update filter event!!')
			self.initAndCheckVersion()
		});
	};

	connectEventSource(unique_exec_id);

	var updateData = function(response){
		var transaction = self.db.transaction('filters_value', "readwrite");
		var objectStore = transaction.objectStore("filters_value");
		var request_local = objectStore.openCursor();
		var value = {}
		request_local.onsuccess = function(event){
			cursor = request_local.result;
			if(cursor){
				if (cursor.value.id in response){
					cursor.value.value = JSON.stringify(response[cursor.value.id])
					cursor.update(cursor.value);
				}
				cursor.continue();
			}
			else{
				return
			}
		}
		request_local.onerror = function(){
			console.log('error request update data')
			return
		}
		transaction.oncomplete = function(){
			endCheckVersion(value)
			console.log('complete update data')
			return
		}
		transaction.onerror = function(){

			console.log('error update data')
			return
		}
	};

	self.getData = function(db, prefix, name){
		var deferred = $.Deferred()
		connection(deferred)
		deferred.done(function(event_type, event){
			var transaction = self.db.transaction('filters_value', "readwrite");
			var objectStore = transaction.objectStore("filters_value");
			var request_local = objectStore.openCursor();
			var value = {}
			request_local.onsuccess = function(event){
				cursor = request_local.result;
				if(cursor){
					if(db){
						if(cursor.value.id == db){
							value[name] = JSON.parse(cursor.value.value)
						}
					}else{
						value[name] = JSON.parse(cursor.value.value)
					}
					cursor.continue();
				}
				else{
					return
				}
			}
			request_local.onerror = function(){
				console.log('error request update data')
				return
			}
			transaction.oncomplete = function(){
				sendNotifications('getData', value, prefix)
				return
			}
			transaction.onerror = function(){
				console.log('error update data')
				return
			}
		});
	};

	self.checkVersionServer = function(values){
		result = ''
		self.filters.forEach(function(element){result += ','+element})
		values['filters'] = result.substr(1)
		values['partition'] = _partition
		$.ajax({
			type: 'POST',
			url: url_static_filters,
			data: values,
			dataType: 'json',
			success: function(response) {
				updateDBFilter(response)
			},
		});
		
	};

	self.checkVersion = function(){
		filters_to_add = self.filters.slice()
		if (self.db){
			var transaction = self.db.transaction('filters_version');
			var objectStore = transaction.objectStore("filters_version");
			var request_local = objectStore.openCursor();
			var value = {}
			request_local.onsuccess = function(event){
				cursor = request_local.result;
				if(cursor){
					if (filters_to_add.indexOf(cursor.value.version)>-1){filters_to_add.splice(filters_to_add.indexOf(cursor.value.version), 1)}
					value[cursor.value.id] = cursor.value.version
					cursor.continue();
				}
				else{
					return
				}
			}
			transaction.oncomplete = function(){
				initVersionData(filters_to_add)
				self.checkVersionServer(value)
				return
			}
			return 
		}
		else{
			console.log('DB is not ready.')
		}
	};

	self.removeDatabase = function(){
		window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB;
		if(window.indexedDB == undefined){
			console.log('IndexedDB is not supported by this browser.')
			return 0
		} else if(BROWSERS_PARTIALLY_SUPPORTED.indexOf(getBrowserName()) != -1){
			console.log('The filters may not work as expected on this web browser.')
		}
		var request = window.indexedDB.open('stonework_filters',1);
		window.indexedDB.deleteDatabase('stonework_filters');

	}

	var connection = function(deferred){
		window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB;
		if(window.indexedDB == undefined){
			console.log('IndexedDB is not supported by this browser.')
			return 0
		} else if(BROWSERS_PARTIALLY_SUPPORTED.indexOf(getBrowserName()) != -1){
			console.log('The filters may not work as expected on this web browser.')
		}
		var request = window.indexedDB.open(_partition + '_stonework_filters',2);
		request.onupgradeneeded = function(event){
			self.db = request.result;
			self.db.onerror = function(event) {
				console.log("Database error: " + event.target.errorCode);
			};
			deferred.resolve('onupgradeneeded', event);
		};
		request.onsuccess = function(event){
			self.db = request.result;
			deferred.resolve('onsuccess', event);
		};
		request.onerror = function(event){
			self.db = request.result;
			deferred.resolve('onerror', event);
		};
	}

	self.initAndCheckVersion = function(){
		
		var deferred = $.Deferred()
		connection(deferred)
		deferred.done(function(event_type, event){
			if(event_type=='onupgradeneeded'){
				var objectStore_values = "";
				var objectStore_version = "";
				if(event.oldVersion < 1 )
				{
					objectStore_values = self.db.createObjectStore("filters_value", { keyPath: "id" });
					objectStore_values.createIndex('value', 'value', { unique: false });
					objectStore_version = self.db.createObjectStore("filters_version", { keyPath: "id" });
					objectStore_version.createIndex('version', 'version', { unique: false });
					objectStore_version.transaction.oncomplete = function(event) {
					    initVersionData(self.filters);
					    self.checkVersion();
					}
				}
				if(event.oldVersion == 1 )
				{
					// Let`s delete the active filters , grouped by ooint_active.
					self.delete_older = true;
				}
			}
			if(event_type=='onsuccess'){
				if (self.delete_older){
					deleteOlder()
				}
				self.databaseReady = true;
				self.checkVersion()
			}
		});
		return 1;
	}	
	setConfig(filters);
}
	