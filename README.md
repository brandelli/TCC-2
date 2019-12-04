# TCC2

**Passos necessários para execução:**

``git clone https://github.com/brandelli/TCC-2``

``cd src``

Crie um ambiente virtual para o python3

``pip install -r requirements.txt``

Faça o download do word embeddings, neste trabalho foi utilizado o GloVe com 50 dimensões do NILC (http://nilc.icmc.usp.br/embeddings).

Coloque o word embeddings na pasta ``data/word_embeddings/real/``, este arquivo não está presente no git devido ao seu tamanho.

Ajuste o arquivo ``data/configuration/config.json``, definindo as etapas que serão realizadas (pré-processamento, treino, teste), os arquivos que vão ser utilizados.

``python app.py``



### Fontes e Materiais utilizados para o desenvolvimento do TCC

Repositório para organizar os materiais e códigos desenvolvidos durante o TCC2
* [Repositório TCC 1](https://github.com/brandelli/TCC-1)
* [Documento do TCC 2](https://www.overleaf.com/read/hkzjkcqxzvdb)


### Referências
* [IberLEF: Iberian Languages Evaluation Forum](https://sites.google.com/view/iberlef-2019/)
* [TASS](http://www.sepln.org/workshops/tass/)
* [tarefa iberlef](http://www.inf.pucrs.br/linatural/wordpress/iberlef-2019/)
* [Anotação POS spaCy](https://spacy.io/api/annotation)

### Materiais Relevantes
* [Repositório com datasets do iberlef](https://github.com/brandelli/iberlef-2019) 
* [Overview das tasks do Iberlef](http://ceur-ws.org/Vol-2421/NER_Portuguese_overview.pdf)
* [Comparing Word Embeddings](https://towardsdatascience.com/comparing-word-embeddings-c2efd2455fe3)
* [Recurrent Neural Networks](https://www.tensorflow.org/tutorials/sequences/recurrent)

### Implementações com RNN
* [Recurrent neural networks and LSTM tutorial in Python and TensorFlow](https://adventuresinmachinelearning.com/recurrent-neural-networks-lstm-tutorial-tensorflow/)
* [LSTM by Example using Tensorflow](https://towardsdatascience.com/lstm-by-example-using-tensorflow-feb0c1968537)
* [Recurrent Neural Networks (RNN) Tutorial | Analyzing Sequential Data Using TensorFlow In Python](https://www.edureka.co/blog/recurrent-neural-networks/)
* [TensorFlow RNN Tutorial](https://www.svds.com/tensorflow-rnn-tutorial/)
* [RNN w/ LSTM cell example in TensorFlow and Python](https://pythonprogramming.net/rnn-tensorflow-python-machine-learning-tutorial/)
* [Recurrent Neural Networks (RNNs)](https://www.easy-tensorflow.com/tf-tutorials/recurrent-neural-networks)
* [thunlp/OpenNRE](https://github.com/thunlp/OpenNRE)
* [A simple deep learning model for stock price prediction using TensorFlow](https://medium.com/mlreview/a-simple-deep-learning-model-for-stock-price-prediction-using-tensorflow-30505541d877)
* [TensorFlow-Examples](https://github.com/aymericdamien/TensorFlow-Examples/blob/master/examples/3_NeuralNetworks/bidirectional_rnn.py)
* [Recurrent Neural Networks by Example in Python](https://towardsdatascience.com/recurrent-neural-networks-by-example-in-python-ffd204f99470)
* [The Most Intuitive and Easiest Guide for Recurrent Neural Network](https://towardsdatascience.com/the-most-intuitive-and-easiest-guide-for-recurrent-neural-network-873c29da73c7)
* [Sequence Tagging With A LSTM-CRF](https://www.depends-on-the-definition.com/sequence-tagging-lstm-crf/)
* [Text classification with an RNN](https://www.tensorflow.org/beta/tutorials/text/text_classification_rnn)
* [How to Develop a Bidirectional LSTM For Sequence Classification in Python with Keras](https://machinelearningmastery.com/develop-bidirectional-lstm-sequence-classification-python-keras/)
* [How to Use Word Embedding Layers for Deep Learning with Keras](https://machinelearningmastery.com/use-word-embedding-layers-deep-learning-keras/)
* [Attention-Based-BiLSTM-relation-extraction](https://github.com/SeoSangwoo/Attention-Based-BiLSTM-relation-extraction/blob/master/train.py)
* [emnlp2017-relation-extraction](https://github.com/UKPLab/emnlp2017-relation-extraction/blob/master/relation_extraction/core/keras_models.py)
* [A hybrid deep learning approach for medical relation extraction](https://arxiv.org/pdf/1806.11189.pdf)
* [Simple Relation Extraction with a Bi-LSTM Model - Mostra a ideia de posição das entidades](https://medium.com/southpigalle/simple-relation-extraction-with-a-bi-lstm-model-part-1-682b670d5e11)
* [Sentiment detection with Keras, word embeddings and LSTM deep learning networks](https://www.liip.ch/en/blog/sentiment-detection-with-keras-word-embeddings-and-lstm-deep-learning-networks)
* [Sentence classification using Bi-LSTM](https://towardsdatascience.com/sentence-classification-using-bi-lstm-b74151ffa565)
* [Embeddings in Keras: Train vs. Pretrained](https://jovianlin.io/embeddings-in-keras/)
* [Keras Models: Sequential vs. Functional](https://jovianlin.io/keras-models-sequential-vs-functional/)
* [Designing Your Neural Networks](https://towardsdatascience.com/designing-your-neural-networks-a5e4617027ed)
* [A 6 Step Field Guide for Building Machine Learning Projects](https://towardsdatascience.com/a-6-step-field-guide-for-building-machine-learning-projects-6e4554f6e3a1)
* [NLP at IEST 2018: BiLSTM-Attention and LSTM-Attention via Soft Voting in Emotion Classification](https://www.aclweb.org/anthology/W18-6226.pdf)
* [Display Deep Learning Model Training History in Keras](https://machinelearningmastery.com/display-deep-learning-model-training-history-in-keras/)
* [Training Deep Learning based Named Entity Recognition from Scratch : Disease Extraction Hackathon](https://appliedmachinelearning.blog/2019/04/01/training-deep-learning-based-named-entity-recognition-from-scratch-disease-extraction-hackathon/)
* [Named-Entity-Recognition-with-Bidirectional-LSTM-CNNs](https://github.com/kamalkraj/Named-Entity-Recognition-with-Bidirectional-LSTM-CNNs)
* [Distant Supervision for Relation Extraction via Piecewise Convolutional Neural Networks](https://www.aclweb.org/anthology/D15-1203.pdf)
* [Relation Classification via Convolutional Deep Neural Network](https://www.aclweb.org/anthology/C14-1220.pdf)
* [Brincando de Processamento Natural de Linguagem com spaCy](https://leportella.com/pt-br/2017/11/30/brincando-de-nlp-com-spacy.html)
* [Visualizing RNNs](http://joshvarty.github.io/VisualizingRNNs/)
* [Build a POS tagger with an LSTM using Keras - Modificação da função de precisão](https://nlpforhackers.io/lstm-pos-tagger-keras/)
* [How Much Training Data is Required for Machine Learning?](https://machinelearningmastery.com/much-training-data-required-machine-learning/)
* [Know your Activation Functions](https://medium.com/analytics-vidhya/know-your-activation-functions-949a42781f5c)
