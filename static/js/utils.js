angular.module('rmUtils', [])

  /**
   * rmL10n
   * ======
   *
   * l10n/i18n utilities
   **/
  .service('rmL10n', function() {

    /**
     * .getString
     * ----------
     *
     * Return a string from the template. This should be used instead of
     * hard-coded strings. To include translatable strings in the HTML with
     * Jinja/Babel, use:
     *    <script type="text/x-strings" id="_strings">
     *    key1:{{ _("the string 1") }}
     *    key2:{{ _("the string 2") }}
     *    </script>
     * Each string should have an unique key, which you'll give to `getString`.
     **/
    this.getString = (function() {
      var strs = {};

      $(function() {
        var lines = $('#_strings').html().split(/\n+/);
        $.each(lines, function(_, line) {
          var kv = line.split(/^([^:]+):/);
          if (kv) {
            strs[kv[1]] = kv[2];
          }
        });
      });

      return function(k) { return strs[k]; };
    })();
  })

  /**
   * rmTime
   * ======
   *
   * Date/time utilities
   **/
  .service('rmTime', function() {

    /**
     * .combineDateTime(date, time[, withSeconds])
     * ===========================================
     *
     * Combine a date and a time, using only its hours/minutes (no seconds).
     **/
    this.combineDateTime = function(date, time, withSeconds) {
      var d = angular.copy(date);

      d.setHours(time.getHours());
      d.setMinutes(time.getMinutes());
      d.setSeconds(withSeconds ? time.getSeconds() : 0);

      return d;
    };

    /**
     * .sameDay(day1, day2)
     * ====================
     *
     * Return true if both dates are on the same day.
     **/
    this.sameDay = function(day1, day2) {
      return day1.getDate() === day2.getDate() &&
             day1.getMonth() === day2.getMonth() &&
             day1.getFullYear() === day2.getFullYear();
    };
  })

  ;

// other stuff
$(function() {

  /**
   * Submit a form from a link with:
   *
   *  <form ... name="myname">...</form>
   *  ...
   *  <a ... data-rm-submit-"myname">...</a>
   **/
  $('a[data-rm-submit]').click(function() {
    var name = $(this).data('rmSubmit');
    $('form[name="' + name + '"').first().submit();
  });


});
