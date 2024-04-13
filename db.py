import chromadb
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name='data_base')
# Now the collection is created and ready to use




# This is how you add stuff to the db, usualy called documents
collection.add(
    documents=["documents" , "More documents"], # This is the text that you want to add to the db
    metadatas=[{"source": "https//example.com"} , {"author": "Jane Doe"}], # This is optional, but it's useful to keep track of the source of the document
    ids=["id1", "id2"] # This is necassary,  didn't really understand how it's important
)

# This is how you query the db, means that you want to search for something , the result will be the most similar documents to the query, document, not a word
results = collection.query(
    query_texts=["doc"], # Input
    n_results=2, # Number of results, has to be less than or equal to the number of documents in the db
    include=['distances', 'metadatas', 'embeddings', 'documents'] # This is optional, you can remove it
)

