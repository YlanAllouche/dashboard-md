/**
 * Dashboard tab switching functionality
 * 
 * Handles switching between different dashboard widgets
 * and stores the active tab in localStorage for persistence
 */

const STORAGE_KEY = 'dashboard-active-tab';
const DEFAULT_TAB = 'initiatives-widget';

/**
 * Initialize dashboard tabs
 */
function initDashboardTabs() {
    const tabs = document.querySelectorAll('.dashboard-tabs button');
    const widgets = document.querySelectorAll('.dashboard-widget');

    // Get saved tab or use default
    const savedTab = localStorage.getItem(STORAGE_KEY) || DEFAULT_TAB;
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    // Set initial active tab
    switchTab(savedTab);
}

/**
 * Switch to a specific tab
 * @param {string} tabId - The ID of the tab/widget to show
 */
function switchTab(tabId) {
    const widgets = document.querySelectorAll('.dashboard-widget');
    const tabs = document.querySelectorAll('.dashboard-tabs button');

    // Hide all widgets
    widgets.forEach(widget => widget.classList.remove('active'));

    // Deactivate all tabs
    tabs.forEach(tab => tab.classList.remove('active'));

    // Show the selected widget
    const selectedWidget = document.getElementById(tabId);
    if (selectedWidget) {
        selectedWidget.classList.add('active');
    }

    // Activate the corresponding tab button
    const selectedTab = document.querySelector(`[data-tab="${tabId}"]`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    // Save to localStorage
    localStorage.setItem(STORAGE_KEY, tabId);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initDashboardTabs);
