import io
from PIL import Image, ImageCms

# source: https://www.reddit.com/r/learnpython/comments/k7xk7r/failed_minimal_tag_size_sanity_pyqt5/givnexh?utm_source=share&utm_medium=web2x&context=3
def convert_to_srgb(file_path):
    '''Convert PIL image to sRGB color space (if possible)'''
    img = Image.open(file_path)
    icc = img.info.get('icc_profile', '')

    if icc:
        io_handle = io.BytesIO(icc)  # virtual file
        src_profile = ImageCms.ImageCmsProfile(io_handle)
        dst_profile = ImageCms.createProfile('sRGB')
        img_conv = ImageCms.profileToProfile(img, src_profile, dst_profile)
        icc_conv = img_conv.info.get('icc_profile', '')

        if icc != icc_conv:
            # ICC profile was changed -> save converted file
            img_conv.save(file_path, format='JPEG', quality=50, icc_profile=icc_conv)

# stretches an image to fill a certain w,h requirement
def stretch_to_fill(img_path, w, h):
    img = Image.open(img_path)
    # using this algorithim: https://stackoverflow.com/a/6565988/11106258
    ratio_img = img.size[0] / img.size[1]
    ratio_screen = w / h
    if ratio_screen > ratio_img:
        img = img.resize((int(img.size[0] * h / img.size[1]), h), Image.ANTIALIAS)
    else:
        img = img.resize((w, int(img.size[1] * w / img.size[0])), Image.ANTIALIAS)
    img.save(img_path)
    # one last check
    img = Image.open(img_path)
    if img.size[0] < w:
        resize_to_width(img_path, w)
    img = Image.open(img_path)
    if img.size[1] < h:
        resize_to_height(img_path, h)

# source: https://stackoverflow.com/a/451580/11106258
def resize_to_width(file_path, w):
    img = Image.open(file_path)
    wpercent = (w / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((w, hsize), Image.ANTIALIAS)
    img.save(file_path)

def resize_to_height(file_path, h):
    img = Image.open(file_path)
    hpercent = (h / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, h), Image.ANTIALIAS)
    img.save(file_path)
