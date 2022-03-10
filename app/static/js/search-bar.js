searchBar = document.querySelector('#search-bar');
datalist = document.querySelector('#places');


searchBar.addEventListener('keyup', () => {

    value = searchBar.value;

    request = fetch(`/search-bar?q=${value}`);
    request
        .then(res => res.json())
        .then(res => {

            datalist.innerHTML = '';

            for (name of res) 
            {
                datalist.innerHTML += `<option value="${name}">`;
            };

        });
});