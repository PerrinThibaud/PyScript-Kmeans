import numpy as np

class Kmeans:
    def __init__(self, X: np.array, K: int = 16, max_iters: int = 10):
        self.X: np.array = np.array(X, copy=True)
        self.K: int = K
        self.max_iters: int = max_iters
        self.initial_centroids: np.array = self.kMeans_init_centroids()
    
    def reset(self, X: np.array, max_iters: int = 10):
        self.X: np.array = np.array(X, copy=True)
        self.max_iters: int = max_iters
        self.initial_centroids: np.array = self.kMeans_init_centroids()
    
    def set_k(self, K: int = 16):
        self.K: int = K

    def kMeans_init_centroids(self):
        """
        This function initializes K centroids that are to be 
        used in K-Means on the dataset X
        
        Args:
            X (ndarray): Data points 
            K (int):     number of centroids/clusters
        
        Returns:
            centroids (ndarray): Initialized centroids
        """
        
        # Randomly reorder the indices of examples
        randidx = np.random.permutation(self.X.shape[0])
        
        # Take the first K examples as centroids
        centroids = self.X[randidx[:self.K]]
        
        return centroids

    def find_closest_centroids(self, centroids):
        """
        Computes the centroid memberships for every example
        
        Args:
            X (ndarray): (m, n) Input values      
            centroids (ndarray): k centroids
        
        Returns:
            idx (array_like): (m,) closest centroids
        
        """
        # matrix of the closest centroid for each x(i)
        idx = np.zeros(self.X.shape[0], dtype=int)

        # distance of each point the each centroids => ||x(i) - µj||² where µj is the position of the j'th centroid
        a = np.linalg.norm(self.X[:, None] - centroids, axis=2)
        # Remains the min distance, in order to get the closest centroid
        idx = np.argmin(a, axis=1)
        
        return idx

    def compute_centroids(self, idx):
        """
        Returns the new centroids by computing the means of the 
        data points assigned to each centroid.
        
        Args:
            X (ndarray):   (m, n) Data points
            idx (ndarray): (m,) Array containing index of closest centroid for each 
                        example in X. Concretely, idx[i] contains the index of 
                        the centroid closest to example i
            K (int):       number of centroids
        
        Returns:
            centroids (ndarray): (K, n) New centroids computed
        """
        m, n = self.X.shape
        centroids = np.zeros((self.K, n))
        
        # µk = 1/|𝐶𝑘| * ∑𝑥(𝑖)
        # where:
        # - µk is the new centroid k
        # - Ck is the set of examples that are assigned to centroid 𝑘
        # - |𝐶𝑘| is the number of examples in the set 𝐶𝑘
        for k in range(self.K):   
            points = self.X[idx == k]
            centroids[k] = np.mean(points, axis = 0)
        return centroids

    def run(self):
        """
        In the data matrix X, each row of X is a single example
        """
        
        # Initialize values
        m, n = self.X.shape
        centroids = self.initial_centroids
        idx = np.zeros(m)
        
        # Run K-Means
        for i in range(self.max_iters):
            
            #Output progress
            print("K-Means iteration %d/%d" % (i, self.max_iters-1))
            # For each example in X, assign it to the closest centroid
            idx = self.find_closest_centroids(centroids)
            
                
            # Given the memberships, compute new centroids
            centroids = self.compute_centroids(idx)
        return centroids, idx

    def reshape(self, centroids, idx, alpha):
        X_recovered = centroids[idx, :] 

        colors_number = np.unique(X_recovered, axis=0) # count the number of color who is normally equals to K

        X_recovered = np.concatenate([ X_recovered * 255, alpha], axis = 1) # adding the aplha column


        # Reshape recovered image into proper dimensions
        # X_recovered = X_recovered.reshape(256, 256, 4) # reshaping to the initial size
        X_recovered = X_recovered.reshape(-1) # reshaping image data size (flatten)
        return X_recovered, colors_number

    # to n and divisible by m
    def closest_number(self, n, m) :
        # Find the quotient
        q = int(n / m)
        
        # 1st possible closest number
        n1 = m * q
        
        # 2nd possible closest number
        if((n * m) > 0) :
            # n2 = (m * (q + 1))
            n2 = (m * (q - 1)) # we always want a lower size
        else :
            n2 = (m * (q - 1))
        
        # if true, then n1 is the required closest number
        if (abs(n - n1) < abs(n - n2)) :
            return n1
        
        # else n2 is the required closest number
        return n2

    def crop(self, img):
        width, height, a = img.shape
        min_size = min(width, height)
        min_size = self.closest_number(min_size, 256)
        starty = width//2-(min_size//2)
        startx = height//2-(min_size//2)
        return img[starty:starty+min_size, startx:startx+min_size, :]

    def resize(self, large_image):
        large_image = self.crop(large_image)
        width, height, alpha = large_image.shape

        input_size = width
        output_size = 256
        bin_size = input_size // output_size
        small_image = large_image.reshape((output_size, bin_size, 
                                   output_size, bin_size, alpha)).max(3).max(1)
        return small_image