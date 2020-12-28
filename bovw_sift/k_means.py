from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans

class MyKMeans:    
    def k_means(self, k, descriptor_list):
        visual_words = KMeans(n_clusters = k)
        visual_words.fit(descriptor_list)
        return visual_words

    def k_means_batch(self, k, descriptor_list, batch):
        visual_words = MiniBatchKMeans(n_clusters = k, batch_size = batch)
        visual_words.fit(descriptor_list)
        return visual_words
