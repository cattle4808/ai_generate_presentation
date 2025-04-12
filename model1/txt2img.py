def generator(config: dict, prompt: str) -> str:
    try:
        response = config["client"].images.generate(
            model=config["img_model"],
            prompt=str(prompt),
            n=1,
            size=str(config["image_size"]),
        )

        _ = {
            "prompt": response.data[0].revised_prompt,
            "url": response.data[0].url
        }

        return _["url"]
    except: return
