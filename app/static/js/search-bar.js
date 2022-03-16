/* Script responsible for getting the user input in the 
search bar and making the request of names in the API */

const searchBar = document.querySelector('#search-bar');
const datalist = document.querySelector('#places');

searchBar.addEventListener('keyup', () => {

    let searchValue = searchBar.value;

    let request = fetch(`/search-bar?q=${searchValue}`);
    request
        .then(res => res.json())
        .then(res => {

            datalist.innerHTML = '';

            for (let name of res) 
            {
                datalist.innerHTML += `<option value="${name}">`;
            };

        });
});