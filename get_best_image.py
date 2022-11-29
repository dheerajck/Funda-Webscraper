def avoid_b64(image, img_tag):
    # ad_link/#overzicht is needed for proper parsing
    if image.startswith("data:image"):
        if img_tag.has_attr("data-lazy"):
            return img_tag["data-lazy"].strip().split()[0]
    return image


def get_best_image_source_list(img_tag):

    if img_tag.has_attr("data-lazy-srcset"):
        image_source: list = [img_tag["data-lazy-srcset"].split(",")[-1].strip().split()[0]]
        image_source[0] = avoid_b64(image_source[0], img_tag)

    elif img_tag.has_attr("srcset"):
        image_source: list = [img_tag["srcset"].split(",")[-1].strip().split()[0]]
        image_source[0] = avoid_b64(image_source[0], img_tag)

    elif img_tag.has_attr("src"):
        # image_source: str = [img_tag["src"].strip()]
        image_source: list = [img_tag["src"].strip().split()[0]]
        image_source[0] = avoid_b64(image_source[0], img_tag)

    else:
        image_source = []

    return image_source


def get_best_image_source_str(img_tag):

    if img_tag.has_attr("data-lazy-srcset"):

        image_source: str = img_tag["data-lazy-srcset"].split(",")[-1].strip().split()[0]
        image_source = avoid_b64(image_source, img_tag)

    elif img_tag.has_attr("srcset"):
        image_source: str = img_tag["srcset"].split(",")[-1].strip().split()[0]
        image_source = avoid_b64(image_source, img_tag)

    elif img_tag.has_attr("src"):
        image_source: str = img_tag["src"].strip()
        image_source = avoid_b64(image_source, img_tag)
    else:
        image_source = None

    return image_source
