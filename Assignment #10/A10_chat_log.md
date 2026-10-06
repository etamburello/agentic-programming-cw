# Classification problem analysis
_Exported on 10/3/2026 at 12:07:17 EDT from Cursor (3.23.12)_

---

**User**

I am a senior Computer Science and Engineering student in university. For the past three assignments we have worked on together, we used a single train/test split to build and evaluate machine-learning models. In this assignment, we will address an important problem: How can we compare models without repeatedly using the test set?

We will learn to use cross-validation to compare models and investigate the effect of a model hyperparameter.
We will work with Logistic Regression, Decision Tree, Random Forest, cross-validation,training vs. validation performance, hyperparameters, overfitting, and final test evaluation
The main workflow is:
Hold out test set → establish baseline → cross-validation → compare models → tune one hyperparameter → select a model → evaluate once on test set → analyze errors

The most important rule for this assignment is: Do not use the test set to decide which model or hyperparameter to choose.

See the Assignment #10 folder with the dataset and the .ipynb file. 
Let's start with part 1(see section 1). Here I want to Define the Classification Problem. Create high_exam_score. Examine the distribution of the two classes.

Part 1 Questions
Explain:
What are you trying to predict?
Why is this a classification problem?
What percentage of students belong to each class?
Is the dataset approximately balanced?

---

**Cursor**

I'll start by reading the assignment notebook and the dataset so we can define the classification problem and answer Part 1 from the data.

The notebook’s first section is the track choice. I’ll check the dataset and how earlier assignments defined `high_exam_score` so we match that setup.

Previous work defined `high_exam_score` as Yes when the exam score is 80 or higher. I’ll match that definition and compute the class split from this dataset.

The class split is the same cutoff as Class 2: Yes at 80 or above. Of 250 students, 99 are Yes (39.6%) and 151 are No (60.4%). I’ll put that definition, the class counts, and the Part 1 answers into section 1 of the notebook.

Section 1 of `Assignment #10/CSE4095_Class4_Starter.ipynb` now uses the classification track. `high_exam_score` is Yes when `exam_score` is 80 or higher and No otherwise, and the notebook prints the class counts and a bar chart.

**What are you trying to predict?** Whether a student will earn a high exam score. The label is Yes at 80 or above and No below 80. The model predicts that label from study habits and background, before the exam, rather than estimating the points themselves.

**Why is this a classification problem?** The target has two categories. The model chooses a group, and a prediction is either the right label or the wrong one. A score of 81 and a score of 100 are both Yes. A score of 79 and a score of 51.4 are both No. How far the score sits from 80 does not change the class.

**What percentage of students belong to each class?** Of the 250 students, 99 are Yes (39.6%) and 151 are No (60.4%).

**Is the dataset approximately balanced?** Yes, approximately. Neither class is rare. No is the larger class, about 60% of the students, and Yes is about 40%. A majority-class guess of No would be right about 60% of the time, so later accuracy numbers need to be compared with that baseline.

Upload the notebook to Colab with `class1_student_habits.csv` and run the first code cell to see the table and the bar chart. We can move to section 2, defining `X` and `y`, when you are ready.

---

**User**

Lets move on to part 2, where I want to select the features. See section 2. Use:
study_hours_per_week
sleep_hours_per_night
attendance_rate
practice_problems_per_week
prior_programming_experience
study_group
commute_minutes

Do not use:
student_id
exam_score
quiz_average

Part 2 Question:
Why would using exam_score be target leakage?

---

**Cursor**

Section 2 is where `X` and `y` get defined. I’ll use the seven habit columns you listed and leave `student_id`, `exam_score`, and `quiz_average` out, then write the leakage answer.

Section 2 now builds `X` from the seven habit columns and `y` as `high_exam_score`. `student_id`, `exam_score`, and `quiz_average` stay out of the model.

**Why would using `exam_score` be target leakage?** `high_exam_score` was built directly from `exam_score`: Yes if the score is 80 or higher, No otherwise. If the model can see the exam score, it does not need study hours, sleep, or attendance. It can apply the same cutoff and get the label right every time. That accuracy would be meaningless, because the feature is the answer written in another form. For a student who has not taken the exam yet, the score would not be available, which is why the habits are the predictors and the exam score is not.

---

**User**

See section 3. I now want to work on part 3, where I want to create the Final Test Set. Split the data into 80% training data and 20% test data
Use: random_state=42 and stratification.

After creating the split, do not use the test set again until Part 10. All model comparison and hyperparameter selection should be performed using the training data.

Part 3 Questions:
Explain:
Why are we holding the test set aside?
What could happen if we repeatedly check test accuracy while modifying our model?

---

**Cursor**

Section 3 is the holdout split. I’ll check how the notebook is laid out now, then add an 80/20 stratified split with `random_state=42` and the answers for why that test set stays unused until the end.

Section 3 holds out the test set with an 80/20 split, `random_state=42`, and `stratify=y`. That gives 200 training students and 50 test students, and both sets stay near the full class mix of about 60% No and 40% Yes. `X_test` and `y_test` are stored and stay unused through the baseline, cross-validation, and hyperparameter tuning. They are used once, at the final evaluation.

**Why are we holding the test set aside?** The test set is the check on students the model has not learned from. Model comparison and hyperparameter choices are made from the 200 training students, using cross-validation. If we look at the test students while we are still choosing, the test set stops being an honest check of how the model would do on someone new. We use it once, after the model is already chosen.

**What could happen if we repeatedly check test accuracy while modifying our model?** Each change we keep because it scored higher on the test set is a choice fitted to those 50 students. The test accuracy can rise because we picked what worked on that particular group, not because the model learned a pattern that will hold for a new student. The final number then looks better than the model really is.

---

**User**

Lets move on to part 4(see section 5), where I want to Build the Preprocessing Pipeline. As in Class 2, your dataset contains numerical features, categorical features, and some missing values. For numerical variables, use: missing-value handling → StandardScaler. For categorical variables, use: missing-value handling → one-hot encoding
Use appropriate scikit-learn tools such as:
SimpleImputer
StandardScaler
OneHotEncoder
ColumnTransformer
Pipeline

Part 4 Questions:
Explain:
Why should preprocessing be included inside the pipeline?
Why is this especially important when using cross-validation?
Which of the models in this assignment are sensitive to feature scaling?
Do Decision Trees and Random Forests generally require scaling?

---

**Cursor**

Section 5 is the preprocessing pipeline. I’ll match the Class 2 setup: impute and scale the numeric columns, impute and one-hot encode the categorical columns, and keep those steps inside a pipeline.

The same seven columns as Class 2 still have blanks in study hours, sleep hours, and prior programming experience. I’ll put imputation and scaling inside one preprocessor and leave the test set untouched.

Section 5 builds one preprocessor and does not touch the test set. Numeric columns (study hours, sleep, attendance, practice problems, commute minutes) are filled with the median, then scaled. Categorical columns (prior programming experience, study group) are filled with the most common category, then one-hot encoded.

**Why should preprocessing be included inside the pipeline?** The imputer, the scaler, and the encoder all learn from data: each column’s median, mean, and standard deviation, plus the most common category and the names that become 0/1 columns. Inside a pipeline, `fit` learns those values only from the rows passed to it, and later rows are prepared with those same values. The preparation and the model stay one workflow.

**Why is this especially important when using cross-validation?** Each fold holds out a different slice of the training data as validation. If you impute and scale the full training set first, the validation rows help set the medians, means, and standard deviations used on that fold’s training rows. The validation score then looks a little better than a new student would get. With the preprocessor inside the pipeline, each fold refits those steps on that fold’s training rows only.

**Which models are sensitive to feature scaling?** Logistic Regression. It multiplies each feature by a weight, and the default model also penalizes large weights. Study hours are small numbers, attendance is usually in the 70s to 100, and commute minutes can be near 0 or well over 100. Without scaling, a column can dominate just because of its units.

**Do Decision Trees and Random Forests generally require scaling?** No. A tree splits on the order of values in one column, such as whether study hours are greater than 6. Changing the units moves the threshold, and the groups stay the same. A random forest is a collection of those trees. The shared pipeline still scales every model, so Logistic Regression is treated correctly and all three models see the same prepared columns.

---

**User**

Now onto Part 5(see section 4), where I just want to establish the baseline. Put undo # TODO line. Create a simple classifier that always predicts the most common training class. You may use DummyClassifier with an appropriate strategy. Instead of evaluating the baseline on the final test set, evaluate it using 5-fold cross-validation on the training data.

Report the mean cross-validation accuracy and the variation across folds, such as standard deviation.

Part 5 Questions:
What does the baseline do?
What is its mean CV accuracy?
Why should our machine-learning models be compared with this baseline?

---

**Cursor**

Section 4 is the baseline. I’ll build a most-frequent classifier, score it with 5-fold cross-validation on the training data only, and use that mean and spread in the written answers.

The most common training class is No, 121 of 200 students. Five-fold cross-validation on the training data gives a mean accuracy of 0.605, with a standard deviation of 0.01. I’ll put that baseline in section 4 and leave the test set unused.

Section 4 scores a most-frequent baseline with 5-fold cross-validation on the training data. The test set is not used.

**What does the baseline do?** It ignores the study habits. On each fold it finds the most common class in that fold’s training rows and predicts that class for every held-out student. In this training set that class is No: 121 of the 200 students scored below 80. So the baseline always predicts No.

**What is its mean CV accuracy?** 0.605, or 60.5%. The five fold accuracies are 0.625, 0.600, 0.600, 0.600, and 0.600. The standard deviation across folds is 0.010. One validation fold has 25 No students out of 40, and the other four have 24 out of 40. Because the prediction is always No, those rates are the accuracies.

**Why should our machine-learning models be compared with this baseline?** A model is only doing useful work if it beats always saying No. An accuracy around 60% can look acceptable and still mean the model learned nothing about the study habits. Later models should be judged against this 60.5% cross-validation accuracy, using the same training students and the same five folds.

---

**User**

Lets move on to part 6, where I want to understand cross-validation using the data. See section 6, and only edit under the #TODO statement and add cell for Part 6 questions. Use 5-fold cross-validation.

Conceptually, the training data is divided into five parts:
Fold 1: VALIDATE | train | train | train | train
Fold 2: train | VALIDATE | train | train | train
Fold 3: train | train | VALIDATE | train | train
Fold 4: train | train | train | VALIDATE | train
Fold 5: train | train | train | train | VALIDATE
 
Each observation gets an opportunity to appear in a validation fold.

Part 6 Questions:
Explain in your own words:
What happens during 5-fold cross-validation?
How many times is each model trained?
Why is cross-validation more informative than evaluating a model using only one training/validation split?
Why do we still keep a separate final test set?

---

**Cursor**

Section 6 is the cross-validation comparison. I’ll read that cell and add the 5-fold comparison only under the `# TODO` line, then add the Part 6 answers.

The comparison uses the same five folds as the baseline, on the 200 training students only. Each model is trained five times, once for each held-out group of 40.

Section 6 compares the baseline, logistic regression, a decision tree, and a random forest on the same five folds of the 200 training students. Each fold trains on 160 students and validates on 40. The test set is not used.

**What happens during 5-fold cross-validation?** The training students are divided into five groups. The model trains on four groups and is scored on the remaining group, then the held-out group changes until every student has been in the validation set once. Each fold refits the imputer, the scaler, and the encoder on that fold’s training rows only. The five accuracies are averaged, and the standard deviation shows how much the score moves when the held-out students change.

**How many times is each model trained?** Five times. Once for each fold, on the four groups that are not being validated. The cross-validation score is the average of those five checks.

**Why is cross-validation more informative than one training/validation split?** One split of 160 and 40 can be lucky or unlucky. Five folds give five scores, and every training student is validated once. The mean is a steadier estimate, and the spread shows whether the result depends on which 40 students were held out. Logistic regression’s folds run from 0.65 to 0.85, so a single split could have landed on either end.

**Why do we still keep a separate final test set?** The cross-validation scores are used to compare models, so those 200 students play a role in the choice. The 50 test students were set aside before any comparison. They are used once, after a model is chosen, to estimate how it does on students that took no part in the decision.

On these folds, mean accuracy is 0.605 for the baseline, 0.740 for logistic regression, 0.595 for the decision tree, and 0.695 for the random forest. The untuned tree does not beat always predicting No.

---

**User**

Under Part 6 questions, I want to implement Part 7 and 8 of this assignment, where I want to compare three classification models and then compare those models with cross-validation. Lets start with Part 7. Create three classifiers:
Model 1 — Logistic Regression
Use: LogisticRegression

Model 2 — Decision Tree
Use DecisionTreeClassifier
Start with max_depth=4

Model 3 — Random Forest
Use RandomForestClassifier
Use a reasonable number of trees, such as n_estimators=200
Use random_state=42 where appropriate.

Then part 8: Evaluate all three models using the same 5-fold cross-validation procedure on the training data.
Also include your majority-class baseline.
Calculate at least mean accuracy, standard deviation of accuracy, precision, and recall.
Create a comparison table similar to the one in the photo provided. 

Part 8 Questions:
Which model has the highest mean CV accuracy?
How large are the differences?
Which model has the highest recall?
Do all metrics identify the same model?
How much does performance vary between folds?

---

**Cursor**

Part 7 and 8 sit after the Part 6 questions. I’ll fit logistic regression, a depth-4 tree, and a 200-tree forest, then score them with the same 5-fold split as the baseline so the comparison table matches the photo.

The scores are in. Logistic regression leads on accuracy, precision, and recall. I’ll add Part 7 and Part 8 after the Part 6 questions, with a comparison table in the same layout as the photo.

Part 8 calls `cross_validate`, which is not imported yet. I’ll add that import, and import the three classifiers in the Part 7 cell so it does not depend on the earlier comparison cell.

Part 7 and Part 8 are in the notebook, just after the Part 6 questions. All four models use the same five folds of the 200 training students. Precision and recall treat Yes as the positive class. The test set is not used.

| Model | Mean CV Accuracy | Std. Accuracy | Precision | Recall |
| --- | --- | --- | --- | --- |
| Majority baseline | 0.605 | 0.010 | 0.000 | 0.000 |
| Logistic Regression | 0.740 | 0.064 | 0.728 | 0.571 |
| Decision Tree | 0.670 | 0.040 | 0.598 | 0.493 |
| Random Forest | 0.690 | 0.072 | 0.642 | 0.518 |

**Which model has the highest mean CV accuracy?** Logistic regression, at 0.740. The random forest is 0.690, the decision tree is 0.670, and the majority baseline is 0.605.

**How large are the differences?** Logistic regression is 0.050 above the random forest and 0.070 above the decision tree. The forest is 0.085 above the baseline, and the tree is 0.065 above it. Logistic regression is 0.135 above always predicting No. The 0.050 gap between the two best models is smaller than logistic regression’s own fold-to-fold standard deviation of 0.064, so the average ranking is clear and one unlucky fold could still put the forest ahead.

**Which model has the highest recall?** Logistic regression, with a mean recall of 0.571 for Yes. The random forest is 0.518 and the decision tree is 0.493. The baseline recall is 0, because it never predicts Yes.

**Do all metrics identify the same model?** Yes. Logistic regression is highest on accuracy, precision, and recall, and the order is the same in every column: logistic regression, then random forest, then the decision tree, then the baseline. Accuracy still makes the baseline look closer than it is. Always predicting No is right about 60.5% of the time, while its precision and recall for Yes are both 0.

**How much does performance vary between folds?** The baseline barely moves, from 0.600 to 0.625. Logistic regression’s accuracy runs from 0.650 to 0.850. The decision tree runs from 0.625 to 0.725. The random forest runs from 0.625 to 0.800. Recall moves more than accuracy. Logistic regression’s Yes recall runs from 0.375 to 0.688, and the decision tree’s runs from 0.375 to 0.750. The mean across five folds is the fairer comparison.

---

**User**

For part 9, see section 7. Here I want to tune one hyperparamerter. Only edit underneath #TODO (dont remove this statement) and add cell for questions. A parameter is learned from data during training. A hyperparameter is chosen before training. For a Decision Tree, one important hyperparameter is max_depth. It controls how deep the tree is allowed to grow.

Part 9 Question
Explain the difference between a model parameter ans hyperparameter. Then explain the distinction in your own words using max_depth as the example.

---

**Cursor**

Section 7 is the `max_depth` search. I’ll keep the `# TODO` line, tune the tree with the same 5-fold split on the training data, and add the parameter-versus-hyperparameter answer underneath.

Section 7 tunes `max_depth` on the same five training folds. The `# TODO` line is still there. Validation accuracy is highest at depth 4 (0.670). Training accuracy keeps climbing and reaches 1.000 when the depth is unlimited, while validation accuracy falls to 0.595. The test set is not used.

**A model parameter is learned from the data during training.** When `fit` runs, the algorithm looks at the training rows and sets those values. **A hyperparameter is chosen before training.** It is a setting of the algorithm, and the training rows do not estimate it.

For this decision tree, the parameters are the splits the tree settles on: which feature to test, the cutoff on that feature, and the class label stored in each leaf. Those come from the 160 students in a training fold. `max_depth` is a hyperparameter. We choose it before `fit` runs, and it limits how many layers of splits the tree may use. At depth 1 the tree is a single question. With no depth limit, the tree separates the training students perfectly, and the validation score gets worse. The extra layers are memorizing the training fold. Cross-validation picks depth 4, because that depth has the highest mean validation accuracy.

---

**User**

I want to add the Part 10 work under Part 9 questions. For part 10, I want to experiment with Decision-Tree Depth. Now investigate: max_depth
Try:
1
2
3
4
6
8
unlimited (None)
For each depth, calculate the mean training accuracy, the mean cross-validation accuracy, and the standard deviation of CV accuracy.
Create a table such as the one in the picture provided. 

---

**Cursor**

Part 10 goes right after the Part 9 questions. I’ll use the same five training folds and build the depth table for 1, 2, 3, 4, 6, 8, and unlimited.

Part 10 is in the notebook, directly under the Part 9 question. It scores the decision tree at depths 1, 2, 3, 4, 6, 8, and unlimited on the same five training folds. The test set is not used.

| max_depth | Training Accuracy | CV Accuracy | CV Std. |
| --- | --- | --- | --- |
| 1 | 0.661 | 0.560 | 0.066 |
| 2 | 0.712 | 0.625 | 0.057 |
| 3 | 0.772 | 0.610 | 0.051 |
| 4 | 0.826 | 0.670 | 0.040 |
| 6 | 0.925 | 0.615 | 0.056 |
| 8 | 0.979 | 0.620 | 0.043 |
| None | 1.000 | 0.595 | 0.060 |

Depth 4 has the highest cross-validation accuracy, 0.670. Training accuracy keeps rising as the tree gets deeper and reaches 1.000 with no depth limit, while the validation accuracy falls back to 0.595.

---

**User**

Under the Part 10 implementation, lets add part 11. Here I want to Visualize Model Complexity. Create a plot showing
x-axis: max_depth and y-axis: accuracy

Plot two lines:
training accuracy;
cross-validation accuracy.

Part 11 Questions:
What happens to training accuracy as max_depth increases?
What happens to cross-validation accuracy?
At what depth does the tree appear to perform best on unseen data?
Do you see evidence of underfitting?
Do you see evidence of overfitting?

---

**Cursor**

Part 11 will use the Part 10 depth results. I’ll add the training-versus-validation plot under that table and answer the five questions from those scores.

Part 11 is under the depth table. The plot uses those seven depths: training accuracy on one line, cross-validation accuracy on the other.

**What happens to training accuracy as max_depth increases?** It rises at every step. It goes from 0.661 at depth 1 to 0.712, 0.772, 0.826, 0.925, and 0.979 at depth 8. With no depth limit it reaches 1.000. A deeper tree fits the training students more closely, until an unlimited tree separates them perfectly.

**What happens to cross-validation accuracy?** It does not follow the training line. It moves from 0.560 at depth 1 to 0.625 at depth 2 and 0.610 at depth 3, then peaks at 0.670 at depth 4. After that it falls to 0.615 at depth 6, 0.620 at depth 8, and 0.595 with no limit.

**At what depth does the tree appear to perform best on unseen data?** Depth 4. Its mean cross-validation accuracy is 0.670, the highest of the seven depths, and its standard deviation is the smallest, 0.040.

**Do you see evidence of underfitting?** Yes, at depth 1. Training accuracy is only 0.661, and cross-validation accuracy is 0.560, below the majority baseline of 0.605. The tree is allowed one split, so both lines stay low.

**Do you see evidence of overfitting?** Yes, after depth 4. Training accuracy keeps climbing toward 1.000 while cross-validation accuracy drops from 0.670 to 0.595. The gap between the two lines gets wider. With no depth limit the tree is perfect on the training rows and only 0.595 on the held-out rows, just under the baseline. The extra depth is memorizing the training fold.

---

**User**

Now to part 12, which is to be put under our part 11 work. Here I want to Understand Underfitting and Overfitting. Use the results to explain these concepts.
Underfitting: A model may be too simple to capture important patterns.
Typical pattern:
Training performance: poor
Validation performance: poor

Good Generalization: The model captures useful patterns that transfer to unseen data.
Typical pattern:
Training performance: good
Validation performance: good

Overfitting: The model learns the training data extremely well but does not generalize as well.
Typical pattern:
Training performance: extremely high
Validation performance: noticeably lower

part 12 Questions:
Which Decision Tree depth appears to underfit?
Which depth appears to generalize best?
Do the deepest trees show signs of overfitting?
Why should we not simply choose the tree with the highest training accuracy?

---

**Cursor**

Part 12 goes under the Part 11 questions. I’ll map the depth results onto underfitting, generalization, and overfitting, then answer the four questions from those scores.

Part 12 is under the Part 11 questions. It reads the depth table as three patterns.

**Underfitting** means the tree is too simple, so both scores stay poor. Depth 1 has training accuracy 0.661 and cross-validation accuracy 0.560, below the baseline of 0.605.

**Good generalization** means the pattern also shows up on held-out students. Depth 4 has training accuracy 0.826 and cross-validation accuracy 0.670, the highest validation score of the seven depths.

**Overfitting** means the tree fits the training rows extremely well and does worse on students it did not train on. Depth 8 reaches training accuracy 0.979 with cross-validation accuracy 0.620. With no depth limit, training accuracy is 1.000 and cross-validation accuracy is 0.595.

**Which depth appears to underfit?** Depth 1. Both scores are poor, and the validation score is below always predicting No.

**Which depth appears to generalize best?** Depth 4. Its cross-validation accuracy is 0.670, the best in the experiment, and the training accuracy of 0.826 shows the tree has actually learned a pattern.

**Do the deepest trees show signs of overfitting?** Yes. At depth 8 and with no limit, training accuracy is extremely high and validation accuracy is noticeably lower. The unlimited tree is perfect on the training fold and about the same as the baseline on the held-out fold.

**Why should we not simply choose the tree with the highest training accuracy?** That choice is the unlimited tree, at 1.000. Its cross-validation accuracy is 0.595, below depth 4 and about the same as always predicting No. The highest training score means the tree memorized the training fold. The depth to keep is the one with the best validation accuracy, which is depth 4.

---

**User**

For parts 13 and 14, add under part 12 questions cell. For part 13, I want to select a Decision-Tree Depth. Based on cross-validation, choose an appropriate value of max_depth. Explain your decision. Do not simply write Depth 4 had the highest score.
Discuss:
mean CV performance;
variability;
model complexity.
If several depths perform very similarly, choosing the simpler model can be reasonable.

For Part 14, I want to compare the Tuned Tree Again. Create a Decision Tree using the depth you selected. Evaluate it using the same 5-fold cross-validation.
Compare:
baseline;
Logistic Regression;
original Decision Tree;
tuned Decision Tree;
Random Forest.

Update your comparison table.

part 14 Question:
Based only on the training-data cross-validation results, which model would you carry forward to final evaluation? Explain your reasoning.

Do not look at the test set before making this decision

---

**Cursor**

Depth 4 is the choice: it has the highest validation accuracy and the smallest fold-to-fold spread, and the simpler trees give up too much accuracy to prefer them. I’ll record that depth, then rebuild the comparison table with the tuned tree included. The test set stays unused.

Parts 13 and 14 are under the Part 12 questions. The depth choice and the model choice both use the training folds only.

**Part 13.** The selected depth is 4.

Depth 4 has the best mean validation accuracy, 0.670. The next simpler tree, depth 2, is 0.625, and depth 8 is 0.620. Those gaps are 0.045 and 0.050. Depth 4 also has the smallest standard deviation, 0.040, with folds from 0.625 to 0.725. Depth 8 is nearly as steady, at 0.043, and its mean is lower. Depths 6, 8, and unlimited fit the training rows more tightly and do worse on the held-out folds, so the extra layers are not helping. Depths 1, 2, and 3 are simpler, and they give up too much validation accuracy. A simpler tree would be reasonable if another depth sat close to 0.670. None does. Depth 2 is 0.045 behind, which is larger than depth 4’s own standard deviation.

**Part 14.** The tuned tree uses that depth. It matches the original tree, because Part 8 already used `max_depth=4`.

| Model | Mean CV Accuracy | Std. Accuracy | Precision | Recall |
| --- | --- | --- | --- | --- |
| Majority baseline | 0.605 | 0.010 | 0.000 | 0.000 |
| Logistic Regression | 0.740 | 0.064 | 0.728 | 0.571 |
| Decision Tree | 0.670 | 0.040 | 0.598 | 0.493 |
| Tuned Decision Tree | 0.670 | 0.040 | 0.598 | 0.493 |
| Random Forest | 0.690 | 0.072 | 0.642 | 0.518 |

**Which model would you carry forward?** Logistic regression. It leads on accuracy, precision, and recall. It is 0.135 above the baseline, 0.070 above the tuned tree, and 0.050 above the random forest. The tree is steadier, with a standard deviation of 0.040, and its mean is lower on every metric. Tuning confirmed the starting tree. It did not change which model goes to the final evaluation.

---

**User**

Lets now move on to part 15(see section). Only edit under #TODO and add cell for questions. Here I want to perform a Final Test Evaluation. Now you may use the held-out test set. Take the model you selected based on cross-validation. Fit it using the complete training set. Evaluate it once on the test set.

Report:
accuracy;
precision;
recall;
confusion matrix.
Also calculate the majority-class test accuracy for context.

part 15 Questions:
How does final test accuracy compare with mean CV accuracy?
Is it reasonably consistent with what you observed during cross-validation?
Did the model outperform the majority-class baseline?
Are precision and recall similar to the CV results?

---

**Cursor**

Section 8 is the one-time test evaluation. I’ll fit the logistic regression model chosen from cross-validation on the full training set, score it once on the held-out test set, and answer the Part 15 questions from those results.

Section 8 fits the logistic regression model from the cross-validation comparison on all 200 training students and scores it once on the 50 test students. The `# TODO` line is still there.

Test accuracy is **0.840**, precision is **0.875**, and recall is **0.700**. The confusion matrix is 28 true negatives, 2 false positives, 6 false negatives, and 14 true positives. The majority-class baseline, which always predicts No, has a test accuracy of **0.600**.

**How does final test accuracy compare with mean CV accuracy?** Test accuracy is 0.840. Mean cross-validation accuracy was 0.740. The test score is 0.100 higher.

**Is it reasonably consistent with cross-validation?** Yes. The five folds were 0.650, 0.725, 0.725, 0.750, and 0.850, with a standard deviation of 0.064. The test accuracy of 0.840 sits near the highest fold and inside that spread. The test set has only 50 students, so one student changes the accuracy by 0.020. The result is on the high side of the folds, and it is the same kind of score those folds already produced.

**Did the model outperform the majority-class baseline?** Yes. The baseline is right on 30 of the 50 test students. Logistic regression is right on 42, which is 12 more.

**Are precision and recall similar to the CV results?** They are higher than the cross-validation means, and they sit at the high end of the folds. Mean CV precision was 0.728, with folds from 0.600 to 1.000. Test precision is 0.875, inside that range. Mean CV recall was 0.571, with folds from 0.375 to 0.688. Test recall is 0.700, just above the best fold. The test set is a bit kinder than the five-fold average. The pattern is the same: most Yes predictions are correct, and the model still misses some students who scored 80 or above.

---

**User**

For part 16, I want to analyze the Final Errors. Using the final model, identify false positives and false negatives. Display the feature values for several incorrectly classified students.

part 16 Questions:
How many false positives occurred?
How many false negatives occurred?
Do you notice any patterns among the mistakes?
Are some observations likely more difficult to classify than others?
Be careful about causal language.

You may form hypotheses about why the model made mistakes, but the model does not establish why a particular student obtained a particular score.

---

**Cursor**

Part 16 is the error analysis. I’ll find the misclassified test students from the final logistic regression model and look at their feature values before writing the answers.

The final model misses 8 of the 50 test students: 2 false positives and 6 false negatives. I’ll list their habit values in the error-analysis cell and keep the wording to what the model saw, not why a student scored what they scored.

Part 16 is in the error-analysis section. The final logistic regression model misses 8 of the 50 test students. The notebook lists the habit values for all of them. `exam_score` is shown only because it defines the label. It was not a predictor.

**How many false positives occurred?** 2. S170 and S133 were predicted Yes, and both scored below 80.

**How many false negatives occurred?** 6. S081, S141, S114, S038, S100, and S090 were predicted No, and all six scored 80 or above.

**Do you notice any patterns among the mistakes?** Five of the eight have a Yes probability between 0.469 and 0.541, so they sit next to the model's 0.5 cutoff. Both false positives are in that group. S170 has a Yes probability of 0.541, with 9.4 study hours and 98.3% attendance. S133 has a Yes probability of 0.501, with 9.7 study hours and 92.9% attendance. In the training set, the Yes medians were about 8.9 study hours and 89.5% attendance. A hypothesis is that the model treated those habits as closer to the training students labeled Yes. That is a hypothesis about the prediction, not a claim that those habits caused either score. S133's exam score is 66.8, so the habits and the label do not line up for that student. Three false negatives are farther from 0.5. S038, S100, and S090 have Yes probabilities of 0.339, 0.331, and 0.298. Their study hours are 5.5, 5.7, and missing, and their attendance rates are 78.3, 82.7, and 72.7, on the low side of the training medians. The model assigned them a clearly lower Yes probability, and the actual label is still Yes.

**Are some observations likely more difficult to classify than others?** Yes. A Yes probability near 0.5 is a close call for this model. S081, at 0.496, is one of those. A second kind of close call comes from the label. `high_exam_score` flips at 80. S170 scored 79.6 and was predicted Yes. S038 scored 80.1 and was predicted No. The scores are less than half a point apart, and the labels are opposite. The model does not establish why either student received that score.

---

**User**

Now to part 17 and 18, which I want to implement under part 16 questions. 
For part 17, I want to ask the question: Why Didn't We Tune Using the Test Set?
Imagine the following workflow:
Try Logistic Regression
        ↓
check TEST accuracy
        ↓
Try Decision Tree
        ↓
check TEST accuracy
        ↓
Change max_depth
        ↓
check TEST accuracy
        ↓
Change max_depth again
        ↓
check TEST accuracy
        ↓

Choose the highest test result
part 17 Questions:
What is wrong with this procedure?
How has the test set indirectly become part of model development?
Why is the final test score no longer a completely independent evaluation?

Now compare it with:
TRAINING DATA
      ↓
cross-validation
      ↓
compare models
      ↓
tune hyperparameters
      ↓
select model
      ↓
FINAL TEST
Explain why the second workflow is preferable.

For part 18, I want to understand scaling and Different Models. We used StandardScaler in the preprocessing pipeline. However, not all models depend on scaling in the same way.
Investigate:
Logistic Regression
Decision Tree
Random Forest

part 18 Questions:
Why is scaling useful for Logistic Regression?
Why do Decision Trees generally not require scaling?
Why do Random Forests generally not require scaling?

Consider a tree rule such as: attendance_rate < 85
If attendance is standardized, the numerical threshold changes, but the ordering of the observations remains the same. This is fundamentally different from algorithms that depend on distances or optimization over differently scaled features.

---

**Cursor**

Parts 17 and 18 belong under the Part 16 questions. I’ll write them from the workflow we actually used: cross-validation on the training students, then one look at the test set.

The first workflow uses the 50 test students to pick the winner. I’ll add that explanation, then a short training-only check that a tree cutoff such as attendance below 85 keeps the same students after scaling.

Parts 17 and 18 are under the Part 16 questions. The scaling check uses the training students only.

**What is wrong with checking the test set after every change?** The test accuracy is being used to choose the model and the depth. Each check is another look at the same 50 students, and the next try is kept or dropped because of that look. Choosing the highest test result is model selection done on the test set.

**How has the test set indirectly become part of model development?** Those 50 rows are not passed to `fit()`. Their labels still steer the search. A depth is tried, the test accuracy is read, and another depth is tried when the number is disappointing. The settings that remain are the ones that scored well on those particular students. The test set has taken the role that cross-validation had on the 200 training students.

**Why is the final test score no longer a completely independent evaluation?** An independent evaluation is a score computed after the model is fixed, on students who did not influence the choice. In that procedure the reported score is the best of several scores on the same students. It is the score of the option that won the comparison. In our own folds, logistic regression’s accuracy already ran from 0.650 to 0.850. Repeated looks at one group of 50 can land on a high number in the same way one lucky fold did.

The workflow we used is preferable because the choices stayed on the training folds. Cross-validation compared the models, selected depth 4, and carried logistic regression forward. The test accuracy of 0.840 was computed once, after that choice, so those 50 students played no role in the selection.

**Why is scaling useful for logistic regression?** It multiplies each feature by a weight, and the default model penalizes large weights. Study hours are small numbers, attendance is usually in the 70s to 100, and commute minutes can be near 0 or well over 100. A one-unit step is one hour for study time and one percentage point for attendance, and the penalty treats those weights as if the units were the same. `StandardScaler` puts each numeric training column on a common scale, so a weight refers to a comparable step in each column.

**Why do decision trees generally not require scaling?** A tree asks a question about one column at a time. On the training students, attendance has mean 85.37 and standard deviation 9.63, so `attendance_rate < 85` becomes scaled attendance `< -0.039`. The printed threshold changes. The students do not. All 95 training students below 85 are the students below -0.039. This is different from an algorithm that adds a weight times a feature, or that uses the distance between students.

**Why do random forests generally not require scaling?** A random forest is a collection of those trees. Each tree splits on the order of values in one feature, so rescaling a column changes the printed cutoff and leaves the groups the same. The shared pipeline still scales every model, because logistic regression needs that common scale and all three models then see the same prepared columns.

---

**User**

Now to part 19, where I want to conduct one final experiment. Implement under the Part 18 questions. Design one additional experiment related to the concepts in this assignment, which is that I want to examine precision/recall instead of accuracy when selecting a tree depth. Before running the experiment
Write: My Hypothesis: I expect ______ because ______.

Then:
perform the experiment;
report your results;
explain whether the results support your hypothesis.
Important
Do not use the final test set for this experiment.

Use cross-validation on the training data.

---

**Cursor**

Part 19 will select tree depth by precision and recall on the training folds, not by accuracy, and it will not touch the test set. I’ll write the hypothesis from the depth results we already have, then run the cross-validation check.

Part 19 is under the Part 18 questions. It rescores the same seven depths with 5-fold cross-validation on the training data. The test set is not used.

**My Hypothesis:** I expect a deeper tree than depth 4 to have the highest mean cross-validation recall, because accuracy is pulled toward the majority class, No. The depth-4 tree’s recall was 0.493, so it missed about half of the held-out Yes students. Extra depth gives the tree more splits that might separate those students on the validation folds. I expect precision not to select that same deeper tree. Deeper trees already overfit on accuracy, and a rule that catches more Yes students can also mark more No students as Yes, which lowers precision.

| max_depth | CV Accuracy | CV Precision | CV Recall |
| --- | --- | --- | --- |
| 1 | 0.560 | 0.349 | 0.312 |
| 2 | 0.625 | 0.574 | 0.341 |
| 3 | 0.610 | 0.521 | 0.509 |
| 4 | 0.670 | 0.598 | 0.493 |
| 6 | 0.615 | 0.512 | 0.471 |
| 8 | 0.620 | 0.522 | 0.520 |
| None | 0.595 | 0.477 | 0.509 |

The results support the hypothesis. Mean recall is highest at depth 8, at 0.520, rather than at depth 4, at 0.493. Mean precision is highest at depth 4, at 0.598. Depth 8’s precision is 0.522. Accuracy and precision select depth 4. Recall selects the deeper tree.

The recall gain is small. Depth 8 is 0.027 above depth 4. Depth 3 and the unlimited tree are both at 0.509, only 0.011 behind depth 8, and depth 8’s recall standard deviation is 0.079. Selecting on recall alone would pick the more complex tree for a small increase in found Yes students, and that tree is less precise. If the goal is finding students who score 80 or above, depth 8 is the recall choice on these training folds. If the goal is the best balance of correct Yes predictions and overall accuracy, depth 4 remains the choice.

---

**User**

Finally on to Part 20, where I want to write the AI reflection. Describe at least one situation where AI helped you:
understand cross-validation;
construct a cross-validation experiment;
understand overfitting;
compare training and validation scores;
understand hyperparameters;
create the max_depth experiment;
interpret results;
debug code.

Answer:
What did you ask?
What did the AI recommend?
Did you accept the recommendation?
How did you verify it?
Did you simplify or modify the AI's proposed solution?
What did you learn?
Also answer:

Did the AI ever suggest using the test set while comparing or tuning models? If so, what did you do?

---

**Cursor**

Part 20 is in the conclusion section. It summarizes the evidence, then answers the reflection from the max_depth experiment.

**What did you ask?** How to compare tree depths without touching the test set, and how to tell underfitting from overfitting.

**What did the AI recommend?** Score depths 1, 2, 3, 4, 6, 8, and unlimited with the same five training folds, and record mean training accuracy next to mean validation accuracy and its standard deviation. The same folds, with the preprocessor refit inside each fold, were the recommendation for comparing the baseline, logistic regression, the tree, and the random forest.

**Did you accept the recommendation?** Yes. The depth table and the model comparison both use those training folds.

**How did you verify it?** Training accuracy rose from 0.661 at depth 1 to 1.000 with no limit. Validation accuracy peaked at 0.670 at depth 4 and fell to 0.595 with no limit. Depth 1 fell below the baseline of 0.605. The baseline’s mean cross-validation accuracy was 0.605, which matches 121 No students out of 200. Adding precision and recall left logistic regression at 0.740 and the depth-4 tree at 0.670.

**Did you simplify or modify the AI’s proposed solution?** Yes. The first depth list also included 5 and 10. It was cut to the seven depths in the assignment table. Depth 4 was still the validation peak, so the shorter list did not change the choice.

**What did you learn?** `max_depth` is chosen before `fit`. The splits inside the tree are what training learns. The training line climbed as the tree got deeper, and the validation line did not follow it.

**Did the AI ever suggest using the test set while comparing or tuning models?** No. The test set stayed unused until logistic regression had already been selected. It was then scored once, and the eight misclassified test students were listed after that. When recall preferred depth 8 by 0.027 over depth 4, that comparison stayed on the training folds.

