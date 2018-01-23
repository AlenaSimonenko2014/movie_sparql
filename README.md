## Deployment

1. Install Apache Jena + Fuseki Server

Download apache-jena-fuseki-x.y.z.zip from https://jena.apache.org/download/,
unzip it and move to that directory. Command

```
...\apache-jena-fuseki-3.6.0>fuseki-server
```
will run the server.

Open http://127.0.0.1:3030/manage.html and add new dataset "first_dataset".

2. Now run Django server
```bash
clone https://github.com/AlenaSimonenko2014/movie_sparql
```
cd movie_sparql
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

```
