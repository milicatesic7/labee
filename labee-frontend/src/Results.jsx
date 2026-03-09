import "./Results.css";
import logo from "./assets/Logo.png";

export function Results({ report, data }) {
  const reportId = report ? report.replace(/\D/g, "") : "1";

  if (!data) return null;

  const handleRefresh = () => {
    window.location.reload();
  };

  const RenderHydrostaticDensity = () => {
    const { measurements = {}, results = {} } = data.hydrostatic_density || {};
    return (
      <div className="report-one-layout">
        <div className="data-row">
          <span>Mass (m):</span>
          <div className="cell mini static">{measurements.m}</div>
          <span>kg</span>
        </div>
        <div className="data-row">
          <span>Seeming Mass (m1):</span>
          <div className="cell mini static">{measurements.m1}</div>
          <span>kg</span>
        </div>
        <hr className="results-hr" />
        <div className="data-row result-highlight">
          <span>Density (rho):</span>
          <div className="cell long">{results.rho || "0"} kg/m³</div>
        </div>
      </div>
    );
  };

  const RenderAcceleration = () => {
    const gravity = data.gravity || {};
    const meas = gravity.measurements || {};
    const res = gravity.results || {};

    const ls = meas.ls || [0, 0, 0, 0, 0];
    const T2 = meas.T_squared || [0, 0, 0, 0, 0];

    return (
      <div className="report-two-layout">
        <div className="table-wrapper">
          <table className="report-table">
            <thead>
              <tr>
                <th>i</th>
                <th>ls [m]</th>
                <th>T² [s²]</th>
              </tr>
            </thead>
            <tbody>
              {ls.map((val, idx) => (
                <tr key={idx}>
                  <td>{idx + 1}.</td>
                  <td>{val?.toFixed(4)}</td>
                  <td>{T2[idx]?.toFixed(4)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="math-results">
          <div className="data-row">
            <span>Slope Coefficient (a):</span>
            <div className="cell long">
              <strong>{res.a || "0"}</strong> s²/m
            </div>
          </div>
          <div className="data-row">
            <span>Gravity (g):</span>
            <div className="cell mini static">
              <strong>{res.g || "0"}</strong>
            </div>
            <span>m/s²</span>
          </div>
        </div>
      </div>
    );
  };

  const RenderGrating = () => {
    const { grating = {} } = data;
    const colors = ["blue", "green", "red"];
    return (
      <div className="report-three-layout">
        <div className="table-wrapper">
          <table className="report-table">
            <thead>
              <tr>
                <th>Color</th>
                <th>Order (m)</th>
                <th>theta_L [°]</th>
                <th>theta_D [°]</th>
                <th>theta_m [°]</th>
                <th>lambda [nm]</th>
              </tr>
            </thead>
            <tbody>
              {colors.map((color) =>
                ["m1", "m2"].map((order) => {
                  const item = grating[order]?.[color] || {};
                  return (
                    <tr key={`${color}-${order}`}>
                      <td style={{ color: color, fontWeight: "bold" }}>
                        {color.toUpperCase()}
                      </td>
                      <td>{order[1]}</td>
                      <td>{item.theta_L}</td>
                      <td>{item.theta_D}</td>
                      <td>{item.theta_m?.toFixed(2)}</td>
                      <td style={{ fontWeight: "bold" }}>
                        {item.lambda_nm?.toFixed(1)}
                      </td>
                    </tr>
                  );
                }),
              )}
            </tbody>
          </table>
        </div>
        <div className="averages-block">
          <h3>Average Wavelengths (lambda_nm):</h3>
          {colors.map((color) => (
            <div className="data-row" key={color}>
              <span style={{ width: "80px" }}>{color}:</span>
              <div
                className="cell long"
                style={{ borderLeft: `5px solid ${color}` }}
              >
                {Number(grating.average?.[color] || 0).toFixed(2)} nm
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderContent = () => {
    switch (reportId) {
      case "1":
        return <RenderHydrostaticDensity />;
      case "2":
        return <RenderAcceleration />;
      case "3":
        return <RenderGrating />;
      default:
        return <div className="final-box">Unknown Report Format</div>;
    }
  };

  return (
    <section className="results-container">
      <div className="results-card">
        <div className="results-header">
          <h2 className="results-title">Analysis - Report {reportId}</h2>
          <img src={logo} alt="logo" height="50px"></img>
        </div>

        {renderContent()}

        <div
          className="edit-controls-wrapper"
          style={{ justifyContent: "center" }}
        >
          <button className="btn-rerun-text" onClick={handleRefresh}>
            RUN LABEE AGAIN
          </button>
        </div>
      </div>
    </section>
  );
}
