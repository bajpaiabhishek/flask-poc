function passwordMatch() {
    const password = document.querySelector('#psw').value;
    const repeatPassword = document.querySelector('#psw-repeat').value;
    let pwdRepeat = document.querySelector('#psw-repeat');
    let pwd = document.querySelector('#psw');
    let button = document.querySelector('body > form > div:nth-child(1) > button');
    document.querySelector('body > form > div:nth-child(1) > p.error').innerHTML = 'Both password should match.';
    pwdRepeat.style['border'] = '2px solid red';
    if (password == repeatPassword) {
        document.querySelector('body > form > div:nth-child(1) > p.error').innerHTML = '';
        pwd.style['border'] = '2px solid green';
        pwdRepeat.style['border'] = '2px solid green';
        button.disabled = false;
    }
}

function isValidEmail() {
    const email = document.querySelector('#email').value;
    const regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    document.querySelector('#email').style['border'] = '2px solid red';
    document.querySelector('body > form > div:nth-child(1) > p.error').innerHTML = 'Please enter valid email. Example : abc@xyz.com';
    if (regex.test(email)) {
        document.querySelector('#email').style['border'] = '2px solid green';
        document.querySelector('body > form > div:nth-child(1) > p.error').innerHTML = '';
    }
}


document.querySelector('#psw-repeat').addEventListener("keyup",
    passwordMatch
)

document.querySelector('#email').addEventListener("keyup",
    isValidEmail
)