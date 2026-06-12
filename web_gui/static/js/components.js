const AppHeader = {
    props: ['title', 'subtitle'],
    emits: ['show-help'],
    template: `
        <header class="app-header">
            <div class="header-left">
                <a href="/" class="logo-container">
                    <span class="logo-tech">Tech</span><span class="logo-bay">Bay</span>
                </a>
                <p class="app-subtitle">{{ subtitle }}</p>
            </div>
            <button class="help-button" @click="$emit('show-help')" data-tooltip="System Help">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="icon">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z" />
                </svg>
            </button>
        </header>
    `
};

const SearchBox = {
    props: ['query', 'isSearching', 'isImproving'],
    emits: ['update:query', 'search', 'improve'],
    template: `
        <div class="search-box-container">
            <input 
                type="text" 
                :value="query"
                @input="$emit('update:query', $event.target.value)"
                @keypress.enter="$emit('search')"
                placeholder="Ask a question or enter keywords..." 
                class="search-input"
                :disabled="isSearching || isImproving"
            />
            <div data-tooltip="Perform Search">
                <button 
                    @click="$emit('search')" 
                    :disabled="isSearching || isImproving || !query.trim()"
                    class="search-button"
                >
                    <span v-if="isSearching" class="flex-center" style="gap: 0.5rem;">
                        <svg class="spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                        Searching...
                    </span>
                    <span v-else>Search</span>
                </button>
            </div>
            <div data-tooltip="Optimize your query with AI">
                <button 
                    @click="$emit('improve')" 
                    :disabled="isSearching || isImproving || !query.trim()"
                    class="search-button secondary"
                    style="margin-left: 0.5rem;"
                >
                    <span v-if="isImproving">Improving...</span>
                    <span v-else>Improve</span>
                </button>
            </div>
        </div>
    `
};

const HelpModal = {
    props: ['show'],
    emits: ['close'],
    template: `
        <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
            <div class="modal-content">
                <button class="modal-close" @click="$emit('close')">&times;</button>
                <div class="markdown-body">
                    <h1>TechBay Search Help</h1>
                    <p>Welcome to TechBay, your intelligent retrieval system. Use this guide to master our advanced search capabilities.</p>
                    
                    <h2>Operator Cheat Sheet</h2>
                    <table class="help-table">
                        <thead>
                            <tr>
                                <th>Operator</th>
                                <th>Meaning</th>
                                <th>Example</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td><code>AND</code></td><td>Both conditions must be present</td><td><code>laptop AND gaming</code></td></tr>
                            <tr><td><code>OR</code></td><td>Either condition can match</td><td><code>oled OR amoled</code></td></tr>
                            <tr><td><code>NOT</code></td><td>Exclude specific keyword</td><td><code>apple AND NOT phone</code></td></tr>
                            <tr><td><code>EXTREMELY</code></td><td>Absolute top priority match</td><td><code>EXTREMELY quiet</code></td></tr>
                            <tr><td><code>VERY</code></td><td>High priority / Push to top</td><td><code>VERY fast</code></td></tr>
                            <tr><td><code>IMPORTANT</code></td><td>Strict deal-breaker</td><td><code>IMPORTANT enterprise</code></td></tr>
                            <tr><td><code>MILDLY</code></td><td>Minor preference bonus</td><td><code>MILDLY waterproof</code></td></tr>
                            <tr><td><code>SOMEWHAT</code></td><td>Flexible compromise</td><td><code>SOMEWHAT cheap</code></td></tr>
                            <tr><td><code>SLIGHTLY</code></td><td>Maximum safety net</td><td><code>SLIGHTLY discount</code></td></tr>
                        </tbody>
                    </table>

                    <h2>Syntax Rules</h2>
                    <ul>
                        <li><strong>Case Sensitivity:</strong> Operators (AND, OR, NOT) and Modifiers (VERY, IMPORTANT, etc.) must be <strong>UPPERCASE</strong>. Search terms must be <strong>lowercase</strong>.</li>
                        <li><strong>Grouping:</strong> Use parentheses <code>( )</code> to control precedence. Example: <code>(amd OR mac) AND NOT intel</code></li>
                    </ul>

                    <h2>Real-World Examples</h2>
                    <div class="help-example">
                        <strong>High-End Workstation:</strong>
                        <code>workstation AND EXTREMELY ram AND EXTREMELY gpu AND SOMEWHAT liquid AND (amd OR mac) AND NOT intel</code>
                    </div>
                    <div class="help-example">
                        <strong>Wireless Earbuds:</strong>
                        <code>earbuds AND IMPORTANT anc AND VERY battery AND MILDLY wireless</code>
                    </div>
                    <div class="help-example">
                        <strong>Smart Home Clearance:</strong>
                        <code>display AND smart AND zigbee AND (SLIGHTLY discount OR SLIGHTLY clearance) AND NOT used</code>
                    </div>

                    <h2>AI Tools</h2>
                    <p><strong>Improve Button:</strong> Type your request in natural language and click "Improve". Our AI will translate it into the TechBay formal language for you!</p>
                    <p><strong>AI Assistant (RAG):</strong> Every search includes an AI-synthesized answer at the top, citing information directly from the search results.</p>
                </div>
            </div>
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
    computed: {
        renderedMessage() {
            if (!this.data || !this.data.message) return '';
            return marked.parse(this.data.message);
        }
    },
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
                <div class="rag-content markdown-body" v-html="renderedMessage"></div>
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
    HelpModal,
    ErrorAlert,
    RagSection,
    ResultsSection
};
