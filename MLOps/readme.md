# MLOps

## Evolution of MLOps
With the growth of services in dynamic environments that demand rapid delivery of business value, the separation between development and operations teams creates communication barriers, deployment issues, and organizational silos, ultimately impacting service quality and efficiency.
`DevOps` emerged as a solution for breaking down organizational silos, enhancing collaboration between development and operations teams, and improving the efficiency and effectiveness of software development and operations.

`MLOps`, which stands for Machine Learning Operations, `extends the DevOps principles and practices specifically to the field of machine learning`. 

In MLOps, the "ML" emphasizes the unique challenges and considerations related to machine learning that arise between machine learning teams and engineering teams responsible for infrastructure, deployment, and maintenance of machine learning models.

MLOps aims to address these challenges and provide a methodology and set of practices to facilitate the development, deployment, and operation of machine learning models in a collaborative and efficient manner.

### `Goal of MLOps`
`ML+Ops` : To enhance productivity and collaboration between ML and Tech teams.
`ML -> Ops` : To enable the machine learning team to directly operate and manage the models they develop.

## Levels of MLOps:
1. `L0 - Manual Process`: 
  - Machine learning relies on various open-source libraries, and due to the nature of open-source, even the same function can produce different results depending on the version used.
  - Key challenges include environment mismatches, dependency conflicts, and manual deployment overhead.
  - As the number of models grow, it becomes difficult to deploy models with better performance quickly.
2. `L1 - Automated ML Pipeline`: 
  - Training pipeline(produces trained models): ensures that the model operates in the same environment as the one used by the machine learning engineer during model development, using containers.
  - Auto Retraining: Retraining models periodically based on new data.
  - Auto Deployment: Avoiding unnecessary retraining and switching back to previous models when needed.
    - May need to integrate automated retraining and model versioning to fully reach this stage.
3. `L2 - Automating the CI/CD Pipeline`:
At this level, CI/CD automation is extended beyond just code to include:
  - Training pipeline validation (ensuring models train correctly when code changes).
  - Package version tracking (handling updates to dependencies that might impact model performance).

Status: beyond Level 0 and partially aligned with Level 1 due to containerization and deployment automation. However, to reach full Level 1, adding Continuous Training (Auto Retrain & Auto Deploy) would help maintain model performance over time. To progress towards Level 2, integrating CI/CD for training pipelines, package version tracking, and automated model validation will be key next steps.

## Components of MLOps

### Core MLOps Technical Capabilities

1. Infrastructure
  - EKS
  - EMR on EKS
  - EMR Studio
  - Athena
  - S3
  - Airflow
  - CodeCommit, CodePipeline, jenkins pipelines
  - CloudWatch

1. `Experimentation`: Provides tools for data analysis, prototyping, and model development, enabling integration with version control systems and tracking of experiments, including data used, hyperparameters, and evaluation metrics.
2. `Data Processing`: Offers capabilities for scalable batch and streaming data processing, data transformation, and feature engineering, ensuring compatibility with various data sources and formats. 
3. `Model Training`: Facilitates efficient model training with support for distributed computing, hyperparameter tuning, and environment provisioning for various machine learning frameworks.
4. `Model Evaluation`: Enables performance assessment of models using evaluation datasets, tracking prediction performance across training runs, and providing tools for comparison and visualization of different models. 
5. `Model Serving`: Supports the deployment of models into production with low-latency, high-availability inference capabilities, autoscaling, and logging of inference requests and results.
6. `Online Experimentation`: Provides features for validating the performance of new models in production through canary and shadow deployments, A/B testing, and multi-armed bandit testing. 
7. `Model Monitoring`: Offers tools to monitor deployed models, ensuring they function correctly and providing alerts for performance degradation or anomalies. 
8. `ML Pipeline Orchestration`: Manages and automates complex workflows involved in training and deploying models, including pipeline execution, metadata tracking, and support for custom components. 
9. `Model Registry`: Serves as a centralized repository for managing the lifecycle of machine learning models, including registration, versioning, and storage of deployment-related information. 
10. `Dataset and Feature Repository`: Facilitates sharing, searching, reusing, and versioning of datasets and features, supporting real-time processing and serving for various data types.
11. `ML Metadata and Artifact Tracking`: Manages information about artifacts generated during the ML lifecycle, enabling history management, experiment tracking, and integration with other MLOps components.

https://mlops-for-all.github.io/en/docs/introduction/intro
