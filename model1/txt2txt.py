from .txt2img import generator

from . import PPTX_STYLE, SCHEMA_X

import os
import random
import string
import re


def generate_filename_from_theme(
        theme: str,
        output_dir: str = "",
        prefix: str = "",
        extension: str = ".pptx",
        length: int = 8,
        max_slug: int = 30,
        custom_slugify: callable = None
) -> str:
    """
    Генерирует полный путь к файлу на основе темы.

    :param theme: Тема (строка, будет приведена к slug)
    :param output_dir: Каталог, куда сохранить файл (если пустой — файл создаётся в cwd)
    :param prefix: Префикс к имени файла (например, "draft_")
    :param extension: Расширение файла (по умолчанию ".pptx")
    :param length: Длина случайного постфикса
    :param max_slug: Максимальная длина slug'а
    :param custom_slugify: Своя функция slugify, если нужно
    :return: Полный путь к файлу
    """

    # Функция slugify (если не передали свою)
    def default_slugify(text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s]+', '_', text)
        return text[:max_slug]

    slugify_fn = custom_slugify if custom_slugify else default_slugify

    slug = slugify_fn(theme)
    uniq = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    filename = f"{prefix}{slug}_{uniq}{extension}"

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        return os.path.join(output_dir, filename)
    return filename


class GeneratePresentation:
    def __init__(self, config: dict):
        self.config = config
        self.client = self.config["client"]

    def __fix_json(self, data: str):
        import re
        import json
        match = re.search(r"```json\s*(.*?)```", data, re.DOTALL)
        if not match:
            raise ValueError("❌ JSON-block not found")

        json_str = match.group(1)
        return json.loads(json_str)

    def __get_image(self, url: str, path: str):
        import requests
        import os
        try:
            name = url.split("/")[-1]
            response = requests.get(url)
            path = os.path.join(path, f"{name}.jpg")
            with open(path, "wb") as f:
                f.write(response.content)

            return path
        except Exception as e:
            print("[!] Error downloading image:", e, url); return

    def __replace_prompt_to_img(self, data: dict, func) -> dict:
        replaced = []
        for slide in data.get("body", []):
            prompt = slide.get("image")
            if prompt:
                image_url = func(self.config, prompt)
                image_path = self.__get_image(image_url, self.config["image_path"])

                slide["image"] = image_path
                replaced.append((prompt, image_url))
        return data

    def generate_presentation_schema(self, theme: str, lang: str, **kwargs):
        extra_params = f"Дополнительные параметры: {kwargs}" if kwargs else ""
        response = self.client.chat.completions.create(
            model=self.config["txt_model"],
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты мастер по созданию JSON-шаблонов для презентаций. "
                        "Следуй строго по структуре. Ответ всегда в виде JSON. "
                        f"Вот шаблон структуры: {SCHEMA_X()} но сделай"
                        f"так чтобы было много текста и строго по плану добавь туда план"
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Сгенерируй JSON-шаблон презентации на тему '{theme}', "
                        f"на языке '{lang}'. {extra_params}"
                    )
                }
            ]
        )
        return response

    def full_generate(self, *args, **kwargs) -> dict:
        from .presentation_generator import generate_ppt_from_json
        import random
        import string
        import os
        response = self.generate_presentation_schema(*args, **kwargs).choices[0].message.content
        fixed = self.__fix_json(response)
        print(fixed)

        json_presentation = self.__replace_prompt_to_img(fixed, generator)

        file = generate_filename_from_theme(theme=args[0], output_dir=self.config["presentation_path"])

        generate_ppt_from_json(json_presentation, file)
        print("Presentations generated:", file)
        return file








