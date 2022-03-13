function main()
{
    instanceUsernameChecker();
    instancePasswordChecker();
}


// username checker and alerter
function instanceUsernameChecker()
{
    let username = document.querySelector('#username');
    let usernameAlert = document.querySelector('#username-alert');
    
    username.addEventListener('keyup', () => {

        if (!username.value.includes(' ') && username.value.length > 0)
        {
            usernameAlert.classList.add('invisible')

        }
        else if (usernameAlert.classList.contains('invisible'))
        {
            usernameAlert.classList.remove('invisible');
        }

    });

}


// password checker and alerter
function instancePasswordChecker()
{
    let password = document.querySelector('#password');
    let passwordAlert = document.querySelector('#password-alert');

    password.addEventListener('keyup', () => {

        if (password.value.length >= 8)
        {
            passwordAlert.classList.add('invisible');
        }
        else if (passwordAlert.classList.contains('invisible'))
        {
            passwordAlert.classList.remove('invisible');
        }

    });
}

main();