# ML
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