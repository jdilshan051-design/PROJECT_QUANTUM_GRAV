// Set this to the deployed FastAPI service URL (no trailing slash).
// Example: https://quantum-grav-api.onrender.com
window.QUANTUM_GRAV_API_URL = "https://YOUR-BACKEND.onrender.com";
window.quantumGravApi = (path) => `${window.QUANTUM_GRAV_API_URL.replace(/\/$/, "")}${path.startsWith("/") ? path : `/${path}`}`;
