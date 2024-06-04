## Project-Awakening<br>Um projeto de teste, sobre inteligência artificial ChatBot.
O sistema foi feito em pro de uma maior flexibilidade, e incrementação de sistemas de machine-learning,<br>e redes neurais para diferentes tarefas como: Classificação de imagens, Detecção de objetos, e definição<br>da forma com que o Bot deveria se comportar de acordo com o comportamento do usuário.
![image](https://github.com/LuizHenrique404/Project-Awakening/assets/143651783/a3ff14dc-4809-449d-8809-fa2db2e96576)
<br>Para o funcionamento do sistema, diferentes ferramentas e algoritmos foram utilizados em diferentes partes.
### NÚCLEO DO SISTEMA
O núcleo do sistema se trata do local onde todos os comandos são interpretados e as ordens principais são dadas.
Por lá a conxeção com os outros arquivos e suas funções. Assim mantendo uma maior organização de código, e facilitando seu entendimento.
### CONEXÃO COM O DATABASE
Sua conexão com o DataBase por meio do MySQL é essencial para seu funcionamento.
Pois com ela, ele armazena os dados importantes envolvendo o usuáario e suas funções principais.
Assim como também armazena os dados de comandos personalizados feitos via o seu modo de aprendizado.
### LEARNING_MODE
![image](https://github.com/LuizHenrique404/Project-Awakening/assets/143651783/5405a7d0-aa91-4f62-915d-f46aed141bdb)
<br>Esta função permite que o usuário insira comandos no sistema, sem a necessidade de programaar, sendo assim, usuários comuns poderão contribuir com o desenvolvimento do Bot.
Por razões de segurança apenas usuários especificados na lista de Admins no arquivo de comandos podem adicionar.
### MACHINE-LEARNING
![image](https://github.com/LuizHenrique404/Project-Awakening/assets/143651783/724ac2ab-c746-4071-9f06-0722dd7dabed)
<br>Boa parte do seu sistema é dedicado ao Machine-Learning, relacionado a classificação de imagens, e a forma com que o bot irá se comportar dependendo da forma com que o usuário estaria tratando o Bot em suas interações. Sendo assim, neste caso, se o usuário agir de maneira mais formal com o Bot, o Bot agirá da mesma forma. Assim como no caso do usuário agir de maneira mais descontraida, ou rude.
<br>Para a construção das IAs foram utilizados o [RandomForesClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html),<br>e o sistema de redes neurais sequenciais do [Keras](https://www.tensorflow.org/guide/keras/sequential_model?hl=pt-br).
