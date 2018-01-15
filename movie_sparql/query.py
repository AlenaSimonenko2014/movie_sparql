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
SELECT ?musicContributor ?contributor_genre ?name_of_contributor ?name ?genre
{
 { SERVICE <http://data.linkedmdb.org/sparql>
     { SELECT DISTINCT ?musicContributor 
        WHERE {
                 ?movie rdfs:label "%s" ;
                        imdb:music_contributor ?musicContributorURI .
                 ?musicContributorURI imdb:music_contributor_name ?musicContributor .

         }
     }
 }

  { SERVICE <http://dbpedia.org/sparql>
   { SELECT ?contributor_genre ?name_of_contributor
      WHERE {
        ?who foaf:name ?name_of_contributor .
        ?who dbo:genre ?contributor_genre .
       ?contributor_genre rdf:type dbo:MusicGenre
      }
    }
  }

  { SERVICE <http://dbpedia.org/sparql>
    { SELECT ?name ?genre
      WHERE {
        ?who foaf:name ?name .
        ?genre rdf:type dbo:MusicGenre.
        ?who dbo:genre ?genre .#<http://dbpedia.org/resource/Progressive_rock> .
      }
    }
  }
 FILTER regex(?name_of_contributor, CONCAT("^", ?musicContributor, ".*"), "i")
 #FILTER (?genre=?contributor_genre)

}

LIMIT 100

"""


def get_contributors_for_movie(name: str):
    sparql = SPARQLWrapper(GET_MOVIE_SOURCE)
    sparql.setQuery(GET_MOVIE_QUERY % name)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return_list = []

    for result in results["results"]["bindings"]:
        # ?musicContributor ?contributor_genre ?name_of_contributor ?name ?genre ?who
        return_list.append({
            'name': result["musicContributor"]["value"],
            'genre': result["genre"]["value"],
            'same_genre_contributor': result["name"]["value"]
        })
        print(result["name"]["value"])#, '\t\t', result["contributor_genre"]["value"],
             # result["name_of_contributor"]["value"], '\t\t', result["name"]["value"], '\t\t', result["genre"]["value"])

    # return_list.append({
    #     'name': "The Beatles",
    #     'genre': "Pop Rock",
    #     'same_genre_contributor': "Killers"
    # })
    return return_list


if __name__ == '__main__':
    get_contributors_for_movie('Meeting People Is Easy')
