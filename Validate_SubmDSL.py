import re

#TRATAR DOS ACENTOS!!!!

# Separa ficheiro de entrada por linhas, sendo dividido por '},\n'.
# É adicionado o conjunto de caracteres "#]" no final de cada linha não vazia e que não termina em '.
def split_file(file_subm):
    new_lines=[]
    delim_final = "#]."
    flag = 0
    
    with open(file_subm) as f:
        split_lines = f.read().split('#]\n')

        for line in split_lines:
            end_of_file = re.findall("#].",line)

            if end_of_file:
                aux = line.split(delim_final)
                line = aux[0] + delim_final
                if aux[1]:
                    flag = 5

            if not line.endswith(".") or not line:
                new_lines.append((line+'#'+']'))

            if line.endswith("."):
                new_lines.append(line[:-1])

    if not end_of_file:
        flag = 1
    return (new_lines,flag)

# Valida todos os campos do ficheiro de entrada de acordo com a estrutura definida no ficheiro "plain.txt"
# Esta função tem que ser optimizada, visto que, só retorna um erro de cada vez (Era fixe retornar todos)
def valida_Subm(file_subm):
    empty_lines = ["Empty"]*4 
    output_lines,flag = split_file(file_subm) 
    split_lines = output_lines + empty_lines
    res = []

    if flag == 1:
        res.append(-6)
    elif flag == 5:
        res.append(-5)

    if(not bool(re.match('\[\# [nN]umero [aA]luno: *[a-zA-Z]?[0-9]{5} *\#\]', split_lines[0]))):                                       
        res.append(-2)
    
    if (not bool(re.match('\[\# [rR]esposta:.*\#\]', split_lines[1], re.DOTALL))):
        res.append(-1)
    
    return res

# Cria uma matriz 2 por numero de campos, sendo que guarda a info neste formato:
# [["Enunciado","Cria o fatorial de um dado inteiro X"],["Template","ASD"],etc]
# Todas as chavetas usadas para delimitar cada campo são removidas

def check_lines(file_subm):
    new_lines = split_file(file_subm)[0]
    largura, altura = 2, len(new_lines)
    matrix = [["" for x in range(largura)] for y in range(altura)]

    for line in new_lines:
        i = 0
        sem_delimitadores = remove_delimitador(line)
        str_dividida = sem_delimitadores.split(':')

        str_dividida[0] = check_spaces(str_dividida[0])
        str_dividida[1] = check_spaces(str_dividida[1])

        matrix[new_lines.index(line)][0] = "\"" + str_dividida[0] + "\""
        matrix[new_lines.index(line)][1] = "\"" + str_dividida[1] + "\""

    return matrix

def check_spaces(stri):
    if stri[:1] == ' ':
        l = list(stri)
        l[0] = ''
        stri = ''.join(l)
    
    if stri[-1:] == ' ':
        l = list(stri)
        l[len(stri)-1] = ''
        stri = ''.join(l)

    return stri

def remove_delimitador(stri):
    first_del = stri.replace("["+"#","")
    snd_del = first_del.replace("#"+"]","")

    return snd_del

    
# Cria um ficheiro JSON com o formato de subm.json
def criarJSON(matriz_linhas):
    f = open("submteste.json","w+")
    f.write("{\"exercicio\": {\n")

    for line in matriz_linhas:
        if line==matriz_linhas[1]:
            f.write('\t' + line[0] + " : " + line[1] + "\n")
        else:
            f.write('\t' + line[0] + " : " + line[1] + ",\n\n")
    f.write("}}")
    f.close()

if __name__ == '__main__':

    res = valida_Subm('plain.txt')

    if not res:
        print("Ficheiro correto!")
        criarJSON(check_lines('plain.txt'))

    for num in reversed(res):
        if(num==-1):
            print("RESPOSTA INVALIDA")
        elif(num==-2):
            print("NUMERO DE ALUNO INVALIDO")
        elif(num==-5):
            print("Existe codigo posterior ao fim de ficheiro analisado!")
        elif(num==-6):
            print("Ficheiro nao terminado como esperado! \"#].\"")