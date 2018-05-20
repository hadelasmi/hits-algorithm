# Overview
This project is an implementation of the HITS (Hyperlink-Induced Topic Search) aka the Hubs and Authorities algorithm on a network of Twitter users to find good hubs and authorities. In this situation, a good hub is a person who follows good authorities and a good authority is a person who is followed by good hubs. In a real-life scenario, a good authority could be a popular music artist and a good hub could be a music lover who follows many accomplished artists.

# Implementation
The network is represented as a directed graph where each node represents a Twitter user. An edge from user A to user B implies that A is a follower of B and B is a friend of A.  

The project consists of two parts
* Fetching the dataset
* Executing the algorithm on the dataset

## Fetching the dataset
The dataset is fetched using the Twitter API with the help of Tweepy. The relevant Python code is present in `src/dataset_fetcher.py`. Given a user to start with (represented by the variable `seed_user` in the code), the algorithm proceeds in a breadth-first search fashion to generate the directed graph. Three limits are used during the process:
* Limit on the number of friends obtained for a user (represented by the variable `friends_limit`)
* Limit on the number of followers obtained for a user (represented by the variable `followers_limit`)
* Limit on the total number of users queried (represented by the variable `limit`)

## HITS Algorithm
The algorithm implemented here is similar to the one given in [Mining of Massive Datasets](http://www.mmds.org/)

## File Structure
|-- data: Contains the structures saved after obtaining the dataset
|   |-- adj_list: Adjaceny list representing the fetched dataset
|   |-- dense_link_matrix: Link matrix using non sparse representation
|   |-- sparse_link_matrix: Link matrix using sparse representation
|   |-- map: Map from user id to matrix index
|   |-- users: Users information
|
|-- src: Contains Python source files
|   |-- hits.py: Implements the HITS algorithm
|   |-- dataset_fetcher.py: Fetches the dataset using Twitter API through Tweepy 
|
|-- README.md
|-- requirements.txt

## Usage
* Clone/download the repository
* Obtain the dataset using:
  ```
    $ python3 dataset_fetcher.py
  ```
  You will be prompted to enter the seed username, Twitter API key and secret.
  Once run, the dataset will be stored in the `data` directory
* The HITS algorithm can be run on this dataset using:
  ```
    $ python3 hits.py
  ```

# Other Contributors
* Anirudh Srinivasan
* Nikhil Iyer