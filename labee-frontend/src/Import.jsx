import { useState, useRef, useEffect } from "react";
import { Results } from "./Results.jsx";
import "./Import.css";
import icon from "./assets/icon-base-small.png";

export function Import() {
  const [selectedReport, setSelectedReport] = useState(null);
  const [imageObjects, setImageObjects] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const [backendData, setBackendData] = useState(null); // NOVO

  const fileInputRef = useRef(null);
  const resultsRef = useRef(null);

  useEffect(() => {
    if (showResults && resultsRef.current) {
      resultsRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, [showResults]);

  const handleImageUpload = (event) => {
    const files = Array.from(event.target.files);

    if (imageObjects.length + files.length > 6) {
      alert("Error: Limit of images exceeded (max 6).");
      return;
    }

    const newObjects = files.map((file) => ({
      file: file,
      url: URL.createObjectURL(file),
    }));

    setImageObjects((prev) => [...prev, ...newObjects]);
  };

  const handleRun = async () => {
    if (!selectedReport) {
      alert("Warning: Please select a report type first!");
      return;
    }
    if (imageObjects.length === 0) {
      alert("Warning: Please upload at least one image!");
      return;
    }

    const formData = new FormData();
    imageObjects.forEach((obj) => {
      formData.append("images", obj.file);
    });

    const reportNumber = selectedReport.replace("Report ", "");
    formData.append("report", reportNumber);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        console.log("Rezultati sa bekenda:", data);

        setBackendData(data); // NOVO
        setShowResults(true);
      } else {
        alert("Server error.");
      }
    } catch (error) {
      console.error("Greška pri slanju:", error);
      alert("Could not connect to the server.");
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <>
      <section className="lab-run-container">
        <div className="lab-controls">
          <button className="btn-select" onClick={triggerFileInput}>
            Select images
          </button>
          <input
            type="file"
            multiple
            accept="image/*"
            ref={fileInputRef}
            onChange={handleImageUpload}
            style={{ display: "none" }}
          />

          <div className="report-list">
            {["Report 1", "Report 2", "Report 3"].map((report) => (
              <div
                key={report}
                className={`report-item ${selectedReport === report ? "active" : ""}`}
                onClick={() => setSelectedReport(report)}
              >
                <img src={icon} alt="icon" /> {report}
              </div>
            ))}
          </div>
        </div>

        <div className="preview-grid">
          {imageObjects.map((obj, index) => (
            <div key={index} className="preview-box-wrapper">
              <div className="preview-box">
                <img src={obj.url} alt="upload" className="uploaded-img" />
              </div>
              <span className="page-label">page: {index + 1}</span>
            </div>
          ))}
        </div>

        <div className="run-area">
          <button className="btn-run" onClick={handleRun}>
            Run Labee
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
