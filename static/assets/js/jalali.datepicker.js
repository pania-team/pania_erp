// jalali.datepicker.js

(function ($) {
    $.fn.jalaliDatepicker = function (options) {
        var settings = $.extend({
            // Default settings
        }, options);

        this.each(function () {
            var $this = $(this);

            // Initialize datepicker
            $this.on('focus', function () {
                // Show datepicker
                console.log('Datepicker opened for ', $this);
            });

            // Custom behavior for Jalali datepicker
        });

        return this;
    };
})(jQuery);

$(document).ready(function () {
    // Initialize Jalali Datepicker on element with id 'id_start_date'
    $('#id_start_date').jalaliDatepicker();
});
