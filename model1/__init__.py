import openai

class GeneratePresentationModel1:
    DEFAULT_CONFIGS = {
        "img_model": "dall-e-3",
        "txt_model": "gpt-4o",
        "presentation_size": ("16", "9"),
        "lang": "ru",
        "client": None,
        "image_path": "images",
        "presentation_path": "presentations",
        "image_size": "1024x1024",
    }

    def __init__(self, api_key, **custom_settings):
        self.api_key = api_key

        self.config = self.DEFAULT_CONFIGS.copy()
        self.config.update(custom_settings)

        self.config["client"] = openai.OpenAI(api_key=self.api_key)

    def set_config(self, key, value):
        self.config[key] = value

    def get_config_value(self, key):
        return self.config.get(key)

    def get_config(self):
        return self.config

    def generate(self, theme, lang=None, **kwargs):
        from .txt2txt import GeneratePresentation
        return GeneratePresentation(self.get_config()).full_generate(theme, lang, **kwargs)


def SCHEMA_X():
    return {
        "titul": {
            "text": "Заголовок презентации",
            "image_prompt": "Описание картинки для обложки (например, 'Грациозная кошка на фоне заката')"
        },
        "main": {
            "intro": "Вступление — 2-3 предложения о теме презентации",
            "plan": [
                "План презентации — список пунктов (например, 'Пункт 1', 'Пункт 2', 'Пункт 3', и так далее)",
            ],
            "style": {
                "color_header": "Цвет текста (в hex, например, '#000000')",
                "color_text": "Цвет текста (в hex, например, '#000000')",
            },
            "image_prompt": "описание картины для наглядности"
        },
        "body": [
            {
                "slide": {
                    "title": "Заголовок слайда (по плану)",
                    "content": [
                        {
                            "subtitle": "Подтема/абзац 1 (например, 'Древние союзники')",
                            "text": "Основной текст этого блока — 2-4 предложения"
                        },
                        {
                            "subtitle": "Подтема/абзац 2 (например, 'Древние союзники') продложи сам"
                        }
                    ]
                },
                "image": "ПРомпт для этого/ None"}, "продолжи по плану"

        ]
    }


PPTX_STYLE = {
    "slide_width": 16,
    "slide_height": 9,

    "title_font": {
        "size": 44,
        "bold": True,
        "align": "center"
    },

    "main_intro": {
        "top": 1.5,
        "left": 1,
        "width": 14,
        "height": 6,
        "font_size": 32,
        "font_name": "Arial Bold",
        "align": "left"
    },

    "slide_title": {
        "top": 0.5,
        "left": 2,
        "width": 14,
        "height": 1.5,
        "font_size": 32,
        "bold": True,
        "align": "left"
    },

    "subtitle": {
        "font_size": 25,
        "bold": True,
        "font_name": "Arial Bold",
        "align": "left"
    },

    "text": {
        "font_size": 20,
        "font_name": "Arial",
        "align": "left"
    },

    "content_box": {
        "top": 0.3,
        "left": 1.3,
        "width": 12,
        "height": 6
    },

    "image": {
        "top": 0.3,
        "left": 1.3,
        "width": 12,
        "height": 6,
        "align": "right",
        "scale": 0.5
    }
}
