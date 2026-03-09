import { useState, useRef } from "react";
import "./index.css";
import { Hero } from "./Hero.jsx";
import { Reports } from "./Reports.jsx";
import { Import } from "./Import.jsx";
import { Footer } from "./Footer.jsx";

export function App() {
  const importSectionRef = useRef(null);
  const scrollToImport = () => {
    importSectionRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };
  return (
    <div>
      <Hero onGenerateClick={scrollToImport} />
      <Reports />
      <div ref={importSectionRef}>
        <Import />
      </div>
      <Footer />
    </div>
  );
}
