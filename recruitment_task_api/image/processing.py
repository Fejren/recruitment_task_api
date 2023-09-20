from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile

from image.models import Image
from user.models import AccountTier
from PIL import Image as ProcessImage


def image_width_calc(height: int, img) -> tuple:
    proportion = height / float(img.size[1])
    width = int(float(img.size[0]) * proportion)
    return width, height


def process_image(image, account_tier: AccountTier, user_id: int):
    saved_image = Image.objects.create(content=image, user_id=user_id)
    img = ProcessImage.open(saved_image.content)

    # Scaled images will be stored in the image list
    images = []
    for size in account_tier.size:
        img_resized = img.resize(image_width_calc(size, img))
        images.append(img_resized)

    # Create Image objects for the resized images
    file_names = []
    if account_tier.has_original is True:
        file_names.append(saved_image.content.name)
    for i in images:
        # Convert PIL.Image to bytes
        image_bytes = BytesIO()
        i.save(image_bytes, format=img.format)
        image_bytes.seek(0)

        # Create SimpleUploadedFile
        file_name = f"{user_id}_resized_{account_tier.size}.{img.format}"
        resized_image = SimpleUploadedFile(file_name, image_bytes.read())
        file_names.append(Image.objects.create(content=resized_image, user_id=user_id).content.name)
    return file_names
