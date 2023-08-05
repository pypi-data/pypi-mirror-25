'''
google/bigquery.py: functions for bigquery

Copyright (c) 2017 Vanessa Sochat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from som.logger import bot
from som.utils import read_json
from glob import glob
import sys
import os


def get_client():
    ''' get a simple client for bigquery'''
    from google.cloud import bigquery
    return bigquery.Client()


def load_data_from_file(dataset_name, table_name, source_file_name):
    bigquery_client = bigquery.Client()
    dataset = bigquery_client.dataset(dataset_name)
    table = dataset.table(table_name)

    # Reload the table to get the schema.
    table.reload()

    with open(source_file_name, 'rb') as source_file:
        # This example uses CSV, but you can use other formats.
        # See https://cloud.google.com/bigquery/loading-data
        job = table.upload_from_file(
            source_file, source_format='text/csv')

    job.result()  # Wait for job to complete

    print('Loaded {} rows into {}:{}.'.format(
        job.output_rows, dataset_name, table_name))

client = get_client()

# The name for the new dataset
dataset_name = 'IRB41449'

# Prepares the new dataset
dataset = client.dataset(dataset_name)

# Creates the new dataset
if dataset.exists() is False:
    dataset.create()

# Dummy metadata and images folder
images = glob('/tmp/Collection/IRB41449/Entity/GL664c1b/*.json')

for image in images:
    metadata = read_json(image)

#TODO:

# 1. create schema for dataset, test upload
# https://cloud.google.com/bigquery/docs/tables
