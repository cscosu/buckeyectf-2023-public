import { useEffect, useState } from "react";

import "./styles.css";
import candlesImage from "./assets/candles.jpg";
import incenseImage from "./assets/incense.jpg";
import plantsImage from "./assets/plants.jpg";
import Navbar from "./Navbar";

function SatisfactionCounter() {
  const [count, setCount] = useState(Math.floor(Math.random() * 1000) + 12442);

  useEffect(() => {
    const interval = setInterval(() => {
      setCount((c) => c + 1);
    }, 1337);
    return () => clearInterval(interval);
  }, []);

  return <>{count}</>;
}

function Home() {
  return (
    <>
      <div id="ocean" className="full vignette">
        <Navbar />
        <div className="content">
          <h1>Ultimate Spa Experience</h1>
          <p>
            Refresh yourself with our most comprehensive relaxation techniques
          </p>
        </div>
      </div>
      <div id="makeup" className="full vignette">
        <div className="content">
          <h1>Unprecedented customer satisfaction</h1>
          <p>
            <SatisfactionCounter /> customers satisfied... + you
          </p>
          <div style={{ height: "400px" }}></div>
        </div>
      </div>
      <div className="triple vignette">
        <div className="images">
          <img src={incenseImage} />
          <img src={plantsImage} />
          <img src={candlesImage} />
        </div>
      </div>
      <div id="bath" className="full vignette">
        <div className="content">
          <h1>Available near you</h1>
          <p>Visit one of our locations today!</p>
          <div style={{ height: "400px" }}></div>
        </div>
      </div>
    </>
  );
}

export default Home;
