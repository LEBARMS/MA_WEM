#!/usr/bin/env python
# coding: utf-8

# In[6]:


from elasticsearch import Elasticsearch
import json

# Connect to Elasticsearch (assumes it's running on localhost:9200)
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "wem_index"

# Define a search query that boosts the title field
query_body = {
    "query": {
        "multi_match": {
            "query": "quotes",              # Replace with your search term
            "fields": [
                "title^3",                 # Boosting the title field by a factor of 3
                "meta_description",        # Normal weight
                "headings"                 # Normal weight; add more fields if needed
            ],
            "fuzziness": "AUTO"            # Enable fuzzy search to handle minor typos/variations
        }
    }
}

# Execute the search query
response = es.search(index=INDEX_NAME, body=query_body)

# Print total number of hits
total_hits = response["hits"]["total"]["value"]
print(f"Total hits: {total_hits}")

# Loop through and print each hit in a readable format
for hit in response["hits"]["hits"]:
    source = hit["_source"]
    score = hit["_score"]
    print("\n------------------------------")
    print(json.dumps(source, indent=2, ensure_ascii=False))
    print(f"Score: {score}")


# In[ ]:




