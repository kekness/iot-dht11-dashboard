from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from db import Database
from plotter import Plotter
from arduino_logger import ArduinoLogger
import threading
import time

DB_FILE = "data.db"

app = FastAPI(title="DHT11 IoT API")
db = Database(DB_FILE)
plotter = Plotter(db)
arduino = ArduinoLogger(port="COM3", baud=9600)  

def background_logger():
    while True:
        try:
            temp, hum = arduino.get_measurement()
            db.save_measurement(temp, hum)
            print(f"Saved: {temp}°C, {hum}%")
        except Exception as e:
            print("logger error:", e)
        time.sleep(1)  

thread = threading.Thread(target=background_logger, daemon=True)
thread.start()

@app.get("/")
def root():
    return {"status": "ok", "message": "DHT11 API is running"}

@app.get("/latest")
def latest():
    rows = db.query("SELECT timestamp, temperature, humidity FROM measurements ORDER BY id DESC LIMIT 1")
    if not rows:
        return JSONResponse({"error": "No data"}, status_code=404)
    ts, temp, hum = rows[0]
    return {"timestamp": ts, "temperature": temp, "humidity": hum}

@app.get("/history")
def history(limit: int = None):
    if limit:
        rows = db.query("SELECT timestamp, temperature, humidity FROM measurements ORDER BY id DESC LIMIT ?", (limit,))
    else:
        rows = db.query("SELECT timestamp, temperature, humidity FROM measurements ORDER BY id DESC")
    return [{"timestamp": ts, "temperature": t, "humidity": h} for ts, t, h in rows]

@app.get("/average")
def average():
    rows = db.query("SELECT AVG(temperature), AVG(humidity) FROM measurements")
    if not rows or rows[0][0] is None:
        return JSONResponse({"error": "No data"}, status_code=404)
    avg_temp, avg_hum = rows[0]
    return {"avg_temperature": round(avg_temp,2), "avg_humidity": round(avg_hum,2)}

@app.get("/plot")
def plot():
    buf = plotter.generate_plot()
    return StreamingResponse(buf, media_type="image/png")
