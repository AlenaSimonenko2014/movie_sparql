from SPARQLWrapper import SPARQLWrapper, JSON

GET_MOVIE_SOURCE = "http://dbpedia.org/sparql"
GET_MOVIE_QUERY = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { <http://dbpedia.org/resource/%s> rdfs:label ?label }
"""


def get_movie(name: str):
    sparql = SPARQLWrapper(GET_MOVIE_SOURCE)
    sparql.setQuery(GET_MOVIE_QUERY % name)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print(result["label"]["value"])

    return {
        "name": "mimi",
        "contributors": []
    }

if __name__ == '__main__':
    get_movie('Alice')
