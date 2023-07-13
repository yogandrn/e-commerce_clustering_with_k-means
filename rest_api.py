from flask import Flask, request, make_response, jsonify
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/index') 
def index() :
    return 'Hello, World!'

@app.route('/products', methods=['GET'])
def get_products() :
    
    products = []
    url = 'https://gql.tokopedia.com/graphql/SearchQueryV4'
    keyword = request.args.get("search")
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
    for i in range (0, 2) :
        initial_query = f'[{{"operationName":"SearchProductQueryV4","variables":{{"params":"device=desktop&navsource=&ob=23&page=${i}&q=${keyword}&related=true&rows=60&safe_search=false&scheme=https&shipping=&source=search&srp_component_id=01.07.00.00&srp_page_id=&srp_page_title=&st=product&start=0&topads_bucket=true&unique_id=1fdabea77fbaf5f1954bdbc40d4a9337&user_addressId=113228966&user_cityId=171&user_districtId=2233&user_id=7773903&user_lat=-6.377643399999999&user_long=106.7621449&user_postCode=16516&user_warehouseId=0&variants="}},"query":"query SearchProductQueryV4($params: String!) {{\\n  ace_search_product_v4(params: $params) {{\\n    header {{\\n      totalData\\n      totalDataText\\n      processTime\\n      responseCode\\n      errorMessage\\n      additionalParams\\n      keywordProcess\\n      componentId\\n      __typename\\n    }}\\n    data {{\\n      banner {{\\n        position\\n        text\\n        imageUrl\\n        url\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      backendFilters\\n      isQuerySafe\\n      ticker {{\\n        text\\n        query\\n        typeId\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      redirection {{\\n        redirectUrl\\n        departmentId\\n        __typename\\n      }}\\n      related {{\\n        position\\n        trackingOption\\n        relatedKeyword\\n        otherRelated {{\\n          keyword\\n          url\\n          product {{\\n            id\\n            name\\n            price\\n            imageUrl\\n            rating\\n            countReview\\n            url\\n            priceStr\\n            wishlist\\n            shop {{\\n              city\\n              isOfficial\\n              isPowerBadge\\n              __typename\\n            }}\\n            ads {{\\n              adsId: id\\n              productClickUrl\\n              productWishlistUrl\\n              shopClickUrl\\n              productViewUrl\\n              __typename\\n            }}\\n            badges {{\\n              title\\n              imageUrl\\n              show\\n              __typename\\n            }}\\n            ratingAverage\\n             labelGroups {{\\n              position\\n              type\\n              title\\n              url\\n              __typename\\n            }}\\n            componentId\\n            __typename\\n          }}\\n          componentId\\n          __typename\\n        }}\\n        __typename\\n      }}\\n      suggestion {{\\n        currentKeyword\\n        suggestion\\n        suggestionCount\\n        instead\\n        insteadCount\\n        query\\n        text\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      products {{\\n        id\\n        name\\n        ads {{\\n          adsId: id\\n          productClickUrl\\n          productWishlistUrl\\n          productViewUrl\\n          __typename\\n        }}\\n        badges {{\\n          title\\n          imageUrl\\n          show\\n          __typename\\n        }}\\n        category: departmentId\\n        categoryBreadcrumb\\n        categoryId\\n        categoryName\\n        countReview\\n        customVideoURL\\n        discountPercentage\\n        gaKey\\n        imageUrl\\n        labelGroups {{\\n          position\\n          title\\n          type\\n          url\\n          __typename\\n        }}\\n        originalPrice\\n        price\\n        priceRange\\n        rating\\n        ratingAverage\\n    count_sold\\n    shop {{\\n          shopId: id\\n          name\\n          url\\n          city\\n          isOfficial\\n          isPowerBadge\\n          __typename\\n        }}\\n        url\\n        wishlist\\n        sourceEngine: source_engine\\n        __typename\\n      }}\\n      violation {{\\n        headerText\\n        descriptionText\\n        imageURL\\n        ctaURL\\n        ctaApplink\\n        buttonText\\n        buttonType\\n        __typename\\n      }}\\n      __typename\\n    }}\\n    __typename\\n  }}\\n}}\\n"}}]'
        req = requests.post(url, headers=header, data=initial_query).json()
        response = req[0]['data']['ace_search_product_v4']['data']['products']
        # response.forE
        for j in response :
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

            # print(j)

            print(
                    j['id'],
                    j['name'],
                    j['imageUrl'], 
                    j['url'], 
                    j['shop']['name'],
                    j['shop']['city'],
                    int(price),
                    int(countSold),
                    # countSold,
                    float(ratingScore),
                    # ratingScore,
                    int(countReview),
            )

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
                    'rating' : float(ratingScore),
                    # 'rating' : ratingScore,
                    'countReview' : int(countReview),
                    'cluster' : 0,
                }
            )
            
            # products.append(response)


    
    return make_response(jsonify(products), 200)

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=80)
