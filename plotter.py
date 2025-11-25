import matplotlib.pyplot as plt
import io
from datetime import datetime

class Plotter:
    def __init__(self, db):
        self.db = db

    def generate_plot(self, limit=200):
        rows = self.db.query("""
            SELECT timestamp, temperature, humidity 
            FROM measurements 
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows.reverse()
        timestamps = [datetime.fromisoformat(r[0]) for r in rows]
        temps = [r[1] for r in rows]
        hums = [r[2] for r in rows]

        plt.figure(figsize=(10,5))
        plt.plot(timestamps, temps, label="Temperature (°C)")
        plt.plot(timestamps, hums, label="Humidity (%)")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.title("DHT11 Temperature & Humidity History")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf
