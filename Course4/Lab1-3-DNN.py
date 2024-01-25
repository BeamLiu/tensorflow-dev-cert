import keras
import matplotlib.pyplot as plt
import numpy as np

from Course4.Utility import plot_series, show_model_history, prepare_timeseries_data, \
    prepare_train_val_data, window_dataset

time, series = prepare_timeseries_data()

split_time = 1100
time_train, x_train, time_valid, x_valid = prepare_train_val_data(time, series, split_time)

window_size = 20
batch_size = 32
shuffle_buffer_size = 1000
train_dataset = window_dataset(x_train, window_size, batch_size, shuffle_buffer_size)
for windows in train_dataset.take(1):
    print(windows[0].shape)

model = keras.models.Sequential([
    keras.layers.Dense(10, input_shape=[window_size], activation=keras.activations.relu),
    keras.layers.Dense(10, activation=keras.activations.relu),
    keras.layers.Dense(1)
])
print(model.summary())

model.compile(loss=keras.losses.mse, optimizer=keras.optimizers.SGD(learning_rate=7e-6, momentum=0.9),
              metrics=['accuracy'])
lr_schedule = keras.callbacks.LearningRateScheduler(
    lambda epoch: 1e-8 * 10 ** (epoch / 20)
)
model.fit(train_dataset, epochs=100, verbose=0)

lrs = 1e-8 * (10 ** (np.arange(100) / 20))
plt.semilogx(lrs, model.history.history["loss"])
plt.axis([1e-8, 1e-3, 0, 300])
plt.title = 'Learning Rate'
plt.show()

forecast = []
for time in range(split_time - window_size, len(series) - window_size):
    if time % 100 == 0:
        print(time)
    forecast.append(model.predict(series[time:time + window_size][np.newaxis], verbose=0))

# forecast = forecast[split_time - window_size:]
predict_result = np.array(forecast).squeeze()
plot_series(time_valid, x_valid)
plot_series(time_valid, predict_result)
print(keras.metrics.mean_squared_error(x_valid, predict_result).numpy())
print(keras.metrics.mean_absolute_error(x_valid, predict_result).numpy())
plt.show()
