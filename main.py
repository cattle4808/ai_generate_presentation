from model1 import GeneratePresentationModel1

OPENAI_API_KEY=""
gen = GeneratePresentationModel1(api_key=OPENAI_API_KEY)

gen.generate(
    theme="Battlefield: 2042, как он упал",
    lang="ru",
    all_text_color="Black on hex",
    slides=4,
    subtitles=3,
    max_len_text_in_subtitle_text=40,
    image_promt="строго по тематике и на 2D старо диснейский стиль")