# Live ISS Location Dashboard

A real-time Streamlit app that tracks the current location of the International Space Station (ISS), displays the astronauts on board, and shows NASA's Astronomy Picture of the Day.

## Features

- Real-time ISS location using Open Notify API
- Live list of astronauts currently aboard the ISS
- NASA Picture of the Day with explanation
- Interactive world map with ISS position marked
- Adjustable auto-refresh interval from 10–60 seconds
- Timezone-adjusted timestamps (PST)

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup Environment Variables

1. [Get a NASA API Key](https://api.nasa.gov/)
2. Create a `.env` file in your project directory:

```
NASA_API_KEY=your_actual_key_here
```

> Your `.env` is included in `.gitignore` for security.

---

##  Running the App

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

##  APIs Used

- [Open Notify API](http://open-notify.org/Open-Notify-API/)
- [NASA APOD (Picture of the Day) API](https://api.nasa.gov/)

---

## Project Structure

```
iss-dashboard/
├── app.py               # Main Streamlit app
├── .env                 # (Not tracked) Holds NASA API key
├── .gitignore           # Ignores .env, __pycache__, etc.
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## 🧠 Author

**Sinuhe Villegas**  
[GitHub](https://github.com/sinuhevillegas)
