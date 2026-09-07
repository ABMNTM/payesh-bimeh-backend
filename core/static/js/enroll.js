const form = document.getElementById('enroll-form');
const confirmModalElement = document.getElementById('confirmModal');
const confirmSubmit = document.getElementById('confirmSubmit');

const confirmModal = new bootstrap.Modal(confirmModalElement);

form.addEventListener('submit', function (event) {
    event.preventDefault();
    console.log("fooooooo")
    confirmModal.show();
});

confirmSubmit.addEventListener('click', function () {
    confirmModal.hide();
    form.submit();
});
