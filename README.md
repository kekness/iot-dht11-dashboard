# DHT11 IoT Monitoring System

This project is an end-to-end solution for monitoring temperature and humidity using a **DHT11 sensor** connected to an Arduino. Data is collected in real-time, stored in a SQLite database, and served via a **FastAPI** web API with optional plotting and historical statistics.

---

## Features

* **Arduino-based sensor reading**

  * Reads temperature and humidity from a DHT11 sensor.
  * Sends readings via serial communication.
  * Detects sensor errors and reports them.

* **Python-based data logging**

  * Reads and parses Arduino serial data.
  * Saves measurements to a SQLite database.
  * Runs a background thread to continuously log sensor data.

* **Web API (FastAPI)**

  * Retrieve the latest sensor reading: `/latest`
  * Retrieve historical measurements: `/history?limit=N`
  * Calculate average temperature and humidity: `/average`
  * Generate a temperature/humidity plot: `/plot`

* **Visualization**

  * Plot temperature and humidity trends using matplotlib.
  * Supports limiting the number of points plotted.

---

## Hardware Requirements

* Arduino board (Uno, Mega, etc.)
* DHT11 temperature & humidity sensor
* Jumper wires
* USB cable for Arduino-PC connection

---

## Software Requirements

* Arduino IDE
* Python 3.9+
* Required Python packages:

  ```bash
  pip install -r requirements.txt
  ```

---

## Arduino Setup

1. Connect the DHT11 sensor to your Arduino:

   * Data pin → Digital Pin 2
   * VCC → 5V
   * GND → GND
2. Upload the DHT11_reader.ino Arduino sketch

---

## Python Backend Setup

1. Clone this repository.
2. Update the Arduino COM port in `arduino_logger.py` (default is `"COM3"`).
3. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

4. The API will be accessible at `http://127.0.0.1:8000`.

---

## API Endpoints

| Endpoint   | Method | Description                                                        |
| ---------- | ------ | ------------------------------------------------------------------ |
| `/`        | GET    | Health check, returns API status.                                  |
| `/latest`  | GET    | Returns the latest temperature & humidity reading.                 |
| `/history` | GET    | Returns historical measurements, optional `limit` query parameter. |
| `/average` | GET    | Returns average temperature and humidity.                          |
| `/plot`    | GET    | Returns a PNG plot of recent temperature & humidity readings.      |

---

## Project Structure

```
.
├── arduino_logger.py   # Reads data from Arduino via serial
├── db.py               # SQLite database handler
├── plotter.py          # Generates plots of measurements
├── main.py             # FastAPI application
├── data.db             # SQLite database file
└── README.md           # Project documentation
```

---

## Notes

* Ensure the Arduino is connected to the correct COM port.
* The logger thread continuously polls the Arduino every second.
* The SQLite database stores timestamps in ISO format for easy querying.
* Matplotlib is used to generate plots in-memory for API responses.

---

This setup provides a complete IoT monitoring system with **real-time logging, storage, API access, and visualization**.
