(function ($) {

    var $form = $('[data-role=poll]'),
        $resultBtn = $form.find('[href=#poll-result]');

    $form.submit(function (event) {

        $.post($form.attr('action'), $form.serialize(), function (response) {

            $resultBtn.tab('show');

            $form.find('#poll-result').html(response.result);

            if ($.notify) {
                $.notify({message: response.message}, {type: 'success'});
            }
        }).fail(function (response) {
            if ($.notify) {
                $.notify({message: response.responseText}, {type: 'error'});
            }
        });

        event.preventDefault();
        return false;
    });

})(jQuery);
