from langchain_core.messages import HumanMessage

class LLMOutputGenerator:
    @staticmethod
    def img_prompt_func(data_dict):
        formatted_texts = "\n".join(data_dict["context"]["texts"])
        messages = []
        # Add images if present
        if data_dict["context"]["images"]:
            for image in data_dict["context"]["images"]:
                image_message = {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                }
                messages.append(image_message)
        # Add text for analysis
        text_message = {
            "type": "text",
            "text": (
                "You are a helpful assistant.\n"
                "You will be given a mixed info(s) .\n"
                "Use this information to provide relevant information to the user question. \n"
                f"User-provided question: {data_dict['question']}\n\n"
                "Text and / or tables:\n"
                f"{formatted_texts}"
            ),
        }
        messages.append(text_message)
        return [HumanMessage(content=messages)]

    @staticmethod
    def format_multimodal_output(inputs):
        return {
            "answer": inputs["llm_output"],
            "source_texts": inputs["context"]["texts"],
            "source_images": inputs["context"]["images"],
        }