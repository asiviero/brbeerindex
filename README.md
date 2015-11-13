# BR Beer Index :beer:

This is a project intended to develop a web crawler for online beer stores, grouping the results and making it easy to compare them after a record linkage algorithm.

Brazilian stores are the current focus, although that could change some time in the near future. It is mostly a learning project, however the best possible results are the main goal.

# Installing

A Vagrantfile is provided, and all the dependencies are listed in the [provisioning script](vagrant_provision.sh). You can either run `$ vagrant up` or `$ sh vagrant_provision.sh`.

# How does it work?

Currently, I'm using [scrapy](http://scrapy.org) for scraping and [dedupe](https://github.com/datamade/dedupe) for the record linkage.

Every store will have a `base url`, which is the main product listing page. It should also define CSS selectors for `next_link`, which tells the scraper where to find the "next page" link and the `product_link`, so the scraper knows which links to follow on those pages.

After that, it scrapes the product pages for name, type and price via XPATH selectors. I thought those to be more flexible in relation to getting data attributes in html documents. Stores must also have those defined, look at [beerspider.py](beerindex/spiders/beerspider.py) for futher info on setting it up.

Data generated should be exported (currently to a CSV file) so it can be used by the record linkage algorithm. The way of storing this data is likely to change.

# Running the scraper

The only particularity of this script is that data should be output to somewhere other than `STDOUT`. As such, the command needed to run the scraper properly is:

    $ scrapy crawl beerspider -o results/scraping_results.csv -t csv

## Notice on the scraper

Since stores usually have anti-scrapping measures, Polipo and Tor are used to route the requests through them, as described [here](http://pkmishra.github.io/blog/2013/03/18/how-to-run-scrapy-with-TOR-and-multiple-browser-agents-part-1-mac/). This isn't perfect yet since Polipo [is detectable by web sites](www.pps.univ-paris-diderot.fr/~jch/software/polipo/tor.html), but it should help.

# Record Linkage

Currently the fuzziest part to me, I'm trusting dedupe to do it and a lot of manual input is required. I intend to progressively automate this process as I gather more knowledge. The test script is largely derived from the [csv_example](https://github.com/datamade/dedupe-examples/blob/master/csv_example/csv_example.py) from dedupe.

It's located at [results/csv_record_linkage.py](results/csv_record_linkage.py) and it's run as follows:

    $ python csv_record_linkage -v

`-v` is not mandatory as it indicates verbosity. I have found it to make it easier to provide manual input if verbosity is on.

The script will ask for clarification several times when it's too unsure to group or not two elements in the set. This is expected.

# Ideas

- [ ] Historic data
- [ ] Improve record linkage to increase automation
- [ ] Automated testing (although I'm still not sure of what to test right now)
- [ ] Create a `gh-pages` to display the results and maybe provide a search interface

# CONTRIBUTING

Please don't hesitate to open issues, send pull requests or contact me at `altsiviero at gmail dot com` :smile:

# LICENSE

Code is licensed under the [LGPL](LICENSE)
