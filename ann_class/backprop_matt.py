import numpy as np
import matplotlib.pyplot as plt
import sklearn.preprocessing as pre


def sigmoid(a):
    return 1 / (1 + np.exp(-a))


def forward(X, W1, b1, W2, b2):
    Z = sigmoid(X.dot(W1) - b1)
    A = Z.dot(W2) + b2
    expA = np.exp(A)
    Y = expA / expA.sum(axis=1, keepdims=True)
    assert np.allclose(Y.sum(axis=1), np.ones(len(X)))
    return Y, Z


def classification_rate(Y, P):
    n_correct = 0
    n_total = 0
    for i in range(len(Y)):
        n_total += 1
        if Y[i] == P[i]:
            n_correct += 1
    return float(n_correct) / n_total


def derivative_w2(Z, T, Y):
    # N, K = T.shape
    # M = Z.shape[1]

    # # slow
    #
    # ret1 = np.zeros((M, K))
    # for n in range(N):
    #     for m in range(M):
    #         for k in range(K):
    #             # T - Y as we are doing gradient ascent
    #             ret1[m, k] += (T[n, k] - Y[n, k]) * Z[n, m]
    # return ret1

    # # better
    # ret2 = np.zeros((M, K))
    # for n in range(N):
    #     for k in range(K):
    #         # T - Y as we are doing gradient ascent
    #         ret2[:, k] += (T[n, k] - Y[n, k]) * Z[n, :]
    # # assert(np.allclose(ret1, ret2))
    # # return ret2

    # # betterer
    # ret3 = np.zeros((M, K))
    # for n in range(N):
    #     ret3 += np.outer(Z[n], T[n] - Y[n])
    # # assert(np.allclose(ret2, ret3))
    # # return ret3

    # bestest
    # - THIS IS THE HIDEDEN LAYER * THE DELTA OF TARGETS FROM PREDICTIONS
    # - TRAINING BACKWARDS FROM OUTPUT TO HIDDEN
    ret4 = Z.T.dot(T - Y)
    # assert(np.allclose(ret3, ret4))
    return ret4


def derivative_b2(T, Y):
    return (T - Y).sum(axis=0)


def derivative_w1(X, Z, T, Y, W2):
    # # slow
    # N, D = X.shape
    # M, K = W2.shape

    # ret1 = np.zeros((D, M))
    # for n in range(N):
    #     for k in range(K):
    #         for m in range(M):
    #             for d in range(D):
    #                 ret1[d, m] += (T[n, k] - Y[n, k]) * W2[m, k] * Z[n, m] * (1 - Z[n, m]) * X[n, d]
    # return ret1

    dZ = (T - Y).dot(W2.T) * Z * (1 - Z)
    # - TRAINING BACKWARDS FROM HIDDEN TO INPUTS
    return X.T.dot(dZ)


def derivative_b1(T, Y, W2, Z):
    return ((T - Y).dot(W2.T) * Z * (1 - Z)).sum(axis=0)


def cost(T, Y):
    tot = T * np.log(Y)
    return tot.sum()


def main():

    Nclass = 500  # num observations of each class
    D = 2         # num dimensions
    M = 3         # 1 hidden layer with size of 3
    K = 3         # num classes

    # three gaussian clouds each w/ different centers
    X1 = np.random.randn(Nclass, D) + np.array([0, -2])
    X2 = np.random.randn(Nclass, D) + np.array([2, 2])
    X3 = np.random.randn(Nclass, D) + np.array([-2, 2])

    Y = np.array([0] * Nclass + [1] * Nclass + [2] * Nclass)
    X = np.vstack((X1, X2, X3))
    # N = len(Y)    # num observations
    T = pre.OneHotEncoder(sparse=False).fit_transform(Y.reshape(-1, 1))

    plt.scatter(X[:, 0], X[:, 1], s=100, c=Y, alpha=0.5)
    plt.show()

    W1 = np.random.randn(D, M)
    b1 = np.random.randn(M)
    W2 = np.random.randn(M, K)
    b2 = np.random.randn(K)

    learning_rate = 10e-7
    costs = []
    # for print shapes stuff at end of main()
    Y1, Z = forward(X, W1, b1, W2, b2)

    for epoch in range(100000):
        output, hidden = forward(X, W1, b1, W2, b2)
        if epoch % 100 == 0:
            c = cost(T, output)
            P = np.argmax(output, axis=1)
            r = classification_rate(Y, P)
            print('cost:', c, 'classification rate:', r)
            costs.append(c)

        # gradient ascent instead of descent
        W2 += learning_rate * derivative_w2(hidden, T, output)
        b2 += learning_rate * derivative_b2(T, output)
        W1 += learning_rate * derivative_w1(X, hidden, T, output, W2)
        b1 += learning_rate * derivative_b1(T, output, W2, hidden)

    plt.plot(costs)
    plt.show()
    print(X.shape, W1.shape, Z.shape, W2.shape, Y1.shape)


if __name__ == '__main__':
    main()
