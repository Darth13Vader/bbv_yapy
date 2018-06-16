import os
from shutil import copy


RESOURCES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../resources')
MODELS_PATH = os.path.join(RESOURCES_PATH, 'models')


def copy_to_resouces(from_path):
    copy(from_path, RESOURCES_PATH)