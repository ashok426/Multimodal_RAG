import base64
import io
import re
import os
from PIL import Image

class ImageProcessor:
    def __init__(self, extracted_dir: str):
        self.extracted_dir = extracted_dir

    def encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def resize_base64_image(self, base64_string: str, size=(128,128)) -> str:
        img_data = base64.b64decode(base64_string)
        img = Image.open(io.BytesIO(img_data))
        resized_img = img.resize(size, Image.LANCZOS)
        buffered = io.BytesIO()
        resized_img.save(buffered, format=img.format)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def generate_img_summaries(self, image_summarize_func, prompt: str):
        img_base64_list = []
        image_summaries = []
        for img_file in sorted(os.listdir(self.extracted_dir)):
            if img_file.endswith(".jpg"):
                img_path = os.path.join(self.extracted_dir, img_file)
                base64_image = self.encode_image(img_path)
                img_base64_list.append(base64_image)
                image_summaries.append(image_summarize_func(base64_image, prompt))
        return img_base64_list, image_summaries

    @staticmethod
    def is_image_data(b64data: str) -> bool:
        image_signatures = {
            b"\xFF\xD8\xFF": "jpg",
            b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A": "png",
            b"\x47\x49\x46\x38": "gif",
            b"\x52\x49\x46\x46": "webp",
        }
        try:
            header = base64.b64decode(b64data)[:8]
            for sig in image_signatures.keys():
                if header.startswith(sig):
                    return True
            return False
        except Exception:
            return False

    @staticmethod
    def looks_like_base64(sb: str) -> bool:
        return re.match("^[A-Za-z0-9+/]+[=]{0,2}$", sb) is not None

    def split_image_text_types(self, docs):
        b64_images = []
        texts = []
        from langchain_core.documents import Document
        for doc in docs:
            if isinstance(doc, Document):
                doc = doc.page_content
            if self.looks_like_base64(doc) and self.is_image_data(doc):
                doc = self.resize_base64_image(doc, size=(1300, 600))
                b64_images.append(doc)
            else:
                texts.append(doc)
        return {"images": b64_images, "texts": texts}