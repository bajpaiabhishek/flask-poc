window.addEventListener('load',
    makeReadOnly)

function makeReadOnly() {
    let value = document.querySelector('#fullname').value;
    if (!(value == '')) {
        document.querySelector('#fullname').readOnly = true;
    }
}

function isNumberValid() {
    const value = document.querySelector('#phone').value;
    const inputField = document.querySelector('#phone');
    let button = document.querySelector('body > div > form > button');
    document.querySelector('body > div > form > p.error').innerHTML = "Enter Valid Mobile Number(10 digits).";
    button.disabled = true;
    inputField.style['border'] = '2px solid red';
    if (value.length == 10) {
        inputField.style['border'] = '2px solid green';
        button.disabled = false;
        document.querySelector('body > div > form > p.error').innerHTML = "";
    }
}

function fileValidation() {
    let fileInput = document.getElementById('photo');

    let filePath = fileInput.value;

    let allowedExtensions = /(\.jpg)$/i;

    if (!allowedExtensions.exec(filePath)) {
        alert('Invalid file type');
        fileInput.value = '';
        return false;
    }
}

document.querySelector('#phone').addEventListener("keyup",
    isNumberValid
)

document.querySelector('#photo').addEventListener("change",
    fileValidation
)