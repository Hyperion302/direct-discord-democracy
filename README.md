# Direct Discord Democracy
The direct discord democracy bot (DDD) is a discord bot designed to implement [direct democracy](https://en.wikipedia.org/wiki/Direct_democracy) within a discord server.

## Installation
### Requirements
* Python < 3.7, > 3.4
* `discord.py` library
* `pymongo` library

`pip install -r pip-requirements.txt`

You must also populate a JSON file named `config.json` with your discord bot token and your MongoDB connection string.

```json
{
    "bot_token":"<bot token>",
    "db_srv":"<srv_connection_string>"
}
```
## Usage
`python main.py`


## Contributions
Pull requests are appreciated.  Please open an issue for any bugs you find.

All pull requests should be tested beforehand.

## License
[MPL 2.0](https://choosealicense.com/licenses/mpl-2.0/)