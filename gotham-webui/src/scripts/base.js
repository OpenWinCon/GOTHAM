jQuery.validator.setDefaults({
  highlight: function(element, errorClass) {
      $(element).addClass("error");
  },
  unhighlight: function(element, errorClass) {
    $(element).removeClass("error");
    $(element).popover('destroy');
  },
  errorPlacement: function(error, element) {
    element.popover({content: error.html(), trigger: "hover", placement: "auto"});
  }
});
