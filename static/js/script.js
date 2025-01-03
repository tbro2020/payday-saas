$(function() {
    toastr.options = {
        "positionClass": "toast-bottom-right",
        "extendedTimeOut": "1000",
        "timeOut": "1500",
        "closeButton": true,
        "progressBar": true
    };

    // Transform DELETE inputs into checkboxes
    $('input[id*="DELETE"]').each(function() {
        $(this).attr('type', 'checkbox').addClass('checkboxinput form-check-input');
    });

    // Debounce function to limit the rate of function execution
    function debounce(func, delay) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    }

    // Function to handle saving changes
    function saveChanges(event) {
        // Make sure the api_change_url variable is defined
        if(typeof api_change_url === 'undefined') return;


        console.log('Saving changes...');
        const field = $(event.target);
        const fieldValue = field.val();
        const fieldName = field.attr('name');
        
        if (fieldName === '_metadata' || fieldName === undefined) return;

        const data = {};
        data[fieldName] = fieldValue;
        $.ajax({
            url: api_change_url,
            method: 'PUT', // or 'PATCH'
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: (response) => toastr.info('Changes saved successfully'),
            error: (error) => toastr.error('Error saving changes')
        });
    }

    // Create a debounced version of the saveChanges function
    const debounced = debounce(saveChanges, 1000);

    // Attach the debounced saveChanges function to form fields
    $('form').on('blur', 'input, select, textarea', debounced);
})