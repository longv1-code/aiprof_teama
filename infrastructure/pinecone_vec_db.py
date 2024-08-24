from pinecone import Pinecone
from infrastructure.util import read_json_file
from infrastructure.embed import embed
from infrastructure.util import load_env

# List to store processed data.
processed_data = []

# Initiate vector database.
pc = Pinecone(api_key=load_env("PC_API_KEY"))

# Index from pinecone, same as collections in other DBs.
index = pc.Index("ai-rate-my-professor")

# processing the data for pinecone.
def process_data(file: str= "./data.json"):
    """Function will load data and process this data to store in a list. List will be stored in
        the vector database.
    """
    # Loading data.
    reviews = read_json_file(file_path=file)
    # Iterating on data.
    for reviews in reviews["reviews"]:
        response = embed(reviews["reviews"])
        embeddings = response["embedding"]
        # insert processed data in the list.
        processed_data.append(
            {
                "values": embeddings,
                "id": reviews["professor"],
                "metadata": {
                    "review": reviews["reviews"],
                    "subject": reviews["subject"],
                    "stars": reviews["stars"]
                }
            }
        )

# process_data()
# print(processed_data)

# Inserting data into the pinecone DB.
def insert_data():
    """Function will process data and then insert it into the pinecone DB at given namespace."""
    process_data()
    index.upsert(
        vectors= processed_data,
        namespace= "prfessor's namepace"  # Such as collection in qdrant DB.
    )

# insert_data()

# Retrieve data:
def query(prompt: str):
    """Function is used to return the data related to the given prompt."""
    def retrieve():
        return index.query(
            namespace="prfessor's namepace",
            vector= embed(prompt)["embedding"],
            top_k=4,
            include_values=True,
            include_metadata=True
        )
    # Retrieve data.
    retrieval = retrieve()
    # Extract only what we need.
    extracted_data = [{'id': match['id'], 'metadata': match['metadata']} for match in retrieval['matches']]
    return extracted_data

# Test
# print(query("Suggest me a teacher which brings real world experience to the class."))