
var adminRegisterCheckbox = document.querySelector('.admin-register');
var adminTokenField = document.querySelector('.admin-token');

if (adminRegisterCheckbox) {
    adminRegisterCheckbox.addEventListener('change', () => {
        if (adminRegisterCheckbox.checked) {
            adminTokenField.style.display = 'block';
        } else {
            adminTokenField.style.display = 'none';
        }
    });
}

// Handle "Show Password" checkbox
var showPasswordCheckbox = document.querySelector('.register-show-password');
var passwordBox = document.querySelector('.register-password');

if (showPasswordCheckbox) {
    showPasswordCheckbox.addEventListener('click', () => {
        passwordBox.type = passwordBox.type === 'password' ? 'text' : 'password';
    });
}

