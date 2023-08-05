# SOM Schemas
The School of Medicine stores data in Google Cloud, with two primary endpoints:

 - storage: means object store of images and text. These are big files.
 - dataset: refers to metadata, meaning a quickly searchable "table like" thing that will then point to one or more images in storage.

Thus, when we talk about a schema, we are talking about the design of the second bullet above. The Schemas in this folder are simple tab separated files that are read in by `create_dataset` in [bigquery.py](../bigquery.py) to generate a BigQuery Datatable, with default as `som-langlotz-lab:stanford`. This document will briefly discuss each schema spec in this folder, which is akin to a table in BigQuery.

## Item Schema
An item is typically an image, with a link to the file in Google Storage. The item also links back to the entity that it is associated with, which in this case is a person, but we call it an "Entity" because, well, you never know. :)
