from .. import prepare_images, parse_images, CONTENT_TYPE


def rioh(*args, **kwargs):
    if callable(args[0]):
        return rioh_request(*args, **kwargs)
    else:
        return rioh_response(*args, **kwargs)


def rioh_response(response):
    return parse_images(response.content, response.headers[CONTENT_TYPE])


def is_rioh_response(response):
    return response.headers[CONTENT_TYPE].startswith(RiohConstants.RIOH_MEDIA_TYPE)


def rioh_request(what, url, images=None, dimensions=None, headers=None, **kwargs):
    content_type_header, image_data = prepare_images(images, dimensions=dimensions)
    image_data = b"".join(image_data)

    if headers is None:
        headers = {}

    headers['Content-Type'] = content_type_header

    return what(url, data=image_data, headers=headers, **kwargs)
