// API Configuration
const API_BASE_URL = '/api';

// Store reference to original functions
let originalIncrement = window.increment;
let originalDecrement = window.decrement;

// Enhanced increment function that syncs with backend
async function incrementWithAPI() {
    try {
        const response = await fetch(`${API_BASE_URL}/counter/increment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Update the global data variable and display
            window.data = result.value;
            document.getElementById("counting").innerText = window.data;
        } else {
            console.error('Backend error:', result.error);
            // Fallback to original function
            originalIncrement();
        }
    } catch (error) {
        console.error('Network error:', error);
        // Fallback to original function
        originalIncrement();
    }
}

// Enhanced decrement function that syncs with backend
async function decrementWithAPI() {
    try {
        const response = await fetch(`${API_BASE_URL}/counter/decrement`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Update the global data variable and display
            window.data = result.value;
            document.getElementById("counting").innerText = window.data;
        } else {
            console.error('Backend error:', result.error);
            // Fallback to original function
            originalDecrement();
        }
    } catch (error) {
        console.error('Network error:', error);
        // Fallback to original function
        originalDecrement();
    }
}

// Load initial counter value from backend
async function loadCounterFromAPI() {
    try {
        const response = await fetch(`${API_BASE_URL}/counter`);
        const result = await response.json();
        
        if (response.ok) {
            window.data = result.value;
            document.getElementById("counting").innerText = window.data;
        } else {
            console.error('Error loading counter:', result.error);
        }
    } catch (error) {
        console.error('Network error:', error);
        // Keep the default value from original script
    }
}

// Override the original functions with API-enabled versions
function enableAPIMode() {
    window.increment = incrementWithAPI;
    window.decrement = decrementWithAPI;
    console.log('API mode enabled - counter will sync with backend');
}

// Restore original functions (disable API mode)
function disableAPIMode() {
    window.increment = originalIncrement;
    window.decrement = originalDecrement;
    console.log('API mode disabled - counter will work locally only');
}

// Check if backend is available
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/counter`);
        return response.ok;
    } catch (error) {
        return false;
    }
}

// Initialize API connection when page loads
document.addEventListener('DOMContentLoaded', async function() {
    const isBackendAvailable = await checkBackendConnection();
    
    if (isBackendAvailable) {
        enableAPIMode();
        await loadCounterFromAPI();
        console.log('Connected to backend successfully');
    } else {
        console.log('Backend not available - using local mode');
    }
});

// Utility functions for manual control
window.apiConnector = {
    enable: enableAPIMode,
    disable: disableAPIMode,
    loadFromBackend: loadCounterFromAPI,
    checkConnection: checkBackendConnection
};
