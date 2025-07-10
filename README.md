# dio-demo-stride
#### Criando um Agente para Detecção de Vulnerabilidades em Arquiteturas

#### Esse projeto tem o intuito de concluir o desafio proposto no bootcamp [BairesDev - Machine Learning Training](https://web.dio.me/track/bairesdev-machine-learning-training), a base dele foi construida sob orientação de https://github.com/hsouzaeduardo em stream da DIO. Veja o projeto original em https://github.com/digitalinnovationone/stride-demo

####  O modelo STRIDE atua como um guia estruturado para a identificação de ameaças, permitindo que as equipes de segurança desenvolvam contramedidas eficazes e garantam que as aplicações web sejam resilientes a uma ampla gama de ataques. Ao adotar uma abordagem proativa de modelagem de ameaças com o STRIDE, as organizações podem fortalecer significativamente sua postura de segurança. Essencialmente, o modelo STRIDE ajuda a analisar sistemas e identificar possíveis vulnerabilidades, classificando-as de acordo com o tipo de propriedade de segurança que elas violam. Essa ferramenta mnemônica utilizada na área de segurança da informação para identificar e categorizar ameaças. STRIDE é um acrônimo para:
 - Spoofing (Falsificação de Identidade): Viola a autenticidade.
 - Tampering (Adulteração): Viola a integridade.
 - Repudiation (Não Repúdio): Viola a não-repudiação.
 - Information Disclosure (Divulgação de Informações): Viola a confidencialidade.
 - Denial of Service (Negação de Serviço - DoS): Viola a disponibilidade.
 - Elevation of Privilege (Elevação de Privilégios - EoP): Viola a autorização.

#### Contribuição do Modelo STRIDE para a Segurança de Aplicações Web
O modelo STRIDE é uma ferramenta valiosa para a modelagem de ameaças (threat modeling), um processo que permite antecipar e mitigar riscos de segurança antes que eles se materializem. Ao aplicar o STRIDE, as equipes de desenvolvimento e segurança podem sistematicamente pensar sobre como um adversário pode atacar uma aplicação web e quais seriam as consequências.

#### O STRIDE pode contribui para manter aplicações web seguras, assim como nos seguintes exemplos:

#### Poder Público: a segurança das aplicações web é crucial devido à sensibilidade dos dados e à importância dos serviços prestados aos cidadãos.
 - Spoofing: Evitar que criminosos se passem por órgãos públicos ou cidadãos para acessar informações confidenciais ou realizar fraudes (ex: falsificação de credenciais de acesso a sistemas de declaração de impostos).
 - Tampering: Prevenir a alteração de dados em registros públicos, como informações de identidade, históricos criminais ou resultados de eleições.
 - Repudiation: Garantir que transações e decisões oficiais não possam ser negadas posteriormente, essencial para processos licitatórios ou emissão de documentos.
 - Information Disclosure: Proteger dados pessoais de cidadãos (endereços, CPF, dados de saúde) e informações governamentais classificadas de vazamentos.
 - Denial of Service (DoS): Assegurar que serviços essenciais, como agendamento de consultas médicas, emissão de documentos ou acesso a informações sobre benefícios, permaneçam disponíveis para a população, evitando interrupções maliciosas.
 - Elevation of Privilege (EoP): Impedir que usuários com baixos privilégios ou atacantes ganhem acesso de administrador a sistemas que controlam infraestrutura crítica ou dados confidenciais.

#### Mercado de Seguros e Financeiro: nestes setores, a confiança e a proteção dos dados são primordiais, dado o alto valor financeiro e a natureza sensível das informações.
 - Spoofing: Prevenir fraudes onde atacantes se passam por clientes ou funcionários para acessar contas, realizar transações não autorizadas ou obter informações financeiras.
 - Tampering: Proteger a integridade de registros de transações, saldos de contas, informações de apólices de seguro e históricos de crédito para evitar perdas financeiras e disputas.
 - Repudiation: Garantir que transações financeiras e contratos de seguro sejam legalmente vinculativos e que as partes não possam negar sua participação. Isso é vital para auditorias e conformidade regulatória.
 - Information Disclosure: Proteger informações financeiras sensíveis (números de cartão de crédito, extratos bancários, histórico de investimentos) e dados de saúde de segurados, evitando vazamentos que poderiam levar a roubo de identidade ou chantagem.
 - Denial of Service (DoS): Manter a disponibilidade de sistemas de home banking, plataformas de investimento e processamento de sinistros para que clientes e corretores possam acessar serviços críticos sem interrupção, especialmente durante períodos de volatilidade de mercado ou emergências.
 - Elevation of Privilege (EoP): Impedir que fraudadores ou insiders mal-intencionados obtenham privilégios para manipular sistemas de aprovação de crédito, movimentar fundos ou alterar limites de seguro.

#### Mercado de Streams de Vídeo: embora possa parecer menos crítico que os outros, a segurança no streaming de vídeo envolve proteção de conteúdo, dados do usuário e modelos de negócios.
 - Spoofing: Evitar que usuários ilegítimos acessem conteúdo pago ou se passem por assinantes premium para burlar restrições. Também proteger criadores de conteúdo de falsificação de identidade.
 - Tampering: Proteger a integridade do conteúdo de vídeo (evitar adulteração de filmes ou séries), bem como metadados e informações de direitos autorais.
 - Repudiation: Assegurar que as ações dos usuários (por exemplo, compra de conteúdo, adesão a assinaturas) sejam rastreáveis e não possam ser negadas, o que é importante para questões de faturamento e licenciamento.
 - Information Disclosure: Proteger dados de usuários (histórico de visualização, informações de pagamento, preferências) de vazamentos, garantindo a privacidade e evitando a criação de perfis maliciosos.
 - Denial of Service (DoS): Garantir que a plataforma de streaming permaneça disponível para os usuários, evitando interrupções que resultariam em perda de assinantes e receita, especialmente durante eventos ao vivo ou lançamentos de conteúdo popular.
 - Elevation of Privilege (EoP): Impedir que usuários ou atacantes obtenham privilégios que lhes permitam acessar conteúdo restrito, modificar informações de outros usuários ou controlar aspectos da plataforma.

 #### Implementação desse projeto - com auxílio do Copilot:

 - frontend: uma aplicação muito simplificada feita em html, css e javscript, constando de um formulário <stride-demo\frontend\prints\formulario.png> de preenchimento para consecução de orientações detalhadas a nível de demonstração tendo por base o STRIDE e sua respectiva representação visual <stride-demo\frontend\prints\visualização_.png> <stride-demo\frontend\prints\visualização_.png> com auxilio da biblioteca cytoscape.
    * como executar: no VS Code, clique com o botão direito do mouse em index.html e selecione Open with Live Server. Alternativa: Clique no botão "Go Live" na barra de status inferior desse IDE. 
 - backend: uma aplicação fastAPI com um único endpoint que realiza realiza a consulta no Agente de IA implantado no Azure <stride-demo\backend\postman\print_postman.png>
    * como executar: `uvicorn main:app --reload`

#### Visite o endereço para muito mais informação sobre segurança: <https://learn.microsoft.com/pt-br/azure/security/develop/threat-modeling-tool>
