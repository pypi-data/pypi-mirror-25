import sys
import numpy


CONTENT_TYPE = 'Content-Type'


class RiohConstants(object):
    MEDIA_TYPE = 'image'
    MEDIA_SUB_TYPE = 'x.raw'

    RIOH_MEDIA_TYPE = MEDIA_TYPE + '/' + MEDIA_SUB_TYPE

    VERSION_MAJOR = 1
    VERSION_MINOR = 0

    VERSION_STR = str(VERSION_MAJOR) + '.' + str(VERSION_MINOR)

    VERSION = 'version'

    ENDIAN = 'endian'
    DATATYPE = 'datatype'
    DIMENSIONS = 'dimensions'
    SIZE = 'size'

    MULTI_IMAGE_SEPARATOR = '_'
    MULTI_DIMENSION_SEPARATOR = 'x'

    ENDIAN_BIG = 'big'
    ENDIAN_LITTLE = 'little'


RC = RiohConstants


def _parse_type(t):
    splitter = [split.strip() for split in t.split(';')]
    return splitter[0], {
        k.lower(): v.lower()
        for k, v
        in [[inner_s.strip() for inner_s in s.split('=')] for s in splitter[1:] if s != '']
    }


def parse_images(raw_data, content_type, reorder_dimensions=False, return_dimensions=False):
    name, parameters = _parse_type(content_type)

    if name != RC.RIOH_MEDIA_TYPE:
        raise RuntimeError("Unsupported media type received.")

    if parameters[RC.VERSION] != RC.VERSION_STR:
        raise RuntimeError("Unsupported parameter format version received.")

    endian_or_default = parameters[RC.ENDIAN] if RC.ENDIAN in parameters else RC.ENDIAN_LITTLE

    endian = endian_or_default.split(RC.MULTI_IMAGE_SEPARATOR)
    datatype = parameters[RC.DATATYPE].split(RC.MULTI_IMAGE_SEPARATOR)
    dimensions = parameters[RC.DIMENSIONS].split(RC.MULTI_IMAGE_SEPARATOR)
    size = parameters[RC.SIZE].split(RC.MULTI_IMAGE_SEPARATOR)

    total_images = max(len(endian), len(datatype), len(dimensions), len(size))

    result = []

    for n in range(total_images):
        n_endian = endian[min(n, len(endian)-1)]
        n_datatype = datatype[min(n, len(datatype)-1)]
        n_dimensions = dimensions[min(n, len(dimensions)-1)]
        n_size = size[min(n, len(size)-1)]

        n_size = [int(s) for s in n_size.split(RC.MULTI_DIMENSION_SEPARATOR)]

        n_elements = numpy.prod(n_size)

        if n_datatype == 'bit':
            n_raw_size = math.ceil(n_elements / 8)

            n_raw_data = raw_data[:n_raw_size]
            raw_data = raw_data[n_raw_size:]

            data = numpy.unpackbits(numpy.fromstring(n_raw_data, dtype=numpy.uint8))

        else:

            n_datatype = numpy.dtype(n_datatype)

            if n_endian == RC.ENDIAN_LITTLE:
                n_datatype = n_datatype.newbyteorder('<')
            elif n_endian == RC.ENDIAN_BIG:
                n_datatype = n_datatype.newbyteorder('>')
            else:
                raise RuntimeError("Unsupported endian received.")

            n_raw_size = n_elements * n_datatype.itemsize

            n_raw_data = raw_data[:n_raw_size]
            raw_data = raw_data[n_raw_size:]

            data = numpy.fromstring(n_raw_data, dtype=n_datatype)

        data = data.reshape(n_size)

        n_dimensions = list(n_dimensions.upper())

        result.append((data, n_dimensions,))

    if reorder_dimensions:
        pass

    if return_dimensions:
        return result
    else:
        return [data for data, n_dimensions in result]


def prepare_images(images, dimensions=None):
    if not isinstance(images, list):
        images = [images]

    if dimensions is None:
        dimensions = ["YX"] * len(images)

    def parameters_for_image(image, dimensions):
        def byteorder_to_endian(byteorder):
            if byteorder == '=' or byteorder == '|':
                return RC.ENDIAN_LITTLE if sys.byteorder == 'little' else RC.ENDIAN_BIG
            elif byteorder == '<':
                return RC.ENDIAN_LITTLE
            elif byteorder == '>':
                return RC.ENDIAN_BIG
            else:
                raise RuntimeError("Unsupported endianness")

        return {
            RC.ENDIAN: byteorder_to_endian(image.dtype.byteorder),
            RC.DATATYPE: image.dtype.name,
            RC.DIMENSIONS: dimensions,
            RC.SIZE: RC.MULTI_DIMENSION_SEPARATOR.join([str(s) for s in image.shape])
        }

    total_parameters = {}

    for image, image_dimensions in zip(images, dimensions):
        parameters = parameters_for_image(image, image_dimensions)
        for k, v in parameters.items():
            if k in total_parameters:
                total_parameters[k] += RC.MULTI_IMAGE_SEPARATOR + parameters[k]
            else:
                total_parameters[k] = parameters[k]

    total_parameters[RC.VERSION] = RC.VERSION_STR

    parameters_str = ';'.join('%s=%s' % (k, v,) for k, v in total_parameters.items())

    return "%s;%s" % (RC.RIOH_MEDIA_TYPE, parameters_str), [image.tobytes() for image in images]
