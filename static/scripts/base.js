var openLogoff = document.querySelector('.logoff-button')
var modalLogoff = document.querySelector('.logoff-box');             
var closeLogoff = document.querySelector('.cancel-logoff');

openLogoff.addEventListener('click', () => {                           
    modalLogoff.showModal();
});

closeLogoff.addEventListener('click', () => {
    modalLogoff.close();
});