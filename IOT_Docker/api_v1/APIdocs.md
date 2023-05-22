# API Docs


#### Methods = * 
#### URL = /
#### Action:
    Print de um simples "Hello world"

#### Methods = GET 
#### URL = /setVideo?videoName=<nome-do-video>&topic=<mqtt-topic>
#### Action:
    Ainda não acabado!

    Define qual video o raspberry pi vai correr
    enviando uma mqtt message para o topic referido
    
    * Recebe videoName - este nome tem que estar na lista de ficheiros do servidor SFTP. Erro 404 caso não esteja presenete
    
    * Recebe topic - o topic refere-se ao topic do mqtt a qual certo raspberry pi está subscrito
    Se a API naõ estiver subscrito retorna erro 404

#### Methods = GET 
#### URL = /getSubscribedTopic
#### Action:
    Retorna um json com todos os topics que a API está subscrita

#### Methods = POST
#### URL = /uploadvideo
#### Action:
    Faz upload do video para pasta ../videos, esta pasta é partilhada com o servidor SFTP

    * ALLOWED_EXTENSIONS refere que extensões de video são permitidas
    
    * Se o ficheiro de video não for nenhum do ALLOWED_EXTENSIONS então é retornado erro 500

