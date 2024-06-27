import requests

# SPARQL query
query = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT {
  ?subject rdf:type ?type .
  ?subject skos:prefLabel ?prefLabel .
  ?subject skos:scopeNote ?scopeNote .
  ?subject skos:altLabel ?altLabel .
  ?subject skos:hiddenLabel ?hiddenLabel .
  ?subject skos:broader ?broader .
  ?subject skos:narrower ?narrower .
  ?subject skos:inScheme ?scheme .
  ?scheme rdf:type skos:ConceptScheme .
  ?scheme skos:hasTopConcept ?topConcept .
  ?topConcept skos:topConceptOf ?scheme .
}
WHERE {
  {
    SELECT DISTINCT ?subject ?type ?prefLabel ?scopeNote ?narrower ?broader ?altLabel ?hiddenLabel ?scheme
    WHERE {
      GRAPH <https://data.cultureelerfgoed.nl/term/id/cht/thesaurus> {
        ?subject rdf:type ?type ;
                 skos:prefLabel ?prefLabel ;
                 skos:scopeNote ?scopeNote .
        FILTER (?type = skos:Concept && LANG(?prefLabel) = 'nl' && LANG(?scopeNote) = 'nl')

        OPTIONAL { ?subject skos:altLabel ?altLabel . FILTER(LANG(?altLabel) = 'nl') }
        OPTIONAL { ?subject skos:hiddenLabel ?hiddenLabel . FILTER(LANG(?hiddenLabel) = 'nl') }
        OPTIONAL { ?subject skos:broader ?broader }
        OPTIONAL { ?subject skos:narrower ?narrower }

        ?subject skos:inScheme ?scheme .
        ?scheme a skos:ConceptScheme .
        FILTER(?scheme = <https://data.cultureelerfgoed.nl/term/id/cht/b532325c-dc08-49db-b4f1-15e53b037ec3>)
      }
    }
  }
  UNION
  {
    SELECT DISTINCT ?scheme ?topConcept
    WHERE {
      GRAPH <https://data.cultureelerfgoed.nl/term/id/cht/thesaurus> {
        ?scheme a skos:ConceptScheme .
        ?scheme skos:hasTopConcept ?topConcept .
        ?topConcept skos:topConceptOf ?scheme .
        FILTER(?scheme = <https://data.cultureelerfgoed.nl/term/id/cht/b532325c-dc08-49db-b4f1-15e53b037ec3>)
      }
    }
  }
}
"""

# Endpoint URL
url = "https://data.cultureelerfgoed.nl/PoolParty/sparql/term/id/cht"

# Set the headers to request Turtle format
headers = {
    'Accept': 'text/turtle'
}

# Perform the SPARQL query
response = requests.post(url, data={'query': query}, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Save the response as a TTL file
    with open("cht-kennisbank.ttl", "w", encoding='utf-8') as f:
        f.write(response.text)
    print("Response saved as cht-kennisbank.ttl")
else:
    print("Error:", response.status_code, response.reason)
