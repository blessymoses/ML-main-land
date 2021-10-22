# Amazon SageMaker

## Linear Learner Algorithm
- Linear Learner is a supervised algorithm that is used to fit a line to the training data.
- It could be used for both classification and regression tasks:
  - `Regression`: output contains continuous numeric values
  - `Binary classification`: Output label must be either 0 or 1 (linear threshold function is used).
  - `Multiclass classification`: output labels must be from 0 to num_classes-1
- The best model optimizes either of the following:
  - `For regression`: focus on continuous metrics such as mean square error, root mean squared error, cross entropy loss, absolute error.
  - `For classification`: focus on discrete metrics such as F1 score, precision, recall or accuracy.
- `Use cases`:
  - Regression tasks: Revenue predictions based on previous years performance.
  - Discrete Binary Classification: Does this patient have a disease or not
  - Discrete Multiclass Classification: Should an autonomous car stop, slow down or accelerate?
- Preprocessing:
  - Ensure that data is shufffled before training.
  - Normalization or feature scaling is a critical preprocessing step to ensure that the model does not become dominated by the weight of a single feature.
- Training:
  - Linear Learner uses stochastic gradient descent to perform the training.
  - Select an appropriate optimization algorithm such as Adam, AdaGrad, and SGD
  - Hyperparameters, such as learning rate can be selected.
  - Overcome model overfitting using L1, L2 regularization
  - Multiple models could be optimized in parallel.
- Validation:
  - Trained models are evaluated against a validation dataset and best model is selected based on the following metrics:
  - For `regression`: mean square error, root mean squared error, cross entropy loss, absolute error.
  - For `classification`: F1 score, precision, recall or accuracy.
- Supported input types by linear learner:
  - RecordIO-wrapped protobuf(note: only Float32 tensors are supported)
  - Text/CSV(First column is assumed to be the target label)
  - File or Pipe mode both supported
- For inference, linear learner algorithm supports application/json, application/x-recordio-protobuf, text/csv formats
- For regression(predictor_type="regressor"), the score is the prediction produced by the model.



# Amazon SageMaker Studio
Amazon SageMaker Studio is a fully integrated development environment (IDE) for machine learning that provides a single, web-based visual interface to perform all the steps for ML development.
## Build, train, deploy, and monitor a machine learning model
Lab: https://aws.amazon.com/getting-started/hands-on/build-train-deploy-monitor-machine-learning-model-sagemaker-studio/?trk=gs_card