# Turitiba Documentation

## JavaScript:

> ### carousel-index.js
>
> * Sets the glider in the index page at the glider element
>
> ### carousel-location.js
>
> * Sets the glider in the location template at the glider element
>
> ### heart-script.js
>
> * Script responsible for doing the post request when the  (like button) is pressed, changing the heart (from solid regular) and updating the likes count in the front-end
>
> ### login.js
>
> * Script responsible for alert the in the login page if the form is not fullfilled correctly by removing the hint text
>
> ### register.js
>
> * Script responsible for alert the in the register page if the form is not fullfilled correctly by changing the color of the hint text
>
> ### search-bar.js
>
> * Script responsible for getting the user input in the search bar and making the request of names in the API
>
> ### user.js
>
> * Script responsible for alert the in the update user page if the form is not fullfilled correctly by changing the color of the hint text

## Python Helper Scripts:

> ### add_locations_to_db.py
>
> * Script responsible for adding the data of all locations in the database. Firstly, it takes the list of the wikipedia name of all locations, then requests the data from the Wikipedia API, inserts the info into the database, writes the addresses of all the images into a text file, images that will be downloaded in the future
>
> ### add_paths_to_db.py
>
> * Script responsible for adding the images path into the DB. Firstly, defines a function that returns the formatted string of the image path. Then, defines a list of dicts with the id, the name and the amount of images \- 1 (implementation detail, the main image of a locations has to have the 999 index, the rest will be counted from 0. So, because there is always a 999 index, amount - 1).  Then, iterates over the list and adds all the images of a determined location
>
> ### add_route_path.py
>
> * Simple script responsible for getting the names of all locations,then formatting into a route like format and adding it into the DB

## Python:

> ### main.py
>
> > #### update_likes_in_all_locations():
> >
> > * Function that updates the likes count in all locations. Firstly, gets the ids of all locations, then iterates over ids and triggers other function that updates the likes count in a determinate location
> >
> > 