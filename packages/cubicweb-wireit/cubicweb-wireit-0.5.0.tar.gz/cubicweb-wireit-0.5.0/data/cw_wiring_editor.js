cw.wireiteditor_setup = function(wiring_eid, wiring_json, lang_eid, lang_json) {

  // Display wiring in the wireit editor

  $("body").addClass("yui-skin-sam");
  var lang = JSON.parse(lang_json);
  lang["languageEid"] = lang_eid;
  var wiring = JSON.parse(wiring_json);
  wiring["eid"] = wiring_eid;
  cw.wiring_editor = new WireIt.WiringEditor(wiring, "wireiteditor", lang);

  // Only for an editable wiring

  if ($('#wireiteditor.editable').length) {
    // setup form submission
    $('form.entityForm').submit(function() {
      var wiring_json = JSON.stringify(cw.wiring_editor.getValue().working);
      $(this).find('input[name^="json-subject:"]').val(wiring_json);
    });
  }
};
