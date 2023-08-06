(function() {

   var util = YAHOO.util,lang = YAHOO.lang;
   var Event = util.Event, Dom = util.Dom, Connect = util.Connect,
     JSON = lang.JSON,widget = YAHOO.widget;

   /**
    * Module Proxy handle the drag/dropping from the module list to the layer
    * (in the WiringEditor)
    * @class ModuleProxy
    * @constructor
    * @param {HTMLElement} el
    * @param {WireIt.WiringEditor} WiringEditor
    */
   WireIt.ModuleProxy = function(el, WiringEditor) {
     this._WiringEditor = WiringEditor;
     WireIt.ModuleProxy.superclass.constructor.call(this,el, "module", {
       dragElId: "moduleProxy"
     });
     this.isTarget = false;
   };

   YAHOO.extend(WireIt.ModuleProxy,YAHOO.util.DDProxy, {
     /**
      * copy the html and apply selected classes
      * @method startDrag
      */
     startDrag: function(e) {
       WireIt.ModuleProxy.superclass.startDrag.call(this,e);
       var del = this.getDragEl(),
       lel = this.getEl();
       del.innerHTML = lel.innerHTML;
       del.className = lel.className;
     },

     /**
      * Override default behavior of DDProxy
      * @method endDrag
      */
     endDrag: function(e) {},

     /**
      * Add the module to the WiringEditor on drop on layer
      * @method onDragDrop
      */
     onDragDrop: function(e, ddTargets) {
       // The layer is the only target :
       var layerTarget = ddTargets[0],
       layer = ddTargets[0]._layer,
       del = this.getDragEl(),
       pos = YAHOO.util.Dom.getXY(del),
       layerPos = YAHOO.util.Dom.getXY(layer.el);
       this._WiringEditor.addModule(
	 this._module ,
	 [pos[0]-layerPos[0]+layer.el.scrollLeft,
	  pos[1]-layerPos[1]+layer.el.scrollTop]);
     }
   });

   /**
    * The WiringEditor class provides a 2 panels interface
    * @class WiringEditor
    * @constructor
    * @param {Object} options
    */
   WireIt.WiringEditor = function(wiring, domid, options) {

     this.modulesByName = {};
     this.setOptions(options);

     this.el = Dom.get(domid);

     this.layout = new widget.Layout(this.el, this.options.layoutOptions);
     this.layout.render();

     this.layer = new WireIt.Layer(this.options.layerOptions);
     this.layer.eventChanged.subscribe(this.onLayerChanged, this, true);

     this.modulesEl = Dom.get('modules');
     this.buildModulesList();

     this.eid = wiring.eid;
     this.displayWiring(wiring);
   };

   WireIt.WiringEditor.prototype = {

     /**
      * @method setOptions
      * @param {Object} options
      */
     setOptions: function(options) {

       /**
	* @property options
	* @type {Object}
	*/
       this.options = {};

       // Load the modules from options
       this.modules = options.modules || [];
       for(var i = 0 ; i < this.modules.length ; i++) {
	 var m = this.modules[i];
	 this.modulesByName[m.name] = m;
       }

       this.adapter = options.adapter || WireIt.WiringEditor.adapters.Ajax;

       this.options.languageEid = options.languageEid;

       this.options.propertiesFields = options.propertiesFields || [
	 {"type": "string", inputParams: {"name": "name", label: "Title", typeInvite: "Enter a title" } },
	 {"type": "text", inputParams: {"name": "description", label: "Description", cols: 30, rows: 4} }
       ];

       this.options.layoutOptions = options.layoutOptions || {
	 height: 800,
	 units: [
	   { position: 'left', width: 320, body: 'left', gutter: '0px', collapse: true,
	     collapseSize: 25, header: 'Modules', scroll: true, animate: true },
	   { position: 'center', body: 'center', gutter: '0px' }
	 ]
       };

       this.options.layerOptions = {};
       var layerOptions = options.layerOptions || {};
       this.options.layerOptions.parentEl = layerOptions.parentEl ? layerOptions.parentEl : Dom.get('center');
       this.options.layerOptions.layerMap = YAHOO.lang.isUndefined(layerOptions.layerMap) ? true : layerOptions.layerMap;
       this.options.layerOptions.layerMapOptions = layerOptions.layerMapOptions || { parentEl: 'layerMap' };

     },

     /**
      * Build the left menu on the left
      * @method buildModulesList
      */
     buildModulesList: function() {

       var modules = this.modules;
       for(var i = 0 ; i < modules.length ; i++) {
	 this.addModuleToList(modules[i]);
       }

       // Make the layer a drag drop target
       if(!this.ddTarget) {
	 this.ddTarget = new YAHOO.util.DDTarget(this.layer.el, "module");
	 this.ddTarget._layer = this.layer;
       }

     },

     /**
      * Add a module definition to the left list
      */
     addModuleToList: function(module) {

       var div = WireIt.cn('div', {className: "WiringEditor-module"});
       if(module.container.icon) {
         div.appendChild( WireIt.cn('img',{src: module.container.icon}) );
       }
       div.appendChild( WireIt.cn('span', null, null, module.name) );

       if (!Dom.hasClass(this.el, 'readonly')) {
	 var ddProxy = new WireIt.ModuleProxy(div, this);
	 ddProxy._module = module;
       }

       this.modulesEl.appendChild(div);
     },

     /**
      * add a module at the given pos
      */
     addModule: function(module, pos) {
       try {
	 var containerConfig = module.container;
	 containerConfig.position = pos;
	 containerConfig.title = module.name;
         containerConfig.eid = module.eid;
	 var container = this.layer.addContainer(containerConfig);
         container.eid = module.eid;
	 Dom.addClass(container.el, "WiringEditor-module-"+module.name);
       }
       catch(ex) {
	 this.alert("Error Layer.addContainer: "+ ex.message);
       }
     },

     /**
      * save the current module
      * @method saveWiring
      */
     saveWiring: function() {

       var value = this.getValue();

       this.tempSavedWiring = {
	 eid: this.eid,
	 working: JSON.stringify(value.working),
	 language: this.options.languageEid,
	 name: Dom.get('wiring-name').value
       };

       this.adapter.saveWiring(this.tempSavedWiring, {
	 success: this.saveWiringSuccess,
	 failure: this.saveWiringFailure,
	 scope: this
       });
     },

     /**
      * saveWiring success callback
      * @method saveWiringSuccess
      */
     saveWiringSuccess: function(o) {
       this.markSaved();
       window.location.href = o;
     },

     /**
      * saveWiring failure callback
      * @method saveWiringFailure
      */
     saveWiringFailure: function(errorStr) {
       this.alert("Unable to save the wiring : " + errorStr);
     },

     alert: function(txt) {
       if(!this.alertPanel){ this.renderAlertPanel(); }
       Dom.get('alertPanelBody').innerHTML = txt;
       this.alertPanel.show();
     },

     /**
      * @method displayWiring : displays a wiring description into the editor
      * @param {String} wiring : the wiring json description
      */
     displayWiring: function(wiring) {
       try {
	 this.preventLayerChangedEvent = true;
	 this.layer.clear();
	 if(lang.isArray(wiring.modules)) {
	   // Containers
	   for(i = 0 ; i < wiring.modules.length ; i++) {
             var m = wiring.modules[i];
             if(this.modulesByName[m.name]) {
               var baseContainerConfig = this.modulesByName[m.name].container;
               YAHOO.lang.augmentObject(m.config, baseContainerConfig);
               m.config.title = m.name;
               var container = this.layer.addContainer(m.config);
               container.eid = m.eid;
               Dom.addClass(container.el, "WiringEditor-module-"+m.name);
               container.setValue(m.value);
             }
             else {
               throw new Error("WiringEditor: module '"+m.name+"' not found !");
             }
	   }
	   // Wires
	   if(lang.isArray(wiring.wires)) {
             for(i = 0 ; i < wiring.wires.length ; i++) {
               this.layer.addWire(wiring.wires[i]);
             }
           }
	 }
	 this.markSaved();
	 this.preventLayerChangedEvent = false;
       }
       catch(ex) {
     	 this.alert(ex);
       }
     },

     renderAlertPanel: function() {
       this.alertPanel = new widget.Panel('WiringEditor-alertPanel', {
	 fixedcenter: true,
	 draggable: true,
	 width: '500px',
	 visible: false,
	 modal: true
       });
       this.alertPanel.setHeader("Message");
       this.alertPanel.setBody("<div id='alertPanelBody'></div><button id='alertPanelButton'>Ok</button>");
       this.alertPanel.render(document.body);
       Event.addListener('alertPanelButton','click', function() {
	 this.alertPanel.hide();
	 }, this, true);
     },

     onLayerChanged: function() {
       if(!this.preventLayerChangedEvent) {
	 this.markUnsaved();
       }
     },

     markSaved: function() {
       Dom.removeClass(Dom.get('wireiteditor-buttons'), 'unsaved');
     },

     markUnsaved: function() {
       Dom.addClass(Dom.get('wireiteditor-buttons'), 'unsaved');
     },

     isSaved: function() {
       return !Dom.hasClass(Dom.get('wireiteditor-buttons'), 'unsaved');
     },

     /**
      * This method return a wiring within the given vocabulary described by the modules list
      * @method getValue
      */
     getValue: function() {

       var i;
       var obj = {modules: [], wires: [], properties: null};

       for( i = 0 ; i < this.layer.containers.length ; i++) {
	 obj.modules.push( {name: this.layer.containers[i].options.title,
                            value: this.layer.containers[i].getValue(),
                            eid: this.layer.containers[i].eid,
                            config: this.layer.containers[i].getConfig()});
       }

       for( i = 0 ; i < this.layer.wires.length ; i++) {
	 var wire = this.layer.wires[i];

	 var wireObj = {
           src: {moduleId: WireIt.indexOf(wire.terminal1.container, this.layer.containers),
                 terminal: wire.terminal1.options.name},
           tgt: {moduleId: WireIt.indexOf(wire.terminal2.container, this.layer.containers),
                 terminal: wire.terminal2.options.name}
	 };
	 obj.wires.push(wireObj);
       }

       return {
	 working: obj
       };
     }


   };


   /**
    * WiringEditor Adapters
    * @static
    */
   WireIt.WiringEditor.adapters = {};


 })();
