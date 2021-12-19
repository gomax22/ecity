# E-City
E-City GitHub Repository for TW6 
Inspired by Miguel Grinberg's "Microblog" project and by "TW6" course at "Università degli Studi di Napoli 'Parthenope'", we were going to create a PWA that could solve few tasks.
Using the Web browser's geolocation feature, users can save their favourite locations.
Users and Locations are recorded into a relational database, based on a simple schema that you can see in "app/models.py".
Once user allowed geolocation, he could watch his position on the map. Moving onto a particular recorded location, he could decide to see location's page, which show information about it. Users could decide to save locations in their saved locations, showed in Profile page.
User saved locations are marked on the map, a popup bound to the marker show information about the marked location.
Features implemented are: secure login, password reset, geolocation feature and PWA installability.
Actually, this project is set to be ready for simply and basic purposes. This project wants to be a start point to extend these basic features to produce something more complex.
Web Tecnologies used for this project are: HTML5, JS, Leaflet.js using OpenStreetMap tiles, CSS3 Bootstrap for front-end development, Python3 and Flask microframework for back-end development. In particular, we decided to implement a relation database using Flask SQLAlchemy.


We recommend to install requirements in your virtual environment before starting to work on this and to optimize the basic back-end logic.
To use this PWA you need to create your own database and run production server on your virtual environment.
Once you have your schema for the relational database, you can create it using these simple commands in your shell:
- flask db init
- flask db migrate
- flask db upgrade

To use email support, you need to set properly environment variables in .flaskenv file.
