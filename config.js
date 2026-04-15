// API Configuration
// Auto-detect API base URL based on environment

const API_BASE_URL = (() => {
    if (typeof window !== 'undefined') {
        const host = window.location.hostname;
        const protocol = window.location.protocol;
        
        // Local development
        if (host === 'localhost' || host === '127.0.0.1') {
            return 'http://localhost:5000';
        }
        
        // Production - use environment variable or same origin
        const prodApiUrl = window.__API_BASE_URL__ || 
                           `${protocol}//api.${host}` ||
                           `${protocol}//${host}`;
        
        return prodApiUrl;
    }
    
    return 'http://localhost:5000';
})();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { API_BASE_URL };
}
