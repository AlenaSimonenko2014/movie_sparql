from SPARQLWrapper import SPARQLWrapper, JSON

GET_MOVIE_SOURCE = "http://localhost:3030/first_dataset/query"
GET_MOVIE_QUERY = """
PREFIX imdb: <http://data.linkedmdb.org/resource/movie/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dbpo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX im: <http://imgpedia.dcc.uchile.cl/resource/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT ?movieTitle ?movieDate ?musicContributor ?who ?genre ?name
{
# { SERVICE <http://data.linkedmdb.org/sparql>
#     { SELECT DISTINCT ?musicContributor
#         WHERE {
#                 ?movie rdfs:label "Titanic" ;
#                        imdb:music_contributor ?musicContributorURI .#;
##                        dcterms:title ?movieTitle ;
##                        dcterms:date ?movieDate .
#
#                 ?musicContributorURI imdb:music_contributor_name ?musicContributor .
#         }
#     }
# }
  
#  { SERVICE <http://dbpedia.org/sparql>
#    { SELECT ?who ?genre
#      WHERE {
#        ?who foaf:name ?name .
#        ?who dbo:genre ?genre .
#        ?genre rdf:type dbo:MusicGenre
#        FILTER regex(?name, CONCAT("^", "Metallica", ".*"), "i")
#
#      }
#    }
#  }
  
  { SERVICE <http://dbpedia.org/sparql>
    { SELECT ?name
      WHERE {
        ?who foaf:name ?name .
        ?who dbo:genre <http://dbpedia.org/resource/%s> .
      }
    }
  }
}

"""


def get_movie(name: str):
    sparql = SPARQLWrapper(GET_MOVIE_SOURCE)
    sparql.setQuery(GET_MOVIE_QUERY % name)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print(result["name"]["value"]) #, '\t\t', result["bandname"]["value"])

    return {
        "name": "mimi",
        "contributors": []
    }

if __name__ == '__main__':
    get_movie('Thrash_metal')
