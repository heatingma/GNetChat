// SignUp & SignIn 
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});



// register & login box
let login=document.getElementById('login');
let register=document.getElementById('register');
let form_box=document.getElementsByClassName('form-box')[0];
let register_box=document.getElementsByClassName('register-box')[0];
let login_box=document.getElementsByClassName('login-box')[0];


// send code
const send_code = document.querySelector('.code')
const test_last_code = document.querySelector('[name=last_email_code]')
let send_flag = false

send_code.addEventListener('click', function (event) {
    if (!verifyMail()){
        email_code_msg.innerHTML = '邮箱不合法'
        return;
    }

    event.preventDefault(); // 阻止表单的默认提交行为
    var inputField = document.getElementsByName("email")[0];
    var inputValue = inputField.value;
    var csrfToken = $('[name=csrfmiddlewaretoken]').val()
    $.ajax({
        type: 'POST',
        url: '/sendemail/',
        data: {
            'to_email': inputValue
        },
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (response) {
            if (response.success) {
                // 请求成功后的处理逻辑
                console.log('Email code sent successfully');
                $("#test_code").val(response.sms_code)
            } else {
                // 处理请求失败的情况
                console.error('Failed to send email code:', response.errors);
            }
        },
        error: function (xhr, status, error) {
            // 处理请求错误的情况
            console.error('Ajax request failed:', error);
        }
    });

    if (send_flag == false) {
        send_flag = true
        // send_code.disabled = true
        let left_seconds = 60
        send_code.innerHTML = `${left_seconds} `
        let timerId = setInterval(function () {
            left_seconds--
            send_code.innerHTML = `${left_seconds}`
            if (left_seconds === 0) {
                send_flag = false
                send_code.disabled = false
                clearInterval(timerId)
                send_code.innerHTML = "Send"
            }
        }, 1000)
    }
})



// LOGIN-Name
const login_email = document.querySelector('[name=login_email]')
login_email.addEventListener('change', CheckLoginEmail)
function CheckLoginEmail() {
    const msg = login_email.nextElementSibling
    msg.innerHTML = ''
    return true
}



// LOGIN-PSD
const login_psd = document.querySelector('[name=login_password]')
login_psd.addEventListener('change', CheckLoginPsd)
function CheckLoginPsd() {
    const msg = login_psd.nextElementSibling
    msg.innerHTML = ''
    return true
}



// verifyName
const username = document.querySelector('[name=username]')
username.addEventListener('change', verifyName)
function verifyName() {
    const reg = /^[a-zA-Z0-9-_]{6,20}$/
    const msg = username.nextElementSibling
    if (!reg.test(username.value)) {
        msg.innerHTML = '输入不合法, 请输入6~20位'
        return false
    }
    msg.innerHTML = ''
    return true
}



// verifyMail
const email = document.querySelector('[name=email]')
email.addEventListener('change', verifyMail)
function verifyMail() {
    const reg = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    const msg = email.nextElementSibling
    if (!reg.test(email.value)) {
        msg.innerHTML = '邮箱不合法, 请输入正确的邮箱'
        return false
    }
    msg.innerHTML = ''
    return true
}




// verifyPassword
const psd = document.querySelector('[name=password1]')
psd.addEventListener('change', verifyPassword)
function verifyPassword() {
    const reg = /^[a-zA-Z0-9-_]{8,20}$/
    const msg = psd.nextElementSibling
    if (!reg.test(psd.value)) {
        msg.innerHTML = '输入不合法, 请输入8~20位'
        return false
    }
    msg.innerHTML = ''
    return true
}



// CheckPassword
const check_psd = document.querySelector('[name=password2]')
check_psd.addEventListener('change', CheckPassword)
function CheckPassword() {
    const msg = check_psd.nextElementSibling
    if (psd.value === check_psd.value) {
        msg.innerHTML = ''
        return true
    }
    msg.innerHTML = '两次密码输入不一致'
    return false
}



// Submit Register
const code = document.querySelector('[name=email_code]')
const last_code = document.querySelector('[name=last_email_code]')
const email_code_msg = document.querySelector('[name=email_code-msg]')
const submit_register = document.querySelector('[name=submit-register]')
let register_flag = true

submit_register.addEventListener('click', function (e) {
    register_flag = true
    if (code.value != last_code.value || !last_code.value) {
        email_code_msg.innerHTML = '验证码错误'
        register_flag = false
    }
    if (!verifyName()) register_flag = false
    if (!verifyMail()) register_flag = false
    if (!verifyPassword()) register_flag = false
    if (!CheckPassword()) register_flag = false
    if (register_flag == false)
        e.preventDefault()
})


// Submit Login
const submit_login = document.querySelector('[name=submit-login]')
let login_flag = true
submit_login.addEventListener('click', function (e) {
    login_flag = true
    if (!CheckLoginEmail()) login_flag = false
    if (!CheckLoginPsd()) login_flag = false
    if (login_flag == false)
        e.preventDefault()
})


// close the error box
var closeButton = document.getElementById('close');
closeButton.addEventListener('click', function () {
    var errorBox = this.closest('.error-box');
    if (errorBox) {
        errorBox.style.display = 'none';
    }
});
