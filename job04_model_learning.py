import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import *
from tensorflow.keras.layers import *

X_train, X_test, Y_train, Y_test = np.load('./news_data_max_28_wordsize_14631.npy',allow_pickle=True)

print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

model = Sequential()
model.add(Embedding(14631,300,input_length=(28)))
model.add(Conv1D(32,kernel_size=5, padding = 'same', activation='relu'))
model.add(MaxPooling1D(pool_size=1))
model.add(LSTM(128,activation='tanh',return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64,activation='tanh',return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64,activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128,activation='relu'))
model.add(Dense(6,activation='softmax'))
model.summary()


model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=128, epochs=100, validation_data=(X_test, Y_test))
model.save('./models/news_category_classfication_model_{}.h5'.format(fit_hist.history['val_accuracy'][-1]))
plt.plot(fit_hist.history['val_accuracy'],label='validation accuracy')
plt.plot(fit_hist.history['accuracy'], label='train accuracy')
plt.legend()
plt.show()


