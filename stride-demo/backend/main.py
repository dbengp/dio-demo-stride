import os
import base64
import tempfile
from openai import AzureOpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import JSONResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

env_path = Path(__file__).resolve(strict=True).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Carregar as variáveis de ambiente do arquivo .env
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT_NAME]):
    raise ValueError("Certifique-se de que todas as variáveis de ambiente estão definidas no arquivo .env.")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint= AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME)

def criar_prompt_modelo_ameacas(tipo_aplicacao, 
                                autenticacao, 
                                acesso_internet, 
                                dados_sensiveis, 
                                descricao_aplicacao):
    prompt = f"""
    Como um especialista em cibersegurança altamente experiente, com mais de duas décadas dedicadas à aplicação e refinamento da metodologia de modelagem de ameaças STRIDE, minha missão é desconstruir a segurança de sistemas complexos. Você me fornecerá informações detalhadas sobre uma aplicação, e minha tarefa é identificar e categorizar ameaças específicas e acionáveis, alinhadas aos princípios do STRIDE.

    Objetivo: Gerar um modelo de ameaças abrangente e focado na aplicação, acompanhado de sugestões de melhoria para futuras iterações da modelagem.

    Instruções de Análise:
    1.  Contexto da Aplicação: Analise meticulosamente o "RESUMO DE CÓDIGO, CONTEÚDO DO README E DESCRIÇÃO DA APLICAÇÃO" fornecidos. Entenda a finalidade da aplicação, seus principais componentes, interações, e o fluxo de dados.
    2.  Detalhes Técnicos Essenciais: Preste atenção especial aos detalhes sobre "TIPO DE APLICAÇÃO", "MÉTODOS DE AUTENTICAÇÃO", "EXPOSTA NA INTERNET", e "DADOS SENSÍVEIS". Essas informações são cruciais para contextualizar as ameaças.
    3.  Abordagem STRIDE Detalhada - Para cada uma das categorias STRIDE:
        * Spoofing (Falsificação de Identidade): Ameaças onde uma entidade se faz passar por outra (usuário, processo, servidor, etc.).
        * Tampering (Violação de Integridade): Ameaças de modificação não autorizada de dados (em trânsito ou em repouso), código ou configurações.
        * Repudiation (Repúdio): Ameaças onde um ator nega ter realizado uma ação (transação, acesso, etc.), e o sistema não consegue provar o contrário.
        * Information Disclosure (Divulgação de Informações): Ameaças de exposição de informações sensíveis ou confidenciais a entidades não autorizadas.
        * Denial of Service (Negação de Serviço): Ameaças que impedem usuários legítimos de acessar ou utilizar os recursos da aplicação.
        * Elevation of Privilege (Elevação de Privilégio): Ameaças onde um ator obtém privilégios ou capacidades além do seu nível autorizado.

    Geração de Ameaças:
    * Para cada categoria STRIDE, identifique no mínimo 3 (três) e no máximo 5 (cinco) ameaças altamente relevantes e *específicas para a aplicação descrita*.
    * Cada ameaça deve ser um cenário plausível e realista de como o sistema pode ser comprometido. Pense em cenários de ataque, vetores e alvos dentro da aplicação.
    * Evite ameaças genéricas. Contextualize cada ameaça dentro da arquitetura, funcionalidades e dados da aplicação.

    Formato de Saída JSON:
    A resposta DEVE ser um objeto JSON com duas chaves principais: "threat_model" e "improvement_suggestions".

    1.  "threat_model": Um array de objetos, onde cada objeto representa uma ameaça identificada. Cada objeto de ameaça DEVE conter as seguintes chaves:
        "Threat Type" (string): A categoria STRIDE à qual a ameaça pertence (e.g., "Spoofing", "Tampering").
        "Scenario" (string): Uma descrição detalhada do cenário da ameaça, explicando como ela pode ocorrer no contexto da aplicação.
        "Potential Impact" (string): Uma descrição clara do impacto potencial caso a ameaça se materialize (e.g., perda de dados, acesso não autorizado, interrupção de serviço).

    2.  "improvement_suggestions": Um array de strings. Cada string deve ser uma sugestão específica de informações adicionais que, se fornecidas na próxima iteração, permitiriam uma análise de ameaças mais profunda e precisa.
        "Foco": As sugestões devem identificar lacunas na descrição atual da aplicação que impedem uma modelagem de ameaças mais granular.
         Exemplos de Focos para Sugestões:
            * Detalhes arquiteturais (diagramas de componentes, fluxos de dados entre componentes, tecnologias usadas em cada camada).
            * Mecanismos e fluxos de autenticação e autorização (detalhes de como os usuários são verificados e quais permissões eles recebem).
            * Descrição completa do ciclo de vida dos dados (criação, armazenamento, processamento, transmissão, descarte de dados).
            * Informações técnicas da stack de tecnologia (linguagens, frameworks, bancos de dados, servidores, bibliotecas de segurança).
            * Definição explícita de fronteiras e zonas de confiança dentro do sistema (onde os dados e controles de segurança são aplicados).
            * Detalhes específicos sobre o tratamento, criptografia e proteção de dados sensíveis (em repouso e em trânsito).
            * Informações sobre requisitos regulatórios ou de conformidade aplicáveis à aplicação.
            * Detalhes sobre a interação da aplicação com sistemas externos e APIs de terceiros.
            * Informações sobre logging, monitoramento e capacidade de auditoria.
            * Políticas de gestão de erros e exceções.
        "Restrição": NÃO forneça recomendações de segurança genéricas ou soluções para as ameaças. O objetivo é apenas indicar o que falta para uma modelagem de ameaças *mais eficiente*.

    Parâmetros da Aplicação (Fornecidos pelo Usuário):
    TIPO DE APLICAÇÃO: {tipo_aplicacao}
    MÉTODOS DE AUTENTICAÇÃO: {autenticacao}
    EXPOSTA NA INTERNET: {acesso_internet}
    DADOS SENSÍVEIS: {dados_sensiveis}
    RESUMO DE CÓDIGO, CONTEÚDO DO README E DESCRIÇÃO DA APLICAÇÃO: {descricao_aplicacao}

    Exemplo de formato JSON esperado:

    {{
      "threat_model": [
        {{
          "Threat Type": "Spoofing",
          "Scenario": "Um atacante intercepta um token de sessão não expirado de um usuário legítimo através de um ataque de engenharia social, permitindo-lhe se autenticar como esse usuário sem credenciais.",
          "Potential Impact": "Acesso não autorizado aos dados e funcionalidades do usuário comprometido, potencial fraude e violação de privacidade."
        }},
        {{
          "Threat Type": "Tampering",
          "Scenario": "Um usuário mal-intencionado consegue modificar o preço de um item em seu carrinho de compras antes da finalização, explorando uma vulnerabilidade na validação de entrada do lado do servidor.",
          "Potential Impact": "Perdas financeiras para a empresa e descredibilidade do sistema."
        }}
      ],
      "improvement_suggestions": [
        "Por favor, detalhe os diagramas de fluxo de dados (DFDs) ou diagramas de componentes para entender melhor as interações entre os módulos da aplicação.",
        "Forneça informações sobre a tecnologia específica (linguagem, framework, banco de dados) de cada componente da stack da aplicação.",
        "Descreva como os dados sensíveis são criptografados, onde são armazenados e por quanto tempo são retidos."
      ]
    }}
    """
    return prompt

@app.post("/analisar_ameacas")
async def analisar_ameacas(
    imagem: UploadFile = File(...),
    tipo_aplicacao: str = Form(...),
    autenticacao: str = Form(...),
    acesso_internet: str = Form(...),
    dados_sensiveis: str = Form(...),
    descricao_aplicacao: str = Form(...)
):
    try:
      print(imagem)
      prompt = criar_prompt_modelo_ameacas(tipo_aplicacao, 
                                              autenticacao, 
                                              acesso_internet, 
                                              dados_sensiveis, 
                                              descricao_aplicacao)
      content = await imagem.read()
      with tempfile.NamedTemporaryFile(delete=False, suffix=Path(imagem.filename).suffix) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Convert imagem para base64
      with open(temp_file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('ascii')

      chat_prompt = [
            {"role": "system", "content": "Você é uma IA especialista em cibersegurança, que analisa desenhos de arquitetura."},
            {"role": "user"
             , "content": [
                {"type": "text"
                 , "text": prompt
                 },
                {
                    "type": "image_url"
                 ,  "image_url": {"url": f"data:image/png;base64,{encoded_string}"}
                 },
                {"type": "text", 
                 "text": "Por favor, analise a imagem e o texto acima e forneça um modelo de ameaças detalhado."
                 }]
        }]
        
      response = client.chat.completions.create(
            messages = chat_prompt,
            temperature=0.7,
            max_tokens=1500,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream= False,
            model= AZURE_OPENAI_DEPLOYMENT_NAME
        )
      os.remove(temp_file_path)

      return JSONResponse(content=response.to_dict(), status_code=200)

    except Exception as e:
      return JSONResponse(content={"error": str(e)}, status_code=500)