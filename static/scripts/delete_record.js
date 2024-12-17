var modal = document.querySelector('.confirm-box');
var openModal = document.querySelector('.search-record');
var closeModal = document.querySelector('.modal-cancel-btn');

openModal.addEventListener('click', () => {
    modal.showModal();
});

closeModal.addEventListener('click', () => {
    modal.close();
});
