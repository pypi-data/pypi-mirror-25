(function ($) {
    $('input[type="file"]').closest('.form-row').addClass('pa_upload-file');

    $('.form-row.pa_upload-file label').append('<div class="upload-ico"><i class="fa fa-upload" /></div>');
    $('.submit-row a.deletelink').html('<i class="fa fa-trash"/>');

    $('#result_list input[type="checkbox"]').parent().addClass('emit-select');
    $('.checkbox-row, .emit-select').each(function (i, elem) {
        if ($(elem).find('input[type="checkbox"]').prop('checked')) {
            $(elem).addClass('active');
        }
    });

    $('.checkbox-row, .emit-select').click(function () {
        $(this).toggleClass('active');
        $(this).find('input[type="checkbox"]').prop('checked', $(this).hasClass('active'));
    });

    $('#result_list thead span.emit-select').click(function () {
        $('input[name="_selected_action"]').trigger('click');
    });

    $('.form-row').each(function (i, elem) {
        var label = $(elem).find('label').first();
        // label.hide();
        label.next().attr('placeholder', "Enter " + label.text())

    });

    $('.vLargeTextField, .vTextField').focus(function () {
        $(this).closest('.form-row').addClass('focused');
    });

//On focusout event
    $('.vLargeTextField, .vTextField').focusout(function () {
        $(this).closest('.form-row').removeClass('focused');
    });

//On label click
    $('body').on('click', '.form-float .form-line .form-label', function () {
        $(this).parent().find('input').focus();
    });

//Not blank form
    $('.form-control').each(function () {
        if ($(this).val() !== '') {
            $(this).parents('.form-line').addClass('focused');
        }
    });
    $('select[multiple="multiple"]').each(function (i, elem) {
        if (!elem.classList.contains('selectfilter')) {
            $(elem).multiSelect();
        }
    });

})(django.jQuery);
