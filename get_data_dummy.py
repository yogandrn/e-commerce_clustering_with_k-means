import requests
import pandas as panda
import math
import random

# function crawling data dari API
def crawling_data(keyword) :
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

    # looping dari halaman 1 - 10
    for i in range (0, 5) :
        # search query 
        initial_query = f'[{{"operationName":"SearchProductQueryV4","variables":{{"params":"device=desktop&navsource=&ob=23&page=${i}&q=${keyword}&related=true&rows=60&safe_search=false&scheme=https&shipping=&source=search&srp_component_id=01.07.00.00&srp_page_id=&srp_page_title=&st=product&start=0&topads_bucket=true&unique_id=1fdabea77fbaf5f1954bdbc40d4a9337&user_addressId=113228966&user_cityId=171&user_districtId=2233&user_id=7773903&user_lat=-6.377643399999999&user_long=106.7621449&user_postCode=16516&user_warehouseId=0&variants="}},"query":"query SearchProductQueryV4($params: String!) {{\\n  ace_search_product_v4(params: $params) {{\\n    header {{\\n      totalData\\n      totalDataText\\n      processTime\\n      responseCode\\n      errorMessage\\n      additionalParams\\n      keywordProcess\\n      componentId\\n      __typename\\n    }}\\n    data {{\\n      banner {{\\n        position\\n        text\\n        imageUrl\\n        url\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      backendFilters\\n      isQuerySafe\\n      ticker {{\\n        text\\n        query\\n        typeId\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      redirection {{\\n        redirectUrl\\n        departmentId\\n        __typename\\n      }}\\n      related {{\\n        position\\n        trackingOption\\n        relatedKeyword\\n        otherRelated {{\\n          keyword\\n          url\\n          product {{\\n            id\\n            name\\n            price\\n            imageUrl\\n            rating\\n            countReview\\n            url\\n            priceStr\\n            wishlist\\n            shop {{\\n              city\\n              isOfficial\\n              isPowerBadge\\n              __typename\\n            }}\\n            ads {{\\n              adsId: id\\n              productClickUrl\\n              productWishlistUrl\\n              shopClickUrl\\n              productViewUrl\\n              __typename\\n            }}\\n            badges {{\\n              title\\n              imageUrl\\n              show\\n              __typename\\n            }}\\n            ratingAverage\\n             labelGroups {{\\n              position\\n              type\\n              title\\n              url\\n              __typename\\n            }}\\n            componentId\\n            __typename\\n          }}\\n          componentId\\n          __typename\\n        }}\\n        __typename\\n      }}\\n      suggestion {{\\n        currentKeyword\\n        suggestion\\n        suggestionCount\\n        instead\\n        insteadCount\\n        query\\n        text\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      products {{\\n        id\\n        name\\n        ads {{\\n          adsId: id\\n          productClickUrl\\n          productWishlistUrl\\n          productViewUrl\\n          __typename\\n        }}\\n        badges {{\\n          title\\n          imageUrl\\n          show\\n          __typename\\n        }}\\n        category: departmentId\\n        categoryBreadcrumb\\n        categoryId\\n        categoryName\\n        countReview\\n        customVideoURL\\n        discountPercentage\\n        gaKey\\n        imageUrl\\n        labelGroups {{\\n          position\\n          title\\n          type\\n          url\\n          __typename\\n        }}\\n        originalPrice\\n        price\\n        priceRange\\n        rating\\n        ratingAverage\\n    count_sold\\n    shop {{\\n          shopId: id\\n          name\\n          url\\n          city\\n          isOfficial\\n          isPowerBadge\\n          __typename\\n        }}\\n        url\\n        wishlist\\n        sourceEngine: source_engine\\n        __typename\\n      }}\\n      violation {{\\n        headerText\\n        descriptionText\\n        imageURL\\n        ctaURL\\n        ctaApplink\\n        buttonText\\n        buttonType\\n        __typename\\n      }}\\n      __typename\\n    }}\\n    __typename\\n  }}\\n}}\\n"}}]'
        
        # ambil response body 
        req = requests.post(url, headers=header, data=initial_query).json()
        response = req[0]['data']['ace_search_product_v4']['data']['products']
        
        # fething dan transform data
        for j in response :
            # set default value 0 jika data not found 
            sold = 'Terjual 0'
            rating = '0'
            countReview = 0
            countReview = j.get('countReview', 0)
            ratingScore = j.get('ratingAverage', '0')
            count_sold = j.get('count_sold', '0')

            if (count_sold == '') : count_sold = 'Terjual 0'
            if (ratingScore == '') : ratingScore = '0'
            
            price = j['price']

            # countSold = count_sold[8:]
            countSold = count_sold.replace('Terjual ', '')
            price = price.replace('.', '')
            price = price.replace('Rp', '')

            # tambahakan data ke dalam array 
            products.append(
                {
                    'id' : j['id'],
                    'name' : j['name'],
                    'imageurl' : j['imageUrl'],
                    'url' : j['url'],
                    'seller' : j['shop']['name'],
                    'location' : j['shop']['city'],
                    'price' : int(price),
                    # 'sold' :  countSold,
                    'sold' : int(countSold),
                    'rating_score' : float(ratingScore),
                    # 'rating' : ratingScore,
                    'count_review' : int(countReview),
                    'cluster' : 0,
                }
            )

    # return data 
    return products


# function untuk melakukan k-means clustering 
def clustering(keyword, filename) :

    data = crawling_data(keyword) #ambil array dari parameter
    hasil_cluster = [] # untuk menampung hasil cluster sementara

    num_cluster = 3 # tentukan jumlah cluster

    # inisialisasi titik pusat cluster / centroid 
    # centroids = {
    #     'c1' : {'sold' : 0, 'rating_score': 0, 'count_review' : 0},
    #     'c2' : {'sold' : 250, 'rating_score': , 'count_review' : 100},
    #     'c3' : {'sold' : 500, 'rating_score': 5, 'count_review' : 250},
    # }

    centroids = {
        'c1' : {'sold' : random.randint(0, 10), 'rating_score': 4.5, 'count_review' : random.randint(0, 10)},
        'c2' : {'sold' : random.randint(100, 200), 'rating_score': 4.75, 'count_review' : random.randint(100, 200)},
        'c3' : {'sold' : random.randint(500, 600), 'rating_score': 5, 'count_review' : random.randint(500, 600)},
    }

    print(centroids)

    max_iteration = 100 # atur iterasi maksimal

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
            # jika c1 yang paling sedikit
            if (c1 < c2 and c1 < c3) :
                sum_c1['sold'] += data[i]['sold'] 
                sum_c1['rating_score'] += data[i]['rating_score'] 
                sum_c1['count_review'] += data[i]['count_review'] 
                jml_c1 += 1
                data[i]['cluster'] = 1

            # jika c2 yang paling sedikit
            if (c2 < c1 and c2 < c3) :
                sum_c2['sold'] += data[i]['sold'] 
                sum_c2['rating_score'] += data[i]['rating_score'] 
                sum_c2['count_review'] += data[i]['count_review'] 
                jml_c2 += 1
                data[i]['cluster'] = 2

            # jika c3 yang paling sedikit
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
            'c1' : {'sold' : round(sum_c1['sold'] / jml_c1, 3), 'rating_score': round(sum_c1['rating_score'] / jml_c1, 3), 'count_review' : round(sum_c1['count_review'] / jml_c1, 3)},
            'c2' : {'sold' : round(sum_c2['sold'] / jml_c2, 3), 'rating_score': round(sum_c2['rating_score'] / jml_c2, 3), 'count_review' : round(sum_c2['count_review'] / jml_c2, 3)},
            'c3' : {'sold' : round(sum_c3['sold'] / jml_c3, 3), 'rating_score': round(sum_c3['rating_score'] / jml_c3, 3), 'count_review' : round(sum_c3['count_review'] / jml_c3, 3)},
        }

        # jika centroid sudah sama, hentikan perulangan 
        if (centroids == new_centroid) :
            break

        # jika masih belum sama, lanjutkan smpai batas maksimal iterasi
        centroids = new_centroid

        print(centroids)

    # menyimpan ke dalam excel 
    dataPrint = panda.DataFrame(data)

    dataPrint.to_excel(filename, index=False)
    print('Data Tersimpan')

    return data


# jalankan method clustering 
clustering('handphone', '02_handphone.xlsx')