/* Script responsible for alert the in the update user page 
if the form is not fullfilled correctly by changing the color of 
the hint text */

// main function
function main()
{
    instanceNameChecker();
    instanceOldPasswordChecker();
    instancePasswordChecker();
    instanceEmailChecker();
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
        }
        else if (!nameAlert.classList.contains('text-danger'))
        {
            nameAlert.classList.add('text-danger');
        }

        
    });
}


function instanceOldPasswordChecker()
{
    let password = document.querySelector('#old-password');
    let passwordAlert = document.querySelector('#old-password-alert');

    password.addEventListener('keyup', () => {

        if (password.value.length >= 8)
        {
            passwordAlert.classList.remove('text-danger');
        }
        else if (!passwordAlert.classList.contains('text-danger'))
        {
            passwordAlert.classList.add('text-danger');
        }

        
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
        }
        else if (!passwordAlert.classList.contains('text-danger'))
        {
            passwordAlert.classList.add('text-danger');
        }

        
    });


    confirmPassword.addEventListener('keyup', () => {

        if (password.value === confirmPassword.value)
        {
            confirmPasswordAlert.classList.remove('text-danger');
        }
        else if (!confirmPasswordAlert.classList.contains('text-danger'))
        {
            confirmPasswordAlert.classList.add('text-danger');
        }

        
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
        }
        else if (!emailAlert.classList.contains('text-danger'))
        {
            emailAlert.classList.add('text-danger');
        }

        
    });

}



main();