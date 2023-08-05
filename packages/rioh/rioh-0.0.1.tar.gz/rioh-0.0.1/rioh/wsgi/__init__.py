from .. import RiohConstants, parse_images


def parse_images_from_env(env):
    return parse_images(env['wsgi.input'].read(int(env['CONTENT_LENGTH'])), env['CONTENT_TYPE'])


def is_rioh_request(env):
    return (env['REQUEST_METHOD'] == 'POST' or env['REQUEST_METHOD'] == 'PUT') and \
           env['CONTENT_TYPE'].startswith(RiohConstants.RIOH_MEDIA_TYPE)
