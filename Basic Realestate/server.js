const http = require("http");
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const PORT = 3000;
const LEADS_FILE = path.join(__dirname, "leads.txt");
const OUTPUT_CSV = path.join(__dirname, "leads_output.csv");

const FIELD_MAP = {
  name: "name",
  email: "email",
  address: "Address",
  company: "Company",
  propertyaddress: "PropertyAddress",
  "property address": "PropertyAddress",
  city: "City",
  state: "State",
  country: "Country",
};

// Track pipeline state
let pipelineRunning = false;
let pipelineLogs = [];

function parseCSV(text) {
  const lines = text.trim().split(/\r?\n/);
  if (lines.length < 2) throw new Error("CSV must have a header row and at least one data row");
  const headers = lines[0].split(",").map((h) => h.trim().replace(/^"|"$/g, ""));
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) continue;
    const values = [];
    let current = "", inQuotes = false;
    for (let c = 0; c < line.length; c++) {
      if (line[c] === '"') { inQuotes = !inQuotes; }
      else if (line[c] === "," && !inQuotes) { values.push(current.trim()); current = ""; }
      else { current += line[c]; }
    }
    values.push(current.trim());
    const row = {};
    headers.forEach((h, idx) => { row[h] = values[idx] || ""; });
    rows.push(row);
  }
  return rows;
}

function rowsToLeads(rows) {
  return rows.map((row) => {
    const lead = {};
    for (const [rawKey, rawVal] of Object.entries(row)) {
      const normalized = rawKey.trim().toLowerCase();
      const outputKey = FIELD_MAP[normalized];
      if (outputKey) lead[outputKey] = rawVal;
    }
    return lead;
  });
}

function parseMultipart(body, boundary) {
  const parts = body.split(`--${boundary}`);
  let filename = "", fileContent = null, fileType = "";
  for (const part of parts) {
    if (part.includes('filename="')) {
      const fnMatch = part.match(/filename="([^"]+)"/);
      if (fnMatch) filename = fnMatch[1];
      const ctMatch = part.match(/Content-Type: ([^\r\n]+)/);
      if (ctMatch) fileType = ctMatch[1].trim();
      const contentStart = part.indexOf("\r\n\r\n");
      if (contentStart !== -1) {
        fileContent = part.slice(contentStart + 4);
        fileContent = fileContent.replace(/\r\n$/, "");
      }
    }
  }
  return { filename, fileContent, fileType };
}

const server = http.createServer((req, res) => {

  // Serve HTML
  if (req.method === "GET" && req.url === "/") {
    const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(html);
    return;
  }

  // Download leads.txt
  if (req.method === "GET" && req.url === "/download") {
    if (!fs.existsSync(LEADS_FILE)) {
      res.writeHead(404, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "No leads file yet" }));
      return;
    }
    const data = fs.readFileSync(LEADS_FILE, "utf8");
    res.writeHead(200, {
      "Content-Type": "application/json",
      "Content-Disposition": 'attachment; filename="leads.txt"',
    });
    res.end(data);
    return;
  }

  // Download leads_output.csv
  if (req.method === "GET" && req.url === "/output") {
    if (!fs.existsSync(OUTPUT_CSV)) {
      res.writeHead(404, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Output CSV not ready yet" }));
      return;
    }
    const data = fs.readFileSync(OUTPUT_CSV);
    res.writeHead(200, {
      "Content-Type": "text/csv",
      "Content-Disposition": 'attachment; filename="leads_output.csv"',
    });
    res.end(data);
    return;
  }

  // Poll pipeline status
  if (req.method === "GET" && req.url === "/status") {
    const outputReady = fs.existsSync(OUTPUT_CSV);
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
      running: pipelineRunning,
      outputReady,
      logs: pipelineLogs.slice(-50), // last 50 lines
    }));
    return;
  }

  // Run the Python pipeline
  if (req.method === "POST" && req.url === "/run") {
    if (pipelineRunning) {
      res.writeHead(409, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Pipeline already running" }));
      return;
    }

    if (!fs.existsSync(LEADS_FILE)) {
      res.writeHead(400, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "No leads.txt found — upload a file first" }));
      return;
    }

    pipelineRunning = true;
    pipelineLogs = ["Starting pipeline..."];

    // Delete old output so UI doesn't show stale file as ready
    if (fs.existsSync(OUTPUT_CSV)) fs.unlinkSync(OUTPUT_CSV);

    const python = spawn("python3", ["leadParser.py"], { cwd: __dirname });

    python.stdout.on("data", (data) => {
      const lines = data.toString().split("\n").filter(Boolean);
      pipelineLogs.push(...lines);
      console.log("[pipeline]", data.toString().trim());
    });

    python.stderr.on("data", (data) => {
      const lines = data.toString().split("\n").filter(Boolean);
      pipelineLogs.push(...lines.map(l => `⚠ ${l}`));
      console.error("[pipeline err]", data.toString().trim());
    });

    python.on("close", (code) => {
      pipelineRunning = false;
      if (code === 0) {
        pipelineLogs.push("✓ Pipeline complete");
        console.log("[pipeline] done");
      } else {
        pipelineLogs.push(`✗ Pipeline exited with code ${code}`);
        console.error(`[pipeline] exited with code ${code}`);
      }
    });

    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ started: true }));
    return;
  }

  // Upload spreadsheet
  if (req.method === "POST" && req.url === "/upload") {
    const contentType = req.headers["content-type"] || "";
    const boundaryMatch = contentType.match(/boundary=(.+)$/);
    if (!boundaryMatch) {
      res.writeHead(400, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "No boundary in multipart" }));
      return;
    }
    const boundary = boundaryMatch[1];
    const chunks = [];
    req.on("data", (chunk) => chunks.push(chunk));
    req.on("end", () => {
      try {
        const rawBody = Buffer.concat(chunks).toString("binary");
        const { filename, fileContent } = parseMultipart(rawBody, boundary);
        const ext = path.extname(filename).toLowerCase();
        let rows = [];
        if (ext === ".csv") {
          rows = parseCSV(fileContent);
        } else if (ext === ".xlsx" || ext === ".xls") {
          try {
            const XLSX = require("xlsx");
            const buf = Buffer.from(fileContent, "binary");
            const workbook = XLSX.read(buf, { type: "buffer" });
            const sheet = workbook.Sheets[workbook.SheetNames[0]];
            rows = XLSX.utils.sheet_to_json(sheet, { defval: "" });
          } catch (e) {
            res.writeHead(500, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ error: "xlsx package not installed. Run: npm install xlsx" }));
            return;
          }
        } else {
          res.writeHead(400, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ error: "Only .csv and .xlsx files are supported" }));
          return;
        }
        const leads = rowsToLeads(rows);
        fs.writeFileSync(LEADS_FILE, JSON.stringify(leads, null, 4), "utf8");
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ success: true, count: leads.length, leads }));
      } catch (err) {
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }

  // Save pre-mapped JSON
  if (req.method === "POST" && req.url === "/save") {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      try {
        const leads = JSON.parse(Buffer.concat(chunks).toString());
        fs.writeFileSync(LEADS_FILE, JSON.stringify(leads, null, 4), "utf8");
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ success: true }));
      } catch (e) {
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  res.writeHead(404);
  res.end("Not found");
});

server.listen(PORT, () => {
  console.log(`\n✅ Leads converter running at http://localhost:${PORT}\n`);
});