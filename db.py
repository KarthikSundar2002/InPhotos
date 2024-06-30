from objectbox import *
import os
import numpy as np

@Entity()
class Photo:
    id = Id()
    path = String()
    vector = Float32Vector(index=HnswIndex(dimensions=512, distance_type= VectorDistanceType.COSINE))
    people = Int32Vector()

@Entity()
class People:
    id = Id()
    name = String()
    vector = Float32Vector(index=HnswIndex(dimensions=512, distance_type= VectorDistanceType.COSINE))
    face_path = String()

class DB:
    def __init__(self, directory):
        self.store = Store(directory=directory+"/objectbox", model_json_file=os.path.join(directory, "objectbox-model.json"))
        self.box = self.store.box(Photo)
        self.people_box = self.store.box(People)
    
    def add(self, path, vector, facial_embeddings, aligned_faces, pps):
        peep_in_photo = []
        ind = 0
        # for each image embedding
        # Check in People box and go through the centroids vector
        # If the sim_score is greater than a threshold, add the person to the people list
        for embedding in facial_embeddings:
            peep_query = self.people_box.query(People.vector.nearest_neighbor(embedding.detach()[0].numpy(), 1)).build()
            res = peep_query.find_with_scores()
            print("Res in Ind " + str(ind))
            print("Res:")
            print(res)
            print("PP:")
            print(pps[ind])
            if len(res) != 0:
                print(res[0][0].face_path)
                print(res[0][1])
                if res[0][1] < 0.5:
                    peep = res[0][0]
                    peep_in_photo.append(peep.id)
                    face_files = os.listdir(peep.face_path)
                    print("Face Files:")
                    print(face_files)
                    print("Hiiiii")
                    aligned_faces[ind].save(peep.face_path + str((len(face_files))%3) + '.jpg')
                else:
                    print("Creating new person")
                    i = os.listdir("./db/faces/")
                    peep_face_path = "./db/faces/" + str(len(i)) + "/"
                    os.makedirs(peep_face_path)
                    aligned_faces[ind].save(peep_face_path + str(0) + '.jpg')
                    peep = People(name="Unknown", vector=embedding.detach()[0].numpy(), face_path=peep_face_path)
                    peep_id = self.people_box.put(peep)
                    peep_in_photo.append(peep_id)
            else:
                i = os.listdir("./db/faces/")
                peep_face_path = "./db/faces/" + str(len(i)) + "/"
                os.makedirs(peep_face_path)
                print("First Entry in DB")
                print(peep_face_path)
                aligned_faces[ind].save(peep_face_path + str(0) + '.jpg')
                peep = People(name="Unknown", vector=embedding.detach()[0].numpy(), face_path=peep_face_path)
                peep_id = self.people_box.put(peep)
                peep_in_photo.append(peep_id)
            ind = ind + 1
        
        photo = Photo(path=path, vector=vector.detach().numpy(), people=peep_in_photo)
        print("Peep in photo:")
        print(peep_in_photo)
        
        self.box.put(photo)
    
    def search(self, vector, ner, max_results=10):
        peep_ids = []
        for i in ner:
            peep_query = self.people_box.query(People.name.equals(i,False)).build()
            res = peep_query.find()
            if len(res) != 0:
                print(res[0].name)
                print(res[0].id)
                peep_ids.append(res[0].id)
        
        query = self.box.query(Photo.vector.nearest_neighbor(vector.detach()[0].numpy(), max_results)).build()
        results = query.find_with_scores()
        print(results)
        res_peeps = [res[0].people for res in results]
        print(res_peeps)
        set_peeps = set(peep_ids)
        print(set_peeps)
        indices = [i for i in range(len(res_peeps)) if set(res_peeps[i]).issuperset(set_peeps)]
        print(indices)
        results = [results[i] for i in indices]
        results = [{"path": result[0].path, "score": result[1]} for result in results]
        return results
    
    def get_people(self):
        return self.people_box.get_all()

    def add_name(self, name, peep_id):
        peep = self.people_box.get(int(peep_id))
        peep.name = name
        self.people_box.put(peep)
    