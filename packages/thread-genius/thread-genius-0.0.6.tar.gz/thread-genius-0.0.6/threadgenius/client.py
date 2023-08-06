import requests
import logging
import base64
from threadgenius.types import ImageUrlInput, ImageFileInput, CatalogObject

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

logger.setLevel(logging.DEBUG)

API_VERSION = 1
BASE_URL = 'https://api.threadgenius.co/v%d' % API_VERSION

class ThreadGenius(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def create_catalog(self, catalog_name):
        """

        :type catalog_name: string
        """
        endpoint = '/catalog'
        data = {
            'name': catalog_name
        }
        res = requests.post(BASE_URL + endpoint, auth=(self.api_key, None), json=data)

        return res.json()

    def get_catalog(self, catalog_gid):
        """

        :type catalog_gid: string
        """
        endpoint = '/catalog/' + catalog_gid
        res = requests.get(BASE_URL + endpoint, auth=(self.api_key, None))

        return res.json()

    def list_all_catalogs(self):
        endpoint = '/catalog'
        res = requests.get(BASE_URL + endpoint, auth=(self.api_key, None))

        return res.json()

    def delete_catalog(self, catalog_gid):
        """

        :type catalog_gid: string
        """
        endpoint = '/catalog/' + catalog_gid
        res = requests.delete(BASE_URL + endpoint, auth=(self.api_key, None))

        return res.json()

    def tag_image(self, image):
        """

        :type image: threadgenius.types.ImageUrlInput, threadgenius.types.ImageFileInput
        """
        endpoint = '/prediction/tag'
        data = {
            'image': {
                'crop': image.crop
            }
        }

        if isinstance(image, ImageUrlInput):
            data['image']['url'] = image.url
        elif isinstance(image, ImageFileInput):
            data['image']['base64'] = base64.b64encode(image.file_object.read())

        res = requests.post(BASE_URL + endpoint, auth=(self.api_key, None), json=data)

        return res.json()

    def tag_image_urls(self, images):
        """

        :type images: list(threadgenius.types.ImageUrlInput)
        """
        assert all([isinstance(im, ImageUrlInput) for im in images]),\
            "Images must be of type threadgenius.datatypes.ImageUrlInput"

        data = {
            'images': [{'url': im.url, 'crop': im.crop} for im in images]
        }

        endpoint = '/prediction/tag'
        res = requests.post(BASE_URL + endpoint, auth=(self.api_key, None), json=data)

        return res.json()

    def get_tag(self, tag_gid):
        """

        :type tag_gid: string
        """
        endpoint = '/prediction/tag/' + tag_gid
        res = requests.get(BASE_URL + endpoint, auth=(self.api_key, None))

        return res.json()

    def list_all_tags(self, next_key=None):
        """

        :type next_key: string
        """
        endpoint = '/prediction/tag'

        if next_key:
            endpoint += '?next_key=%s' % next_key

        res = requests.get(BASE_URL + endpoint, auth=(self.api_key, None))

        return res.json()

    def detect_image(self, image):
        """

        :type image: threadgenius.types.ImageUrlInput, threadgenius.types.ImageFileInput
        """
        endpoint = '/prediction/detect'
        data = {
            'image': {
                'crop': image.crop
            }
        }

        if isinstance(image, ImageUrlInput):
            data['image']['url'] = image.url
        elif isinstance(image, ImageFileInput):
            data['image']['base64'] = base64.b64encode(image.file_object.read())

        res = requests.post(BASE_URL + endpoint, auth=(self.api_key, None), json=data)

        return res.json()

    def detect_image_urls(self, images):
        """

        :type images: list(threadgenius.types.ImageUrlInput)
        """
        assert all([isinstance(im, ImageUrlInput) for im in
                    images]), "Images must be of type threadgenius.datatypes.ImageUrlInput"

        data = {
            'images': [{'url': im.url, 'crop': im.crop} for im in images]
        }

        endpoint = '/prediction/detect'
        res = requests.post(BASE_URL + endpoint, auth=(self.api_key, None), json=data)

        return res.json()

    def get_detection(self, detect_gid):
        """

        :type detect_gid: string
        """
        endpoint = '/prediction/detect/' + detect_gid
        res = requests.get(BASE_URL + endpoint, auth=(self.api_key, None))

        return res.json()

    def list_all_detections(self, next_key=None):
        """

        :param next_key: string
        """
        endpoint = '/prediction/detect'

        if next_key:
            endpoint += '?next_key=%s' % next_key

        res = requests.get(BASE_URL + endpoint, auth=(self.api_key, None))

        return res.json()


    def add_catalog_objects(self, catalog_gid, objects):
        """

        :type catalog_gid: string
        :type objects: list(threadgenius.types.CatalogObject)
        """
        assert all([isinstance(im, CatalogObject) for im in objects]),\
            "Objects must be of type threadgenius.datatypes.CatalogObject"

        data = {
            'objects': [{
                'image': {
                    'url': obj.image_url_input.url,
                    'crop': obj.image_url_input.crop
                },
                'metadata': obj.metadata
            } for obj in objects]
        }

        endpoint = '/catalog/' + catalog_gid + '/object'
        res = requests.post(BASE_URL + endpoint, auth=(self.api_key, None), json=data)

        return res.json()

    def delete_catalog_object(self, catalog_gid, object_gid):
        """

        :type catalog_gid: string
        :type object_gid: string
        """
        endpoint = '/catalog/' + catalog_gid + '/object/' + object_gid
        res = requests.delete(BASE_URL + endpoint, auth=(self.api_key, None))

        return res.json()

    def get_catalog_object(self, catalog_gid, object_gid):
        """

        :type catalog_gid: string
        :type object_gid: string
        """
        endpoint = '/catalog/' + catalog_gid + '/object/' + object_gid
        res = requests.get(BASE_URL + endpoint, auth=(self.api_key, None))

        return res.json()

    def list_all_catalog_objects(self, catalog_gid, next_key=None):
        """

        :type catalog_gid: string
        :type next_key: string
        """
        endpoint = '/catalog/' + catalog_gid + '/object'

        if next_key:
            endpoint += '?next_key=%s' % next_key

        res = requests.get(BASE_URL + endpoint, auth=(self.api_key, None))

        return res.json()

    def search_by_keywords(self, catalog_gid, keywords, n_results):
        """

        :type catalog_gid: string
        :type keywords: list(string)
        :type n_results: int
        """
        if not isinstance(keywords, list):
            raise Exception("Keywords should be a list of strings.")

        data = {
            'keywords': keywords,
            'n_results': n_results
        }
        endpoint = '/catalog/' + catalog_gid + '/search'
        res = requests.post(BASE_URL + endpoint, auth=(self.api_key, None), json=data)

        return res.json()

    def search_by_image(self, catalog_gid, image, n_results):
        """

        :type catalog_gid: string
        :type image: threadgenius.types.ImageUrlInput, threadgenius.types.ImageFileInput
        :type n_results: int
        """
        data = {
            'image': {
                'crop': image.crop
            },
            'n_results': n_results
        }

        if isinstance(image, ImageUrlInput):
            data['image']['url'] = image.url
        elif isinstance(image, ImageFileInput):
            data['image']['base64'] = base64.b64encode(image.file_object.read())

        endpoint = '/catalog/' + catalog_gid + '/search'
        res = requests.post(BASE_URL + endpoint, auth=(self.api_key, None), json=data)

        return res.json()

    def add_catalog_object(self, catalog_gid, object):
        """

        :type catalog_gid: string
        :param object: threadgenius.types.CatalogObject
        """
        return self.add_catalog_objects(catalog_gid, [object])

    def get_usage_summary(self):

        endpoint = '/usage'
        res = requests.get(BASE_URL + endpoint, auth=(self.api_key, None))

        return res.json()
