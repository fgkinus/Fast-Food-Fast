import os

from flask_restplus import abort
import cloudinary as Cloud

from app.V2 import DB

# configure image storage
Cloud.config.update = ({
    'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})


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
    def upload_image():
        """
        upload images
        :return:
        """
