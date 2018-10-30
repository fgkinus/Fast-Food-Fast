import os

from flask_restplus import abort
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from app.V2 import DB


class Utils:
    """a class instance for static utility functions"""

    @staticmethod
    def parse_int(number):
        """
        converts input to valid int or trows exception
        :param number:
        :return: number
        """
        try:
            number = int(number)
            return number
        except:
            DB.logger.error("invalid input parameter could not be parsed to int")
            abort(400, "The parameter was not  a valid number")

    @staticmethod
    def upload_image(image):
        """
        upload images
        :return url:
        """

        try:
            upload_result = upload(file=image)
            url, options = cloudinary_url(upload_result['public_id'])
            return url
        except:
            abort(503, "The cloud image server storage is not available ")
