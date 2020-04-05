from yelp_lambda.dispatcher_types import (
    ReviewsDispatcherRequest,
    StatusesDispatcherRequest,
)


class DispatcherInput:
    REVIEWS = ReviewsDispatcherRequest(
        user_id="5prk8CtPPBHNpa6BOja2ug",
        urls=[
            "https://www.yelp.com/user_details_reviews_self?rec_pagestart=0&userid=5prk8CtPPBHNpa6BOja2ug",
            "https://www.yelp.com/user_details_reviews_self?rec_pagestart=10&userid=5prk8CtPPBHNpa6BOja2ug",
            "https://www.yelp.com/user_details_reviews_self?rec_pagestart=20&userid=5prk8CtPPBHNpa6BOja2ug",
        ],
    )

    STATUSES = StatusesDispatcherRequest(
        user_id="5prk8CtPPBHNpa6BOja2ug",
        biz_ids_to_review_ids={
            "chick-fil-a-westminster-5": "Pg6aIJBjs8CNVJvUtUBPmg",
            "walmart-huntington-beach-2": "OpvxuBt1ChGi9rfLwTAgMA",
            "total-wine-and-more-huntington-beach-2": "SLe2OO-06aM1GbA6TJiLJw",
            "david-l-baker-memorial-golf-center-fountain-valley": "VOBaprFuLryTvTvyGjIjCQ",
            "chipotle-mexican-grill-fountain-valley-3": "dTxo85w-ghJCcnubgCtV6g",
            "in-n-out-burger-cerritos": "aP03ALU4ryjJ-2rn6OK0lA",
            "la-mirada-golf-course-la-mirada": "LdsYmD1P0LzydhrKHHT73A",
            "bunker21-artesia": "CPx8tpbxRHrofwc5PdZ5Kw",
            "aroma-golf-range-los-angeles": "sUKuLnHWVLrlsJtU2-4i0w",
            "han-yang-buena-park": "3-nA8CTpJVUz0Xubin1ORQ",
            "mcdonalds-la-palma-4": "_-7pO5Jq5gmS-4ZhdptqHw",
            "aloha-family-billiards-buena-park": "U_yiTX51HWo78jOaV0pIxQ",
            "kabab-crush-artesia-4": "apHy99vF1l5XHI8Hxmy9Ow",
            "kaju-soft-tofu-restaurant-buena-park": "-H_0dEdwpe2mhdYb_wWMrA",
            "iron-wood-nine-golf-course-cerritos": "blSV3JFheTbvc6lsuuAfBQ",
            "chipotle-mexican-grill-cerritos-9": "ofWhnV6m26kMyCpUjT56XA",
            "yoko-buena-park": "MS1f3LaFfHeh5kcF2qt-1A",
            "myung-dong-kyoja-anaheim-5": "X0_-zEk0_CKj24wEEoau9A",
            "roger-dunn-golf-shops-seal-beach-3": "Ve3BLwnfMTXZMwCViW-MLg",
            "thai-addict-cuisine-buena-park-2": "ZfHJEeZFKTPFwAJGMYiXrA",
            "chick-fil-a-cerritos": "dy_dxor2rVhpNuSUrrBw0w",
            "panda-express-cerritos": "-eb-SRIXvQ_tyJKFldJMyw",
            "in-n-out-burger-la-mirada": "MD1zzz0eP0GgRLfDqzS7og",
            "jangmo-jip-la-palma": "1TFeSFZdJts8Vd-x5XV3rA",
            "las-galas-los-angeles": "q2pionpcY_-WZPwSWelTFw",
        },
    )
