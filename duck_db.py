import duckdb

class DB:
    def __init__(self, is_first_time=False):
        self.conn = duckdb.connect("./duckdb/vec.db")
        self.conn.execute("""
            INSTALL vss;
            LOAD vss;
                        """)
        self.conn.execute("SET hnsw_enable_experimental_persistence = true")
        if is_first_time:
            self.create_photos_table()

    def create_photos_table(self):
        self.conn.execute("CREATE SEQUENCE photos_id START 1;")
        self.conn.execute("CREATE TABLE photos (id INTEGER PRIMARY KEY DEFAULT nextval('photos_id'), path STRING, vector FLOAT[512]);")
        self.conn.execute("CREATE INDEX idx_photos ON photos USING HNSW(vector) WITH (metric = 'cosine')")

    def add(self, path, vec):
        vec = vec.astype('float32').tolist()
        self.insert_photo(path, vec)
    
    def search(self, vector, max_results=10):
        results = self.find_photo_from_embedding(vector[0])
        results = [{"path": res[1]} for res in results]
        return results
   
    def find_photo_from_embedding(self, embedding):
        print("Here in DB Function")
        print(embedding.shape)
        embedding = embedding.astype('float32').tolist()
        query_str = f"SELECT * FROM photos ORDER BY array_cosine_similarity(vector, Cast({embedding} As FLOAT[512])) LIMIT 10"
        query = self.conn.execute(query_str)
        return query.fetchall()
    
    def insert_photo(self, path, vector):
        query_str = f"INSERT INTO photos VALUES (DEFAULT,'{path}', Cast({vector} As FLOAT[512]))"
        self.conn.execute(query_str)