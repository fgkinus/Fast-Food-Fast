from flask_restplus import abort

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
