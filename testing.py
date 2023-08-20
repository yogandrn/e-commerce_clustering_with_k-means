import math
import numpy as np

# Data dalam bentuk dictionary
datas = [
    {'id_product': '35509867', 'sold': 367, 'rating_score': 4.897, 'count_review': 198, 'cluster': 0},
    {'id_product': '35509877', 'sold': 0, 'rating_score': 0, 'count_review': 0, 'cluster': 0},
    {'id_product': '35507877', 'sold': 1250, 'rating_score': 4.567, 'count_review': 987, 'cluster': 0},
    {'id_product': '35589857', 'sold': 20, 'rating_score': 4.9, 'count_review': 18, 'cluster': 0},
    {'id_product': '35309877', 'sold': 128, 'rating_score': 4.708, 'count_review': 99, 'cluster': 0},
    {'id_product': '35509887', 'sold': 2008, 'rating_score': 4.67, 'count_review': 1702, 'cluster': 0},
    {'id_product': '33569877', 'sold': 367, 'rating_score': 4.897, 'count_review': 0, 'cluster': 0},
    {'id_product': '35509877', 'sold': 30, 'rating_score': 4.897, 'count_review': 19, 'cluster': 0},
    {'id_product': '35519807', 'sold': 1, 'rating_score': 0, 'count_review': 0, 'cluster': 0},
    {'id_product': '35539872', 'sold': 188, 'rating_score': 4.755, 'count_review': 184, 'cluster': 0},
    {'id_product': '35509571', 'sold': 0, 'rating_score': 0, 'count_review': 0, 'cluster': 0},
    {'id_product': '35709677', 'sold': 3, 'rating_score': 5, 'count_review': 2, 'cluster': 0},
    {'id_product': '35579822', 'sold': 45, 'rating_score': 4.865, 'count_review': 24, 'cluster': 0},
    {'id_product': '35509867', 'sold': 367, 'rating_score': 4.897, 'count_review': 198, 'cluster': 0},
    {'id_product': '35509877', 'sold': 340, 'rating_score': 4.634, 'count_review': 298, 'cluster': 0},
    {'id_product': '35507877', 'sold': 1098, 'rating_score': 4.497, 'count_review': 1023, 'cluster': 0},
    {'id_product': '35589857', 'sold': 16, 'rating_score': 4.9, 'count_review': 12, 'cluster': 0},
    {'id_product': '35309877', 'sold': 156, 'rating_score': 4.8, 'count_review': 88, 'cluster': 0},
    {'id_product': '35509887', 'sold': 10, 'rating_score': 4.8, 'count_review': 9, 'cluster': 0},
    {'id_product': '33569877', 'sold': 2, 'rating_score': 0, 'count_review': 0, 'cluster': 0},
    {'id_product': '35509877', 'sold': 29, 'rating_score': 4.897, 'count_review': 9, 'cluster': 0},
    {'id_product': '35519807', 'sold': 1, 'rating_score': 0, 'count_review': 0, 'cluster': 0},
    {'id_product': '35539872', 'sold': 2409, 'rating_score': 4.655, 'count_review': 1902, 'cluster': 0},
    {'id_product': '35509571', 'sold': 0, 'rating_score': 0, 'count_review': 0, 'cluster': 0},
    {'id_product': '35709677', 'sold': 15, 'rating_score': 5, 'count_review': 10, 'cluster': 0},
    {'id_product': '35579822', 'sold': 72, 'rating_score': 4.865, 'count_review': 34, 'cluster': 0},
    {'id_product': '35539872', 'sold': 208, 'rating_score': 4.755, 'count_review': 50, 'cluster': 0},
    {'id_product': '35509571', 'sold': 4, 'rating_score': 5, 'count_review': 2, 'cluster': 0},
    {'id_product': '35709677', 'sold': 13, 'rating_score': 4.9, 'count_review': 6, 'cluster': 0},
    {'id_product': '35579822', 'sold': 82, 'rating_score': 4.885, 'count_review': 44, 'cluster': 0},
    {'id_product': '35509867', 'sold': 450, 'rating_score': 4.797, 'count_review': 345, 'cluster': 0},
    {'id_product': '35509877', 'sold': 1, 'rating_score': 5, 'count_review': 1, 'cluster': 0},
    {'id_product': '35507877', 'sold': 1198, 'rating_score': 4.597, 'count_review': 903, 'cluster': 0},
    {'id_product': '35589857', 'sold': 16, 'rating_score': 4.9, 'count_review': 12, 'cluster': 0},
    {'id_product': '35309877', 'sold': 156, 'rating_score': 4.8, 'count_review': 88, 'cluster': 0},
    {'id_product': '35509887', 'sold': 10, 'rating_score': 4.8, 'count_review': 9, 'cluster': 0},
    {'id_product': '33569877', 'sold': 2, 'rating_score': 0, 'count_review': 0, 'cluster': 0},
    {'id_product': '35509877', 'sold': 29, 'rating_score': 4.897, 'count_review': 9, 'cluster': 0},
    {'id_product': '35519807', 'sold': 1, 'rating_score': 0, 'count_review': 0, 'cluster': 0},
    {'id_product': '35539872', 'sold': 1569, 'rating_score': 4.655, 'count_review': 1202, 'cluster': 0},
    {'id_product': '35509571', 'sold': 567, 'rating_score': 4.876, 'count_review': 450, 'cluster': 0},
    {'id_product': '35709677', 'sold': 55, 'rating_score': 4.895, 'count_review': 23, 'cluster': 0},
    {'id_product': '35579822', 'sold': 92, 'rating_score': 4.587, 'count_review': 86, 'cluster': 0},
    # ... tambahkan data lainnya jika ada
]

def cluster(data) :
    # Fitur yang akan digunakan untuk clustering
    features = ['sold', 'rating_score', 'count_review']

    # Jumlah kluster yang diinginkan
    num_clusters = 3

    # Pusat kluster awal yang Anda tentukan (dalam bentuk list of dictionaries)
    initial_centers = [
        {'sold': 15, 'rating_score': 4.8, 'count_review': 10},
        {'sold': 50, 'rating_score': 4.9, 'count_review': 50},
        {'sold': 100, 'rating_score': 5, 'count_review': 100}
    ]
    # Mengubah initial_centers menjadi satu list yang berisi nilai fitur secara berurutan
    centers = np.array([initial_centers[i][feature] for feature in features for i in range(num_clusters)])

    # Maksimum iterasi
    max_iters = 100

    for _ in range(max_iters):
        # Menyimpan hasil kluster untuk setiap data point
        cluster_assignments = []

        # Assign data point ke kluster terdekat
        for item in data:
            distances = []
            for center_idx in range(num_clusters):
                distance = 0
                for feature in features:
                    distance += (item[feature] - centers[center_idx * len(features) + features.index(feature)]) ** 2
                distances.append(math.sqrt(distance))
            cluster_assignments.append(distances.index(min(distances)))

        # Menghitung pusat baru untuk setiap kluster
        new_centers = np.zeros((num_clusters, len(features)))
        cluster_counts = np.zeros(num_clusters)
        for i, item in enumerate(data):
            cluster_idx = cluster_assignments[i]
            for feature_idx, feature in enumerate(features):
                new_centers[cluster_idx, feature_idx] += item[feature]
            cluster_counts[cluster_idx] += 1
        for cluster_idx in range(num_clusters):
            new_centers[cluster_idx] /= cluster_counts[cluster_idx]

        # Mengecek apakah pusat kluster sudah konvergen
        if np.all(centers == new_centers):
            break

        centers = new_centers.flatten()

    # Memperbarui nilai 'cluster' di setiap item data
    for i, item in enumerate(data):
        item['cluster'] = cluster_assignments[i]

    # Menampilkan hasil kluster untuk setiap key 'cluster'
    # for cluster_id in range(num_clusters):
    #     clustered_data = [item for item in data if item['cluster'] == cluster_id]
    #     print(f"Cluster {cluster_id}:")
    #     for item in clustered_data:
    #         print(item)
    #     print("\n")

    # print (data)
    return data

# print(cluster(datas))


def clustering(params) :

    data = params #ambil array dari parameter
    hasil_cluster = [] # untuk menampung hasil cluster sementara

    num_cluster = 3 # tentukan jumlah cluster

    # inisialisasi titik pusat cluster / centroid 
    centroids = {
        'c1' : {'sold' : 25, 'rating_score': 4.7, 'count_review' : 25},
        'c2' : {'sold' : 100, 'rating_score': 4.8, 'count_review' : 100},
        'c3' : {'sold' : 250, 'rating_score': 4.9, 'count_review' : 250},
    }

    max_iteration = 20 # atur iterasi maksimal

    for _ in range(max_iteration) :
        # centroids = init_centroids
        sum_c1 = {'sold' : 0, 'rating_score' : 0, 'count_review' : 0}
        sum_c2 = {'sold' : 0, 'rating_score' : 0, 'count_review' : 0}
        sum_c3 = {'sold' : 0, 'rating_score' : 0, 'count_review' : 0}
        jml_c1 = 0
        jml_c2 = 0
        jml_c3 = 0

        for i in range(len(data)) :
            distance = []
            # print(item)
            c1 = math.sqrt((data[i]['sold'] - centroids['c1']['sold']) ** 2 + (data[i]['rating_score'] - centroids['c1']['rating_score']) ** 2 + (data[i]['count_review'] - centroids['c1']['count_review']) ** 2)
            c2 = math.sqrt((data[i]['sold'] - centroids['c2']['sold']) ** 2 + (data[i]['rating_score'] - centroids['c2']['rating_score']) ** 2 + (data[i]['count_review'] - centroids['c2']['count_review']) ** 2)
            c3 = math.sqrt((data[i]['sold'] - centroids['c3']['sold']) ** 2 + (data[i]['rating_score'] - centroids['c3']['rating_score']) ** 2 + (data[i]['count_review'] - centroids['c3']['count_review']) ** 2)
            # print(c1, c2, c3)
            if (c1 < c2 and c1 < c3) :
                sum_c1['sold'] += data[i]['sold'] 
                sum_c1['rating_score'] += data[i]['rating_score'] 
                sum_c1['count_review'] += data[i]['count_review'] 
                jml_c1 += 1
                data[i]['cluster'] = 1

            if (c2 < c1 and c2 < c3) :
                sum_c2['sold'] += data[i]['sold'] 
                sum_c2['rating_score'] += data[i]['rating_score'] 
                sum_c2['count_review'] += data[i]['count_review'] 
                jml_c2 += 1
                data[i]['cluster'] = 2

            if (c3 < c1 and c3 < c2) :
                sum_c3['sold'] += data[i]['sold'] 
                sum_c3['rating_score'] += data[i]['rating_score'] 
                sum_c3['count_review'] += data[i]['count_review'] 
                jml_c3 += 1
                data[i]['cluster'] = 3
            
            # print(data[i])
        
        print(jml_c1, jml_c2, jml_c3)

        # buat centroid baru 
        new_centroid = {
            'c1' : {'sold' : round(sum_c1['sold'] / jml_c1, 2), 'rating_score': round(sum_c1['rating_score'] / jml_c1, 2), 'count_review' : round(sum_c1['count_review'] / jml_c1, 2)},
            'c2' : {'sold' : round(sum_c2['sold'] / jml_c2, 2), 'rating_score': round(sum_c2['rating_score'] / jml_c2, 2), 'count_review' : round(sum_c2['count_review'] / jml_c2, 2)},
            'c3' : {'sold' : round(sum_c3['sold'] / jml_c3, 2), 'rating_score': round(sum_c3['rating_score'] / jml_c3, 2), 'count_review' : round(sum_c3['count_review'] / jml_c3, 2)},
        }

        if (centroids == new_centroid) :
            break

        centroids = new_centroid

        # print(centroids)

    # print(data)
    return data

print(clustering(datas))