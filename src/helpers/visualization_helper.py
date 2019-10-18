import matplotlib.pyplot as plt

def plot_model_history_graph(history):
    plot_model_accuracy(history)
    plot_model_loss(history)

def plot_model_accuracy(history):
    plt.plot(history.history['accuracy'])
    plt.title('Acurácia do Modelo')
    plt.ylabel('Acurácia')
    plt.xlabel('Época')
    plt.legend(['Acurácia'], loc='bottom right')
    plt.show()

def plot_model_loss(history):
    plt.plot(history.history['loss'])
    plt.title('Perda do Modelo')
    plt.ylabel('Perda')
    plt.xlabel('Época')
    plt.legend(['Perda'], loc='top left')
    plt.show()