import { useEffect, useMemo, useState } from 'react';

const defaultLocation = {
  latitude: '17.385',
  longitude: '78.4867',
};

function App() {
  const [location, setLocation] = useState(defaultLocation);
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchWeather = async (coords = location) => {
    const latitude = Number(coords.latitude);
    const longitude = Number(coords.longitude);

    if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
      setError('Please enter valid latitude and longitude values.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const params = new URLSearchParams({
        latitude: String(latitude),
        longitude: String(longitude),
      });

      const response = await fetch(`http://127.0.0.1:8000/weather?${params.toString()}`);

      if (!response.ok) {
        throw new Error('Unable to fetch weather data.');
      }

      const data = await response.json();
      setWeather(data);
    } catch (err) {
      setError(err.message || 'Something went wrong while loading the weather.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWeather(defaultLocation);
  }, []);

  const hourly = useMemo(() => {
    const source = weather?.hourly;

    if (!source || typeof source !== 'object') {
      return [];
    }

    const entries = Object.entries(source);
    const totalItems = entries.reduce((max, [, values]) => {
      if (Array.isArray(values)) {
        return Math.max(max, values.length);
      }
      return max;
    }, 0);

    return Array.from({ length: totalItems }, (_, index) => {
      const row = {};

      entries.forEach(([key, values]) => {
        row[key] = Array.isArray(values) ? values[index] : null;
      });

      return row;
    });
  }, [weather]);

  const current = hourly[0] || {};
  const nextHours = hourly.slice(0, 12);

  const weatherStatus = (() => {
    const precipitation = Number(current.precipitation ?? 0);
    const wind = Number(current.wind_speed_10m ?? 0);
    const temperature = Number(current.temperature_2m ?? 0);

    if (precipitation > 1.5) {
      return {
        label: 'Raining',
        emoji: '🌧️',
        tone: 'rain',
      };
    }

    if (wind > 25) {
      return {
        label: 'Windy',
        emoji: '💨',
        tone: 'wind',
      };
    }

    if (temperature > 28) {
      return {
        label: 'Sunny',
        emoji: '☀️',
        tone: 'sun',
      };
    }

    return {
      label: 'Cloudy',
      emoji: '⛅',
      tone: 'cloud',
    };
  })();

  const metrics = [
    {
      label: 'Temperature',
      value: `${current.temperature_2m ?? '--'} °C`,
      detail: 'Air temperature',
    },
    {
      label: 'Humidity',
      value: `${current.relative_humidity_2m ?? '--'} %`,
      detail: 'Relative humidity',
    },
    {
      label: 'Rainfall',
      value: `${current.precipitation ?? '--'} mm`,
      detail: 'Rain probability',
    },
    {
      label: 'Wind',
      value: `${current.wind_speed_10m ?? '--'} km/h`,
      detail: 'Wind speed',
    },
  ];

  const handleSubmit = (event) => {
    event.preventDefault();
    fetchWeather(location);
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-wrap">
          <div className="brand-icon">☁️</div>
          <div>
            <p className="eyebrow">Forecast</p>
            <h2>Weather AI</h2>
          </div>
        </div>

        <form className="search-panel" onSubmit={handleSubmit}>
          <label>
            Latitude
            <input
              type="number"
              step="0.0001"
              value={location.latitude}
              onChange={(e) =>
                setLocation((prev) => ({ ...prev, latitude: e.target.value }))
              }
            />
          </label>

          <label>
            Longitude
            <input
              type="number"
              step="0.0001"
              value={location.longitude}
              onChange={(e) =>
                setLocation((prev) => ({ ...prev, longitude: e.target.value }))
              }
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? 'Loading...' : 'Get Weather'}
          </button>
        </form>

        <div className="status-card">
          <p className="small-label">Location</p>
          <strong>
            {Number(location.latitude || 0).toFixed(3)}, {Number(location.longitude || 0).toFixed(3)}
          </strong>
        </div>
      </aside>

      <main className="main-panel">
        <header className="header-row">
          <div>
            <p className="eyebrow">AI-driven hyper-local weather</p>
            <h1>Weather Warning Dashboard</h1>
          </div>
          <div className="header-badge">Live</div>
        </header>

        <div className={`status-banner ${weatherStatus.tone}`}>
          <span className="status-emoji">{weatherStatus.emoji}</span>
          <div>
            <small>Current condition</small>
            <strong>{weatherStatus.label}</strong>
          </div>
        </div>

        {error && <div className="error-box">{error}</div>}

        <section className="metrics-grid">
          {metrics.map((metric) => (
            <article className="metric-card" key={metric.label}>
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
              <small>{metric.detail}</small>
            </article>
          ))}
        </section>

        <section className="forecast-panel">
          <div className="panel-header">
            <h3>Next 12 hours</h3>
          </div>

          <div className="forecast-list">
            {nextHours.map((entry, index) => {
              const temp = Number(entry.temperature_2m ?? 0);
              const relativeHeight = Math.max(20, Math.min(100, (temp + 10) * 2.6));

              return (
                <div className="forecast-item" key={`${entry.time}-${index}`}>
                  <span className="time-label">{entry.time?.slice(11, 16) || '--:--'}</span>
                  <div className="bar-rail">
                    <div className="bar-fill" style={{ height: `${relativeHeight}%` }} />
                  </div>
                  <strong>{temp.toFixed(1)}°</strong>
                </div>
              );
            })}
          </div>
        </section>

        <section className="info-grid">
          <div className="detail-card">
            <h3>Current conditions</h3>
            <ul>
              <li>
                <span>Cloud cover</span>
                <strong>{current.cloud_cover ?? '--'}%</strong>
              </li>
              <li>
                <span>Pressure</span>
                <strong>{current.pressure_msl ?? '--'} hPa</strong>
              </li>
              <li>
                <span>Vapour deficit</span>
                <strong>{current.vapour_pressure_deficit ?? '--'} kPa</strong>
              </li>
            </ul>
          </div>

          <div className="detail-card">
            <h3>Weather summary</h3>
            <p>
              {current.temperature_2m != null
                ? `Current conditions are around ${current.temperature_2m}°C with ${current.relative_humidity_2m}% humidity.`
                : 'Load weather data to view the local summary.'}
            </p>
            <p>
              {current.precipitation != null
                ? `Rainfall is currently ${current.precipitation} mm, and wind is moving at ${current.wind_speed_10m} km/h.`
                : 'No rainfall details yet.'}
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
