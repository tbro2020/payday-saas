$(document).ready(function () {
    const MAX_ROWS = 200;
    const REQUIRED_COLUMNS = [
        /* { name: 'surname', type: 'string' },
        { name: 'first_name', type: 'string' },
        { name: 'name', type: 'string' },
        { name: 'net', type: 'number' } */
    ];

    $('.importer-widget').on('change', function (event) {
        handleFileSelect(event, MAX_ROWS, REQUIRED_COLUMNS);
    });
});

function handleFileSelect(event, maxRows, requiredColumns) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => processFile(e, file, maxRows, requiredColumns);
    reader.onerror = () => displayErrors([`FileReader error: ${reader.error.message}`], event.target);

    if (file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || file.name.endsWith('.xlsx')) {
        reader.readAsBinaryString(file);
    } else if (file.type === 'text/csv' || file.name.endsWith('.csv')) {
        reader.readAsText(file);
    } else {
        displayErrors([`Unsupported file type: ${file.type}`], event.target);
    }
}

function processFile(event, file, maxRows, requiredColumns) {
    const data = event.target.result;

    try {
        if (file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || file.name.endsWith('.xlsx')) {
            const workbook = XLSX.read(data, { type: 'binary' });
            const firstSheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[firstSheetName];
            const jsonData = XLSX.utils.sheet_to_json(worksheet);
            processData(jsonData, maxRows, requiredColumns);
        } else if (file.type === 'text/csv' || file.name.endsWith('.csv')) {
            Papa.parse(data, {
                header: true,
                complete: (results) => processData(results.data, maxRows, requiredColumns),
                error: (error) => displayErrors([`Error parsing CSV file: ${error.message}`], event.target)
            });
        }
    } catch (error) {
        displayErrors([`Error processing file: ${error.message}`], event.target);
    }
}

function processData(data, maxRows, requiredColumns) {
    if (data.length > maxRows) {
        displayErrors([`File exceeds the maximum row limit of ${maxRows}.`], $('.importer-widget')[0]);
        return;
    }

    const transformedData = data.map(row => row);
    validateData(transformedData, requiredColumns);
    displayData(transformedData, maxRows);
}

function validateData(data, requiredColumns) {
    const errorMessages = [];
    const table = $('#preview').find('table').DataTable();

    data.forEach((row, rowIndex) => {
        let rowErrors = [];
        requiredColumns.forEach(column => {
            if (!row.hasOwnProperty(column.name)) {
                rowErrors.push(`Missing required column: ${column.name}`);
            } else if (typeof row[column.name] !== column.type) {
                rowErrors.push(`Incorrect data type for column: ${column.name}. Expected ${column.type}.`);
            }
        });

        if (rowErrors.length > 0) {
            errorMessages.push(`Row ${rowIndex + 1}: ${rowErrors.join(', ')}`);
            $(table.row(rowIndex).node()).addClass('error-row'); // Highlight error row
        }
    });

    if (errorMessages.length > 0) {
        displayErrors(errorMessages, $('.importer-widget')[0]);
    }
}

function displayErrors(errors, inputElement) {
    if (errors.length > 0) {
        toastr.error(errors.join('<br>'));
        $(inputElement).val(''); // Clear the file input
    }
    $('#errorMessages').html(errors.length > 0 ? errors.join('<br>') : 'No validation errors found.');
}

function displayData(data, maxRows) {
    let $section = $('#preview');

    if ($section.length) {
        $section.remove();
    }

    $section = $('<div>').attr('id', 'preview').addClass('card').appendTo('section');
    const $cardBody = $('<div>').addClass('card-body').appendTo($section);
    const $table = $('<table>').appendTo($cardBody).addClass('table table-striped');

    $table.append('<thead><tr></tr></thead><tbody></tbody>');

    const columns = Object.keys(data[0]).map(key => {
        $table.find('thead tr').append(`<th>${key}</th>`);
        return { title: key, data: key };
    });

    $table.DataTable({
        data: data,
        pageLength: maxRows, // Set the default number of entries to show
        columns: columns,
        searching: false,
        lengthChange: false,
        columnDefs: [
            {
                targets: '_all',
                render: $.fn.dataTable.render.text()
            }
        ]
    });
}
