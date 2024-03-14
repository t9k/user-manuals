import argparse
import json
import logging
import os
import shutil

import tensorflow as tf
from tensorflow.keras import callbacks, datasets, layers, models, optimizers

parser = argparse.ArgumentParser(
    description='Distributed training of Keras model for MNIST with '
    'MultiWorkerMirroredStrategy.')
parser.add_argument('--aimd',
                    action='store_true',
                    default=False,
                    help='Use AIMD to record training data.')
parser.add_argument('--api_key',
                    type=str,
                    help='API Key for requesting AIMD server. '
                    'Required if --aimd is set.')
parser.add_argument(
    '--folder_path',
    type=str,
    default='aimd-example',
    help='Path of AIMD folder in which trial is to be created. '
    'Required if --aimd is set.')
parser.add_argument('--log_dir',
                    type=str,
                    help='Path of the TensorBoard log directory.')
parser.add_argument('--no_cuda',
                    action='store_true',
                    default=False,
                    help='Disable CUDA training.')
parser.add_argument(
    '--server_url',
    type=str,
    default='https://proxy.nc201.kube.tensorstack.net/t9k/aimd/server',
    help='URL of AIMD server. Required if --aimd is set.')
parser.add_argument('--save_path',
                    type=str,
                    default=None,
                    help='Save path of the trained model.')
parser.add_argument('--trial_name',
                    type=str,
                    default='mnist_keras_distributed',
                    help='Name of AIMD trial to create. '
                    'Required if --aimd is set.')
args = parser.parse_args()
logger = logging.getLogger('print')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logger.propagate = False

if args.no_cuda:
    # Sets all GPUs invisible
    tf.config.set_visible_devices([], 'GPU')
gpus = tf.config.get_visible_devices('GPU')
if gpus:
    # Print GPU info
    logger.info('NVIDIA_VISIBLE_DEVICES: {}'.format(
        os.getenv('NVIDIA_VISIBLE_DEVICES')))
    logger.info('T9K_GPU_PERCENT: {}'.format(os.getenv('T9K_GPU_PERCENT')))
    logger.info('Visible GPUs: {}'.format(
        tf.config.get_visible_devices('GPU')))
    # Set memory growth
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    # # Set GPU memory limit
    # tf.config.set_logical_device_configuration(
    #     gpus[0], [tf.config.LogicalDeviceConfiguration(memory_limit=1024)])

strategy = tf.distribute.MultiWorkerMirroredStrategy()

# Get information for current worker.
tf_config = json.loads(os.environ['TF_CONFIG'])
world_size = len(tf_config['cluster']['worker'])
task_index = tf_config['task']['index']

if args.aimd and task_index == 0:
    from t9k import aimd
    trial = aimd.init(server_url=args.server_url,
                      trial_name=args.trial_name,
                      folder_path=args.folder_path,
                      api_key=args.api_key)

params = {
    'batch_size': 32 * world_size,
    'epochs': 10,
    'learning_rate': 0.001 * world_size,
    'conv_channels1': 32,
    'conv_channels2': 64,
    'conv_channels3': 64,
    'conv_kernel_size': 3,
    'maxpool_size': 2,
    'linear_features1': 64,
    'seed': 1,
}

if args.aimd and task_index == 0:
    trial.params.update(params)
    trial.params.parse(dist_tf_strategy=strategy)

with strategy.scope():
    model = models.Sequential([
        layers.Conv2D(params['conv_channels1'],
                      params['conv_kernel_size'],
                      activation='relu',
                      input_shape=(28, 28, 1)),
        layers.MaxPooling2D((params['maxpool_size'], params['maxpool_size'])),
        layers.Conv2D(params['conv_channels2'],
                      params['conv_kernel_size'],
                      activation='relu'),
        layers.MaxPooling2D((params['maxpool_size'], params['maxpool_size'])),
        layers.Conv2D(params['conv_channels3'],
                      params['conv_kernel_size'],
                      activation='relu'),
        layers.Flatten(),
        layers.Dense(params['linear_features1'], activation='relu'),
        layers.Dense(10, activation='softmax'),
    ])
    model.compile(
        optimizer=optimizers.Adam(learning_rate=params['learning_rate']),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

print(os.path.join(os.getcwd(), 'mnist.npz'))
(train_images, train_labels), (test_images,
                               test_labels) = datasets.mnist.load_data(
                                   path=os.path.join(os.getcwd(), 'mnist.npz'))
train_images = train_images.reshape((60000, 28, 28, 1)).astype("float32") / 255
test_images = test_images.reshape((10000, 28, 28, 1)).astype("float32") / 255
train_images, val_images = tf.split(train_images, [48000, 12000], axis=0)
train_labels, val_labels = tf.split(train_labels, [48000, 12000], axis=0)
train_dataset = tf.data.Dataset.from_tensor_slices(
    (train_images, train_labels)).shuffle(
        48000, seed=params['seed']).repeat().batch(params['batch_size'])
val_dataset = tf.data.Dataset.from_tensor_slices(
    (val_images, val_labels)).batch(400)
test_dataset = tf.data.Dataset.from_tensor_slices(
    (test_images, test_labels)).batch(1000)

train_callbacks = []
test_callbacks = []

if args.aimd and task_index == 0:
    from t9k.aimd.keras import AIMDFitCallback, AIMDEvalCallback
    train_callbacks.append(AIMDFitCallback(trial))
    test_callbacks.append(AIMDEvalCallback(trial))

if args.log_dir and task_index == 0:
    log_dir = args.log_dir
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir, ignore_errors=True)
    tensorboard_callback = callbacks.TensorBoard(log_dir=log_dir)
    train_callbacks.append(tensorboard_callback)

model.fit(train_dataset,
          epochs=params['epochs'],
          steps_per_epoch=48000 // params['batch_size'],
          validation_data=val_dataset,
          callbacks=train_callbacks,
          verbose=2)

if args.save_path:
    if task_index == 0:
        save_path = args.save_path
    else:
        dirname = os.path.dirname(args.save_path)
        basename = os.path.basename(
            args.save_path) + '_temp_' + str(task_index)
        save_path = os.path.join(dirname, basename)
    if os.path.exists(save_path):
        shutil.rmtree(save_path, ignore_errors=True)
    model.save(save_path)
    if task_index != 0:
        shutil.rmtree(save_path, ignore_errors=True)

model.evaluate(test_dataset, callbacks=test_callbacks, verbose=2)

if args.aimd and task_index == 0:
    trial.finish()
