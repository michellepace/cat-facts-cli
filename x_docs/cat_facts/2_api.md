# Cat Facts API Documentation

Base URL for all endpoints `https://cat-fact.herokuapp.com`

_The response time will likely be a few seconds long on the first request, because this app is running on a free Heroku dyno. Subsequent requests will behave as normal._

## Endpoints

[`/facts`](https://alexwohlbruck.github.io/cat-facts/docs/endpoints/facts.html) Retrieve and query facts

[`/users`](https://alexwohlbruck.github.io/cat-facts/docs/endpoints/users.html)\* Get user data

<sub>* Requires authentication. As of now, this can only be achieved by logging in manually on the website.</sub>

## Models

[`Fact`](https://alexwohlbruck.github.io/cat-facts/docs/models/fact.html) An animal fact

[`User`](https://alexwohlbruck.github.io/cat-facts/docs/models/user.html) A user of the Cat Facts site
