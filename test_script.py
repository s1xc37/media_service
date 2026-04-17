import requests
import os
import time

# Адрес твоего Media Service
URL = "http://127.0.0.1:5000/upload"

# Папка, где лежат тестовые фото
SOURCE_FOLDER = "media-Service/val"

def start_streaming():
    if not os.path.exists(SOURCE_FOLDER):
        print(f"Ошибка: Папка {SOURCE_FOLDER} не найдена!")
        return

    # Получаем список всех файлов в папке
    files = [f for f in os.listdir(SOURCE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not files:
        print("В папке нет подходящих изображений.")
        return

    print(f"Начинаю отправку {len(files)} файлов...")

    for filename in files:
        file_path = os.path.join(SOURCE_FOLDER, filename)
        
        # Открываем файл в бинарном режиме
        with open(file_path, "rb") as f:
            print(f"Отправка {filename}...", end=" ")
            
            try:
                # Отправляем файл
                response = requests.post(URL, files={"file": (filename, f, "image/jpeg")})
                
                # Выводим результат от Media Service
                if response.status_code == 200:
                    print(f"OK | Результат: {response.json().get('status')}")
                else:
                    print(f"Ошибка {response.status_code}")
                    
            except Exception as e:
                print(f"Ошибка соединения: {e}")

        # Небольшая пауза, чтобы имитировать интервалы между кадрами
        time.sleep(0.5)

if __name__ == "__main__":
    start_streaming()