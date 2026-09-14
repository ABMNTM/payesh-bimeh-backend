document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('select-all-user').addEventListener('click', function () {
        document.querySelectorAll('.field-checkbox-user input[type=checkbox]').forEach(cb => cb.checked = true);
    });
    document.getElementById('select-none-user').addEventListener('click', function () {
        document.querySelectorAll('.field-checkbox-user input[type=checkbox]').forEach(cb => cb.checked = false);
    });
    document.getElementById('select-all-person').addEventListener('click', function () {
        document.querySelectorAll('.field-checkbox-person input[type=checkbox]').forEach(cb => cb.checked = true);
    });
    document.getElementById('select-none-person').addEventListener('click', function () {
        document.querySelectorAll('.field-checkbox-person input[type=checkbox]').forEach(cb => cb.checked = false);
    });
});