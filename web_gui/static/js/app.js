const { createApp, ref } = Vue;

const app = createApp({
    components: globalThis.AppComponents,
    setup() {
        const query = ref('');
        const isSearching = ref(false);
        const hasSearched = ref(false);
        const globalError = ref(null);
        
        const ragData = ref(null);
        const resultsData = ref(null);

        const performSearch = async () => {
            const q = query.value.trim();
            if (!q || isSearching.value) return;

            isSearching.value = true;
            hasSearched.value = true;
            globalError.value = null;
            ragData.value = null;
            resultsData.value = null;

            try {
                const response = await fetch("/api/search", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: q })
                });

                if (!response.ok) {
                    throw new Error('Server returned status: ' + response.status);
                }

                const data = await response.json();
                ragData.value = data.rag;
                resultsData.value = data.results;
                
            } catch (err) {
                globalError.value = err.message || "An unexpected error occurred.";
                console.error(err);
            } finally {
                isSearching.value = false;
            }
        };

        return {
            query,
            isSearching,
            hasSearched,
            performSearch,
            globalError,
            ragData,
            resultsData
        };
    }
});

app.mount('#app');
