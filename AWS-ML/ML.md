# ML

- `Label` is the variable we're predicting
  - Typically represented by the variable `y`
- `Features` are input variables describing your data
  - Typically represented by the variables `{x1, x2, ... , n}`
- `Example` is a particular instance of data, `x`
- `Labeled example` has {features, label}: (x, y)
  - used to train the model
- `Unlabeled example` has {features, ?}: (x, ?)
  - used for making predictions on new data
- `Model` maps examples to predicted labels: y
  - A model defines the relationship between features and label.
  - Defined by internal parameters, which are learned
  - `Inference` means applying the trained model to unlabeled examples. That is, you use the trained model to make useful predictions (y')
  - A `regression model` predicts continuous values.
    - What is the value of a house in California?
    - What is the probability that a user will click on this ad?
  - A `classification model` predicts discrete values.
    - Is a given email message spam or not spam?
    - Is this an image of a dog, a cat, or a hamster?
  - `Training` means creating or learning the model. That is, you show the model labeled examples and enable the model to gradually learn the relationships between features and label.
    - Training a model simply means learning (determining) good values for all the weights and the bias from labeled examples.
    - In supervised learning, a machine learning algorithm builds a model by examining many examples and attempting to find a model that minimizes loss; this process is called `empirical risk minimization`.
  - `loss` is a number indicating how bad the model's prediction was on a single example.
    - The goal of training a model is to find a set of weights and biases that have low loss, on average, across all examples.
    

## Supervised Learning
  - Training algorithms using labeled input/output data
  - Performance is assessed by comparing trained model vs real input
    - `Classification`
      - predict two or more discrete outcomes
    - `Regression`
      - predict continuous numeric output
      - `Simple linear regression`:
        - Predict the value of one variable Y based on another variable X.
        - X is called the independant varaible and Y is called the dependant variable.
        - Why simple? because it examines relationship between two variables only.
        - Why linear? when the independant variable increases (or decreases), the dependant variable increases (or decreases) in a linear fashion.
        - y = mX + b, b -> y intercept, m -> slope
        - How to obtain model parameters? Least sum of squares
          - Least squares fitting is a way to find the best fit curve or line for a set of points.
          - Least squares method is used to obtain the coefficients m and b.
          - The sum of the squares of the offsets(residuals) are used to estimate the best fit curve or line.
## Unsupervised Learning
  - Training algorithms with no labeled data. It attempts at discovering hidden patterns on its own
    - `Clustering`
## Reinforcement Learning
  - Algorithm take actions to maximize cumulative reward

## Q&A
### What are the main assumptions of a linear regression?
- A linear regression models a relationship between the dependant variable y and independant variable x
- Two main assumptions:
  - The relationship between the dependant variable y and the explanatory variables X is linear.
  - The residual errors from the regression fit are normally distributed.
### What are the most common types of linear regression?
- What are the most common estimation techniques for linear regression?
  - Ordinary Least Squares
  - Generalized Least Squares
  - Penalized Least Squares
    - L1 (LASSO)
    - L2 (Ridge)
### Describe the formula for logistic regression and how the algorithm is used for binary classification
### How does a Decision Tree decide on its splits?
- What is the criteria for a split point?
  - A decision tree can use the Information Gain to decide on the splitting criteria.
  - The decision tree is built in a top-down fashion, but the question is how do you choose which attribute to split at each node?
  - The answer is, find the feature that best splits the target class into the purest possible children nodes.
  - This measure of purity is called the information.
  - It represents the expected amount of information that would be needed to specify whether a new instance should be classified 0 or 1, given the example that reached the node.
  - Entropy on the other hand is a measure of impurity.
  - Now, by comparing the entropy before and after the split, we obtain a measure of information gain, or how much information we gained by doing the split using that particular feature.
  - Information Gain = Entropy before - Entropy after
### What advantages does a decision tree model have?
- Very easy to interpret and understand
- Works on both continuous and categorical features
- No normalization or scaling necessary
- prediction algorithm runs very fast
### What is the difference between a random forest versus boosting tree algorithms?
- Boosting Trees
  - Reassign weights to samples based on the results of previous iterations of classifications.
  - Harder to classify points get weighted more.
  - Iterative algorithm where each execution is based on the previous results.
- Random Forest
  - RF applies bootstrap aggregation to train many different trees.
  - This creates an ensemble of different individual decision trees.
  - In random forest algorithm, instead of using information gain or gini index for calculating the root node, the process of finding the root node and splitting the feature nodes will happen randomly.
### Given a dataset of features `x` and labels `y`, what assumptions are made when using Naive Bayes methods?
- Naive Bayes algorithm assumes that the features of `X` are conditionally independent of each other for the given `Y`.
- The idea that each feature is independent of each other may not always be true, but we assume it to be true to apply Naive Bayes. This "naive" assumption is where the namesake comes from.
### Describe how the support vector machine(SVM) algorithm works



## Microservices
- A microservice is an architectural and organizational design approach that arranges loosely coupled services. 
- One of the main benefits of using the microservice approach for ML applications is independence from the main software product. Having a feature service (the ML application) that is separate from the main software product has two key benefits:
  - It enables cross-functional teams to engage in distributed development, which results in faster deployments.
  - The scalability of the software is significantly improved. 
- an application built with a microservice architecture composes of several small, independent services that communicate through application programming interfaces (APIs). Typically, each service is owned by a smaller, self-contained team responsible for implementing changes and updates when necessary.
- Microservices are decoupled, monolith architecture is tightly coupled and runs as a single service
- machine learning (ML) applications are often complex systems with many moving parts and must be able to scale to meet business demands. Using a microservice architecture for ML applications is usually desirable.
### Why FASTAPI is better than FLASK?
- Flask uses WSGI whereas FASTAPI uses ASGI 
  - WSGI (stands for Web Server Gateway Interface) where you can define your application as a callable that takes two arguments the first argument environ describes the request and the environment the server running in and the second argument is a synchronous callable which you call to start the response to yield the body.
  - WSGI doesn’t have the ability to officially deal with Web Sockets. can’t use async or await 
  - ASGI stands for Asynchronous Server Gateway Interface. In ASGI also you define your application as a callable which is asynchronous by default.

## Feature engineering
In machine learning, a feature is data that is used as the input for ML models to make predictions.
- `Exploratory Data Analysis`: EDA contains summarizing, visualizing and getting deeply acquainted with the important traits of a data set.
- `Data Preprocessing`: At this stage, we will decide what needs to be cleaned and how that cleaning can be accomplished. This is referred to as Data Preprocessing.
- `Feature Engineering`: Feature Engineering is known as the process of transforming raw data (that has already been processed by Data Engineers) into features that better represent the underlying problem to predictive models, resulting in improved model accuracy on unseen data.

## MLOps
### 3 high level approaches to consider for MLOps
1. Continuous Integration and Continuous Delivery (CI/CD) - rapidly iterate on the models
2. Model governance - keep track of your models and their performance over time
3. Reproducibility - essential for debugging and troubleshooting
### best practices in MLOps
1. `Continuous integration and continuous delivery (CI/CD)`: automating the building, testing, and deploying code changes to release software faster and more reliably.
2. `Version control`: to track changes to your code and data to enable the chance to revert back to previous versions if needed
3. `Configuration management`: Automate the provisioning and configuring of your ML infrastructure using tools; Infrastructure as code
4. `Orchestration`: A process for orchestration can allow you to deploy new versions of your models quickly and easily roll back changes if needed. (kubernetes)
5. `Monitoring`: Set up monitoring of your ML pipeline and models to detect issues early and identify performance bottlenecks.
6. `Logging`: Collect log data from your ML pipeline; this is the process of capturing and storing information about events that occur during the running of a machine learning model.
7. `Testing`: Use unit, functional, and performance tests to validate your ML code and models before being deployed to production.
8. `A/B testing`: When deploying new ML models or algorithm changes, use A/B testing to compare the new version’s performance against the current production version.
9. `DevOps culture`: Encourage a culture of collaboration between development and operations teams to help ensure that ML projects successfully create a climate for open communication and a shared understanding of objectives and goals.
10. `Security`: Implement security controls throughout your ML pipeline to protect sensitive data and prevent unauthorized access.
11. `Compliance`: Ensure that your ML system meets all relevant compliance requirements related to data privacy or financial regulations.
12. `Scalability`: Design your ML system to be scalable to handle increasing volume or complexity over time to reduce the likelihood of performance issues or outages down the road.
13. `High availability`: Configure your system to tolerate failures of individual components without impacting service availability to help reduce downtime in the event of an issue and improve customer satisfaction.
14. `Disaster recovery`: Plan how you will recover from a significant failure or outage of your ML system. This includes having data backups and trained models and a way to retrain models if needed. Overall, the goal is to resume quickly with minimal interruption.
15. `Financial management`: Manage costs associated with your ML systems, such as compute resources, storage, or algorithm licensing fees. A process is critical here to manage costs related to developing and deploying machine learning models.
### challenges in MLOps
1. Incorporating machine learning into the software development cycle: Machine learning is a complex process that requires significant resources and expertise. Therefore, integrating machine learning into the traditional software development cycle can be challenging.
2. Managing machine learning lifecycles: Machine learning models often have short lifecycles due to changes in data or retraining, potentially leading to significant challenges for teams that need to manage and deploy these models.
3. Ensuring quality and trust in machine learning models: Since machine learning models are based on data, they can be subject to bias and errors. Therefore, it is important to ensure that these models are high quality and trustworthy before being deployed in production.
