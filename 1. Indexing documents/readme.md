
# Indexing Documents with Elasticsearch or Solr

This repository contains resources for indexing documents into Elasticsearch and Apache Solr. Both Elasticsearch and Solr are powerful, open-source search platforms that offer robust capabilities for handling and analyzing large datasets.

![Indexing](https://gg-cms-admin-prd.s3.eu-west-1.amazonaws.com/iocms/sharding_3cb0e30cbe.png)
Image source: https://www.giffgaff.io/tech/elasticsearch-index-management

## Repository Contents

- [Elastic Search](../1.%20Indexing%20documents/Elastic%20Search/): A directory containing a Python notebook (`elasticsearch_indexer.ipynb`) that demonstrates how to index documents into Elasticsearch.
- [Solr](../1.%20Indexing%20documents/Solr/): A directory containing a Python script (`solr_indexing.py`) that shows how to index documents into Solr.

You can also index your documents in Watson Discovery by following the [documentation here](https://cloud.ibm.com/docs/discovery-data?topic=discovery-data-upload-data).

## Getting Started

1. Clone this repository.
2. Navigate to the respective directory for Elasticsearch or Solr.
3. Install the required dependencies (see the Dependencies section below).
4. Update the connection details in the notebook or script as necessary.
5. Run the notebook or script to index documents into the respective search platform.

## Usage

The `elasticsearch_indexer.ipynb` notebook and the `solr_indexing.py` script both provide step-by-step guides on how to index documents into Elasticsearch and Solr respectively. This includes initializing a connection to an instance of the search platform, creating an index or collection, and adding documents to the index or collection.

## Dependencies

These resources require Python 3.6 or later. Additionally, the Elasticsearch notebook requires the `elasticsearch` Python library, and the Solr script requires the `pysolr` Python library.

You can install these libraries using pip:

```
pip install elasticsearch pysolr
```

Also, you need to have access to Elasticsearch and Solr instances to run the notebook and script.
