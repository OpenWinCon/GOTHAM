$(function() {
  $("#login-form").validate({
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
      }
    },
    debug: true
  });
});
