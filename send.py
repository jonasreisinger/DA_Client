from aiohttp import web
import numpy as np
import io
import aiohttp

async def send_npy_file(token):
    print("UPLOAD")
    # Zufälliges NumPy-Array erstellen
    data_np = np.random.rand(100, 100)  # Erzeugt ein 100x100 Array mit Zufallswerten

    # NumPy-Array in einen BytesIO-Puffer speichern
    buffer = io.BytesIO()
    np.save(buffer, data_np)
    buffer.seek(0)  # Zurück zum Anfang des Puffers

    # Header für den Request festlegen, einschließlich Authorization Header
    headers = {
        'Content-Type': 'application/octet-stream',
        'Authorization': f'Bearer {token}'  # Token wird als Bearer Token hinzugefügt
    }

    # Asynchrone HTTP-Session erstellen und POST-Request senden
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8080/upload', data=buffer.getvalue(), headers=headers) as response:
            # Antwort auslesen und ausgeben
            print("Status:", response.status)
            response_text = await response.text()
            print("Response:", response_text)
