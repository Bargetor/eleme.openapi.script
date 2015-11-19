 # -*- coding: utf-8 -*-
import urllib, hashlib, httplib, time, mimetypes
from cgi import FieldStorage
import json
import sys
import os
import binascii
import eleme_application_set
import base
reload(sys)
sys.setdefaultencoding('utf-8')

logger = base.get_logger(os.path.basename(__file__))

text_geo = [{"geometry": {"type": "Polygon", "coordinates": [[[121.381303, 31.243521], [121.380938, 31.242778], [121.380735, 31.242421], [121.380627, 31.242196], [121.380541, 31.24204], [121.38037, 31.241664], [121.380284, 31.241499], [121.38023, 31.241389], [121.380166, 31.241269], [121.380134, 31.241178], [121.379951, 31.24093], [121.379748, 31.24071], [121.379565, 31.240499], [121.379426, 31.24037], [121.379297, 31.240205], [121.379104, 31.239967], [121.378911, 31.239747], [121.378696, 31.239471], [121.377881, 31.238554], [121.377291, 31.237848], [121.376561, 31.237077], [121.37566, 31.236013], [121.375123, 31.235435], [121.374684, 31.234967], [121.374265, 31.234499], [121.374126, 31.23427], [121.374072, 31.234105], [121.374029, 31.233912], [121.3739, 31.233334], [121.373782, 31.232738], [121.373675, 31.232334], [121.3736, 31.231967], [121.373342, 31.230821], [121.374319, 31.23038], [121.375542, 31.22983], [121.377065, 31.229133], [121.377913, 31.228775], [121.378857, 31.228545], [121.37964, 31.228399], [121.381539, 31.228096], [121.382891, 31.227903], [121.38361, 31.229628], [121.384661, 31.231977], [121.385713, 31.23449], [121.386753, 31.236527], [121.386764, 31.236554], [121.387183, 31.237426], [121.387504, 31.238095], [121.388213, 31.239499], [121.388695, 31.24049], [121.387912, 31.240701], [121.386839, 31.240985], [121.385766, 31.241315], [121.385251, 31.241389], [121.383728, 31.24226], [121.381582, 31.243361], [121.381679, 31.243297], [121.381303, 31.243521]]]}, "type": "Feature", "properties": {"delivery_price": 20}}]


class ElemeAPIContextRequester(object):
    """docstring for ElemeAPIContextRequester"""
    def __init__(self, consumer_key, consumer_secret):
        super(ElemeAPIContextRequester, self).__init__()
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.base_url_path = 'v2.openapi.ele.me'
        #test
        # self.base_url_path = 'v2.rhyme.alpha.elenet.me'


    def base_request(self, path_url, url_params = {}, params  = {}):
        return self.base_request_get(path_url, params)

    def base_request_get(self, path_url, url_params = {}, params = {}):
        all_params = dict(url_params, **params)
        request_path_url = self.__build_sig_request_url(path_url, all_params, url_params = url_params)
        response = self.__get(request_path_url, params)
        return response

    def base_request_put(self, path_url, url_params = {}, put_params = {}):
        all_params = dict(url_params, **put_params)
        request_path_url = self.__build_sig_request_url(path_url, all_params)
        response = self.__put(request_path_url, put_params, self.__get_base_headers())
        return response

    def base_request_post(self, path_url, url_params = {}, post_params = {}):
        all_params = dict(url_params, **post_params)
        request_path_url = self.__build_sig_request_url(path_url, all_params)
        response = self.__post(request_path_url, post_params, self.__get_base_headers())
        return response

    def base_request_delete(self, path_url, url_params = {}, delete_params = {}):
        all_params = dict(url_params, **delete_params)
        request_path_url = self.__build_sig_request_url(path_url, all_params)
        response = self.__delete(request_path_url, delete_params, self.__get_base_headers())
        return response

    def base_request_upload(self, path_url, url_params = {}, upload_params = {}):
        request_path_url = self.__build_sig_request_url(path_url, url_params)
        headers = self.__get_base_headers()
        content_type, body = self.__encode_multipart_formdata('file', upload_params['file'])

        headers['Content-Type'] = content_type

        connection = self.__get_http_connection()
        # body = urllib.urlencode(params)
        try:
            connection.request('POST', url = request_path_url, body = body, headers = headers)
            response = connection.getresponse().read()
            logger.info('the {} response is {}'.format(path_url, response))
            return json.loads(response)
        except Exception, e:
            logger.error(e)
            return self.base_request_upload(path_url, url_params, upload_params)


    def download(self, url, download_path, file_name):
        response = urllib.urlopen(url)
        download_file = open("{}/{}".format(download_path, file_name), 'wb')
        download_file.write(response.read())
        download_file.close()
        logger.info("download url:{} to {}/{}".format(url, download_path, file_name))

    def __encode_multipart_formdata(self, file_name, file_data):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (file_name, file_name))
        L.append('Content-Type: %s' % self.__get_content_type(file_name))
        L.append('')
        L.append(file_data)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def __get_content_type(self, file_name):
        return mimetypes.guess_type(file_name)[0] or 'application/octet-stream'

    def gen_sig(self, path_url, params, consumer_secret):
        params = self.concat_params(params)

        url = u'{}?{}{}'.format(path_url, params, consumer_secret)

        to_hash = url.encode('utf-8').encode('hex')

        sig = hashlib.new('sha1', to_hash).hexdigest()

        # logger.info('the path_url is : {} and params is : {} and to_hash is : {} and sig is : {}'.format(path_url, params, to_hash, sig))
        return sig

    def concat_params(self, params):
        pairs = []
        for key in sorted(params):

            val = params[key]
            if isinstance(val, unicode):
                val = urllib.quote_plus(val.encode("utf-8"))
            elif isinstance(val, str):
                val = urllib.quote_plus(val)


            if not isinstance(val, FieldStorage):
                pairs.append("{}={}".format(key, val))

        return '&'.join(pairs)

    def __build_sig_request_url(self, path_url, params, url_params = {}):
        url = 'http://{}{}'.format(self.base_url_path, path_url)
        url_params = dict(self.__get_base_params(), **url_params)
        params = dict(params, **url_params)
        sig = self.gen_sig(url, params, self.consumer_secret)
        url_params['sig'] = sig
        request_path_url = '{}?{}'.format(path_url, self.concat_params(url_params))
        return request_path_url

    def __get_http_connection(self):
        return httplib.HTTPConnection(self.base_url_path, strict = False, timeout = 10)

    def __get_base_params(self):
        params = {}
        params['consumer_key'] = self.consumer_key
        params['timestamp'] = time.time().__long__()
        return params

    def __get_base_headers(self):
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return headers

    def __get(self, url, params = {}, headers = {}):
        return self.__open_url(url, 'GET', params, headers)

    def __put(self, url, params, headers):
        return self.__open_url(url, 'PUT', params, headers)

    def __post(self, url, params, headers):
        return self.__open_url(url, 'POST', params, headers)

    def __delete(self, url, params, headers):
        return self.__open_url(url, 'DELETE', params, headers)


    def __open_url(self, url, method = 'GET', params = {}, headers = {}):
        connection = self.__get_http_connection()
        body = urllib.urlencode(params)
        logger.info('the {} request url is : {} , and body is {}'.format(method, url, body))
        try:
            connection.request(method, url = url, body = body, headers = headers)
            response = connection.getresponse().read()
            logger.info('the {} {} response is {} : '.format(method, url, response))
            return json.loads(response)
        except Exception, e:
            #当做重试一次吧
            logger.error(e)
            return self.__open_url(url, method, params, headers)

        # return response



class ElemeOrderRequester(object):
    """docstring for ElemeOrderRequester"""

    def __init__(self, context_requester):
        super(ElemeOrderRequester, self).__init__()
        self.context_requester = context_requester

    def get_new_orders(self, restaurant_id = None):
        request_path_url = '/order/new/'
        params = {}
        if restaurant_id :
            params['restaurant_id'] = restaurant_id

        return self.context_requester.base_request_get(request_path_url, params)

    def get_order_info(self, eleme_order_id, is_use_tp_id = False):
        if not eleme_order_id:
            return None

        request_path_url = "/order/{}/"

        params = {}
        if is_use_tp_id:
            params['tp_id'] = 1

        request_path_url = request_path_url.format(eleme_order_id)
        return self.context_requester.base_request_get(request_path_url, url_params = params)

    def change_order_status(self, eleme_order_id, status, reason = None):
        if not eleme_order_id:
            return None

        request_path_url = '/order/{}/status/'

        request_path_url = request_path_url.format(eleme_order_id)
        params = {}
        params['status'] = status
        if reason:
            params['reason'] = reason

        return self.context_requester.base_request_put(request_path_url, put_params = params)

    def confirm_order(self, eleme_order_id):
        return self.change_order_status(eleme_order_id, 2)

    def cancel_order(self, eleme_order_id, reason):
        return self.change_order_status(eleme_order_id, -1, reason)


class ElemeRestaurantRequester(object):
    """docstring for ElemeRestaurantRequester"""
    def __init__(self, context_requester, restaurant_id):
        super(ElemeRestaurantRequester, self).__init__()
        self.context_requester = context_requester
        self.restaurant_id = restaurant_id

    def get_all_categories(self):
        request_path_url = '/restaurant/{}/food_categories/'
        if not self.restaurant_id:
            return None
        request_path_url = request_path_url.format(self.restaurant_id)
        return self.context_requester.base_request(request_path_url)

    def get_restaurant_info(self):
        request_path_url = '/restaurant/{}/'
        if not self.restaurant_id:
            return None
        request_path_url = request_path_url.format(self.restaurant_id)

        return self.context_requester.base_request_get(request_path_url)

    def update_restaurant_name(self, new_name):
        params = {}
        params['name'] = new_name

        return self.update_restaurant_info(params)

    def update_restaurant_open_time(self, open_time):
        params = {}
        params['open_time'] = open_time

        return self.update_restaurant_info(params)

    def update_restaurant_address(self, address):
        params = {}
        params['address_text'] = address

        return self.update_restaurant_info(params)


    def update_restaurant_info(self, params):
        request_path_url = "/restaurant/{}/info/"

        if not self.restaurant_id:
            return None

        request_path_url = request_path_url.format(self.restaurant_id)
        return self.context_requester.base_request_put(request_path_url, put_params = params)

    def open_restaurant(self):
        return self.update_restaurant_status(1)

    def close_restaurant(self):
        return self.update_restaurant_status(0)

    def update_restaurant_phone(self, phone):
        if not phone:
            return None
        params = {}
        params['phone'] = phone
        return self.update_restaurant_info(params)


    def update_restaurant_status(self, status):
        if not self.restaurant_id:
            return None

        request_path_url = "/restaurant/{}/business_status/"

        request_path_url = request_path_url.format(self.restaurant_id)
        params = {}
        params['is_open'] = status

        return self.context_requester.base_request_put(request_path_url, put_params = params)

    def binding(self, tp_restaurant_id):
        if not self.restaurant_id or not tp_restaurant_id:
            return
        request_path_url = "/restaurant/binding/"

        params = {}
        params['restaurant_id'] = self.restaurant_id
        params['tp_restaurant_id'] = tp_restaurant_id

        return self.context_requester.base_request_post(request_path_url, post_params = params)

    def rebinding(self, tp_restaurant_id):
        if not self.restaurant_id or not tp_restaurant_id:
            return
        request_path_url = "/restaurant/binding/"

        params = {}
        params['restaurant_id'] = self.restaurant_id
        params['tp_restaurant_id'] = tp_restaurant_id

        return self.context_requester.base_request_put(request_path_url, put_params = params)


    def get_restaurant_by_tp_id(self, tp_restaurant_id):
        if not tp_restaurant_id:
            return
        request_path_url = "/restaurant/binding/"

        params = {}
        params['tp_restaurant_id'] = tp_restaurant_id

        return self.context_requester.base_request_get(request_path_url, url_params = params)

    def set_geo(self, geos):
        if not self.restaurant_id or not geos:
            return None

        request_path_url = "/restaurant/{}/geo/"

        params = {}
        params['geo_json'] = json.JSONEncoder().encode(geos)

        request_path_url = request_path_url.format(self.restaurant_id)
        return self.context_requester.base_request_put(request_path_url, put_params = params)

    def get_restaurant_menu(self):
        if not self.restaurant_id:
            return None

        request_path_url = "/restaurant/{}/menu/"

        request_path_url = request_path_url.format(self.restaurant_id)
        return self.context_requester.base_request_get(request_path_url)

    def update_order_mode_to_open_platform(self):
        return self.update_order_mode(1)

    def update_order_mode_to_napos(self):
        return self.update_order_mode(2)

    def update_order_mode(self, order_mode):
        if not self.restaurant_id or not order_mode:
            return

        request_path_url = '/restaurant/{}/order_mode/'
        request_path_url = request_path_url.format(self.restaurant_id)

        params = {}
        params['order_mode'] = order_mode

        return self.context_requester.base_request_put(request_path_url, put_params = params)

    def update_book(self, is_bookable):
        if not self.restaurant_id or not is_bookable:
            return

        params = {}
        params['is_bookable'] = is_bookable
        return self.update_restaurant_info(params)

class ElemeOwnRestaurantsRequester(object):
    """docstring for OwnRestaurantsRequester"""
    def __init__(self, context_requester):
        super(ElemeOwnRestaurantsRequester, self).__init__()
        self.context_requester = context_requester
        self.request_path_url = '/restaurant/own/'

    def request(self):
        return self.context_requester.base_request(self.request_path_url)

class ElemeCategoryRequester(object):
    """docstring for ElemeCategoryRequester"""
    def __init__(self, context_requester, food_category_id = None):
        super(ElemeCategoryRequester, self).__init__()
        self.context_requester = context_requester
        self.food_category_id = food_category_id

    def create_new(self, restaurant_id, name, weight):
        if not restaurant_id or not name or not weight:
            return None
        request_path_url = '/food_category/'

        params = {}
        params['restaurant_id'] = restaurant_id
        params['name'] = name
        params['weight'] = weight

        return self.context_requester.base_request_post(request_path_url, post_params = params)


    def get_all_foods(self):
        if not self.food_category_id:
            return None

        request_path_url = '/food_category/{}/foods/'
        request_path_url = request_path_url.format(self.food_category_id)
        return self.context_requester.base_request(request_path_url)

    def update_name(self, new_name):
        params = {}
        params['name'] = new_name
        return self.update(params)

    def update(self, params):
        if not self.food_category_id or not params:
            return None

        request_path_url = '/food_category/{}/'
        request_path_url = request_path_url.format(self.food_category_id)

        return self.context_requester.base_request_put(request_path_url, put_params = params)

    def delete(self):
        if not self.food_category_id:
            return None

        request_path_url = '/food_category/{}/'.format(self.food_category_id)

        return self.context_requester.base_request_delete(request_path_url)


class ElemeFoodRequester(object):
    """docstring for ElemeFoodRequester"""
    def __init__(self, context_requester, food_id = None):
        super(ElemeFoodRequester, self).__init__()
        self.context_requester = context_requester
        self.food_id = food_id

    def create_new(self, food_category_id, name, price = -1, description = '', max_stock = 10000, stock = 10000, tp_food_id = None, image_hash = None):
        if not food_category_id or not name or price < 0:
            return None
        request_path_url = '/food/'

        params = {}
        params['food_category_id'] = food_category_id
        params['name'] = name
        params['price'] = price
        params['description'] = description
        params['max_stock'] = max_stock
        params['stock'] = stock

        if tp_food_id:
            params['tp_food_id'] = tp_food_id

        if image_hash:
            params['image_hash'] = image_hash

        return self.context_requester.base_request_post(request_path_url, post_params = params)

    # tp_food_ids 最多100个
    def request_food_by_tp_id(self, tp_food_ids):
        pass

    def update_stock_by_tp_id(self, stock_info_json):
        params = {}
        params['stock_info'] = json.JSONEncoder().encode(stock_info_json)
        print params['stock_info']

        request_path_url = '/foods/stock/'

        return self.context_requester.base_request_put(request_path_url, put_params = params)

    def update_tp_food_id(self, tp_food_id):
        params = {}
        params['tp_food_id'] = tp_food_id

        return self.update(params)

    def update_image_hash(self, image_hash):
        params = {}
        params['image_hash'] = image_hash
        return self.update(params)

    def update(self, params):
        if not self.food_id:
            return None

        request_path_url = '/food/{}/'
        request_path_url = request_path_url.format(self.food_id)

        return self.context_requester.base_request_put(request_path_url, put_params = params)

    def delete(self):
        if not self.food_id:
            return None

        request_path_url = '/food/{}/'.format(self.food_id)
        return self.context_requester.base_request_delete(request_path_url)


class ElemeImageRequester(object):
    """docstring for ElemeImageRequester"""
    def __init__(self, context_requester):
        super(ElemeImageRequester, self).__init__()
        self.context_requester = context_requester

    def get_image_url(self, image_hash):
        if not image_hash:
            return None

        request_path_url = '/image/{}/'
        request_path_url = request_path_url.format(image_hash)

        return self.context_requester.base_request_get(request_path_url)

    def upload_image(self, image_name):
        logger.info('upload image, name is {}'.format(image_name))
        if not image_name:
            return None

        try:
            image_file = file(image_name, 'rb')
            image_file_data = image_file.read()
            # print image_file.tell()
            # print '1'
            # print "%s" % (binascii.hexlify(image_file_data))
            image_file.close()
        except Exception, e:
            print e
            return None

        request_path_url = '/image/'

        params = {}
        params['file'] = image_file_data

        return self.context_requester.base_request_upload(request_path_url, upload_params = params)

class ElemeCommentRequester(object):
    """docstring for ElemeCommentRequester"""
    def __init__(self, context_requester, restaurant_id = None):
        super(ElemeCommentRequester, self).__init__()
        self.context_requester = context_requester
        self.restaurant_id = restaurant_id

    def get_comment_count(self):
        if not self.restaurant_id:
            return None

        request_path_url = '/comment/{}/count/'.format(self.restaurant_id)
        return self.context_requester.base_request_get(request_path_url)

    def get_comment_list(self, offset = 1, limit = 20):
        if not self.restaurant_id:
            return None

        request_path_url = '/comment/{}/list_view/'.format(self.restaurant_id)

        params = {}
        params['offset'] = offset
        params['limit'] = limit

        return self.context_requester.base_request_get(request_path_url, url_params = params)


    def reply(self, comment_id, content, replier_name):
        if not comment_id or not self.restaurant_id or not content or not replier_name:
            return None

        request_path_url = '/comment/{}/reply/'.format(self.restaurant_id)

        params = {}
        params['comment_id'] = comment_id
        params['content'] = content
        params['replier_name'] = replier_name

        return self.context_requester.base_request_post(request_path_url, post_params = params)

def main():
    application = eleme_application_set.eleme_application_set['bsz']
    context_requester = ElemeAPIContextRequester(application.consumer_key, application.consumer_secret)

    # 查询所属餐厅
    own_restaurant_requester = ElemeOwnRestaurantsRequester(context_requester)
    response = own_restaurant_requester.request()
    print response
    print len(response['data']['restaurants'])

    # 订单相关
    order_requester = ElemeOrderRequester(context_requester)

    # while True:
    #     json_data = order_requester.get_new_orders()
    #     print json_data
    #     order_ids = json_data['data']['order_ids']
    #     if order_ids:
    #         print order_ids
    #         break

    # order_requester.get_order_info(100147321377401161, is_use_tp_id = True)
    # order_requester.confirm_order(100147321377401161)
    # order_requester.cancel_order(100147321377401161, '开放平台取消')

    # 餐厅相关
    # restaurant_requester = ElemeRestaurantRequester(context_requester, '62671548')
    # restaurant_requester.get_restaurant_info()
    # all_categories = restaurant_requester.get_all_categories()['data']['food_categories']
    # print all_categories

    # print restaurant_requester.get_restaurant_by_tp_id('26823299')
    # for category in all_categories:
    #     print category
    #     food_category_requester = ElemeCategoryRequester(context_requester, category['food_category_id'])
    #     print food_category_requester.get_all_foods()


    # print restaurant_requester.get_restaurant_by_tp_id('96000')
    # print restaurant_requester.binding('96553')
    # print restaurant_requester.update_restaurant_phone('87654321')
    # print restaurant_requester.update_restaurant_name('Open API 测试餐厅')
    # print restaurant_requester.update_restaurant_address('武侯区科院街5号(近领事馆路棕北中学)')
    # print restaurant_requester.update_restaurant_open_time('9:00-22:00')
    # print restaurant_requester.set_geo(text_geo)


    # 分类相关
    # food_category_requester = ElemeCategoryRequester(context_requester, '3371496')

    # print food_category_requester.get_all_foods()
    # print food_category_requester.create_new(62028381, '川菜', 100)


    # 食物相关
    food_requester = ElemeFoodRequester(context_requester)
    # stock_info_json = {'4739284732': {'432432': '中文', '432423': 10}, "43242": {"43242112":399}}
    # print food_requester.update_stock_by_tp_id(stock_info_json)

    # print food_requester.create_new('4055272', '川菜', price = 15.5)
    # print food_requester.delete()

    # 图片相关
    # image_requester = ElemeImageRequester(context_requester)

    # print image_requester.get_image_url('a35292a9a7412ddeb01af94aa922a2dcd9798623')

    # path = os.path.split(os.path.realpath(__file__))[0]
    # path = '/Users/Bargetor/Documents/Bargetor/workspace/python/elemeopenapi/elemeopenapi/elemeapi'
    # print image_requester.upload_image('{}/{}'.format(path ,'abc.jpeg'))

    # 评论相关
    # comment_requester = ElemeCommentRequester(context_requester, 37018602)
    # comment_requester.get_comment_count()
    # print comment_requester.get_comment_list()
    # print comment_requester.reply(832, 'test', replier_name = 'xiaosi')


if __name__ == '__main__':
    main()
