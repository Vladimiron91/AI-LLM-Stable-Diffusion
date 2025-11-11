# Stable Diffusion Image Generator (Hugging Face API)

Этот проект позволяет генерировать изображения с помощью модели  
**Stable Diffusion (CompVis/stable-diffusion-v1-4)** через API Hugging Face.

---

## Функциональность

- Генерация изображений по текстовому запросу (*prompt*)
- Использование `negative_prompt` для улучшения качества
- Сохранение изображений на диск
- Поддержка нескольких запросов подряд
- Работа без GPU (все вычисления выполняет сервер HuggingFace)