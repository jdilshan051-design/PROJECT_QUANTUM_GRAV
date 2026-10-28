// Deployed FastAPI service URL (no trailing slash).
window.QUANTUM_GRAV_API_URL = "https://project-quantum-grav-api.vercel.app";
window.quantumGravApi = (path) => `${window.QUANTUM_GRAV_API_URL.replace(/\/$/, "")}${path.startsWith("/") ? path : `/${path}`}`;
