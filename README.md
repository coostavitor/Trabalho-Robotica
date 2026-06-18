A_estrela-no-Gazebo

Implementação do A* em um robô no Gazebo, fazendo sair de um labirinto

Alunos:
Vitor Alves Costa
Christopher Elias de Souza


1. Importe os arquivos

Abra um terminal, siga os passo de 1. a 9. no Github abaixo:

 https://github.com/milenafariap/ros2_workshop/
Após isso, pressione Ctrl + C no terminal, feche o terminal e finalize baixando os arquivos aqui presente;

2. Substitua os arquivos:

Substitua o explore_world.sdf na pasta world baixado no passo anterior.

Logo após isso, mova os outros arquivos baixados para pasta scripts.

3. Execute o programa

Abra dois terminais. Em um dos terminais, siga os passos do 6. ao 9. no link abaixo:

 https://github.com/milenafariap/ros2_workshop/
Aperte o "play" do Gazebo. No outro terminal, execute isso:

 docker exec -it ros2_workshop_container bash
e logo após, no mesmo terminal, faça isso:

cd /root/workshop_assets
source install/setup.bash
cd assets/scripts
PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH python3 movimento.py

OBS: Conseguimos fazer os codigos funcionarem e o carrinho se movimentar, mas nao conseguimos fazer ele seguir o caminho para sair 
da forma esperada.

