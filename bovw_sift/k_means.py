from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans

class MyKMeans:    
    def k_means(self, k, descriptor_list):
        visual_words = KMeans(n_clusters = k, verbose=1)
        visual_words.fit(descriptor_list)
        return visual_words

    def k_means_batch(self, k, descriptor_list, batch):
        print("What")
        visual_words = MiniBatchKMeans(n_clusters=k, batch_size=batch)
        print("Fitting")
        visual_words.fit(descriptor_list)
        return visual_words
