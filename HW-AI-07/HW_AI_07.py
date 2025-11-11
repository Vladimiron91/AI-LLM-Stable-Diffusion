import requests
import io
from PIL import Image
import os
from dotenv import load_dotenv


def setup_env():
    """Загрузка токена HF"""
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        print("HF_TOKEN not found in .env")
        hf_token = input("Enter your HuggingFace token: ")

    return hf_token


def generate_image(prompt, token, negative_prompt="", model_id="CompVis/stable-diffusion-v1-4",
                   num_inference_steps=40):
    """Генерация изображения через Hugging Face Stable Diffusion"""
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "negative_prompt": negative_prompt,
            "num_inference_steps": num_inference_steps
        }
    }

    print(f"\nGenerating: {prompt}")
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    return Image.open(io.BytesIO(response.content))


def save_image(image, filename):
    """Сохранение результата"""
    image.save(filename)
    print(f"Saved: {filename}")
    return filename


def main():
    token = setup_env()

    # ✅ 3 ПРОМПТА: базовый, художественный, сложный (prompt-engineering)
    prompts = [
        # 1 — простой промпт
        "Beautiful sunset over a quiet lake, soft warm colors, realistic landscape",

        # 2 — средний по сложности художественный стиль
        "A futuristic Moscow city with neon lights, flying cars, ultra-detailed, cinematic look, sharp focus",

        # 3 — сложный промпт с prompt-engineering
        (
            "A medieval knight cat cooking soup in a rustic kitchen, ultra-realistic, "
            "8k, highly detailed, volumetric lighting, golden hour, "
            "studio quality, cinematic atmosphere, masterpiece, award-winning illustration"
        ),
    ]

    negative_prompt = (
        "blurry, distorted, low quality, deformed face, extra limbs, bad anatomy, noisy, "
        "pixelated, oversaturated, watermark, text"
    )

    for i, prompt in enumerate(prompts):
        try:
            image = generate_image(
                prompt=prompt,
                token=token,
                negative_prompt=negative_prompt,
                num_inference_steps=35
            )

            filename = f"stable_diffusion_result_{i+1}.png"
            save_image(image, filename)

            try:
                from IPython.display import display
                display(image)
            except ImportError:
                pass

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
