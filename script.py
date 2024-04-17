from openai import OpenAI 

from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.llms import OpenAI  
from langchain_community.embeddings import OpenAIEmbeddings

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from datasets import load_dataset
# you'll need to get your own opwnai key if you wanna help, I forgot to put these keys in a .ignore file :). If you actually wanna help, text me to send you this ASTRA_DB_SECURE_CONNECT_BUNDLE file so u can use it
ASTRA_DB_SECURE_CONNECT_BUNDLE = "\\Users\\mmahf\\Desktop\\Coding\\Randoms\\AstraDB\\secure-connect-vectordb.zip"

ASTRA_CLIENT_ID = "JjmPfnAKGnKAntDGZUbvPleM"
ASTRA_CLIENT_SECRET = "epQnR.8p4QxMQ3hx8y29ZkNuDZ+k0HGEifLTeoYlxUdPpdWhK+CJ-d0iXB7nd0UwSZkpTZAepPY6pGd_uXPfRRLDq5kFBZ2g8hZAvYMTxofKU37cl63c5p25qhctL+NU"
ASTRA_TOKEN = "AstraCS:JjmPfnAKGnKAntDGZUbvPleM:0fd2958b0b17a1be6880ceb20b694b666af995677fa27f06474420ceffe2d21f"

ASTRA_DB_KEYSPACE = "default_keyspace"
OPENAI_API_KEY = "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"




cloud_config= {
        'secure_connect_bundle': ASTRA_DB_SECURE_CONNECT_BUNDLE
}

auth_provider = PlainTextAuthProvider(ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
astra_session = cluster.connect()

llm = OpenAI(OPENAI_API_KEY)

embeddings = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)

cassandra = Cassandra(
    embedding=embeddings,
    session=astra_session,
    keyspace=ASTRA_DB_KEYSPACE,
    table_name="table"
)



print("Loading data from Hugging Face")
dataset = load_dataset("Biddls/Onion_News" , split = "train")
headlines = dataset["text"][:50]


print("Generating embeddings")
cassandra.add_texts(headlines)



print("inserted headlines:" , len(headlines))


# I have no idea what I'm doing here, I just wrote this code from a youtube video.
