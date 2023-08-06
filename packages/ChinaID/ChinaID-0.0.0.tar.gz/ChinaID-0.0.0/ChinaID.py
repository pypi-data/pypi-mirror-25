import AreaNumber
import Verification
import logging

Logger = logging.getLogger('Log')


def parse(id_no):
    census_register = AreaNumber.parse(id_no)
    birthday = id_no[6:14]
    gender = '男' if int(id_no[16]) % 2 else '女'
    legal = Verification.verification(id_no)

    result = {
        'CensusRegister': census_register,
        'Birthday': birthday,
        'Gender': gender,
        'Legal': legal
    }

    Logger.debug(result)
    return result


def update_area_number():
    AreaNumber.get_area_number()


def _init_logger():
    file_handler = logging.FileHandler(".log")
    file_handler.formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    Logger.addHandler(file_handler)
    Logger.setLevel(logging.DEBUG)


_init_logger()
update_area_number()