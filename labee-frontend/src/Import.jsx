import { useState, useRef, useEffect } from "react";
import { Results } from "./Results.jsx";
import "./Import.css";
import icon1 from "./assets/report1-icon.svg";
import icon2 from "./assets/report2-icon.svg";
import icon3 from "./assets/report3-icon.svg";
import bee from "./assets/bee-fly.png";

export function Import() {
  const [selectedReport, setSelectedReport] = useState(null);
  const [imageObject, setImageObject] = useState(null);
  const [showResults, setShowResults] = useState(false);
  const [backendData, setBackendData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const fileInputRef = useRef(null);
  const resultsRef = useRef(null);

  const reports = [
    { id: "Report 1", label: "Report 1", icon: icon1 },
    { id: "Report 2", label: "Report 2", icon: icon2 },
    { id: "Report 3", label: "Report 3", icon: icon3 },
  ];

  useEffect(() => {
    if (showResults && resultsRef.current) {
      resultsRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, [showResults]);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImageObject({
        file: file,
        url: URL.createObjectURL(file),
      });
    }
  };

  const handleRun = async () => {
    if (!selectedReport) {
      alert("Warning: Please select a report type first!");
      return;
    }
    if (!imageObject) {
      alert("Warning: Please upload an image!");
      return;
    }

    setIsLoading(true);
    setShowResults(false);

    const formData = new FormData();
    formData.append("images", imageObject.file);

    let reportOption = "1";
    if (selectedReport === "Report 2") reportOption = "2";
    if (selectedReport === "Report 3") reportOption = "3";

    formData.append("report", reportOption);

    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        setBackendData(data);
        setShowResults(true);
      } else {
        alert("Server error.");
      }
    } catch (error) {
      console.error("Greška pri slanju:", error);
      alert("Could not connect to the server.");
    } finally {
      setIsLoading(false);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  const BeeSwarm = () => {
    const bees = Array.from({ length: 5 });
    return (
      <>
        {bees.map((_, i) => {
          const isLeftToRight = i % 2 === 0;
          return (
            <img
              key={i}
              src={bee}
              className={`natural-bee ${isLeftToRight ? "ltr" : "rtl"}`}
              style={{
                top: `${20 + i * 15}%`,
                animationDelay: `${i * 1.8}s`,
                animationDuration: `${8 + Math.random() * 2}s`,
                width: "100px",
                zIndex: 9999,
              }}
              alt="bee"
            />
          );
        })}
      </>
    );
  };

  return (
    <>
      {isLoading && <BeeSwarm />}

      <section
        className={`lab-run-container ${isLoading ? "blur-effect" : ""}`}
      >
        <div className="lab-controls">
          <button className="btn-select" onClick={triggerFileInput}>
            Select image
          </button>
          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            onChange={handleImageUpload}
            style={{ display: "none" }}
          />

          <div className="report-list">
            {reports.map((report) => (
              <div
                key={report.id}
                className={`report-item ${selectedReport === report.id ? "active" : ""}`}
                onClick={() => setSelectedReport(report.id)}
              >
                <img
                  src={report.icon}
                  alt={report.label}
                  className="report-icon"
                />
                <span>{report.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="preview-area">
          <div
            className={`preview-box ${!imageObject ? "empty" : ""}`}
            onClick={triggerFileInput}
          >
            {imageObject ? (
              <img
                src={imageObject.url}
                alt="upload"
                className="uploaded-img"
              />
            ) : (
              <div className="dash-placeholder">
                <span className="plus-icon">+</span>
                <span className="placeholder-text">Drop your lab photo</span>
              </div>
            )}
          </div>
        </div>

        <div className="run-area">
          <button className="btn-run" onClick={handleRun}>
            RUN LABEE
          </button>
        </div>
      </section>

      {showResults && (
        <div ref={resultsRef}>
          <Results report={selectedReport} data={backendData} />
        </div>
      )}
    </>
  );
}
