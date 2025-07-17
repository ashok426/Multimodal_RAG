from typing import Any, Dict, List

class IngestionPipeline:
    def __init__(self, source: str):
        self.source = source
        self.raw_elements = None
        self.processed_data = {
            "Header": [],
            "Footer": [],
            "Title": [],
            "NarrativeText": [],
            "Text": [],
            "ListItem": [],
            "Image": [],
            "Table": [],
        }

    def load_data(self):
        from unstructured.partition.pdf import partition_pdf
        self.raw_elements = partition_pdf(
            filename=self.source,
            strategy="hi_res",
            extract_images_in_pdf=True,
            extract_image_block_types=["Image", "Table"],
            extract_image_block_to_payload=False,
            extract_image_block_output_dir="extracted_data"
        )

    def process_data(self):
        for element in self.raw_elements:
            t = str(type(element))
            if "Header" in t:
                self.processed_data["Header"].append(str(element))
            elif "Footer" in t:
                self.processed_data["Footer"].append(str(element))
            elif "Title" in t:
                self.processed_data["Title"].append(str(element))
            elif "NarrativeText" in t:
                self.processed_data["NarrativeText"].append(str(element))
            elif "Text" in t:
                self.processed_data["Text"].append(str(element))
            elif "ListItem" in t:
                self.processed_data["ListItem"].append(str(element))
            elif "Image" in t:
                self.processed_data["Image"].append(str(element))
            elif "Table" in t:
                self.processed_data["Table"].append(str(element))

    def get_processed_data(self) -> Dict[str, List[Any]]:
        return self.processed_data