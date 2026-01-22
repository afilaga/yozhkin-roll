(function () {
    // Configuration
    const PRESERVED_PARAMS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
    const STORAGE_KEY_PREFIX = 'yozhkin_';

    // 1. Capture & Storage
    try {
        const urlParams = new URLSearchParams(window.location.search);
        PRESERVED_PARAMS.forEach(param => {
            if (urlParams.has(param)) {
                localStorage.setItem(STORAGE_KEY_PREFIX + param, urlParams.get(param));
            }
        });
    } catch (e) {
        console.error('UTM Sync: Storage failed', e);
    }

    // 2. Data Retrieval
    const getStoredParams = () => {
        const data = {};
        PRESERVED_PARAMS.forEach(param => {
            const val = localStorage.getItem(STORAGE_KEY_PREFIX + param);
            if (val) data[param] = val;
        });
        return data;
    };

    // 3. Injection Logic
    const injectIntoForms = () => {
        const params = getStoredParams();
        if (Object.keys(params).length === 0) return;

        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            Object.entries(params).forEach(([key, value]) => {
                // Check if input exists
                let input = form.querySelector(`input[name="${key}"]`);
                if (!input) {
                    input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = key;
                    form.appendChild(input);
                }
                // Always update value to latest (sticky)
                input.value = value;
            });
        });
        console.log(`UTM Sync: Injected params into ${forms.length} forms`, params);
    };

    // 4. Metrica Sync
    const syncMetrica = () => {
        const params = getStoredParams();
        if (Object.keys(params).length > 0 && typeof ym !== 'undefined') {
            // Actual Counter ID from seo_head.html
            ym(91003929, 'params', params);
            console.log('UTM Sync: Pushed to Metrica', params);
        }
    };

    // Initialize
    const init = () => {
        injectIntoForms();
        syncMetrica();

        // Watch for dynamic forms (Tilda popups)
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.addedNodes.length) {
                    injectIntoForms();
                }
            });
        });
        observer.observe(document.body, { childList: true, subtree: true });
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
