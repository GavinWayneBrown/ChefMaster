
    // Add this temporarily at the start of your script section
    document.addEventListener('DOMContentLoaded', function() {
        // Log all form input names
        document.querySelectorAll('input[type="hidden"]').forEach(input => {
            console.log('Input name:', input.name);
        });
    });
     console.log('')
            document.getElementById('add-instruction').addEventListener('click', function() {
        // Get the total forms input
        var totalFormsInput = document.querySelector('input[name$=TOTAL_FORMS]');
        var formIdx = parseInt(totalFormsInput.value);
        
        // Get the template form
        var template = document.querySelector('.instruction-form');
        var newForm = template.cloneNode(true);
        
        // Replace prefix in the new form
        newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formIdx);
        
        // Update input names and ids
        newForm.querySelectorAll('input, textarea').forEach(function(input) {
            // Update name attribute
            input.setAttribute('name', input.getAttribute('name').replace(/-\d+-/, '-' + formIdx + '-'));
            
            // Update id attribute
            input.setAttribute('id', input.getAttribute('id').replace(/_\d+_/, '_' + formIdx + '_'));
            
            // Clear the value
            input.value = '';
        });
        
        // Append the new form
        document.getElementById('instructions').appendChild(newForm);
        
        // Increment the total forms count
        totalFormsInput.value = formIdx + 1;
    });
    
    document.getElementById('add-ingredient').addEventListener('click', function() {
        // Be specific about which TOTAL_FORMS we're getting
        var totalFormsInput = document.querySelector('[name="ingredient_set-TOTAL_FORMS"]');
        var formIdx = parseInt(totalFormsInput.value);
        
        var template = document.querySelector('.ingredient-form');
        var newForm = template.cloneNode(true);
        
        newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formIdx);
        
        newForm.querySelectorAll('input').forEach(function(input) {
            input.setAttribute('name', input.getAttribute('name').replace(/-\d+-/, '-' + formIdx + '-'));
            input.setAttribute('id', input.getAttribute('id').replace(/_\d+_/, '_' + formIdx + '_'));
            input.value = '';
        });
        
        document.getElementById('ingredients').appendChild(newForm);
        totalFormsInput.value = formIdx + 1;
    });