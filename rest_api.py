from flask import Flask, request, make_response, jsonify, Response, send_file
from flask_cors import CORS
import pandas as pd
import requests
import math
import numpy as np
import random 
import hashlib

app = Flask(__name__)
# Ubah konfigurasi
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'yv1DTocZOOPkoXQOtYfxUbMjSL9mBhwpfXaBw247kC2J3kDNgi3SshrzQzGgCg0'
app.config['SERVER_TIMEOUT'] = 90

CORS(app)

@app.route('/')
@app.route('/index') 
def index() :
    return send_file("index.html")

@app.route('/search', methods=['GET'])
def fetchAPI() :
    #ambil parameter dari user
    keyword = request.args.get("q") 

    # lakukan crawling data
    products = searchProduct(keyword) 
    
    # return response data produk
    return make_response(jsonify(products), 200)


@app.route('/products', methods=['GET'])
def get_products() :
    #ambil parameter dari user
    keyword = request.args.get("search") 

    # lakukan crawling data
    products = crawling_data(keyword) 
    
    # return response data produk
    return make_response(jsonify(products), 200)



@app.route('/clustering', methods=['GET'])
def kmeans_clustering() :
    #ambil parameter dari user
    keyword = request.args.get("search") 

    # lakukan crawling data
    products = crawling_data(keyword) 

    # lakukan clustering 
    clustered_data = clustering(products)

    # return response data hasil clustering
    return make_response(jsonify(clustered_data), 200)

    # Serialize the data to JSON and calculate its hash for ETag
    serialized_data = jsonify(products).get_data()
    etag = hashlib.sha1(serialized_data).hexdigest()

    # Check if client provided 'If-None-Match' header and if it matches the ETag
    if request.headers.get('If-None-Match') == etag:
        response = make_response(jsonify({'status' : 'Not Modified', 'message' : 'Data was the same'}), 304)  # Not Modified
    else:
        response.headers['ETag'] = etag
    return response


# function crawling data dari API
def crawling_data(keyword) :
    results = {}
    products = [] #array kosong untuk menyimpan produk

    # url tujuan 
    url = 'https://gql.tokopedia.com/graphql/SearchQueryV4'

    # set header untuk request 
    header = {
    'authority':'gql.tokopedia.com',
    'accept':'*/*',
    'accept-language':'en-US,en;q=0.9',
    'content-type':'application/json',
    'cookie':'_UUID_NONLOGIN_=04bacffdb33ae7cc9b1d427bbddf171a; _UUID_NONLOGIN_.sig=DVQhA3-ELQQJ9h0SYyVjFHoJFSk; bm_sz=7BF80AE05E5A8AF9664B95B6B2CE2CB3~YAAQBnUyF7+r5qGFAQAAKCdQsRI1Fh/SmyNRRdC9BW4wVU0lmI//2NiLVakPZhTxG0wL2ubZGIjNV6e+kXZ1+5ZqKkK9Fw/Fd+O+T9RZfLp8CXmjV1euh9PVY53K0Ta4CCk1u0Z5EWh1W7Tti6X5jLafWIR+oT1/OgtW3caeEbHOsPQ1EHLHGulXM6KVI3zveFNIMPOUjD8NpeM8Qu5s6zGQIoKdJTLcC/8oqDXy+wClFnEjDZppP084pNd4y/G+c8CSpxAsspL5iuVQVlYRRuwJwE8HYpToOZCsi86tFQjUNjOzLdI=~4272449~3356209; _abck=67ADF742634B2294651C94063EC293ED~0~YAAQBnUyF8ar5qGFAQAAsitQsQkCdgYNV6G8p8uT+aOLF4WEFJEn1yIPMDgyA54iRmSs8IgsBbjhWcRUT1ZGACKO2ODHrZ5oTi8X5dZN5tDx/TwNBUAGKhLKJLUWcC1VB2KHhvD4clCL7uQ4J1mNd5g+9qyDwYVnUvJ4EebQiAsTA6BuyXB0diBrJNOzaw3Ee7WxsSY2/eBVn6PLX+M9fSkvzbjVm5zzyD0aJdY/LmUiZ0w99cb5qp38p9x1woCcn8yvXnCjZpDwpw+uHfaRujN37jTOJlnQz0zKBrX1CIswAGrVHy9wGLjd6Gqwo2qOMAXI02xcsjvTyb3rg90fhcSPJTFDshm1G2FfkcgQp1mgKH+88WYNmd2ownQl6LjOhZnoULvxgiwbqg9gQG0VlVLTnRjaIuqoi/8I4w==~-1~-1~-1; ak_bmsc=DFC7AAF6F9F64270E723EC89908FAC33~000000000000000000000000000000~YAAQBnUyF8er5qGFAQAAojFQsRKFY0XUHN7MfHSDByA9wJyAqK+lXOBbDN4lcRH915Gq1dYUzpCNH7qZCc0MX6BmmYxcbS18HVIdQm2EiYZw1O3EYUs7OBEUadOfqaUa8ihG7VZCAv341wmOHLLxYcxwc508BPH50IneEX1DKlxK0I/cQHhTu8EpVbHZQqr26VrWCOF0Oui9tLcCCPD2oVLq96ptTzSXPzi2go/LndgeetiC4xtTyO65AK7Owx1BcO4T8/C77fVGoeD+LsdQOHCpJ8tjSvdlQoByTj2WR21LDWBwdLR8XOKXtTIAOtLetfCozF6fz2nS75mU8Py7JDoYMaEyHzOmx6Sg+e4vgr39hj2TkJhhY0mWd51+z1EWKJVlh0094vg8GRjh+U3V03NKkmn39oQk12mwImgckxqNvbn2leWZpJ9f+yLRZ1gkBl1j+KFhdw/C4UI3/gkg6VRLlBqXfEB3FtrKIp/789+eVEzXkGQxb0XPCzU=; _SID_Tokopedia_=j6466YAGtp0pdwjx6o3ZvLax0AXvqIatZCtCkJCGgGBvMewHfR1cVZUvt_H0pQMGfjF_o671zjJYno7bObLNo3_uBKI5F2R2rIfRd9R6RQi_7YRpbgfB-pPWvq_hE6RE; DID=c6330112a5306c2292ef00c3384a948935bb5fc3d741651dc80dc4d4e31b663de5b642e3feead70772b2585af3697f42; DID_JS=YzYzMzAxMTJhNTMwNmMyMjkyZWYwMGMzMzg0YTk0ODkzNWJiNWZjM2Q3NDE2NTFkYzgwZGM0ZDRlMzFiNjYzZGU1YjY0MmUzZmVlYWQ3MDc3MmIyNTg1YWYzNjk3ZjQy47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; _gcl_au=1.1.1390752592.1673717104; _UUID_CAS_=11873256-ff6e-4c2e-991a-0912169c4034; _CASE_=21783e133e786068686d6e76783b133e78606a7678363836786078103b313b282e3b7a0a2f293b2e78767839133e78606b6d6c76783635343d786078787678363b2e7860787876782a19357860787876782d133e78606b68686b6a696d6f767829133e78606b6b6f696a6f6d697678290e232a3f78607868327876782d3229786078012106782d3b283f32352f293f05333e0678606b68686b6a696d6f760678293f282c33393f052e232a3f06786006786832067876067805052e232a3f343b373f06786006780d3b283f32352f293f29067827762106782d3b283f32352f293f05333e0678606a760678293f282c33393f052e232a3f06786006786b6f37067876067805052e232a3f343b373f06786006780d3b283f32352f293f2906782707787678360f2a3e786078686a6869776a6b776b6f0e6a6a60686f606a68716a6d606a6a7827; _gid=GA1.2.2077103790.1673717105; __asc=be6737fb185b1504654124dd24e; __auc=be6737fb185b1504654124dd24e; _fbp=fb.1.1673717109190.132615314; _dc_gtm_UA-126956641-6=1; _ga_70947XW48P=GS1.1.1673717104.1.1.1673717202.58.0.0; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.2.1594572164.1673717105; _dc_gtm_UA-9801603-1=1',
    'origin':'https://www.tokopedia.com',
    'referer':'https://www.tokopedia.com',
    'sec-ch-ua':'"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':'"Windows"',
    'sec-fetch-dest':'empty',
    'sec-fetch-mode':'cors',
    'sec-fetch-site':'same-site',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
    'x-device':'default_v3',
    'x-source':'tokopedia-lite',
    'x-tkpd-lite-service':'zeus',
    'x-version':'68ba647',
    }

    # search query 
    initial_query = f'[{{"operationName":"SearchProductQueryV4","variables":{{"params":"device=desktop&navsource=&ob=23&q=${keyword}&related=true&rows=200&safe_search=false&scheme=https&shipping=&source=search&srp_component_id=01.07.00.00&srp_page_id=&srp_page_title=&st=product&start=0&topads_bucket=false&unique_id=1fdabea77fbaf5f1954bdbc40d4a9337&user_addressId=113228966&user_cityId=171&user_districtId=2233&user_id=7773903&user_lat=-6.377643399999999&user_long=106.7621449&user_postCode=16516&user_warehouseId=0&variants="}},"query":"query SearchProductQueryV4($params: String!) {{\\n  ace_search_product_v4(params: $params) {{\\n    header {{\\n      totalData\\n      totalDataText\\n      processTime\\n      responseCode\\n      errorMessage\\n      additionalParams\\n      keywordProcess\\n      componentId\\n      __typename\\n    }}\\n    data {{\\n      banner {{\\n        position\\n        text\\n        imageUrl\\n        url\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      backendFilters\\n      isQuerySafe\\n      ticker {{\\n        text\\n        query\\n        typeId\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      redirection {{\\n        redirectUrl\\n        departmentId\\n        __typename\\n      }}\\n      related {{\\n        position\\n        trackingOption\\n        relatedKeyword\\n        otherRelated {{\\n          keyword\\n          url\\n          product {{\\n            id\\n            name\\n            price\\n            imageUrl\\n            rating\\n            countReview\\n            url\\n            priceStr\\n            wishlist\\n            shop {{\\n              city\\n              isOfficial\\n              isPowerBadge\\n              __typename\\n            }}\\n            ads {{\\n              adsId: id\\n              productClickUrl\\n              productWishlistUrl\\n              shopClickUrl\\n              productViewUrl\\n              __typename\\n            }}\\n            badges {{\\n              title\\n              imageUrl\\n              show\\n              __typename\\n            }}\\n            ratingAverage\\n             labelGroups {{\\n              position\\n              type\\n              title\\n              url\\n              __typename\\n            }}\\n            componentId\\n            __typename\\n          }}\\n          componentId\\n          __typename\\n        }}\\n        __typename\\n      }}\\n      suggestion {{\\n        currentKeyword\\n        suggestion\\n        suggestionCount\\n        instead\\n        insteadCount\\n        query\\n        text\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      products {{\\n        id\\n        name\\n        ads {{\\n          adsId: id\\n          productClickUrl\\n          productWishlistUrl\\n          productViewUrl\\n          __typename\\n        }}\\n        badges {{\\n          title\\n          imageUrl\\n          show\\n          __typename\\n        }}\\n        category: departmentId\\n        categoryBreadcrumb\\n        categoryId\\n        categoryName\\n        countReview\\n        customVideoURL\\n        discountPercentage\\n        gaKey\\n        imageUrl\\n        labelGroups {{\\n          position\\n          title\\n          type\\n          url\\n          __typename\\n        }}\\n        originalPrice\\n        price\\n        priceRange\\n        rating\\n        ratingAverage\\n    count_sold\\n    shop {{\\n          shopId: id\\n          name\\n          url\\n          city\\n          isOfficial\\n          isPowerBadge\\n          __typename\\n        }}\\n        url\\n        wishlist\\n        sourceEngine: source_engine\\n        __typename\\n      }}\\n      violation {{\\n        headerText\\n        descriptionText\\n        imageURL\\n        ctaURL\\n        ctaApplink\\n        buttonText\\n        buttonType\\n        __typename\\n      }}\\n      __typename\\n    }}\\n    __typename\\n  }}\\n}}\\n"}}]'
            
    # ambil response body 
    httpRequest = requests.post(url, headers=header, data=initial_query).json()
    response = httpRequest[0]['data']['ace_search_product_v4']['data']['products']

    # fething dan transform data
    for data in response :
        # ambil atribut data yang dibutuhkan 
        count_sold = data['count_sold'] if data['count_sold'] != '' else 'Terjual 0'
        ratingScore = data['ratingAverage'] if data['ratingAverage'] != '' else '0'
        countReview = data['countReview'] if data['countReview'] != '' else '0.0'
        price = data['price'] if data['price'] != '' else 'Rp0'
                
        count_sold = count_sold.replace('Terjual ', '')
        price = price.replace('.', '')
        price = price.replace('Rp', '')

        products.append(
                {
                    'id' : str(data['id']),
                    'name' : data['name'],
                    'image_url' : data['imageUrl'],
                    'url' : data['url'],
                    'seller' : data['shop']['name'],
                    'location' : data['shop']['city'],
                    'price' : int(price),
                    'sold' : int(count_sold),
                    'rating_score' : float(ratingScore),
                    'count_review' : int(countReview),
                }
            )

    results['total_products'] = len(products)
    results['data'] = products
    return products


# function untuk melakukan k-means clustering 
def clustering(params) :
    data = params #ambil array dari parameter untuk diolah
    response_data = {} # object untk response

    num_cluster = 3 # tentukan jumlah cluster

    # jika data produk lebih dari jumlah k cluster
    if (len(data) > num_cluster) :
        # ambil data secara acak sebagai centroid awal 
        random_data = randomize(data, num_cluster)
    else : # jika kurang dari jumlah k cluster, tampil data
        return {'data' : []}

    # urutkan dari terkecil ke terbesar (Ascending)
    sorted_data = sorted(random_data, key=lambda x: x["sold"] + x["rating_score"] + x["count_review"], reverse=False)

    # inisialisasi centroid awal berdasarkan data yang sudah dipilih acak
    centroids = {
        'c1' : {'sold' : sorted_data[0]['sold'], 'rating_score' : sorted_data[0]['rating_score'], 'count_review' : sorted_data[0]['count_review']},
        'c2' : {'sold' : sorted_data[1]['sold'], 'rating_score' : sorted_data[1]['rating_score'], 'count_review' : sorted_data[1]['count_review']},
        'c3' : {'sold' : sorted_data[2]['sold'], 'rating_score' : sorted_data[1]['rating_score'], 'count_review' : sorted_data[2]['count_review']},
    }

    print(centroids)

    max_iteration = 100 # atur iterasi maksimal
    for iterasi in range(max_iteration) :
        # buat variable untuk menyimpan data hasil cluster sementara (temporary)
        sum_c1 = {'sold' : 0, 'rating_score' : 0, 'count_review' : 0}
        sum_c2 = {'sold' : 0, 'rating_score' : 0, 'count_review' : 0}
        sum_c3 = {'sold' : 0, 'rating_score' : 0, 'count_review' : 0}
        jml_c1 = 0
        jml_c2 = 0
        jml_c3 = 0

        # lakukan iterasi setiap data 
        for i in range(len(data)) :
            # hitung jarak item data dengan setiap centroid (c1 atau c2)
            euq_c1 = math.sqrt((data[i]['sold'] - centroids['c1']['sold']) ** 2 + (data[i]['rating_score'] - centroids['c1']['rating_score']) ** 2 + (data[i]['count_review'] - centroids['c1']['count_review']) ** 2)
            euq_c2 = math.sqrt((data[i]['sold'] - centroids['c2']['sold']) ** 2 + (data[i]['rating_score'] - centroids['c2']['rating_score']) ** 2 + (data[i]['count_review'] - centroids['c2']['count_review']) ** 2)
            euq_c3 = math.sqrt((data[i]['sold'] - centroids['c3']['sold']) ** 2 + (data[i]['rating_score'] - centroids['c3']['rating_score']) ** 2 + (data[i]['count_review'] - centroids['c3']['count_review']) ** 2)

            # tentukan cluster dari setiap data berdasarkan jarak ke pusat centrois terdekat 

            # jika c1 yang paling sedikit
            if (euq_c1 < euq_c2 and euq_c1 < euq_c3) :
                sum_c1['sold'] += data[i]['sold'] 
                sum_c1['rating_score'] += data[i]['rating_score'] 
                sum_c1['count_review'] += data[i]['count_review'] 
                jml_c1 += 1
                data[i]['cluster'] = 1

            # jika c2 yang paling sedikit
            if (euq_c2 < euq_c1 and euq_c2 < euq_c3) :
                sum_c2['sold'] += data[i]['sold'] 
                sum_c2['rating_score'] += data[i]['rating_score'] 
                sum_c2['count_review'] += data[i]['count_review'] 
                jml_c2 += 1
                data[i]['cluster'] = 2

            # jika c3 yang paling sedikit
            if (euq_c3 < euq_c1 and euq_c3 < euq_c2) :
                sum_c3['sold'] += data[i]['sold'] 
                sum_c3['rating_score'] += data[i]['rating_score'] 
                sum_c3['count_review'] += data[i]['count_review'] 
                jml_c3 += 1
                data[i]['cluster'] = 3
            
          
            # data[i]['cluster'] = 0
            # print(data[i])

        
        # hitung centroid baru, jika data milik cluster masih 0, gunakan centroid lama
        c1_sold = round(sum_c1['sold'] / jml_c1, 3) if jml_c1 > 0 else centroids['c1']['sold']
        c1_rating_score =  round(sum_c1['rating_score'] / jml_c1, 3) if jml_c1 > 0 else centroids['c1']['rating_score']
        c1_review_count = round(sum_c1['count_review'] / jml_c1, 3) if jml_c1 > 0 else centroids['c1']['count_review']
        c2_sold = round(sum_c2['sold'] / jml_c2, 3) if jml_c2 > 0 else centroids['c2']['sold']
        c2_rating_score = round(sum_c2['rating_score'] / jml_c2, 3) if jml_c2 > 0 else centroids['c2']['rating_score']
        c2_review_count = round(sum_c2['count_review'] / jml_c2, 3) if jml_c2 > 0 else centroids['c2']['count_review']
        c3_sold = round(sum_c3['sold'] / jml_c3, 3) if jml_c3 > 0 else centroids['c3']['sold']
        c3_rating_score = round(sum_c3['rating_score'] / jml_c3, 3) if jml_c3 > 0 else centroids['c3']['rating_score']
        c3_review_count = round(sum_c3['count_review'] / jml_c3, 3) if jml_c3 > 0 else centroids['c3']['count_review']
        
        # masukan variable ke centroid baru 
        new_centroid = {
            'c1' : {'sold' : c1_sold, 'rating_score': c1_rating_score, 'count_review' : c1_review_count},
            'c2' : {'sold' : c2_sold, 'rating_score': c2_rating_score, 'count_review' : c2_review_count},
            'c3' : {'sold' : c3_sold, 'rating_score': c3_rating_score, 'count_review' : c3_review_count},
        }
        # new_centroid = {
        #     'c1' : {'sold' : round(sum_c1['sold'] / jml_c1, 3), 'rating_score': round(sum_c1['rating_score'] / jml_c1, 3), 'count_review' : round(sum_c1['count_review'] / jml_c1, 3)},
        #     'c2' : {'sold' : round(sum_c2['sold'] / jml_c2, 3), 'rating_score': round(sum_c2['rating_score'] / jml_c2, 3), 'count_review' : round(sum_c2['count_review'] / jml_c2, 3)},
        #     'c3' : {'sold' : round(sum_c3['sold'] / jml_c3, 3), 'rating_score': round(sum_c3['rating_score'] / jml_c3, 3), 'count_review' : round(sum_c3['count_review'] / jml_c3, 3)},
        # }
        # print(jml_c1, jml_c2, jml_c3)

        # jika centroid sudah sama, hentikan perulangan 
        if (centroids == new_centroid) :
            break

        # jika masih belum sama, lanjutkan smpai batas maksimal iterasi dengan mengubah centroid
        centroids = new_centroid

        print(centroids)
        print(iterasi)

    # print(data)
    response_data['centroids'] = centroids
    response_data['cluster_1'] = jml_c1
    response_data['cluster_2'] = jml_c2
    response_data['cluster_3'] = jml_c3
    response_data['data'] = data
    return response_data


# function crawling raw data 
def searchProduct(keyword) :
    results = {}
    productIds = [] #array kosong untuk menyimpan produk
    allProductIds = [] #array kosong untuk menyimpan produk
    products = [] #array kosong untuk menyimpan produk

    # url tujuan 
    url = 'https://gql.tokopedia.com/graphql/SearchQueryV4'

    # set header untuk request 
    header = {
    'authority':'gql.tokopedia.com',
    'accept':'*/*',
    'accept-language':'en-US,en;q=0.9',
    'content-type':'application/json',
    'cookie':'_UUID_NONLOGIN_=04bacffdb33ae7cc9b1d427bbddf171a; _UUID_NONLOGIN_.sig=DVQhA3-ELQQJ9h0SYyVjFHoJFSk; bm_sz=7BF80AE05E5A8AF9664B95B6B2CE2CB3~YAAQBnUyF7+r5qGFAQAAKCdQsRI1Fh/SmyNRRdC9BW4wVU0lmI//2NiLVakPZhTxG0wL2ubZGIjNV6e+kXZ1+5ZqKkK9Fw/Fd+O+T9RZfLp8CXmjV1euh9PVY53K0Ta4CCk1u0Z5EWh1W7Tti6X5jLafWIR+oT1/OgtW3caeEbHOsPQ1EHLHGulXM6KVI3zveFNIMPOUjD8NpeM8Qu5s6zGQIoKdJTLcC/8oqDXy+wClFnEjDZppP084pNd4y/G+c8CSpxAsspL5iuVQVlYRRuwJwE8HYpToOZCsi86tFQjUNjOzLdI=~4272449~3356209; _abck=67ADF742634B2294651C94063EC293ED~0~YAAQBnUyF8ar5qGFAQAAsitQsQkCdgYNV6G8p8uT+aOLF4WEFJEn1yIPMDgyA54iRmSs8IgsBbjhWcRUT1ZGACKO2ODHrZ5oTi8X5dZN5tDx/TwNBUAGKhLKJLUWcC1VB2KHhvD4clCL7uQ4J1mNd5g+9qyDwYVnUvJ4EebQiAsTA6BuyXB0diBrJNOzaw3Ee7WxsSY2/eBVn6PLX+M9fSkvzbjVm5zzyD0aJdY/LmUiZ0w99cb5qp38p9x1woCcn8yvXnCjZpDwpw+uHfaRujN37jTOJlnQz0zKBrX1CIswAGrVHy9wGLjd6Gqwo2qOMAXI02xcsjvTyb3rg90fhcSPJTFDshm1G2FfkcgQp1mgKH+88WYNmd2ownQl6LjOhZnoULvxgiwbqg9gQG0VlVLTnRjaIuqoi/8I4w==~-1~-1~-1; ak_bmsc=DFC7AAF6F9F64270E723EC89908FAC33~000000000000000000000000000000~YAAQBnUyF8er5qGFAQAAojFQsRKFY0XUHN7MfHSDByA9wJyAqK+lXOBbDN4lcRH915Gq1dYUzpCNH7qZCc0MX6BmmYxcbS18HVIdQm2EiYZw1O3EYUs7OBEUadOfqaUa8ihG7VZCAv341wmOHLLxYcxwc508BPH50IneEX1DKlxK0I/cQHhTu8EpVbHZQqr26VrWCOF0Oui9tLcCCPD2oVLq96ptTzSXPzi2go/LndgeetiC4xtTyO65AK7Owx1BcO4T8/C77fVGoeD+LsdQOHCpJ8tjSvdlQoByTj2WR21LDWBwdLR8XOKXtTIAOtLetfCozF6fz2nS75mU8Py7JDoYMaEyHzOmx6Sg+e4vgr39hj2TkJhhY0mWd51+z1EWKJVlh0094vg8GRjh+U3V03NKkmn39oQk12mwImgckxqNvbn2leWZpJ9f+yLRZ1gkBl1j+KFhdw/C4UI3/gkg6VRLlBqXfEB3FtrKIp/789+eVEzXkGQxb0XPCzU=; _SID_Tokopedia_=j6466YAGtp0pdwjx6o3ZvLax0AXvqIatZCtCkJCGgGBvMewHfR1cVZUvt_H0pQMGfjF_o671zjJYno7bObLNo3_uBKI5F2R2rIfRd9R6RQi_7YRpbgfB-pPWvq_hE6RE; DID=c6330112a5306c2292ef00c3384a948935bb5fc3d741651dc80dc4d4e31b663de5b642e3feead70772b2585af3697f42; DID_JS=YzYzMzAxMTJhNTMwNmMyMjkyZWYwMGMzMzg0YTk0ODkzNWJiNWZjM2Q3NDE2NTFkYzgwZGM0ZDRlMzFiNjYzZGU1YjY0MmUzZmVlYWQ3MDc3MmIyNTg1YWYzNjk3ZjQy47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; _gcl_au=1.1.1390752592.1673717104; _UUID_CAS_=11873256-ff6e-4c2e-991a-0912169c4034; _CASE_=21783e133e786068686d6e76783b133e78606a7678363836786078103b313b282e3b7a0a2f293b2e78767839133e78606b6d6c76783635343d786078787678363b2e7860787876782a19357860787876782d133e78606b68686b6a696d6f767829133e78606b6b6f696a6f6d697678290e232a3f78607868327876782d3229786078012106782d3b283f32352f293f05333e0678606b68686b6a696d6f760678293f282c33393f052e232a3f06786006786832067876067805052e232a3f343b373f06786006780d3b283f32352f293f29067827762106782d3b283f32352f293f05333e0678606a760678293f282c33393f052e232a3f06786006786b6f37067876067805052e232a3f343b373f06786006780d3b283f32352f293f2906782707787678360f2a3e786078686a6869776a6b776b6f0e6a6a60686f606a68716a6d606a6a7827; _gid=GA1.2.2077103790.1673717105; __asc=be6737fb185b1504654124dd24e; __auc=be6737fb185b1504654124dd24e; _fbp=fb.1.1673717109190.132615314; _dc_gtm_UA-126956641-6=1; _ga_70947XW48P=GS1.1.1673717104.1.1.1673717202.58.0.0; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.2.1594572164.1673717105; _dc_gtm_UA-9801603-1=1',
    'origin':'https://www.tokopedia.com',
    'referer':'https://www.tokopedia.com',
    'sec-ch-ua':'"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':'"Windows"',
    'sec-fetch-dest':'empty',
    'sec-fetch-mode':'cors',
    'sec-fetch-site':'same-site',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
    'x-device':'default_v3',
    'x-source':'tokopedia-lite',
    'x-tkpd-lite-service':'zeus',
    'x-version':'68ba647',
    }

    # query = f'[{{"operationName":"SearchQueryV4","variables":{{"sid":"9351716","page":1,"perPage":80,"etalaseId":"etalase","sort":1,"user_districtId":"2274","user_cityId":"176","user_lat":"","user_long":""}},"query":"query SearchQueryV4($sid: String\u0021, $page: Int, $perPage: Int, $keyword: String, $etalaseId: String, $sort: Int, $user_districtId: String, $user_cityId: String, $user_lat: String, $user_long: String) {{\\n  GetShopProduct(shopID: $sid, filter: {{page: $page, perPage: $perPage, fkeyword: $keyword, fmenu: $etalaseId, sort: $sort, user_districtId: $user_districtId, user_cityId: $user_cityId, user_lat: $user_lat, user_long: $user_long}}) {{\\n    status\\n    errors\\n    links {{\\n      prev\\n      next\\n      __typename\\n    }}\\n    data {{\\n      name\\n      product_url\\n      product_id\\n      price {{\\n        text_idr\\n        __typename\\n      }}\\n      primary_image {{\\n        original\\n        thumbnail\\n        resize300\\n        __typename\\n      }}\\n      flags {{\\n        isSold\\n        isPreorder\\n        isWholesale\\n        isWishlist\\n        __typename\\n      }}\\n      campaign {{\\n        discounted_percentage\\n        original_price_fmt\\n        start_date\\n        end_date\\n        __typename\\n      }}\\n      label {{\\n        color_hex\\n        content\\n        __typename\\n      }}\\n      label_groups {{\\n        position\\n        title\\n        type\\n        url\\n        __typename\\n      }}\\n      badge {{\\n        title\\n        image_url\\n        __typename\\n      }}\\n      stats {{\\n        reviewCount\\n        rating\\n        __typename\\n      }}\\n      category {{\\n        id\\n        __typename\\n      }}\\n      __typename\\n    }}\\n    __typename\\n  }}\\n}}\\n"}}]'
    
    max_count_sold = 0
    max_count_review = 0

    # search query 
    initial_query = f'[{{"operationName":"SearchProductQueryV4","variables":{{"params":"device=desktop&navsource=&ob=23&q=${keyword}&related=true&rows=200&safe_search=false&scheme=https&shipping=&source=search&srp_component_id=01.07.00.00&srp_page_id=&srp_page_title=&st=product&start=0&topads_bucket=false&unique_id=1fdabea77fbaf5f1954bdbc40d4a9337&user_addressId=113228966&user_cityId=171&user_districtId=2233&user_id=7773903&user_lat=-6.377643399999999&user_long=106.7621449&user_postCode=16516&user_warehouseId=0&variants="}},"query":"query SearchProductQueryV4($params: String!) {{\\n  ace_search_product_v4(params: $params) {{\\n    header {{\\n      totalData\\n      totalDataText\\n      processTime\\n      responseCode\\n      errorMessage\\n      additionalParams\\n      keywordProcess\\n      componentId\\n      __typename\\n    }}\\n    data {{\\n      banner {{\\n        position\\n        text\\n        imageUrl\\n        url\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      backendFilters\\n      isQuerySafe\\n      ticker {{\\n        text\\n        query\\n        typeId\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      redirection {{\\n        redirectUrl\\n        departmentId\\n        __typename\\n      }}\\n      related {{\\n        position\\n        trackingOption\\n        relatedKeyword\\n        otherRelated {{\\n          keyword\\n          url\\n          product {{\\n            id\\n            name\\n            price\\n            imageUrl\\n            rating\\n            countReview\\n            url\\n            priceStr\\n            wishlist\\n            shop {{\\n              city\\n              isOfficial\\n              isPowerBadge\\n              __typename\\n            }}\\n            ads {{\\n              adsId: id\\n              productClickUrl\\n              productWishlistUrl\\n              shopClickUrl\\n              productViewUrl\\n              __typename\\n            }}\\n            badges {{\\n              title\\n              imageUrl\\n              show\\n              __typename\\n            }}\\n            ratingAverage\\n             labelGroups {{\\n              position\\n              type\\n              title\\n              url\\n              __typename\\n            }}\\n            componentId\\n            __typename\\n          }}\\n          componentId\\n          __typename\\n        }}\\n        __typename\\n      }}\\n      suggestion {{\\n        currentKeyword\\n        suggestion\\n        suggestionCount\\n        instead\\n        insteadCount\\n        query\\n        text\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      products {{\\n        id\\n        name\\n        ads {{\\n          adsId: id\\n          productClickUrl\\n          productWishlistUrl\\n          productViewUrl\\n          __typename\\n        }}\\n        badges {{\\n          title\\n          imageUrl\\n          show\\n          __typename\\n        }}\\n        category: departmentId\\n        categoryBreadcrumb\\n        categoryId\\n        categoryName\\n        countReview\\n        customVideoURL\\n        discountPercentage\\n        gaKey\\n        imageUrl\\n        labelGroups {{\\n          position\\n          title\\n          type\\n          url\\n          __typename\\n        }}\\n        originalPrice\\n        price\\n        priceRange\\n        rating\\n        ratingAverage\\n    count_sold\\n    shop {{\\n          shopId: id\\n          name\\n          url\\n          city\\n          isOfficial\\n          isPowerBadge\\n          __typename\\n        }}\\n        url\\n        wishlist\\n        sourceEngine: source_engine\\n        __typename\\n      }}\\n      violation {{\\n        headerText\\n        descriptionText\\n        imageURL\\n        ctaURL\\n        ctaApplink\\n        buttonText\\n        buttonType\\n        __typename\\n      }}\\n      __typename\\n    }}\\n    __typename\\n  }}\\n}}\\n"}}]'
            
    # ambil response body 
    httpRequest = requests.post(url, headers=header, data=initial_query).json()
    response = httpRequest
    # response = httpRequest[0]['data']['ace_search_product_v4']['data']

    return response


@app.route('/privacy-policy') 
def privacy_policy() :
    return send_file("privacy-policies.html")


def randomize(array, length) :
    random_data = random.sample(array, length)
    if (random_data[0]["sold"] != random_data[1]["sold"] and random_data[1]["sold"] != random_data[2]["sold"] and random_data[0]["sold"] != random_data[2]["sold"]) :
        return random_data
    else :
        return randomize(array, length)

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=80)


