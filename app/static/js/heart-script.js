/* Script responsible for doing the post request when the
    heart (like button) is pressed, changing the heart (from solid
    to regular) and updating the likes count in the front-end */

let heart = document.querySelector('#heart');
let likes = document.querySelector('#likes');

heart.addEventListener('click', () => {

    let path = window.location.href;
    path = path.split('/')
    let locationName = path[path.length - 1]

    let xml = new XMLHttpRequest();
    xml.open('POST', `/manage-likes/${locationName}`);
    xml.send()
    
    let innerHTML = heart.innerHTML;
    if (innerHTML.includes('fa-regular'))
    {
        heart.innerHTML = '<i class="fa-solid fa-heart"></i>';
    }
    else
    {
        heart.innerHTML = '<i class="fa-regular fa-heart"></i>';
    }

    
    setTimeout(() => {
        let likes_req = fetch(`/get-likes/${locationName}`);
        likes_req
            .then(resp => resp.json())
            .then(resp => {
                likes.textContent = resp['likes'];
            });
    }, 1);
    
});