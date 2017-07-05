$(function() {
  $("#form-step1").validate({
    rules: {
      id: {
        required: true,
        minlength: 4,
        maxlength: 16
      },
      pw: {
        required: true,
        minlength: 6,
        maxlength: 32
      },
      pw_re: {
        required: true,
        minlength: 6,
        maxlength: 32
      }
    },
    submitHandler: function(form) {
      $.ajax({
        url: form.action,
        type: form.method,
        data: $(form).serialize(),
        success: function(response) {
          document.location.href = "/main.html";
        },
        error: function(response, data) {
          console.log("error");
          alert(response.responseJSON.message);
        }
      });
    },
    debug: true
  });
});
