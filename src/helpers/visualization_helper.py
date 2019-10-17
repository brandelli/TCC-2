import matplotlib.pyplot as plt

def plot_model_history_graph(history):
    plot_model_accuracy(history)
    plot_model_loss(history)

def plot_model_accuracy(history):
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['custom_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['accuracy', 'custom_accuracy'], loc='bottom right')
    plt.show()

def plot_model_loss(history):
    plt.plot(history.history['loss'])
    plt.title('Model Loss')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['loss'], loc='top left')
    plt.show()