### CS 4300 Fall 2023 Group 2
### Harvestly
### Common Utilities

""" Implementation of Common utilities methods """

from PIL import Image

from Common.services import ImageService

def validate_file(file):
    """ Validate image file contents, format, max and min size
    
    Returns:
        Tuple containing boolean and string.
        First element validation result (boolean)
        Second element error message or None (str)
    """

    # return since image upload is optional
    if not file:
        return (True, None)

    # validate image file contents
    try:
        with Image.open(file) as image:
            # check image is valid and readable
            image.verify()

            # check image format is supported
            if image.format not in ImageService.ACCEPTED_FILE_TYPES:
                return (False, "Invalid file format.")

    except Exception:
        return (False, "Invalid file.")

    return (True, None)


def validate_image_dimensions(image):
    """ Takes an image file and validates its width and height against
        the max allowed as defined in Image model: MAX_IMAGE_SIZE

    Returns:
        Tuple containing boolean and string.
        First element validation result (boolean)
        Second element error message or None (str)
    """

    if not image:
        return (True, None)

    try:
        with Image.open(image) as img:
            max_width, max_height = ImageService.MAX_IMAGE_SIZE

            if img.width > max_width or img.height > max_height:
                exceeded_dimension = "width" if img.width > max_width else "height"

                return (
                    False,
                    f"Image {exceeded_dimension} exceeds maximum allowed. Max allowed is \
                        {ImageService.MAX_IMAGE_SIZE[0]}x{ImageService.MAX_IMAGE_SIZE[1]}"
                    )

    except Exception:
        return (False, "Invalid image file.")

    return (True, None)


def validate_file_size(file):
    """Checks file is not too large or small in size
    
    Returns:
        Tuple containing boolean and string.
        First element validation result (boolean)
        Second element error message or None (str)
    """

    if not file:
        return (True, None)

    if file.size > ImageService.MAX_FILE_SIZE:
        return (
            False,
            f"Image file too large. max size is {ImageService.MAX_FILE_SIZE_MB} MB"
        )

    if file.size < ImageService.MIN_FILE_SIZE:
        return (
            False,
            f"Image file too small. min size is {ImageService.MIN_FILE_SIZE_KB} KB"
        )

    return (True, None)
