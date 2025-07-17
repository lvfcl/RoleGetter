import deepl
import os
import re

DEEPL_API_KEY = "5676e1dd-f5a2-489c-b994-ab8fa383bd4a:fx"

translator = deepl.Translator(DEEPL_API_KEY)

def translate_ass_with_deepl(input_path: str, output_path: str, target_lang="uk"):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Файл {input_path} не найден!")

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    translated_lines = []
    dialogue_pattern = re.compile(
        r"^(Dialogue:\s*\d+,\d+:\d+:\d+\.\d+,\d+:\d+:\d+\.\d+,[^,]*,[^,]*,\d+,\d+,\d+,[^,]*,)(.*)$"
    )

    for line in lines:
        match = dialogue_pattern.match(line)
        if match:
            prefix = match.group(1)
            original_text = match.group(2).strip()

            if original_text:
                try:
                    translated_text = translator.translate_text(original_text, target_lang=target_lang).text
                except Exception as e:
                    print(f"[!] Ошибка перевода строки: {original_text} → {e}")
                    translated_text = original_text
            else:
                translated_text = original_text

            translated_lines.append(prefix + translated_text + "\n")
        else:
            translated_lines.append(line)

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(translated_lines)

