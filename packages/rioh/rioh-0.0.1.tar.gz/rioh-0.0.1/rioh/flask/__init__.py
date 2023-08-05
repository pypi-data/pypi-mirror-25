from flask import request
from .. import parse_images, RiohConstants, CONTENT_TYPE


def parse_images_from_request():
    return parse_images(request.get_data(), request.headers.get(CONTENT_TYPE))


def is_rioh_request():
    return request.headers.get(CONTENT_TYPE).startswith(RiohConstants.RIOH_MEDIA_TYPE)
