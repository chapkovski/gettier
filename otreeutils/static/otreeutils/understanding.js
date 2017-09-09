var N_QUESTIONS = null;
var HINT_TEXT_EMPTY = null;
var input_n_wrong_attempts = null;


function checkUnderstandingQuestionsForm() {
    var n_correct = 0;
    for (var q_idx = 0; q_idx < N_QUESTIONS; q_idx++) {
        var input_id = 'id_q_input_' + q_idx;
        var input_field = $('#' + input_id);
        var label = $('label[for=' + input_id + ']');
        var v = input_field.val();
       // self.isItKnowledge = v;
        var correct = $('#id_q_correct_' + q_idx).val();

        input_field.removeClass('error').addClass('ok');
        label.removeClass('error').addClass('ok');
        n_correct++;
    }

    if (n_correct == N_QUESTIONS) {
        $('#form').submit();
    } else {
        var cur_n_wrong_attempts = parseInt(input_n_wrong_attempts.val());
        if (isNaN(cur_n_wrong_attempts)) {
            cur_n_wrong_attempts = 0;
        }
        input_n_wrong_attempts.val(cur_n_wrong_attempts + 1);
    }
}


function setupUnderstandingQuestionsForm(n_questions, hit_text_empty, field_n_wrong_attempts, set_correct_answers) {
    N_QUESTIONS = n_questions;
    HINT_TEXT_EMPTY = hit_text_empty;
    input_n_wrong_attempts = $('#id_' + field_n_wrong_attempts);

    for (var q_idx = 0; q_idx < N_QUESTIONS; q_idx++) {
        var input_id = 'id_q_input_' + q_idx;
        var input_field = $('#' + input_id);
        var label = $('label[for=' + input_id + ']');

        if (set_correct_answers) {
            var correct = $('#id_q_correct_' + q_idx).val();
            input_field.val(correct);
        }

        input_field.focus(function (e) {   // reset classes function
            var inp = $(e.target);
            var par = inp.parent();
            var lbl = $('label[for=' + inp.prop('id') + ']');
            inp.removeClass('ok').removeClass('error');
            lbl.removeClass('ok').removeClass('error');
            par.find('.hint').remove();
        });
    }