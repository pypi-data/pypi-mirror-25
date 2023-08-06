$(function() {

    $('.nav-tabs a').on('click', function(e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $('[data-role=multiselect]').multiSelect({
        selectableHeader: gettext('<p>Not selected</p>'),
        selectionHeader: gettext('<p>Selected</p>'),
    });

    // $('[data-role="datepicker"]').daterangepicker({
    //     autoUpdateInput: false,
    //     singleDatePicker: true,
    //     locale: {
    //         format: DATEPICKER_FORMAT
    //     }
    // }).on('apply.daterangepicker', function(ev, picker) {
    //     $(this).val(picker.startDate.format(DATEPICKER_FORMAT));
    // }).on('cancel.daterangepicker', function(ev, picker) {
    //     $(this).val('');
    // });

    $('[data-role="datepicker"]').datepicker({
        format: DATEPICKER_FORMAT,
        todayBtn: "linked",
        language: DATEPICKER_LANGUAGE,
        keyboardNavigation: false,
        todayHighlight: true
    });

    $('[data-role="timepicker"]').timepicker({
        timeFormat: TIMEPICKER_FORMAT,
        interval: 15,
        dropdown: true,
        scrollbar: true,
        dynamic: true
    });

    $('[data-role="daterangepicker"]').daterangepicker({
        autoUpdateInput: false,
        locale: {
            format: DATERANGEPICKER_FORMAT
        }
    }).on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format(DATERANGEPICKER_FORMAT) + ' - ' + picker.endDate.format(DATERANGEPICKER_FORMAT));
    }).on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });
})
