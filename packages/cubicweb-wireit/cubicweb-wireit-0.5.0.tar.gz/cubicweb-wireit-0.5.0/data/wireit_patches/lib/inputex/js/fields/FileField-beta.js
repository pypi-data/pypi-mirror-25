(function() {

   var inputEx = YAHOO.inputEx, Event = YAHOO.util.Event;

/**
 * @class Create a file input
 * @extends inputEx.Field
 * @constructor
 * @param {Object} options Added options:
 * <ul>
 * </ul>
 */
inputEx.FileField = function(options) {
	inputEx.FileField.superclass.constructor.call(this,options);
};
YAHOO.lang.extend(inputEx.FileField, inputEx.Field, 
/**
 * @scope inputEx.FileField.prototype   
 */   
{
   // return eid set by file upload if any
    getValue: function() {
      return this.el.getAttribute('eid');
    },

    setValue: function(value, sendUpdatedEvt) {
      // XXX use of jQuery here
      if (!value) {return;}
      var inputFile = this.el;
      var field = this;
      field.el.setAttribute('eid', value);
      $(field.elvalue).one('server-response', function(event) {
	var $fileLink = $(event.target).find('a').attr('target', '_blank');
	$(field.divEl).find('input').hide();
	if ($('#wireiteditor').hasClass('editable')) {
	  $('<img src="/data/cancel.png" style="cursor: pointer" />').one('click', function() {
	    $(field.el).show();
	    $(field.el).removeAttr('eid');
	    $(field.elvalue).empty();
	  }).appendTo($fileLink.parent());
	}
      });
      $(field.elvalue).loadxhtml('/' + value, {vid: 'wireit_fileincontext', __notemplate: ''});
    },

   /**
    * Render an 'INPUT' DOM node
    */
   renderComponent: function() {
      
      // Attributes of the input field
      var attributes = {};
      attributes.id = this.divEl.id?this.divEl.id+'-field':YAHOO.util.Dom.generateId();
      attributes.type = "file";
      if(this.options.name) attributes.name = this.options.name;
   
      // Create the node
      this.el = inputEx.cn('input', attributes);
      this.elvalue = inputEx.cn('div', {id: attributes.id + '-file'}); // file link container

      // Setup file upload
      var field = this;
      $(this.el).attr('data-url', '/wireit_upload').fileupload({
        dataType: 'json',
        paramName: 'files[]',
        done: function(e, data) {
	  field.setValue(data.result.eid);
        }
      });
      
      // Append it to the main element
      this.fieldContainer.appendChild(this.el);
      this.fieldContainer.appendChild(this.elvalue);
   },

  disable: function() {this.el.disabled = true;}
});

/**
 * Register this class as "file" type
 */
inputEx.registerType("file", inputEx.FileField);

})();