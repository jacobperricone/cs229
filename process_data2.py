import pickle
import nltk
from pandas.stats.api import ols
import statsmodels.api as sm
import statsmodels
from sklearn import datasets, linear_model
from textblob import TextBlob
from nltk.tokenize import TabTokenizer
import re
from textblob.sentiments import NaiveBayesAnalyzer
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import time
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob.np_extractors import ConllExtractor
from sklearn import datasets, linear_model
#matplotlib inline
import seaborn as sns
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from pyzipcode import ZipCodeDatabase
from geopy.geocoders import Nominatim
from nltk.tag import StanfordNERTagger
from nltk.internals import find_jars_within_path
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
import os
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine
#'aggregatematchups','gamelist', 'matchups','playbyplay', 'players2', 'playerstats2',
#,'gamelist', 'matchups','playbyplay', 'players2', 'playerstats2', 'playerstatsbyteam','teamstats'
file_types = ['aggregatematchups']

project_dir = '/Users/jacobperricone/Desktop/STANFORD/fall16/cs229/project/data/'


# Create database with data base namme, log in to sql through user_name and passowrd
def create_database(DB_NAME, user_name, password):
    cnx = mysql.connector.connect(user=user_name, password=password)
    cursor = cnx.cursor()

    try:
        cnx.database = DB_NAME
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                cursor.execute(
                    "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            except mysql.connector.Error as err:
                print("Failed creating database: {}".format(err))
                exit(1)
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)



# return chunk of db
def chunks(l, n):
    for i in xrange(0, len(l), n):
         yield l.iloc[i:i+n]

# write big thing to database
def write_to_db(engine, frame, table_name, chunk_size, if_exist_param = 'replace'):
    for idx, chunk in enumerate(chunks(frame, chunk_size)):
        chunk.to_sql(con=engine, name=table_name, if_exists='append')

#fill database directory with tables
def fill_database(directory):

    engine = create_engine('mysql+pymysql://root:Redstring01!1@127.0.0.1:3306/' + directory,
                                   echo=False)

    cwd = project_dir + directory + '/'
    os.chdir(cwd)

    # if 'Reg' in directory:
    #     second_split = reg
    # else
    #     second_split =
    for table_type in file_types:

        tmp = os.listdir(cwd)
        print os.getcwd()
        files = [x for x in tmp if x.startswith(table_type)]
        for i, file_name in enumerate(files):
            print "%d: \t %s \t %s" % (i, table_type, file_name)
            try:
                print engine
                if i == 0:
                    x = pd.read_csv(file_name, sep="\t")
                    headers = x.columns
                   # write_to_db(engine, x, table_type, 5000)
                else:
                    tmp = pd.read_csv(file_name, sep="\t")
                    x= x.append(tmp[headers], ignore_index=True)

            except ValueError as err:
                pass;
        write_to_db(engine, x, table_type, 5000)

    os.chdir('..')

#denominator = tfdf.shape[1] + np.sum(np.sum(np.multiply(np.matlib.repmat(defect_posteriors[j, :].T,1, tfdf.shape[1]), tfdf), 0))
def main():
    #
    regular_directories = [x for x in os.listdir(project_dir) if 'reg' in x]
    playoff_directories = [x for x in os.listdir(project_dir) if 'Playoffs' in x]
    master_directories = [x for x in os.listdir(project_dir) if 'Master' in x]
    # run this shit
    # for dir in master_directories: create_database(dir)

    for dir in master_directories[1:]: fill_database(dir)






main()