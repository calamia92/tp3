// Configuration de l'API
const API_BASE_URL = window.location.origin + '/api/sentiment';

// Éléments DOM
const textInput = document.getElementById('textInput');
const charCount = document.getElementById('charCount');
const analyzeBtn = document.getElementById('analyzeBtn');
const analyzeSentencesBtn = document.getElementById('analyzeSentencesBtn');
const loadHistoryBtn = document.getElementById('loadHistoryBtn');
const results = document.getElementById('results');
const resultContent = document.getElementById('resultContent');
const loading = document.getElementById('loading');
const history = document.getElementById('history');
const sentimentForm = document.getElementById('sentimentForm');

// Configuration CSRF pour Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Headers par défaut pour les requêtes
const defaultHeaders = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken
};

// Compteur de caractères
textInput.addEventListener('input', function() {
    const count = this.value.length;
    charCount.textContent = count;
    
    if (count > 9000) {
        charCount.style.color = '#ef4444';
    } else if (count > 7000) {
        charCount.style.color = '#f59e0b';
    } else {
        charCount.style.color = '#6b7280';
    }
});

// Fonctions utilitaires
function showSection(element) {
    element.classList.remove('hidden');
}

function hideSection(element) {
    element.classList.add('hidden');
}

function showLoading() {
    showSection(loading);
    hideSection(results);
}

function hideLoading() {
    hideSection(loading);
}

// Fonction pour créer la barre de confiance
function createConfidenceBar(confidence, sentiment) {
    const percentage = Math.round(confidence * 100);
    const colorMap = {
        positive: '#10b981',
        negative: '#ef4444',
        neutral: '#6b7280'
    };
    
    return `
        <div class="confidence-bar">
            <div class="confidence-bar-label">
                <span>Confiance</span>
                <span>${percentage}%</span>
            </div>
            <div class="confidence-progress">
                <div class="confidence-fill" 
                     style="width: ${percentage}%; background-color: ${colorMap[sentiment] || '#6b7280'}">
                </div>
            </div>
        </div>
    `;
}

// Fonction pour formater le sentiment
function formatSentiment(sentiment, confidence) {
    const sentimentMap = {
        positive: { label: 'Positif', icon: 'fas fa-smile', class: 'sentiment-positive' },
        negative: { label: 'Négatif', icon: 'fas fa-frown', class: 'sentiment-negative' },
        neutral: { label: 'Neutre', icon: 'fas fa-meh', class: 'sentiment-neutral' }
    };
    
    const config = sentimentMap[sentiment] || sentimentMap.neutral;
    
    return `
        <div class="sentiment-result ${config.class}">
            <i class="${config.icon}"></i>
            <span>${config.label}</span>
            <span>(${Math.round(confidence * 100)}%)</span>
        </div>
    `;
}

// Fonction pour analyser un texte
async function analyzeSentiment() {
    const text = textInput.value.trim();
    
    if (!text) {
        alert('Veuillez entrer un texte à analyser.');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze/`, {
            method: 'POST',
            headers: defaultHeaders,
            body: JSON.stringify({ text })
        });
        
        if (!response.ok) {
            throw new Error(`Erreur ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        resultContent.innerHTML = `
            <div class="analysis-result">
                <h4><i class="fas fa-chart-line"></i> Analyse du sentiment</h4>
                <div class="analyzed-text">
                    <strong>Texte analysé :</strong>
                    <p style="font-style: italic; margin-top: 0.5rem;">"${data.text}"</p>
                </div>
                
                ${formatSentiment(data.sentiment, data.confidence)}
                ${createConfidenceBar(data.confidence, data.sentiment)}
                
                ${data.details ? `
                    <div class="details" style="margin-top: 1rem; font-size: 0.875rem; color: #6b7280;">
                        <strong>Détails :</strong>
                        <div style="margin-top: 0.5rem;">
                            Score positif: ${Math.round((data.details.positive_score || 0) * 100)}% |
                            Score négatif: ${Math.round((data.details.negative_score || 0) * 100)}%
                        </div>
                    </div>
                ` : ''}
                
                <div style="margin-top: 1rem; font-size: 0.75rem; color: #9ca3af;">
                    Analysé le ${new Date().toLocaleString('fr-FR')}
                </div>
            </div>
        `;
        
        showSection(results);
        loadHistory();
        
    } catch (error) {
        console.error('Erreur:', error);
        resultContent.innerHTML = `
            <div class="error-result" style="color: #ef4444; padding: 1rem; background: #fef2f2; border-radius: 0.5rem;">
                <i class="fas fa-exclamation-triangle"></i>
                Erreur lors de l'analyse : ${error.message}
            </div>
        `;
        showSection(results);
    } finally {
        hideLoading();
    }
}

// Fonction pour analyser par phrases
async function analyzeSentences() {
    const text = textInput.value.trim();
    
    if (!text) {
        alert('Veuillez entrer un texte à analyser.');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze-sentences/`, {
            method: 'POST',
            headers: defaultHeaders,
            body: JSON.stringify({ text })
        });
        
        if (!response.ok) {
            throw new Error(`Erreur ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        let sentencesHTML = '';
        if (data.sentences && data.sentences.length > 0) {
            sentencesHTML = data.sentences.map((sentence, index) => `
                <div class="sentence-item">
                    <div class="sentence-text">"${sentence.sentence}"</div>
                    ${formatSentiment(sentence.sentiment, sentence.confidence)}
                </div>
            `).join('');
        } else {
            sentencesHTML = '<p>Aucune phrase détectée dans le texte.</p>';
        }
        
        resultContent.innerHTML = `
            <div class="sentences-analysis">
                <h4><i class="fas fa-list"></i> Analyse par phrases</h4>
                <p><strong>Texte original :</strong> "${data.original_text}"</p>
                <p><strong>Nombre de phrases détectées :</strong> ${data.total_sentences}</p>
                
                <div class="sentences-list">
                    ${sentencesHTML}
                </div>
                
                <div style="margin-top: 1rem; font-size: 0.75rem; color: #9ca3af;">
                    Analysé le ${new Date().toLocaleString('fr-FR')}
                </div>
            </div>
        `;
        
        showSection(results);
        
    } catch (error) {
        console.error('Erreur:', error);
        resultContent.innerHTML = `
            <div class="error-result" style="color: #ef4444; padding: 1rem; background: #fef2f2; border-radius: 0.5rem;">
                <i class="fas fa-exclamation-triangle"></i>
                Erreur lors de l'analyse des phrases : ${error.message}
            </div>
        `;
        showSection(results);
    } finally {
        hideLoading();
    }
}

// Fonction pour charger l'historique
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/history/`, {
            headers: defaultHeaders
        });
        
        if (!response.ok) {
            throw new Error(`Erreur ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.length === 0) {
            history.innerHTML = '<p style="color: #6b7280; font-style: italic;">Aucune analyse dans l\'historique.</p>';
            return;
        }
        
        history.innerHTML = data.map(item => `
            <div class="history-item">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    ${formatSentiment(item.sentiment, item.confidence)}
                    <div class="history-date">${new Date(item.created_at).toLocaleString('fr-FR')}</div>
                </div>
                <div style="font-size: 0.875rem; color: #4b5563;">
                    "${item.text.length > 100 ? item.text.substring(0, 100) + '...' : item.text}"
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Erreur lors du chargement de l\'historique:', error);
        history.innerHTML = `<p style="color: #ef4444;">Erreur lors du chargement de l'historique.</p>`;
    }
}

// Fonction pour définir un texte d'exemple
function setExampleText(text) {
    textInput.value = text;
    textInput.dispatchEvent(new Event('input'));
    textInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    textInput.focus();
}

// Event listeners
sentimentForm.addEventListener('submit', function(e) {
    e.preventDefault();
    analyzeSentiment();
});

analyzeSentencesBtn.addEventListener('click', analyzeSentences);
loadHistoryBtn.addEventListener('click', loadHistory);

// Raccourcis clavier
textInput.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        analyzeSentiment();
    }
});

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    loadHistory();
    textInput.title = "Astuce: Ctrl+Entrée pour analyser rapidement";
});

// Fonction globale pour les exemples
window.setExampleText = setExampleText;