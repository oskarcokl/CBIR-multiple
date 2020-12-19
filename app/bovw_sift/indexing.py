from image_loader import ImageLoader 
from sift_descriptor import SiftDescriptor
from sklearn.cluster import KMeans


def index():
    test_folder_path = "../../data/test/"
    train_folder_path = "../../data/train/"

    
    
    # Small image dataset for testing
    small_folder_path = "../../data/small/"

    print("loading images")
    imageLoader = ImageLoader()
    #test_images = imageLoader.load_images_from_folder_and_grayscale(test_folder_path)
    #train_images = imageLoader.load_images_from_folder_and_grayscale(train_folder_path)
    (small_images, small_imageIDs) = imageLoader.load_images_from_folder_and_grayscale(small_folder_path)
    print("finished loading images")


    siftDescriptor = SiftDescriptor()

    (small_descriptor_list, small_bovw_features) = siftDescriptor.describe(small_images) 
    #(train_descriptor_list, train_bovw_features) = siftDescriptor.describe(train_images) 
    #(test_descriptor_list, test_train_bovw_feature) = siftDescritpor.describe(train_images)
    
    # Getting clusters from the descriptor_list
    visual_words = k_means(150, small_descriptor_list)
    print(type(visaul_words))


def k_means(k, descriptor_list):
    visual_words = KMeans(n_clusters = k, n_init=10)
    visual_words.fit(descriptor_list)
    return visual_words

def build_histogram(descriptor_list, clusters):
    histogram = np.zeros(len(clusters.cluster_centers_))
    cluster_result = clusters.predict(descriptor_list)
    for i in cluster_result:
        histogram[i] += 1.0
    return histogram


index()
