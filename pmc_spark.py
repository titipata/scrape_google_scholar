import os
from glob import glob
from pmc_utils import *
from pyspark.sql import Row, SQLContext
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName('google_scholar')\
    .setMaster('local[8]')\
    .set('executor.memory', '8g')\
    .set('driver.memory', '8g')\
    .set('spark.driver.maxResultSize', '0')

save_path = '...' # path to save

if __name__ == '__main__':
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    pages = glob('.../*.html') # insert path to PMC html
    pages_rdd = sc.parallelize(pages)

    articles = pages_rdd.map(extract_article).\
        filter(lambda x: x is not None).\
        map(lambda x: Row(**x))
    cited_articles = pages_rdd.map(extract_cited_articles).\
        filter(lambda x: x is not None).\
        flatMap(lambda xs: [x for x in xs]).\
        map(lambda x: Row(**x))

    articles_df = articles.toDF()
    cited_articles_df = cited_articles.toDF()

    articles_df.write.parquet(os.path.join(save_path ,'pmc_articles_df.parquet'))
    cited_articles_df.write.parquet(os.path.join(save_path ,'pmc_cited_articles_df.parquet'))
