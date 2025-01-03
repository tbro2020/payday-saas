// Define custom autocomplete keywords
/* var keywords = [
    { name: 'variable1', value: 'variable_1', meta: 'custom variable' },
    { name: 'variable2', value: 'variable_2', meta: 'custom variable' },
]; */


// Create a custom completer
var completers = {
    getCompletions: function(editor, session, pos, prefix, callback) {
        let keywords = JSON.parse(document.getElementById("keywords").textContent);
        callback(null, keywords.map(function(keyword) {
            return {
                caption: keyword.name,
                value: keyword.value,
                meta: keyword.meta
            };
        }));
    }
};

(function() {
    function getDocHeight() {
        var D = document;
        return Math.max(
            Math.max(D.body.scrollHeight, D.documentElement.scrollHeight),
            Math.max(D.body.offsetHeight, D.documentElement.offsetHeight),
            Math.max(D.body.clientHeight, D.documentElement.clientHeight)
        );
    }

    function getDocWidth() {
        var D = document;
        return Math.max(
            Math.max(D.body.scrollWidth, D.documentElement.scrollWidth),
            Math.max(D.body.offsetWidth, D.documentElement.offsetWidth),
            Math.max(D.body.clientWidth, D.documentElement.clientWidth)
        );
    }

    function next(elem) {
        do {
            elem = elem.nextSibling;
        } while (elem && elem.nodeType != 1);
        return elem;
    }

    function prev(elem) {
        do {
            elem = elem.previousSibling;
        } while (elem && elem.nodeType != 1);
        return elem;
    }

    function drawModal() {
        // Create the modal div
        var modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'modal-editor';
        modal.tabIndex = -1;
        modal.setAttribute('aria-labelledby', 'modal-editor-label');
        modal.setAttribute('aria-hidden', 'true');
    
        // Create the modal-dialog div
        var modalDialog = document.createElement('div');
        modalDialog.className = 'modal-dialog modal-lg';
    
        // Create the modal-content div
        var modalContent = document.createElement('div');
        modalContent.className = 'modal-content';
    
        // Create the modal-body div
        var modalBody = document.createElement('div');
        modalBody.className = 'modal-body modal-editor';
        modalBody.id = 'modal-editor-body';
    
        // Append modal-body to modal-content
        modalContent.appendChild(modalBody);
    
        // Append modal-content to modal-dialog
        modalDialog.appendChild(modalContent);
    
        // Append modal-dialog to modal
        modal.appendChild(modalDialog);
    
        // Append modal to body
        document.body.appendChild(modal);
    }
    
    function destroyModal() {
        var modal = document.getElementById('modal-editor');
        if (modal == undefined) return;
        modal.remove();
    }
    
    function showModal(widget, main_block, editor) {
        // Create a new editor container inside the modal
        var newEditorDiv = document.createElement('div');
        newEditorDiv.style.height = '100%';

        drawModal();
        $('#modal-editor-body').append(newEditorDiv);
    
        // Initialize the new editor with the same settings and data as the original editor
        var newEditor = ace.edit(newEditorDiv);
        newEditor.getSession().setValue(editor.getSession().getValue());
    
        // Apply the same options as the original editor
        newEditor.setOptions({
            mode: editor.getSession().getMode().$id,
            theme: editor.getTheme(),
            useWrapMode: editor.getSession().getUseWrapMode(),
            minLines: editor.getOption("minLines"),
            maxLines: editor.getOption("maxLines"),
            showPrintMargin: editor.getShowPrintMargin(),
            showInvisibles: editor.getShowInvisibles(),
            tabSize: editor.getOption("tabSize"),
            fontSize: editor.getOption("fontSize"),
            readOnly: editor.getOption("readOnly"),
            useSoftTabs: editor.getSession().getUseSoftTabs(),
            showGutter: editor.getOption("showGutter"),
            behavioursEnabled: editor.getOption("behavioursEnabled"),
            useWorker: editor.getOption("useWorker"),
            enableBasicAutocompletion: true,
            enableSnippets: true,
            enableLiveAutocompletion: false
        });
        newEditor.completers = [completers];
    
        // Show the modal and fit the new editor to it
        $('#modal-editor').modal('show').on('shown.bs.modal', () => newEditor.resize());
    
        // Move the edited data back to the original editor and clean up when the modal is closed
        $('#modal-editor').on('hide.bs.modal', function () {
            var content = newEditor.getSession().getValue();
            editor.getSession().setValue(content);
    
            // Destroy the modal editor
            newEditor.destroy();
    
            // Remove the new editor container from the DOM
            newEditorDiv.remove();

            // Remove the modal
            destroyModal();
        });
    }
    

    function apply_widget(widget) {
        var div = widget.firstChild,
            textarea = next(widget),
            mode = widget.getAttribute('data-mode'),
            theme = widget.getAttribute('data-theme'),
            wordwrap = widget.getAttribute('data-wordwrap'),
            minlines = widget.getAttribute('data-minlines'),
            maxlines = widget.getAttribute('data-maxlines'),
            showprintmargin = widget.getAttribute('data-showprintmargin'),
            showinvisibles = widget.getAttribute('data-showinvisibles'),
            tabsize = widget.getAttribute('data-tabsize'),
            fontsize = widget.getAttribute('data-fontsize'),
            usesofttabs = widget.getAttribute('data-usesofttabs'),
            readonly = widget.getAttribute('data-readonly'),
            showgutter = widget.getAttribute('data-showgutter'),
            behaviours = widget.getAttribute('data-behaviours'),
            useworker = widget.getAttribute('data-useworker'),
            toolbar = prev(widget);

        // Initialize editor and attach to widget element (for use in formset:removed)
        var editor = widget.editor = ace.edit(div);

        var main_block = div.parentNode.parentNode;
        if (toolbar != null) {
            // Toolbar maximize/minimize button
            var min_max = toolbar.getElementsByClassName('django-ace-max_min');
            min_max[0].onclick = function() {
                showModal(widget, main_block, editor);
                return false;
            };
        }

        // Load initial data
        editor.getSession().setValue(textarea.value);

        // The editor is initially absolute positioned
        textarea.style.display = "none";

        // Options
        if (mode) {
            var Mode = ace.require("ace/mode/" + mode).Mode;
            editor.getSession().setMode(new Mode());
        }
        if (theme) {
            editor.setTheme("ace/theme/" + theme);
        }
        if (wordwrap == "true") {
            editor.getSession().setUseWrapMode(true);
        }
        if (!!minlines) {
            editor.setOption("minLines", minlines);
        }
        if (!!maxlines) {
            editor.setOption("maxLines", maxlines=="-1" ? Infinity : maxlines);
        }
        if (showprintmargin == "false") {
            editor.setShowPrintMargin(false);
        }
        if (showinvisibles == "true") {
            editor.setShowInvisibles(true);
        }
        if (!!tabsize) {
            editor.setOption("tabSize", tabsize);
        }
        if (!!fontsize) {
            editor.setOption("fontSize", fontsize);
        }
        if (readonly == "true") {
            editor.setOption("readOnly", readonly);
        }
        if (usesofttabs == "false") {
            editor.getSession().setUseSoftTabs(false);
        }
        if (showgutter == "false") {
            editor.setOption("showGutter", false);
        }
        if (behaviours == "false") {
            editor.setOption("behavioursEnabled", false);
        }
        if (useworker == "false") {
            editor.setOption("useWorker", false);
        }

        // Enable language tools
        ace.require('ace/ext/language_tools');
        editor.setOptions({
            enableBasicAutocompletion: true,
            enableSnippets: true,
            enableLiveAutocompletion: false
        });
        editor.completers = [completers];

        // Write data back to original textarea
        editor.getSession().on('change', function() {
            textarea.value = editor.getSession().getValue();
        });

        editor.commands.addCommand({
            name: 'Show modal',
            bindKey: {win: 'Ctrl-F11',  mac: 'Command-F11'},
            exec: function(editor) {
                showModal(widget, main_block, editor);
                // minimizeMaximize(widget, main_block, editor);
            },
            readOnly: true // false if this command should not apply in readOnly mode
        });

        editor.commands.addCommand({
            name: 'Modal',
            bindKey: {win: 'Ctrl-M',  mac: 'Command-M'},
            exec: function(editor) {
                showModal(widget, main_block, editor);
            },
            readOnly: true // false if this command should not apply in readOnly mode
        });
    }

    /**
     * Determine if the given element is within the element that holds the template
     * for dynamically added forms for an InlineModelAdmin.
     *
     * @param {*} widget - The element to check.
     */
    function is_empty_form(widget) {
        var empty_forms = document.querySelectorAll('.empty-form, .grp-empty-form');
        for (empty_form of empty_forms) {
            if (empty_form.contains(widget)) {
                return true
            }
        }
        return false
    }

    function init() {
        var widgets = document.getElementsByClassName('django-ace-widget');

        for (widget of widgets) {
            // Skip the widget in the admin inline empty-form
            if (is_empty_form(widget)) {
                continue;
            }

            // Skip already loaded widgets
            if (!widget.classList.contains("loading")) {
                continue;
            }

            widget.className = "django-ace-widget"; // Remove `loading` class

            apply_widget(widget);
        }
    }

    // Django's jQuery instance is available, we are probably in the admin
    if (typeof django == 'object' && typeof django.jQuery == 'function') {
        django.jQuery(document).on('formset:added', function (event, $row, formsetName) {
            // Row added to InlineModelAdmin, initialize new widgets
            init();
        });
        django.jQuery(document).on('formset:removed', function (event, $row, formsetName) {
            // Row removed from InlineModelAdmin, destroy attached editor
            $row.find('div.django-ace-widget')[0].editor.destroy()
        });
    }

    if (window.addEventListener) { // W3C
        window.addEventListener('load', init);
    } else if (window.attachEvent) { // Microsoft
        window.attachEvent('onload', init);
    }
})();
