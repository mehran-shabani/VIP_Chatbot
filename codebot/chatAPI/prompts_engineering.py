def generate_prompt(user_input):
    return [
        {
            "role": "system",
            "content": (
                "شما یک توسعه‌دهنده ارشد در فلاتر و جنگو هستید. "
                "کدهای تولیدی شما باید دقیق، بهینه، کامل و مستند باشند."
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
