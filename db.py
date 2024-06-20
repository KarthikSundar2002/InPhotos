from objectbox import *

@Entity()
class Photo:
    id = Id()
    path = String()
    vector = Float32Vector(index=HnswIndex(dimensions=512, distance_type= VectorDistanceType.COSINE))

class DB:
    def __init__(self, directory="/home/stark/Documents/projects/InPhotos/db"):
        self.store = Store()
        self.box = self.store.box(Photo)
    
    def add(self, path, vector):
        photo = Photo(path=path, vector=vector.detach().numpy())
        self.box.put(photo)
    
    def search(self, vector, max_results=10):
        query = self.box.query(Photo.vector.nearest_neighbor(vector.detach()[0].numpy(), max_results)).build()
        results = query.find_with_scores()
        results = [{"path": result[0].path, "score": result[1]} for result in results]
        return results
        