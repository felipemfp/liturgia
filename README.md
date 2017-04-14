# liturgia

:church: :open_book: We scrape the [Liturgia Diária - CNBB](http://liturgiadiaria.cnbb.org.br/) and push a markdown everyday.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python >= 3
- pip

### Installing

(Optional) Setup a virtualenv

```
python3 -m venv env
source env/bin/activate
```

Install the requirements

```
pip install -r requirements.txt
```

And you are ready to go

```
python scraper.py
```

## Built With

* [requests](http://docs.python-requests.org/en/master/)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/felipemfp/liturgia/tags). 

## Authors

* **Felipe Pontes** - *Initial work* - [felipemfp](https://github.com/felipemfp)

See also the list of [contributors](https://github.com/felipemfp/liturgia/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* Inspired by [josephyzhou/github-trending](https://github.com/josephyzhou/github-trending)
