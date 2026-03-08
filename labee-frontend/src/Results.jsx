import { useState, useEffect } from "react";
import "./Results.css";

export function Results({ report, data }) {
  const reportId = report ? report.replace(/\D/g, "") : "1";

  const [localData, setLocalData] = useState(null);

  useEffect(() => {
    if (data) {
      console.log("DATA FROM BACKEND:", data);
      setLocalData(data);
      return;
    }

    // fallback mock ako backend jos nije povezan
    const mock = {
      1: {
        mass: "7.6",
        seemingMass: "6.8",
        density: "2850.42",
        finalResult: "2850.4 ± 25.0",
      },
    };

    setLocalData(mock[reportId]);
  }, [reportId, data]);

  if (!localData) return null;

  return (
    <div>
      <h2>Backend Result</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
