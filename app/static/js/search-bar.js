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