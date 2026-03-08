import { useState } from "react";
import "./Hero.css";
import bee from "./assets/bee.png";
import logo from "./assets/Logo.png";

export function Hero({ onGenerateClick }) {
  const [isFlying, setIsFlying] = useState(false);

  function runBee() {
    if (isFlying) return;
    setIsFlying(true);

    setTimeout(() => {
      setIsFlying(false);
    }, 1000);
  }

  return (
    <section className="hero">
      <img src={bee} alt="Bee" className={`bee ${isFlying ? "fly" : ""}`} />

      <img
        src={logo}
        alt="Logo"
        className="logo"
        onMouseEnter={runBee}
        style={{ cursor: "pointer" }}
      />

      <h2 className="main-heading">Buzz through your lab reports!</h2>
      <p className="sub-text">
        Your lab data in. Honey-smooth results and precision insights out.
      </p>
      <button className="cta-btn" onClick={onGenerateClick}>
        Generate my results
      </button>
    </section>
  );
}
