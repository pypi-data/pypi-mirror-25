class ImageInputBase(object):
    def __init__(self, crop=None):
        self.crop = crop

        if self.crop:
            assert isinstance(self.crop, list), "Crop needs to be of type list"


class ImageUrlInput(ImageInputBase):
    def __init__(self, url, crop=None):
        """

        :type crop: list
        :type url: string
        """
        self.url = url

        super(ImageUrlInput, self).__init__(crop=crop)


class ImageFileInput(ImageInputBase):
    def __init__(self, file_object, crop=None):
        """

       :type crop: list
       :type file_object: file-like object
        """
        self.file_object = file_object

        super(ImageFileInput, self).__init__(crop=crop)


class CatalogObject(object):
    def __init__(self, image_url_input, metadata=None):
        """

        :type image_input: threadgenius.types.ImageUrlInput
        :type metadata:
        """
        self.image_url_input = image_url_input
        self.metadata = metadata

        assert isinstance(self.image_url_input, ImageUrlInput), "Image needs to be of type threadgenius.datatypes.ImageUrlInput"

        if self.metadata:
            assert isinstance(self.metadata, dict), "Metadata needs to be of type dict"
