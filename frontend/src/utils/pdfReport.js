export function generatePdfReport(record, explanation = null) {
  const reportWindow = window.open("", "_blank");
  if (!reportWindow) {
    alert("Please allow popups to generate the UNSW-NB15 PDF report.");
    return;
  }

  const timestamp = record.timestamp || new Date().toLocaleString();
  const modelName = (record.model_used || "svm").toUpperCase();
  const features = record.features || {};
  const isAttack = record.prediction?.includes("Attack");
  const threatColor = isAttack ? "#dc2626" : "#16a34a";
  const threatBg = isAttack ? "#fef2f2" : "#f0fdf4";

  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>UNSW-NB15 Security Audit Report - ${record.threat}</title>
      <style>
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #0f172a; margin: 0; padding: 40px; background: #fff; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0284c7; padding-bottom: 20px; margin-bottom: 30px; }
        .logo { font-size: 22px; font-weight: 800; color: #0284c7; }
        .card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 24px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th { text-align: left; background: #f1f5f9; padding: 10px; border-bottom: 2px solid #e2e8f0; font-size: 12px; text-transform: uppercase; color: #475569; }
        td { padding: 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; }
        .footer { margin-top: 50px; border-top: 1px solid #e2e8f0; padding-top: 20px; font-size: 11px; color: #94a3b8; text-align: center; }
        @media print { .no-print { display: none; } }
      </style>
    </head>
    <body>
      <div class="no-print" style="margin-bottom: 20px; text-align: right;">
        <button onclick="window.print()" style="background: #0284c7; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer;">
          🖨️ Print / Save as PDF
        </button>
      </div>

      <div class="header">
        <div>
          <div class="logo">QUANTUM IDS — UNSW-NB15 SECURITY REPORT</div>
          <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Hybrid Quantum-Classical Telemetry Analysis</div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 12px; color: #64748b;">Report ID: UNSW-RPT-${Math.floor(Math.random()*899999 + 100000)}</div>
          <div style="font-size: 12px; color: #64748b;">Date: ${timestamp}</div>
        </div>
      </div>

      <div class="card" style="border-left: 6px solid ${threatColor}; background: ${threatBg};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-size: 12px; text-transform: uppercase; color: #64748b; font-weight: 600;">Prediction Result</div>
            <div style="font-size: 26px; font-weight: 800; color: ${threatColor}; margin-top: 4px;">${record.prediction}</div>
          </div>
          <div style="text-align: right;">
            <span style="display: inline-block; padding: 6px 14px; border-radius: 9999px; font-weight: 700; color: ${threatColor}; border: 1px solid ${threatColor};">
              ${record.threat} RISK
            </span>
            <div style="font-size: 13px; color: #475569; font-weight: 600; margin-top: 6px;">
              Confidence: ${record.confidence}%
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <h3 style="margin-top: 0; font-size: 15px; color: #0f172a;">Dataset & Model Metadata</h3>
        <table>
          <tr>
            <td style="color: #64748b;">Dataset Source:</td>
            <td style="font-weight: 600;">UNSW-NB15 Benchmark</td>
            <td style="color: #64748b;">Evaluated Model:</td>
            <td style="font-weight: 600;">${modelName} Classifier</td>
          </tr>
          <tr>
            <td style="color: #64748b;">Feature Scaling:</td>
            <td style="font-weight: 600;">MinMaxScaler (0 to 2π)</td>
            <td style="color: #64748b;">Quantum Feature Map:</td>
            <td style="font-weight: 600;">ZFeatureMap (4 Qubits)</td>
          </tr>
        </table>
      </div>

      <div class="card">
        <h3 style="margin-top: 0; font-size: 15px; color: #0f172a;">PCA Feature Components</h3>
        <table>
          <thead>
            <tr>
              <th>PCA Vector Component</th>
              <th>Sample Value</th>
              <th>UNSW-NB15 Telemetry Metric</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Feature 1 (f1)</td>
              <td style="font-family: monospace;">${features.f1 ?? 'N/A'}</td>
              <td>Flow Rate & Bytes Count</td>
            </tr>
            <tr>
              <td>Feature 2 (f2)</td>
              <td style="font-family: monospace;">${features.f2 ?? 'N/A'}</td>
              <td>Protocol State & Error Flags</td>
            </tr>
            <tr>
              <td>Feature 3 (f3)</td>
              <td style="font-family: monospace;">${features.f3 ?? 'N/A'}</td>
              <td>Session Duration & Packet Load</td>
            </tr>
            <tr>
              <td>Feature 4 (f4)</td>
              <td style="font-family: monospace;">${features.f4 ?? 'N/A'}</td>
              <td>Host Destination TTL & Connection Density</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="footer">
        Generated by Quantum Intrusion Detection System (UNSW-NB15 Edition)
      </div>
    </body>
    </html>
  `;

  reportWindow.document.write(html);
  reportWindow.document.close();
}
