from SPARQLWrapper import SPARQLWrapper, JSON

GET_MOVIE_SOURCE = "http://dbpedia.org/sparql"
GET_MOVIE_QUERY = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/resource/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name ?bandname where {
   ?person foaf:name ?name .
   ?band dbo:bandMember ?person .
   ?band dbo:genre dbp:%s .
   ?band foaf:name ?bandname .
}
"""


def get_movie(name: str):
    sparql = SPARQLWrapper(GET_MOVIE_SOURCE)
    sparql.setQuery(GET_MOVIE_QUERY % name)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print(result["name"]["value"], '\t\t', result["bandname"]["value"])

    return {
        "name": "mimi",
        "contributors": []
    }

if __name__ == '__main__':
    get_movie('Punk_rock')
