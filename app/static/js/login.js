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
            elementsRules['username'] = true;
        }
        else if (usernameAlert.classList.contains('invisible'))
        {
            usernameAlert.classList.remove('invisible');
            elementsRules['username'] = false;
        }

        submitButtonRuler();
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
            elementsRules['password'] = true;
        }
        else if (passwordAlert.classList.contains('invisible'))
        {
            passwordAlert.classList.remove('invisible');
            elementsRules['password'] = false;
        }

        submitButtonRuler();
    });
}


// submit button ruler
function submitButtonRuler()
{
    let sum = 0;

    allElements.forEach(element => {

        sum += elementsRules[element] ? 1 : 0;

    });

    let submitButton = document.querySelector('#submit');

    submitButton.disabled = !(sum === allElements.length);

}

let allElements = ['username', 'password'];
let elementsRules = {};

allElements.forEach(element => {
    
    elementsRules[element] = false;

});


main();