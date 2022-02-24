// main function
function main()
{
    instanceNameChecker();
    instancePasswordChecker();
    instanceEmailChecker();
    instanceUsernameChecker();
}


// name checker and alerter
function instanceNameChecker() 
{
    
    let name = document.querySelector(`#name`);
    let nameAlert = document.querySelector(`#name-alert`);
    
    name.addEventListener('keyup', () => {
        
        if (name.value.length > 0 && name.value.includes(' '))
        {
            nameAlert.classList.remove('text-danger');
            elementsRules['name'] = true;
        }
        else if (!nameAlert.classList.contains('text-danger'))
        {
            nameAlert.classList.add('text-danger');
            elementRules['name'] = false;
        }

        submitButtonRuler();
    });
}


// password checker and alerter
function instancePasswordChecker()
{
    let password = document.querySelector('#password');
    let confirmPassword = document.querySelector('#confirm-password');

    let passwordAlert = document.querySelector('#password-alert');
    let confirmPasswordAlert = document.querySelector('#confirm-password-alert');

    password.addEventListener('keyup', () => {

        if (password.value.length >= 8)
        {
            passwordAlert.classList.remove('text-danger');
            elementsRules['password'] = true;
        }
        else if (!passwordAlert.classList.contains('text-danger'))
        {
            passwordAlert.classList.add('text-danger');
            elementsRules['password'] = false;
        }

        submitButtonRuler();
    });


    confirmPassword.addEventListener('keyup', () => {

        if (password.value === confirmPassword.value)
        {
            confirmPasswordAlert.classList.remove('text-danger');
            elementsRules['confirm-password'] = true;
        }
        else if (!confirmPasswordAlert.classList.contains('text-danger'))
        {
            confirmPasswordAlert.classList.add('text-danger');
            elementsRules['confirm-password'] = false;
        }

        submitButtonRuler();
    });

}


// email checker and alerter
function instanceEmailChecker()
{
    let email = document.querySelector('#email');
    let emailAlert = document.querySelector('#email-alert');

    email.addEventListener('keyup', () => {

        if (email.value.includes('@') && email.value.includes('.'))
        {
            emailAlert.classList.remove('text-danger');
            elementsRules['email'] = true;
        }
        else if (!emailAlert.classList.contains('text-danger'))
        {
            emailAlert.classList.add('text-danger');
            elementsRules['email'] = false;
        }

        submitButtonRuler();
    });

}


// username checker and alerter
function instanceUsernameChecker()
{
    let username = document.querySelector('#username');
    let usernameAlert = document.querySelector('#username-alert');
    
    username.addEventListener('keyup', () => {

        if (!username.value.includes(' ') && username.value.length > 0)
        {
            usernameAlert.classList.remove('text-danger')
            elementsRules['username'] = true;
        }
        else if (!usernameAlert.classList.contains('text-danger'))
        {
            usernameAlert.classList.add('text-danger');
            elementsRules['username'] = false;
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

let allElements = ['name', 'email', 'username', 'password', 'confirm-password'];
let elementsRules = {};

allElements.forEach(element => {
    
    elementsRules[element] = false;

});


main();