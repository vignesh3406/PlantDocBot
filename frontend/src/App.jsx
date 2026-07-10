import { useState, useRef, useCallback } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [previewUri, setPreviewUri] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef(null);

  const pickFile = useCallback((f) => {
    if (f && f.type.startsWith('image/')) {
      setFile(f);
      setPreviewUri(URL.createObjectURL(f));
      setResult(null);
      setError(null);
    }
  }, []);

  const clear = () => {
    setFile(null);
    setPreviewUri(null);
    setResult(null);
    setError(null);
    if (inputRef.current) inputRef.current.value = '';
  };

  const analyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    const fd = new FormData();
    fd.append('file', file);
    try {
      const res = await axios.post('http://127.0.0.1:8000/predict', fd);
      setResult(res.data);
    } catch {
      setError('Could not reach the backend. Make sure it is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  const fmtSize = (b) => {
    if (b < 1024) return b + ' B';
    if (b < 1048576) return (b / 1024).toFixed(1) + ' KB';
    return (b / 1048576).toFixed(1) + ' MB';
  };

  const healthy = result?.disease?.toLowerCase().includes('healthy');
  const conf = result ? (result.confidence * 100).toFixed(1) : 0;
  const prettyDisease = result?.disease?.replace(/___/g, ' — ').replace(/_/g, ' ');

  return (
    <div className="page">
      {/* ── Top bar ── */}
      <header className="topbar">
        <div className="topbar-left">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M7 20h10"/><path d="M10 20c5.5-2.5 8-8 6-13"/><path d="M6.7 8.5c1.5 1 3.3 1.5 5.3 1.5 2 0 3.8-.5 5.3-1.5"/><path d="M14 20c-5.5-2.5-8-8-6-13"/></svg>
          <span className="topbar-name">PlantDoc</span>
        </div>
        <span className="topbar-right">v1.0</span>
      </header>

      {/* ── Content ── */}
      <main className="container">
        <h1 className="page-heading">Leaf disease check</h1>
        <p className="page-desc">
          Drop a photo of any plant leaf below. The model will tell you what's wrong and how to fix it.
        </p>

        {/* Upload */}
        <div className="section-label">Image</div>

        {!file ? (
          <div
            className={`upload-area${dragOver ? ' drag-over' : ''}`}
            onClick={() => inputRef.current?.click()}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => { e.preventDefault(); setDragOver(false); pickFile(e.dataTransfer.files[0]); }}
          >
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            <div className="upload-text">
              Drag an image here, or <strong>browse</strong>
            </div>
            <div className="upload-hint">JPG, PNG — up to 200 MB</div>
            <input
              type="file"
              ref={inputRef}
              accept="image/*"
              onChange={(e) => pickFile(e.target.files[0])}
            />
          </div>
        ) : (
          <div className="file-card fade-in">
            <img className="file-card-image" src={previewUri} alt="Leaf" />
            <div className="file-card-body">
              <div className="file-info">
                <div className="file-name">{file.name}</div>
                <div className="file-size">{fmtSize(file.size)}</div>
              </div>
              <div className="file-actions">
                <button className="btn btn-fill" onClick={analyze} disabled={loading}>
                  {loading ? 'Analyzing…' : 'Analyze'}
                </button>
                <button className="btn btn-outline" onClick={clear}>Remove</button>
              </div>
            </div>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="loader-wrap">
            <div className="loader-dot" />
            <div className="loader-dot" />
            <div className="loader-dot" />
            <span>Running model inference…</span>
          </div>
        )}

        {error && <div className="error-msg">{error}</div>}

        {/* Results */}
        {result && (
          <>
            <div className="divider" />

            <div className="results fade-in">
              {/* Stats */}
              <div className="stat-row">
                <div className="stat-box">
                  <div className="stat-label">Detection</div>
                  <div className={`stat-value ${healthy ? 'green' : 'red'}`}>
                    {prettyDisease}
                  </div>
                </div>
                <div className="stat-box">
                  <div className="stat-label">Confidence</div>
                  <div className="stat-value">{conf}%</div>
                  <div className="conf-bar">
                    <div className="conf-fill" style={{ width: `${conf}%` }} />
                  </div>
                </div>
              </div>

              {/* Treatment */}
              <div className="result-block">
                <div className="result-block-title">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                  Treatment
                </div>
                <div className="result-body">{result.treatment}</div>
              </div>

              {/* Products */}
              {result.products?.length > 0 && (
                <div className="result-block">
                  <div className="result-block-title">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 002-1.61L23 6H6"/></svg>
                    Suggested products
                  </div>
                  <ul className="chip-list">
                    {result.products.map((p, i) => (
                      <li key={i} className="chip">{p}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </>
        )}
      </main>

      <footer className="footer">
        PlantDoc · PyTorch + React · {new Date().getFullYear()}
      </footer>
    </div>
  );
}

export default App;
