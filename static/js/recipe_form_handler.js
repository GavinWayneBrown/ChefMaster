// static/js/recipe_form_handler.js

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add-instruction').addEventListener('click', function() {
        var formIdx = document.querySelectorAll('.instruction-form').length;
        var newForm = document.querySelector('.instruction-form').cloneNode(true);
        newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formIdx);
        newForm.querySelectorAll('input').forEach(function(input) {
            input.value = '';
        });
        document.getElementById('instructions').appendChild(newForm);
        
        // Update the management form
        document.getElementById('id_instruction_set-TOTAL_FORMS').value = formIdx + 1;
    });

    document.getElementById('add-ingredient').addEventListener('click', function() {
        var formIdx = document.querySelectorAll('.ingredient-form').length;
        var newForm = document.querySelector('.ingredient-form').cloneNode(true);
        newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formIdx);
        newForm.querySelectorAll('input').forEach(function(input) {
            input.value = '';
        });
        document.getElementById('ingredients').appendChild(newForm);
        
        // Update the management form
        document.getElementById('id_ingredient_set-TOTAL_FORMS').value = formIdx + 1;
    });

    // Handle removing instructions
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-instruction')) {
            event.target.closest('.instruction-form').remove();
            var formIdx = document.querySelectorAll('.instruction-form').length;
            document.getElementById('id_instruction_set-TOTAL_FORMS').value = formIdx;
        }
    });

    // Handle removing ingredients
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-ingredient')) {
            event.target.closest('.ingredient-form').remove();
            var formIdx = document.querySelectorAll('.ingredient-form').length;
            document.getElementById('id_ingredient_set-TOTAL_FORMS').value = formIdx;
        }
    });
});