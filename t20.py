import gym
from random import *
import matplotlib.pyplot as plt


def crossover(individuos, num):
    individuos.sort(reverse=True)
    num_sobrevivente = num // 2
    for i in range(num_sobrevivente, len(individuos)):
        individuos.pop(num_sobrevivente)

    t = list(range(num_sobrevivente))
    shuffle(t)

    for i in range(num_sobrevivente // 2):
        casal = [individuos[t[i]][1], individuos[t[i + 1]][1]]
        filho1 = []
        filho2 = []

        tam = len(casal[0])

        for j in range(tam):
            alet = randint(0, 1)
            filho1.append(casal[alet][j])
            filho2.append(casal[1 - alet][j])

        individuos.append([0, filho1])
        individuos.append([0, filho2])


def mutacao(individuos, actions):
    # for _ in range(1):
    for i in individuos:
        alet = randint(0, 1)
        if alet == 0:
            celula = randint(0, len(i[1]) - 1)
            i[1][celula] = [actions[randint(0, len(actions) - 1)], actions[randint(0, len(actions) - 1)],
                            actions[randint(0, len(actions) - 1)], actions[randint(0, len(actions) - 1)]]


def cria_individuos(actions, quantidade, passos, tam_gene, repedicao):
    individuos = []
    for j in range(quantidade):

        action = []
        individuo = []

        for k in range(tam_gene):
            act1 = randint(0, len(actions) - 1)
            act2 = randint(0, len(actions) - 1)
            act3 = randint(0, len(actions) - 1)
            act4 = randint(0, len(actions) - 1)
            for o in range(repedicao):
                action.append([actions[act1], actions[act2], actions[act3], actions[act4]])

        individuos.append([0, action])

    return individuos


def simular(env, individuos, passos, tam_gene, repeticao):
    ciclos = passos // (tam_gene * repeticao)
    res = []
    for ind in individuos:
        env.reset()
        ind[0] = 0

        for i in range(500):
            # env.render()

            # print('Action: ', actions[i % 12])

            observation, reward, done, info = env.step(ind[1][i % (tam_gene * repeticao)])  # take a random action
            # print('Reward: ', reward)
            ind[0] += reward

    return res


def main():
    env = gym.make('BipedalWalker-v2')
    esc = [-1, 0, 1]
    passos = 500
    num_ind = 100
    tam_gene = 40
    repeticao = 1
    individuos = cria_individuos(esc, 1000, passos, tam_gene, repeticao)
    grafico_x = []
    grafico_y = []
    ciclos = passos // (tam_gene * repeticao)
    for i in range(200):
        simular(env, individuos, passos, tam_gene, repeticao)
        crossover(individuos, num_ind)
        mutacao(individuos, esc)
        print('Ciclo ', i)
        for j in range(5):
            print('     ', individuos[j][0])
        print('    ......')
        print('     ', individuos[num_ind // 2 - 1][0])
        grafico_x.append(i)
        grafico_y.append(individuos[0][0])

    plt.plot(grafico_x, grafico_y)
    plt.title("Resultados")
    plt.xlabel("Gerações")
    plt.ylabel("Valor de adaptação")
    plt.savefig("resulado")
    for p in range(5):

        print(individuos[p][0])
        env.reset()
        for i in range(500):
            env.render()

            # print('Action: ', actions[i % 12])

            observation, reward, done, info = env.step(
                individuos[p][1][i % (tam_gene * repeticao)])  # take a random action
            print('Reward: ', reward)


if __name__ == "__main__":
    main()
