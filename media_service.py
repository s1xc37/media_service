import httpx
import io
from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
from PIL import Image  # Используем PIL, она легче и уже в зависимостях

app = FastAPI()

# Загружаем модель один раз
model = YOLO("cvModel.pt")

TARGET_URL = "http://127.0.0.1:8000/eventProcessor/img"

@app.post("/upload")
async def receive_stream(file: UploadFile = File(...)):
    content = await file.read()
    
    # --- CV ПРОВЕРКА ЧЕРЕЗ ULTRALYTICS ---
    # Создаем объект изображения из байтов напрямую
    img = Image.open(io.BytesIO(content))
    
    # Вызываем predict. 
    # conf=0.5 здесь не ставим, чтобы вручную проверить результат
    results = model.predict(img, verbose=False)
    
    # Вытаскиваем максимальный confidence
    max_conf = 0.0
    if len(results[0].boxes) > 0:
        max_conf = float(results[0].boxes.conf.max())

    # УСЛОВИЕ: если модель не уверена (< 0.5), отправляем дальше
    if max_conf < 0.5:
        print(f"Событие подтверждено (conf: {max_conf:.2f}). Отправляем...")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    TARGET_URL,
                    files={"file": (file.filename, content, file.content_type)},
                    data={"metadata": f'{{"confidence": {max_conf}, "source": "yolo26n"}}'}
                )
                return {"status": "forwarded", "yolo_conf": max_conf}
            except Exception as e:
                return {"status": "error", "message": str(e)}
    
    return {"status": "filtered", "yolo_conf": max_conf}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5000)