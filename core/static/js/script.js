$(document).ready(() => {
    toastr.options = {
        positionClass: "toast-bottom-right",
        extendedTimeOut: 1000,
        timeOut: 1500,
        closeButton: true,
        progressBar: true,
    };

    // Transform DELETE inputs into checkboxes
    $('input[id*="DELETE"]').each(function () {
        $(this).prop('type', 'checkbox').addClass('checkboxinput form-check-input');
    });

    // Debounce function to limit the rate of function execution
    const debounce = (func, delay) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    };

    // Function to get cookie value by name
    const getCookie = (name) => {
        const cookies = document.cookie.split(';').map(cookie => cookie.trim());
        const cookie = cookies.find(cookie => cookie.startsWith(`${name}=`));
        return cookie ? decodeURIComponent(cookie.split('=')[1]) : null;
    };

    // Function to handle saving changes
    const saveChanges = (event) => {
        if (typeof api_change_url === 'undefined') return;

        console.log('Saving changes...');
        const field = $(event.target);
        const fieldValue = field.val();
        const fieldName = field.attr('name');

        if (fieldName === '_metadata' || !fieldName) return;

        $.ajax({
            url: api_change_url,
            method: 'PATCH',
            crossDomain: true,
            contentType: 'application/json',
            data: JSON.stringify({ [fieldName]: fieldValue }),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            xhrFields: {
                withCredentials: true,
            },
            success: () => toastr.info('Changes saved successfully'),
            error: () => toastr.error('Error saving changes'),
        });
    };

    // Create a debounced version of the saveChanges function
    const debouncedSaveChanges = debounce(saveChanges, 1000);

    // Attach the debounced saveChanges function to form fields
    $('form').on('blur', 'input, select, textarea', debouncedSaveChanges);
});
