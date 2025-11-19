Este é um projeto codado em Python, que ajuda a descobrir qual carreira tech (ML, UX/UI, DevOps) combina mais com o seu perfil atual.

Ele não é apenas um quiz de "Sim ou Não"; usamos NumPy e médias ponderadas para calcular a afinidade do seu perfil com as vagas.

O que ele faz?
 Quiz Interativo: faz perguntas rápidas sobre suas habilidades (Lógica, Criatividade, Ética, etc).

 Match Inteligente: O sistema sabe que Criatividade é crucial para Design, mas Automação é vital para DevOps. Ele pesa isso na decisão final.

 Mentor Virtual: Se você tem um match alto com uma carreira, mas carece em uma habilidade crítica, o sistema te avisa exatamente o que estudar (ex: "Aprenda Pandas" ou "Estude LGPD").

 Ranking: Mostra as opções ordenadas da que mais combina para a que menos combina.

 Como executar?
Você só precisa do Python instalado e de uma biblioteca extra para a matemática funcionar.

Após baixar e abrir o arquivo em seu ambiente de programação de preferência: 

Instale a biblioteca do numpy 
No seu terminal, rode:
pip install numpy

Agora, basta iniciar o código

Bash

python carreiras.py
 Como a mágica acontece?
Se você está curioso sobre a lógica, o sistema funciona assim:

O "Match" (Afinidade)
Imagine que você tirou nota 5 em Lógica.

Para um Engenheiro de ML, isso vale muito (peso alto).

Para um Designer, vale menos (peso baixo).

O script pega suas notas, multiplica pela importância de cada habilidade naquela carreira específica e te dá uma porcentagem de compatibilidade. É matemática vetorial aplicada à vida real!

O aviso (Gaps)
O sistema é inteligente: ele só sugere estudos se a habilidade for muito importante para a carreira e sua nota for baixa. Assim, ele foca no que realmente importa para você evoluir.



Configuração (O Banco de Dados): Logo no começo, temos os dicionários DB_C e DB_CARREIRAS. Caso queira adicionar novas carreiras as coloque lá.


Exemplo de como adicionar uma carreira nova:

Python

É só colar isso na lista DB_CARREIRAS
Carreira('Desenvolvedor Front-end', {
    'criatividade': 30, 
    'logica': 30, 
    'adaptabilidade': 20
})
 Exemplo de Resultado:



============================================================
 RESULTADOS PARA: JOÃO
============================================================

🏆 RECOMENDAÇÃO PRINCIPAL: DevOps & SRE
 Match de Perfil: 92.5%

⚠️  PONTOS DE ATENÇÃO:
   • Ética Digital (Sua Nota: 2)

     Ação: Estude LGPD e vieses em IA.

