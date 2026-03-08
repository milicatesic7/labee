import "./Reports.css";
import { useState } from "react";
import icon from "./assets/icon-base.png";
import arrowd from "./assets/arrow-down.png";
import arrowu from "./assets/arrow-up.png";

function Report({ num, heading, open, onToggle, text, video }) {
  return (
    <div className="report">
      <div className="report-heading">
        <img src={icon} alt="icon" className="icon-img" />
        <h2>Report {num}</h2>
      </div>

      <div className="report-content">
        <div
          className="report-visible"
          onClick={onToggle}
          style={{ cursor: "pointer" }}
        >
          <h3>{heading}</h3>
          <img
            src={open ? arrowu : arrowd}
            className="arrow-icon"
            alt="arrow"
          />
        </div>

        {open && (
          <div className="report-hidden-active">
            <p className="report-text">{text}</p>

            <iframe
              width="300"
              height="200"
              src={video}
              title={`YouTube video player ${num}`}
              allowFullScreen
            ></iframe>
          </div>
        )}
      </div>
    </div>
  );
}

export function Reports() {
  const [openReport, setOpenReport] = useState(null);

  return (
    <section className="reports">
      <Report
        num={1}
        heading="Density of Solid Objects (Hydrostatic Balance)"
        text="Find the density of a solid object, no matter its shape, using a hydrostatic balance and Archimedes’ principle."
        video="https://www.youtube.com/embed/XWZExTDUKHc"
        open={openReport === 1}
        onToggle={() => setOpenReport(openReport === 1 ? null : 1)}
      />

      <Report
        num={2}
        heading="Gravitational Acceleration (Simple Pendulum)"
        text="Measure Earth’s gravitational acceleration by timing the motion of a simple pendulum. 
        By recording how long one full swing takes and using the pendulum formula,
         you can calculate the value of gravity."
        video="https://www.youtube.com/embed/0D8XfW856nw?si=FaI26jTbsv2BC4hj"
        open={openReport === 2}
        onToggle={() => setOpenReport(openReport === 2 ? null : 2)}
      />

      <Report
        num={3}
        heading="Wavelength of Light (Fraunhofer Diffraction)"
        text="Determine the wavelength of light using diffraction through an 
        optical grating. By measuring how light spreads into bright maxima at different angles,
         you can calculate its wavelength with precision."
        video="https://www.youtube.com/embed/clvFSXNVuOA?si=IDgkjbXBRpDlkEiR"
        open={openReport === 3}
        onToggle={() => setOpenReport(openReport === 3 ? null : 3)}
      />
    </section>
  );
}
