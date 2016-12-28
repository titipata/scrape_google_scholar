import os
from glob import glob
from gs_utils import *
from pyspark.sql import Row, SQLContext
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName('google_scholar')\
    .setMaster('local[8]')\
    .set('executor.memory', '8g')\
    .set('driver.memory', '8g')\
    .set('spark.driver.maxResultSize', '0')

save_path = '.../Downloads/sample-set'

if __name__ == '__main__':
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    pages = glob('.../Downloads/sample-set/*.htm') # path to sample set
    pages_rdd = sc.parallelize(pages)
    bodies = pages_rdd.map(get_body)

    authors = bodies.map(get_author_detail).\
        filter(lambda x: x is not None).\
        map(lambda x: Row(**x))
    authors_df = authors.toDF().drop_duplicates()
    authors_df.write.parquet(os.path.join(save_path ,'gs_authors_df.parquet'))

    publications = bodies.map(get_publications).\
        filter(lambda x: x is not None).\
        flatMap(lambda xs: [x for x in xs]).\
        map(lambda x: Row(**x))
    publications_df = publications.toDF().drop_duplicates()
    publications_df.write.parquet(os.path.join(save_path ,'gs_publications_df.parquet'))

    citations = bodies.map(get_citations_trend).\
        filter(lambda x: x is not None).\
        flatMap(lambda xs: [x for x in xs]).\
        map(lambda x: Row(**x))
    citations_df = citations.toDF().drop_duplicates()
    citations_df.write.parquet(os.path.join(save_path ,'gs_citations_df.parquet'))
