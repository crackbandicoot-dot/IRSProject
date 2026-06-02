const AppHeader = {
    props: ['title', 'subtitle'],
    template: `
        <header class="app-header">
            <h1 class="app-title">{{ title }}</h1>
            <p class="app-subtitle">{{ subtitle }}</p>
        </header>
    `
};

const SearchBox = {
    props: ['query', 'isSearching'],
    emits: ['update:query', 'search'],
    template: `
        <div class="search-box-container">
            <input 
                type="text" 
                :value="query"
                @input="$emit('update:query', $event.target.value)"
                @keypress.enter="$emit('search')"
                placeholder="Ask a question or enter keywords..." 
                class="search-input"
                :disabled="isSearching"
            />
            <button 
                @click="$emit('search')" 
                :disabled="isSearching || !query.trim()"
                class="search-button"
            >
                <span v-if="isSearching" class="flex-center" style="gap: 0.5rem;">
                    <svg class="spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    Searching...
                </span>
                <span v-else>Search</span>
            </button>
        </div>
    `
};

const ErrorAlert = {
    props: ['message'],
    template: `
        <div class="alert-error">
            <div>
                <p style="font-weight: bold;">Error</p>
                <p>{{ message }}</p>
            </div>
        </div>
    `
};

const RagSection = {
    props: ['data'],
    template: `
        <div class="rag-container">
            <div v-if="data.error" class="rag-error">
                <strong>RAG Assistant Error:</strong> {{ data.error }}
            </div>
            <div v-else-if="data.message" class="rag-message">
                <div class="rag-indicator"></div>
                <div class="rag-header">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="icon"><path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" /></svg>
                    AI Assistant
                </div>
                <div class="rag-content">{{ data.message }}</div>
            </div>
        </div>
    `
};

const ResultsSection = {
    props: ['data'],
    methods: {
        openUrl(url) {
            if (url) window.open(url, '_blank');
        }
    },
    template: `
        <div>
            <h2 class="section-title">Search Results</h2>
            
            <div v-if="data.error" class="rag-error" style="margin-bottom: 1.5rem;">
                <strong>Search Error:</strong> {{ data.error }}
            </div>
            
            <div v-else-if="data.data && data.data.length > 0" class="results-list">
                <div v-for="(item, index) in data.data" :key="index" 
                     class="result-card"
                     @click="openUrl(item.url)"
                     :style="item.url ? 'cursor: pointer;' : ''">
                    <a v-if="item.url" :href="item.url" target="_blank" class="result-title" @click.stop>
                        {{ item.title || item.doc_id || 'Untitled Document' }}
                    </a>
                    <h3 v-else class="result-title">
                        {{ item.title || item.doc_id || 'Untitled Document' }}
                    </h3>
                    
                    <div class="result-score">
                        Relevance Score: {{ typeof item.score === 'number' ? item.score.toFixed(4) : item.score }}
                    </div>
                    
                    <p class="result-snippet" v-html="item.snippet || item.content || 'No description available.'"></p>
                </div>
            </div>
            
            <div v-else class="no-results">
                <svg class="icon-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p style="font-size: 1.125rem;">No results found for your query.</p>
            </div>
        </div>
    `
};

globalThis.AppComponents = {
    AppHeader,
    SearchBox,
    ErrorAlert,
    RagSection,
    ResultsSection
};
