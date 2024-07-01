import duckdb, os
import numpy as np

class DB:
    def __init__(self):
        self.conn = duckdb.connect("./duckdb/vec.db")
        self.conn.execute("""
            INSTALL vss;
            LOAD vss;
                        """)
        self.conn.execute("SET hnsw_enable_experimental_persistence = true")
        self.create_photos_table()
        self.create_people_table()
        self.num_people = 0

    def create_photos_table(self):
        self.conn.execute("CREATE SEQUENCE photos_id START 1;")
        self.conn.execute("CREATE TABLE photos (id INTEGER PRIMARY KEY DEFAULT nextval('photos_id'), path STRING, vector FLOAT[512], people INTEGER[]);")
        self.conn.execute("CREATE INDEX idx_photos ON photos USING HNSW(vector) WITH (metric = 'cosine')")

    def create_people_table(self):
        self.conn.execute("CREATE TABLE people (id INTEGER, name STRING, vector FLOAT[512], face_path STRING, num_photos INTEGER DEFAULT 0);")
        self.conn.execute("CREATE INDEX idx_people ON people USING HNSW(vector) WITH (metric = 'cosine')")

    def add(self, path, vec, facial_embeds, aligned_faces, pps):
        peep_in_photo = []
        ind = 0
        vec = vec.detach().numpy().astype('float32').tolist()
        
        for embedding in facial_embeds:
            peep_query = self.find_people_from_embedding(embedding)
            if peep_query is not None:
                id ,name,vector ,face_path,num_photos,sim_score= peep_query
                if sim_score > 0.5:
                    peep_in_photo.append(id)
                    face_files = os.listdir(face_path)
                    aligned_faces[ind].save(face_path + str((len(face_files))%3) + '.jpg')
                    new_embedding = embedding.detach()[0].numpy()
                    new_embedding = (new_embedding + vector)/(num_photos + 1)
                    num_photos  = num_photos + 1
                    #self.update_people_embedding(id, new_embedding, num_photos)
                else:
                    i = os.listdir("./db/faces/")
                    peep_face_path = "./db/faces/" + str(len(i)) + "/"
                    os.makedirs(peep_face_path)
                    aligned_faces[ind].save(peep_face_path + str(0) + '.jpg')
                    self.num_people = self.num_people + 1
                    insert_peep_id = self.insert_person(self.num_people,"Unknown", embedding.detach()[0].numpy(), peep_face_path)
                    peep_in_photo.append(insert_peep_id)
            else:
                i = os.listdir("./db/faces/")
                peep_face_path = "./db/faces/" + str(len(i)) + "/"
                os.makedirs(peep_face_path)
                aligned_faces[ind].save(peep_face_path + str(0) + '.jpg')
                self.num_people = self.num_people + 1
                insert_peep_id = self.insert_person(self.num_people,"Unknown", embedding.detach()[0].numpy(), peep_face_path)
                peep_in_photo.append(insert_peep_id)
            ind = ind + 1
        self.insert_photo(path, vec, peep_in_photo)
    
    def search(self, vector, ner, max_results=10):
        peep_ids = []
        for i in ner:
            peep_query = self.find_people_by_name(i)
            if peep_query is not None:
                id ,name,vec ,face_path,num_photos = peep_query
                peep_ids.append(id)
        
        results = self.find_photo_from_people_and_embedding(peep_ids, vector)
        results = [{"path": res[1]} for res in results]
        return results

    def get_people(self):
        query = self.conn.execute("SELECT * FROM people")
        return query.fetchall()
    
    def add_name(self, name, peep_id):
        id ,old_name,vector ,face_path,num_photos = self.find_people_by_id(peep_id)
        vector = np.array(vector).astype('float32').tolist()
        self.conn.execute(f"""BEGIN TRANSACTION;
                          DELETE FROM people WHERE ID = {id};
                          COMMIT; """)
        self.conn.execute(f"INSERT INTO people VALUES ({id}, '{name.lower()}', {vector}, '{face_path}', {num_photos})")

    def find_people_by_id(self, id):
        query = self.conn.execute(f"SELECT * FROM people WHERE ID = {id}")
        return query.fetchone()
    
    def find_people_by_name(self, name):
        name = name.lower()
        query = self.conn.execute(f"SELECT * FROM people WHERE name = '{name}'")
        return query.fetchone()

    def find_people_from_embedding(self, embedding):
        embedding = embedding.detach()[0].numpy()
        embedding = embedding.astype('float32').tolist()
        query_str = f"SELECT id,name,vector,face_path,num_photos, array_cosine_similarity(vector, Cast({embedding} As FLOAT[512])) AS distance FROM people ORDER BY distance LIMIT 1"
        query = self.conn.execute(query_str)
        res = query.fetchone()
        return res
   
    def find_photo_from_people_and_embedding(self, peep_ids, embedding):
        embedding = embedding.detach()[0].numpy()
        embedding = embedding.astype('float32').tolist()
        query_str = f"SELECT * FROM photos WHERE list_has_all(people,{peep_ids}) ORDER BY array_cosine_similarity(vector, Cast({embedding} As FLOAT[512])) LIMIT 10"
        query = self.conn.execute(query_str)
        return query.fetchall()
    
    def update_people_embedding(self, peep_id, embedding, num_photos):
        embedding = embedding.astype('float32').tolist()
        id ,name,vector ,face_path,old_num_photos = self.find_people_by_id(peep_id)
        self.conn.execute(f"""BEGIN TRANSACTION;
                          DELETE FROM people WHERE ID = {peep_id};
                          COMMIT; """)
        self.conn.execute(f"INSERT INTO people VALUES ({peep_id}, '{name.lower()}', {embedding}, '{face_path}', {num_photos})") 
       
    def insert_person(self, id,name, embedding, face_path):
        embedding = embedding.astype('float32').tolist()
        query = self.conn.execute(f"""
                          INSERT INTO people VALUES ({id},'{name}', {embedding}, '{face_path}',DEFAULT)
                          RETURNING id
                          """)
        res = query.fetchone()
        return res[0]
    
    def insert_photo(self, path, vector, people):
        query_str = f"INSERT INTO photos VALUES (DEFAULT,'{path}', Cast({vector} As FLOAT[512]), {people})"
        self.conn.execute(query_str)