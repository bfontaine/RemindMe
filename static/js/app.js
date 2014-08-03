(function() {
  // RemindMe code
  // yo

  // TODO use Angular, this is just a test
  var $form = $('#sms-form');
  if (!$form.length) return;

  Date.setLocale($form.attr('data-locale'));

  $('#when').on('blur', function() {
    $(this).val(function(_, text) {
      return Date.future(text).toGMTString();
    });
  });
})();
