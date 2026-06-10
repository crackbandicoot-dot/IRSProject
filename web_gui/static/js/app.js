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
                // First call: start search and return results
                ragData.value = { message: "Preparing AI answer..." };
                
                const response = await fetch("/api/search", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: q })
                });

                if (!response.ok) {
                    throw new Error('Server returned status: ' + response.status);
                }

                const data = await response.json();
                resultsData.value = data.results;
                const queryId = data.id;
                
                // Allow user to interact with the search box again while RAG prepares
                isSearching.value = false;

                // Second call: get RAG results
                const ragResponse = await fetch(`/api/rag/${queryId}`);
                if (!ragResponse.ok) {
                    throw new Error('Server returned status: ' + ragResponse.status);
                }

                const ragJson = await ragResponse.json();
                ragData.value = ragJson.rag;
                
            } catch (err) {
                globalError.value = err.message || "An unexpected error occurred.";
                console.error(err);
                
                if (isSearching.value) {
                    isSearching.value = false;
                }
            }
        };

        const improveQuery = async () => {
            const q = query.value.trim();
            if (!q || isSearching.value) return;

            isSearching.value = true;
            globalError.value = null;

            try {
                const response = await fetch("/api/improve_query", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: q })
                });

                if (!response.ok) {
                    throw new Error('Server returned status: ' + response.status);
                }

                const data = await response.json();
                if (data.improved_query && data.improved_query.improved_query) {
                    query.value = data.improved_query.improved_query;
                } else if (data.improved_query && data.improved_query.error) {
                    globalError.value = data.improved_query.error;
                }
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
            improveQuery,
            globalError,
            ragData,
            resultsData
        };
    }
});

app.mount('#app');
