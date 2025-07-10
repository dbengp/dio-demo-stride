document.addEventListener('DOMContentLoaded', () => {
    const cyContainer = document.getElementById('cy');
    const suggestionsContainer = document.getElementById('suggestions');
    const suggestionsList = document.getElementById('suggestionsList');
    const threatDetailsContainer = document.getElementById('threatDetails');
    const showThreatModelBtn = document.getElementById('showThreatModel');
    const showSuggestionsBtn = document.getElementById('showSuggestions');

    let cy = null; // Variável para armazenar a instância do Cytoscape
    let currentThreatData = null; // Variável para armazenar o JSON dinâmico

    // Oculta os botões de visualização inicialmente
    showThreatModelBtn.style.display = 'none';
    showSuggestionsBtn.style.display = 'none';

    // Event listener para o formulário
    document.getElementById('threatAnalysisForm').addEventListener('submit', async (event) => {
        event.preventDefault(); // Impede o envio padrão do formulário

        const form = event.target;
        const formData = new FormData(form);
        const loadingMessage = document.getElementById('loadingMessage');
        const errorMessage = document.getElementById('errorMessage');

        loadingMessage.style.display = 'block';
        errorMessage.style.display = 'none';
        threatDetailsContainer.style.display = 'none';
        cyContainer.style.display = 'none';
        suggestionsContainer.style.display = 'none';
        showThreatModelBtn.style.display = 'none';
        showSuggestionsBtn.style.display = 'none';

        try {
            const response = await fetch('http://127.0.0.1:8000/analisar_ameacas', { // Substitua pela URL real do seu backend FastAPI
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Erro do servidor: ${response.status} - ${errorText}`);
            }

            const data = await response.json();
            console.log("Dados recebidos do backend:", data);

            // Armazena os dados dinâmicos
            currentThreatData = data.content; // O FastAPI retorna o JSON dentro de 'content'

            // Exibe os botões de visualização após receber os dados
            showThreatModelBtn.style.display = 'inline-block';
            showSuggestionsBtn.style.display = 'inline-block';

            // Automaticamente exibe o modelo de ameaças após a análise
            initializeCytoscape(currentThreatData);
            cyContainer.style.display = 'block';
            formContainer.style.display = 'none'; // Esconde o formulário após a submissão bem-sucedida

        } catch (error) {
            console.error('Erro ao analisar ameaças:', error);
            errorMessage.textContent = `Erro: ${error.message}. Verifique o console para mais detalhes.`;
            errorMessage.style.display = 'block';
        } finally {
            loadingMessage.style.display = 'none';
        }
    });


    function initializeCytoscape(data) {
        const elements = [];
        const threatTypes = new Set();

        // Verifica se 'threat_model' existe e é um array
        if (!data || !Array.isArray(data.threat_model)) {
            console.error("Dados inválidos: 'threat_model' não encontrado ou não é um array.");
            errorMessage.textContent = "Erro: Estrutura de dados inválida recebida do servidor.";
            errorMessage.style.display = 'block';
            return;
        }

        // Adiciona os nós para os tipos de ameaça e as ameaças
        data.threat_model.forEach((threat, index) => {
            const threatType = threat["Threat Type"];
            threatTypes.add(threatType);

            // Adiciona o nó do tipo de ameaça se ainda não existir
            if (!elements.find(el => el.data.id === threatType)) {
                elements.push({
                    data: { id: threatType, label: threatType },
                    classes: 'cy-node-threat-type'
                });
            }

            // Adiciona o nó da ameaça
            const threatId = `threat-${threatType.replace(/\s/g, '-')}-${index}`; // ID mais robusto
            elements.push({
                data: {
                    id: threatId,
                    label: threat.Scenario.substring(0, 50) + '...', // Rótulo curto para o nó
                    fullScenario: threat.Scenario, // Armazena o cenário completo para detalhes
                    threatType: threatType,
                    potentialImpact: threat["Potential Impact"]
                },
                classes: 'cy-node-threat'
            });

            // Adiciona a aresta entre o tipo de ameaça e a ameaça
            elements.push({
                data: {
                    id: `${threatType}-${threatId}`,
                    source: threatType,
                    target: threatId
                },
                classes: 'cy-edge'
            });
        });

        if (cy) {
            cy.destroy(); // Destrói a instância anterior se existir
        }

        cy = cytoscape({
            container: cyContainer,
            elements: elements,
            style: [
                {
                    selector: 'node',
                    style: {
                        'background-color': '#ccc',
                        'label': 'data(label)',
                        'font-size': '12px',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'color': '#333',
                        'text-wrap': 'wrap',
                        'text-max-width': '120px',
                        'text-overflow-wrap': 'anywhere'
                    }
                },
                {
                    selector: '.cy-node-threat-type',
                    style: {
                        'background-color': '#3498db',
                        'color': 'white',
                        'width': '100px',
                        'height': '100px',
                        'font-weight': 'bold',
                        'shape': 'round-rectangle',
                        'text-wrap': 'wrap', // Garante que o texto do tipo de ameaça quebre linha
                        'text-max-width': '90px' // Limita a largura do texto para caber no nó
                    }
                },
                {
                    selector: '.cy-node-threat',
                    style: {
                        'background-color': '#ecf0f1',
                        'border-width': '1px',
                        'border-color': '#bdc3c7',
                        'width': '150px',
                        'height': '150px',
                        'shape': 'ellipse'
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 2,
                        'line-color': '#95a5a6',
                        'target-arrow-shape': 'triangle',
                        'target-arrow-color': '#95a5a6',
                        'curve-style': 'bezier'
                    }
                }
            ],
            layout: {
                name: 'cose',
                animate: true,
                animationDuration: 500,
                padding: 50
            }
        });

        // Evento de clique para exibir detalhes da ameaça
        cy.on('tap', 'node.cy-node-threat', function(evt) {
            const nodeData = evt.target.data();
            document.getElementById('detailThreatType').textContent = nodeData.threatType;
            document.getElementById('detailScenario').textContent = nodeData.fullScenario;
            document.getElementById('detailPotentialImpact').textContent = nodeData.potentialImpact;
            threatDetailsContainer.style.display = 'block';
            suggestionsContainer.style.display = 'none';
        });

        // Oculta os detalhes ao clicar fora do nó
        cy.on('tap', function(evt) {
            if (evt.target === cy) {
                threatDetailsContainer.style.display = 'none';
            }
        });
    }

    function displaySuggestions(suggestions) {
        suggestionsList.innerHTML = ''; // Limpa a lista existente

        // Verifica se 'improvement_suggestions' existe e é um array
        if (!Array.isArray(suggestions)) {
            console.error("Dados inválidos: 'improvement_suggestions' não é um array.");
            errorMessage.textContent = "Erro: Estrutura de sugestões inválida recebida do servidor.";
            errorMessage.style.display = 'block';
            return;
        }

        suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.textContent = suggestion;
            suggestionsList.appendChild(li);
        });
        suggestionsContainer.style.display = 'block';
        cyContainer.style.display = 'none';
        threatDetailsContainer.style.display = 'none';
        formContainer.style.display = 'none';
    }

    showThreatModelBtn.addEventListener('click', () => {
        if (currentThreatData) {
            initializeCytoscape(currentThreatData);
            cyContainer.style.display = 'block';
            suggestionsContainer.style.display = 'none';
            threatDetailsContainer.style.display = 'none';
            formContainer.style.display = 'none';
        } else {
            alert('Por favor, analise as ameaças primeiro.');
        }
    });

    showSuggestionsBtn.addEventListener('click', () => {
        if (currentThreatData) {
            displaySuggestions(currentThreatData.improvement_suggestions);
        } else {
            alert('Por favor, analise as ameaças primeiro.');
        }
    });
});