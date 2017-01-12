# Scrape Google Scholar

This is snippet to scrape downloaded Google Scholar html page using PySpark.
**Note** To use this snippet, you have to download and store html page first.
One way to download Google Scholar pages is to use [scrapinghub.com](https://scrapinghub.com/)

To run the snippet, download [Spark](http://spark.apache.org/downloads.html),
modify parameters in `gs_spark.py` and run the following:

```bash
~/spark-2.0.0/bin/spark-submit gs_spark.py
```

# Scrape citations from PMC

`pmc_utils.py` contains a snippet to scrape citations and details of article.
We can slowly download HTML using following snippet, where `pmcs.csv` is a csv file
contains PMC string in each rows.

```bash
while read p
do
  wget --header="Accept: text/html" --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0" https://www.ncbi.nlm.nih.gov/pmc/articles/$p/citedby/ -O $p.html
done < pmcs.csv
```

where `pmcs.csv` is a text file where each row is something like `PMC1217341`.
After downloading enough html files, modify `pmc_spark.py` and run the following.

```bash
~/spark-2.0.0/bin/spark-submit pmc_spark.py
```
