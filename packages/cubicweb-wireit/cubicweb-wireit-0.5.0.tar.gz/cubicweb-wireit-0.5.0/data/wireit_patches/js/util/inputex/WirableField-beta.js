// This file should be placed between "inputEx/field.js" and all other inputEx fields
// see http://javascript.neyric.com/inputex
(function() {

   var lang = YAHOO.lang;

/**
 * Copy of the original inputEx.Field class that we're gonna override to extend it.
 * @class BaseField
 * @namespace inputEx
 */
inputEx.BaseField = inputEx.Field;

/**
 * Class to make inputEx Fields "wirable".Re-create inputEx.Field adding the wirable properties
 * @class Field
 * @namespace inputEx
 * @extends inputEx.BaseField
 */
inputEx.Field = function(options) {
   inputEx.Field.superclass.constructor.call(this,options);
};

lang.extend(inputEx.Field, inputEx.BaseField, {

   /**
    * Adds a wirable option to every field
    * @method setOptions
    */
   setOptions: function(options) {
      inputEx.Field.superclass.setOptions.call(this, options);

      this.options.wirable = lang.isUndefined(options.wirable) ? false : options.wirable;
      this.options.container = options.container;
      this.options.term_type = options.term_type;
      this.options.term_allowed_types = options.term_allowed_types;
      this.options.editable = lang.isUndefined(options.editable) ? true : options.editable;
      this.options.disabled = lang.isUndefined(options.disabled) ? false : options.disabled;
   },

   /**
    * Adds a terminal to each field
    * @method render
    */
   render: function() {
      inputEx.Field.superclass.render.call(this);

      if (this.options.disabled) {
         var name = $(this.divEl).text().strip();
         // consult a container/element option that overrides the module level option
         if (! $(this.options.container.options.canedit).attr(name)) {
           this.disable();
         }
      }

      if(this.options.wirable) {
         this.renderTerminal();
      }
   },

   /**
    * Render the associated input terminal
    * @method renderTerminal
    */
   renderTerminal: function() {

      var ttypes = this.options.term_type.split('_');
      var iotype = ttypes[0], fieldtype = ttypes[1];
      YAHOO.util.Dom.addClass(this.divEl, iotype);
      var wrapper = inputEx.cn('div', {
	className: 'WireIt-InputExTerminal ' + iotype + '_term ' + fieldtype});
      var pos, dir, fakedir, src;
      if (iotype == "output") {
	pos = this.fieldContainer.nextSibling;
	dir = [1,0];
	fakedir = [-1,0];
	src = true;
      }
      else {
	pos = this.labelDiv;
	dir = [-1,0];
	fakedir = [1,0];
	src = false;
      }

      this.divEl.insertBefore(wrapper, pos);
      this.terminal = new WireIt.Terminal(wrapper, {
         name: this.options.name,
         direction: dir,
         fakeDirection: fakedir,
	 editable: this.options.editable,
	 alwaysSrc: src,
         ddConfig: {
            type: this.options.term_type,
            allowedTypes: this.options.term_allowed_types
         },
      nMaxWires: 1 }, this.options.container);

      // Dfly name for this terminal
      this.terminal.dflyName = "input_"+this.options.name;

      // Reference to the container
      if(this.options.container) {
         this.options.container.terminals.push(this.terminal);
      }

      // Register the events
      this.terminal.eventAddWire.subscribe(this.onAddWire, this, true);
      this.terminal.eventRemoveWire.subscribe(this.onRemoveWire, this, true);
    },

    /**
     * Remove the input wired state on the
     * @method onAddWire
     */
    onAddWire: function(e, params) {
       this.options.container.onAddWire(e,params);
       if (! this.options.container.options.canedit) {
           this.disable();
       }
       if (this.el.value === '') {
           this.el.value = "[wired]";
       }
       YAHOO.util.Dom.addClass(this.divEl, 'Wired');
    },

    /**
     * Remove the input wired state on the
     * @method onRemoveWire
     */
    onRemoveWire: function(e, params) {
       this.options.container.onRemoveWire(e,params);

       this.enable();
       this.el.value = "";
       YAHOO.util.Dom.removeClass(this.divEl, 'Wired');
    }

});


})();