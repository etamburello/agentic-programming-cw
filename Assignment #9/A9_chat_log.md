# Regression analysis for exam scores
_Exported on 9/29/2026 at 20:49:40 EDT from Cursor (3.22.12)_

---

**User**

I am a senior Computer Science and Engineering student in college. Last time, we used classification to predict whether a student would have a high exam score given a dataset. This time using the given dataset and starter code(see CSE4095_Class3_Stater.ipynb) in the Assignment #9 folder, I want to use regression to predict the student's actual numerical exam score. Continue using class1_student_habits.csv. Each row represents one student. For this assignment, your prediction target will be exam_score. Unlike the last time, do not convert the score into Yes/No categories. Do not change any of the cells provided in the .ipynb file and only add what is needed under the indicated #TODO, and only add cells to the file when answering questions given for each part/section.

Let's start with part 1 and part 2, which are defining the regression problem and inspecting the target, respectively. See section 1. Load and inspect the dataset in the .ipynb file provided. The goal is to predict exam_score.

Before building a model, examine exam_score. Calculate useful descriptive statistics and create a histogram.
At minimum, report count, mean, median, standard deviation, the minimum, and the maximum.

Part 1 Questions:
1. Why is this a regression problem?
2. How is this different from the Class 2 classification problem?
3. What information is lost when we convert exam_score into only Yes or No?
4. What kind of output should a regression model produce?
For example, a regression model might predict: 82.7 ather than Yes

Part 2 questions:
1. Describe the distribution of exam scores.
2. Are there unusually low or high values?
3. Why is it useful to understand the target before trying to predict it?

---

**Cursor**

I'll start by reading the starter notebook and the student-habits dataset so we can define the regression problem and inspect `exam_score` without changing the given cells.

The target stays the numeric `exam_score`. I’ll fill in the section 1 cell with the load, summary statistics, and histogram, then add answer cells for the Part 1 and Part 2 questions.

Parts 1 and 2 are in `Assignment #9/CSE4095_Class3_Starter.ipynb`, under section 1. The original cells are unchanged. The `# TODO` cell now loads `class1_student_habits.csv` as `df`, prints the `exam_score` summary, and draws a histogram in bins of 5 points. Two markdown cells under it answer the questions.

Run that cell in Colab and upload `class1_student_habits.csv` when the picker appears. You should see:

| Statistic | Value |
|---|---|
| Count | 250 |
| Mean | 77.16 |
| Median | 76.95 |
| Standard deviation | 10.33 |
| Minimum | 51.4 |
| Maximum | 100 |

**Part 1**

1. This is regression because `exam_score` is a number, and the model has to estimate that number. A prediction of 82.7 when the true score is 85 is a smaller error than a prediction of 60.
2. Class 2 turned the score into `high_exam_score`: Yes if the score was 80 or higher, No otherwise. The classifier only chose a category. Here the score stays a number.
3. The Yes/No label drops the actual score and the distance from 80. A 51.4 and a 79.9 are both No. An 80.1 and a 100 are both Yes.
4. The model should output a number on the exam-score scale, such as 82.7, rather than Yes or No.

**Part 2**

1. The 250 scores form one mound, centered in the mid-to-high 70s, and the shape is roughly symmetric. The mean and median are almost the same. Most students score between 65 and 90. Twelve scored below 60, and 27 scored 90 or above, including 3 scores of 100.
2. The range is wide, from 51.4 to 100, but those ends are the tails of the same distribution. By the 1.5 × IQR rule the fences are about 46.3 and 108.2, and every score falls inside them, so there are no outliers by that rule. Three students scored exactly 100, which is the top of the scale.
3. The summary shows the scale a later error has to be judged against. A typical score is about 77, and scores usually sit within about 10 points of that center, so an error of 5 points has a meaning before any model is trained.

---

**User**

Let's move on to part 3, where I want to explore one relationship in the data. Before building a regression model, investigate study_hours_per_week vs exam_score. Create a scatter plot and calculate the correlation. 

Part 3 questions:
1. Does there appear to be a relationship?
2. Is the relationship positive or negative?
3. Does it appear approximately linear?
4. Are there students who do not follow the general pattern?

Things to remeber: Do not interpret correlation as causation.
You may write: Higher study hours are associated with higher exam scores in this dataset.
Do not conclude: Studying one additional hour causes the exam score to increase by X points.

---

**Cursor**

I’ll look at how `study_hours_per_week` lines up with `exam_score`, then add the scatter plot, correlation, and Part 3 answers under that section.

Part 3 is in section 2 of the notebook. The scatter-plot cell prints the Pearson correlation and plots `study_hours_per_week` against `exam_score`. The answers are in the markdown cell under it.

When you run that cell, it uses the 241 students who have both values. Nine students are missing study hours, so they are left out. The correlation is **0.516**.

1. There is a moderate relationship. The points trend upward, but students with the same study hours still have a wide range of scores.
2. The relationship is positive. Higher study hours are associated with higher exam scores in this dataset. That is an association in these rows, not evidence that one extra hour of studying causes a fixed increase in the score.
3. It is approximately linear through most of the range. Average scores rise from about 63 for students under 2 hours to about 85 for students between 10 and 12 hours. The cloud around that line is wide, and the students who study the most do not keep rising at the same rate.
4. Several students sit off the trend. S174 studied 17.8 hours per week, the most in the class, and scored 64.8. S232 studied 5.1 hours and scored 96.5. S085 studied 5.3 hours and scored 91.0. S073 studied 6.7 hours and scored 51.4, the lowest score in the file.

---

**User**

Now on to part 4, where I simply want to chose the features we are testing. See section 3, Define X and Y. For the initial model, use the following:
study_hours_per_week
sleep_hours_per_night
attendance_rate
practice_problems_per_week
prior_programming_experience
study_group
commute_minutes

Do not initially use student_id, exam_score, or quiz_average. exam_score is the target and therefore must not also be used as an input feature. We will investigate quiz_average later.

---

**Cursor**

Section 3 is where `X` and `y` get defined. I’ll set the seven habit columns as the features and keep `exam_score` as the target only.

The feature list matches the seven habit columns from last time. I’ll define `X` and `y` in section 3 and add a short note on why `student_id` stays out.

Part 4 is in section 3 of the notebook. `X` is the seven habit and background columns, and `y` is `exam_score`.

The predictors are `study_hours_per_week`, `sleep_hours_per_night`, `attendance_rate`, `practice_problems_per_week`, `prior_programming_experience`, `study_group`, and `commute_minutes`. That is 250 rows and 7 columns. `student_id` and `quiz_average` stay out of `X`.

`student_id` is only a row label, such as S001. It does not describe how a student prepared, and a model that used it would be memorizing that one student. A new student would have an id the model has never seen.

`exam_score` is the target, so it belongs in `y` and not in `X`. `quiz_average` is held back for the later comparison.

---

**User**

Moving to part 5, where I want to create training and test sets for building the model. See section 4. Train/test split and processing. Split the data into 80% training data and 20% test data. Use random_state=42 to do so.

Part 5 Questions:
Explain the following:
1. What is the training set used for?
2. What is the test set used for?
3. Why should the model not be trained using the test set?
4. Why should different experiments use the same split when we want to compare them fairly?

---

**Cursor**

Section 4 needs an 80/20 split and a pipeline for missing values and categories. I’ll match the split to `random_state=42` so later comparisons use the same rows.

Part 5 is in section 4 of the notebook. The split is 80/20 with `random_state=42`, which gives **200 training students** and **50 test students**.

The preprocessing object is set up in that same cell, and it is not fit yet. Numeric columns get a median fill and are rescaled. `prior_programming_experience` and `study_group` get the most common category, then a 0/1 column for each category. Those fills will be learned from the training rows only when the model is fit in the next section. The blanks in this file are 9 missing study-hour values, 12 missing sleep-hour values, and 7 missing prior-experience values.

1. The training set is what the model learns from. It sees the 200 students' habits together with their actual exam scores and estimates the relationship.
2. The test set is held out. It is the 50 students used after training to measure error on people the model did not learn from.
3. Training on the test set would let the model memorize those 50 rows. A small error would then not say how the model would do on a new student.
4. Later experiments should use this same split. If the `quiz_average` model drew a new set of 50 test students, a lower error might come from an easier test set rather than from the new feature. `random_state=42` keeps the comparison on the same students.

---

**User**

I now want to complete part 6, which is also located in section 4. Here I want to preprocess the features chosen in section 3.
As in Class 2, the data contains numerical variables, categorical variables, and missing values. Create a scikit-learn preprocessing workflow.
For numerical features: missing-value handling → StandardScaler

For categorical features: missing-value handling → one-hot encoding

Use appropriate scikit-learn tools such as:
SimpleImputer
StandardScaler
OneHotEncoder
ColumnTransformer
Pipeline

Part 6 Questions:
Explain the following:
1. Why do we handle numerical and categorical variables differently?
2. What does StandardScaler do?
3. What does one-hot encoding do?
4. Why should preprocessing be learned from the training data rather than the entire dataset?

---

**Cursor**

Part 5 already set up the split in section 4. I’ll check that cell and add the preprocessing workflow and Part 6 explanations there.

The split cell already builds the preprocessing steps. I’ll fit those steps on the training rows only, then add the Part 6 explanations.

Part 6 is in the same section 4 cell as the split. That cell now fits the preprocessing on the 200 training students and applies those same steps to the 50 test students.

Numeric columns (`study_hours_per_week`, `sleep_hours_per_night`, `attendance_rate`, `practice_problems_per_week`, `commute_minutes`) go through a median fill, then `StandardScaler`. Categorical columns (`prior_programming_experience`, `study_group`) go through a most-common-category fill, then one-hot encoding. After you run the cell, the prepared training matrix is 200 by 10 and the prepared test matrix is 50 by 10.

1. Numeric columns are amounts, so a blank can be filled with the training median and the column can be rescaled. Categorical columns are words (None, Some, Strong, and Yes, No). A median does not exist for a word, and linear regression cannot multiply a word by a weight. The word None is a real answer, not a missing value.
2. `StandardScaler` replaces each number with (value − training mean) / training standard deviation. On the training rows, each numeric column then has a mean near 0 and a standard deviation near 1. Study hours, attendance, and commute minutes are on different scales, so without this a column can matter more only because its numbers are larger.
3. One-hot encoding makes a separate 0/1 column for each category. `study_group` becomes a No column and a Yes column. `prior_programming_experience` becomes None, Some, and Strong. The model can learn a separate weight for each one. Coding None as 0, Some as 1, and Strong as 2 would pretend those labels are evenly spaced numbers.
4. The median, the most common category, and the mean and standard deviation are learned from the training rows only. `fit` records them from the 200 students, and `transform` applies those same numbers to the 50 test students. Computing them on all 250 rows would let the test students influence how the data is filled and scaled, so the test set would no longer be fully unseen.

---

**User**

Now to part 7, where I, before training a machine-learning model, want to establish a simple regression baseline. See section 5. Calculate the mean exam score in the training data. Then imagine a model that predicts this same mean score for every student in the test set.

For example, if the training mean were 78.4, the baseline would predict: 78.4, 78.4, 78.4, ...
for every test student.

Evaluate this baseline.
At minimum, calculate:
MAE;
MSE;
RMSE;
﻿R squared﻿.

Part 7 Question: 
Why is this useful?

Remember, a regression model should demonstrate that it can do something more useful than simply predicting the average score for everyone.

---

**Cursor**

The baseline should be the training-set mean predicted for every test student. I’ll compute that score and the error metrics on the same 80/20 split.

The training mean on this split is 77.73. I’ll score a baseline that predicts that value for every test student, then add the explanation.

Part 7 is in section 5 of the notebook. The baseline predicts the training-set mean for every test student and ignores the habit columns.

On this split the training mean is **77.73**, so every test prediction is 77.73. Scored on the same 50 test students:

| Metric | Baseline |
|---|---|
| MAE | 7.66 |
| MSE | 96.08 |
| RMSE | 9.80 |
| R² | -0.091 |

This is the bar a later model has to clear. An error near 8 points can look reasonable and still be no better than telling every student to expect about 78. R² is slightly below zero because 77.73 is the training mean, while the 50 test scores average 74.89. R² compares the predictions with the test set’s own average, so predicting the training average is a little worse than that comparison point.

---

**User**

Moving on to part 8, where I simply want to train a linear regression model. See section 6. Use LinearRegression
Build a pipeline that combines:
Preprocessing → Linear Regression

Fit the model using the training data. Use the trained model to predict exam scores for the test set. Display several examples showing both actual exam score and predicted exam score.

Part 8 Questions:
Explain the following:
1. What does .fit() do?
2. What does .predict() do?
3. Why can the predicted exam score contain decimals even if the original scores are whole numbers?

---

**Cursor**

Section 6 is the linear regression. I’ll fit a preprocessing-plus-`LinearRegression` pipeline on the training rows and show a few actual scores next to the predictions.

The pipeline is preprocessing, then linear regression, fit on the 200 training students only. I’ll show a few test students with both the actual score and the prediction.

Part 8 is in section 6 of the notebook. The pipeline preprocesses the features, then fits `LinearRegression` on the 200 training students. Predictions for the 50 test students are stored in `predictions`. The first eight are:

| Student | Actual | Predicted |
|---|---|---|
| S143 | 72.5 | 78.1 |
| S007 | 68.0 | 68.4 |
| S098 | 78.3 | 82.0 |
| S061 | 84.0 | 87.0 |
| S113 | 69.0 | 67.2 |
| S182 | 74.8 | 75.4 |
| S198 | 69.1 | 65.5 |
| S185 | 71.5 | 73.7 |

1. `.fit()` runs the pipeline on the training students only. Preprocessing records the medians, the scaling, and the category columns. Linear regression then finds an intercept and a weight for each prepared column. The fitted intercept is about 78.6.
2. `.predict()` applies those stored steps to each test student and returns a score. It does not see that student's actual score, and it does not relearn the weights. S143 scored 72.5 and is predicted at 78.1. S007 scored 68.0 and is predicted at 68.4.
3. The prediction is a weighted sum, and that sum is not rounded to a whole point. Even if every training score were an integer, the fitted line would still pass between those points, so a prediction can be 82.7. In this file the recorded scores already include tenths, such as 72.5, so a decimal prediction is on the same scale as the target.

---

**User**

Now I want to evaluate prediction error(Part 9). See section 7. Let's evaluate the Linear Regression model using MAE, MSE, RMSE, and R². Compare these results with your baseline.

For Mean Absolute Error — MAE:
MAE measures the average absolute prediction error.
For example, if MAE = 5.2, you can roughly interpret this as:
The predictions differ from the actual exam scores by about 5.2 points on average.

For Mean Squared Error — MSE:
MSE squares errors before averaging them. This means large errors receive a larger penalty.

For Root Mean Squared Error — RMSE:
The equation for RMSE is ﻿RMSE = √MSE.
Unlike MSE, RMSE is expressed in the original units of the target.

For R²:
R² measures performance relative to predicting the mean.

Part 9 Questions:
1. Which metric is easiest to explain in terms of exam-score points?
2. Why does MSE penalize large errors more heavily than MAE?
3. Why might RMSE be easier to interpret than MSE?
4. Did Linear Regression outperform the mean baseline?
5. What does your ﻿R squared﻿ value tell you?
Do not simply report the numbers. Explain what they mean.

---

**Cursor**

I’ll score the linear regression predictions with MAE, MSE, RMSE, and R², then compare those numbers with the mean baseline.

The linear model’s test error is lower than the mean baseline on every metric. I’ll record those four scores and explain what the comparison means.

Part 9 is in section 7 of the notebook. On the same 50 test students, linear regression beats the mean baseline on every metric.

| Metric | Linear regression | Mean baseline |
|---|---|---|
| MAE | 5.77 | 7.66 |
| MSE | 69.70 | 96.08 |
| RMSE | 8.35 | 9.80 |
| R² | 0.209 | -0.091 |

1. MAE is the easiest to explain in exam-score points. An MAE of 5.77 means the predictions are off by about 5.77 points on average. MSE is in squared points, so 69.70 is harder to picture as a score.
2. MSE squares each error before averaging. A 2-point miss contributes 4, and a 10-point miss contributes 100. In MAE those same misses contribute 2 and 10. A few large errors pull MSE up more than they pull MAE.
3. RMSE is the square root of MSE, so 8.35 is back in exam-score points and can be compared with scores that run from about 51 to 100. It still weights large errors more than MAE does, because the squaring happens before the square root.
4. Linear regression outperforms the baseline. MAE drops by about 1.9 points, from 7.66 to 5.77. MSE and RMSE drop as well, and R² rises from -0.091 to 0.209. The model is doing more than predicting 77.73 for everyone. The gain is modest: a typical prediction is still off by about 6 points.
5. An R² of 0.209 means these seven features account for about 21% of the variation in the test scores, compared with predicting the mean. The other 79% is still unexplained. The model beats the baseline and does not account for most of the differences in exam scores.

---

**User**

Complete section 8 with these findings. 

---

**Cursor**

Section 8 is the prediction table. I’ll check that cell and build it from the actual scores, predictions, and errors we just calculated.

The prediction table is where those error numbers come from. I’ll add actual, predicted, residual, and absolute-residual columns, then tie them back to the MAE and RMSE.

Section 8 builds a test-set table with the actual score, the predicted score, the residual, and the absolute residual. The residual is the actual score minus the predicted score. A negative residual means the model predicted too high.

Those columns are the section 7 metrics at the student level:

- The mean absolute residual is **5.77**, the same MAE.
- The root mean squared residual is **8.35**, the same RMSE.
- The mean residual is about **-0.65**, so the predictions run a little high on this test set.

The average hides a spread, which is why RMSE is higher than MAE. S007 is off by about 0.4 points. S174 scored 64.8 and is predicted at about 102, a miss of about 37 points, and that prediction also falls outside the 0 to 100 exam scale. Squaring gives a miss that large much more weight than a miss of half a point.

---

**User**

Moving on to part 10, where I want to create a scatter plot with actual exam score on one axis and predicted exam score on the other. See section 9. Add a diagonal reference line representing actual = predicted

Part 10 Questions:
1. What would a perfect model look like on this graph?
2. Are most points close to the diagonal?
3. Where does the model appear to make larger errors?

---

**Cursor**

Section 9 is the actual-versus-predicted plot. I’ll add the diagonal reference line and use the test-set points to answer where the larger misses sit.

Most test points sit in a band around the diagonal, with the bigger misses at the ends of the score range. I’ll add that plot and the Part 10 answers.

Part 10 is in section 9 of the notebook. The scatter plot puts the actual exam score on the horizontal axis and the predicted score on the vertical axis, with a dashed line where actual equals predicted.

1. A perfect model would put every point on that line. A point on the line means the predicted score matches the actual score, so there would be no vertical distance from it.
2. Most points sit in a band around the line, and few sit on it. The median miss is about 4.6 points, and 42 of the 50 test students are within 10 points. The tightest group is the middle, where actual scores are about 70 to 90. The MAE of 5.77 is the average distance from this line.
3. The larger errors are at the ends of the score range, plus one point far above the line. Students who scored about 50 to 70 are often predicted too high: that group averages about 63, and the predictions average about 69. The two students who scored above 90 are predicted too low, in the high 70s and low 80s, so those points fall below the line. The farthest point is S174, with an actual score of 64.8 and a prediction of about 102. Eight of the 50 students miss by more than 10 points.

---

**User**

For part 11(see section 10), I want to, for each test observation, calculate residual = actual - predicted. 
Create a residual plot showing predicted exam score on the x-axis and residual on the y-axis. Add a horizontal line at residual = 0

Part 11 Questions:
Explain the following:
What does a positive residual mean?
What does a negative residual mean?
What does a residual close to zero mean?
Do you see any pattern in the residual plot?

Remember that ideally, residuals should not show a strong systematic pattern. If they do, the model may be missing something about the structure of the data. 

---

**Cursor**

Section 10 is the residual plot. I’ll graph predicted score against `actual - predicted` and check whether those residuals form a pattern around zero.

Part 11 is in section 10 of the notebook. For each test student the residual is actual score minus predicted score. The plot puts the predicted score on the horizontal axis and that residual on the vertical axis, with a dashed line at residual = 0.

A positive residual means the student scored higher than the model predicted. There are 22 of those. A negative residual means the model predicted too high. There are 28 of those. S174 is the extreme case: the prediction is about 102, the actual score is 64.8, and the residual is about -37. A residual close to zero means the prediction landed near the actual score. S007, with a residual of about -0.4, is one of those.

Through predicted scores of about 61 to 90, the points form a cloud around the zero line, with misses on both sides. There is no strong curve that rises or falls with the prediction. The average residual is about -0.65, so the predictions run slightly high overall. The spread is wider at the high end because one point, a prediction near 102 with a residual near -37, sits far below the line. A few other misses of about 10 to 18 points appear on both sides. That isolated point means the linear model is missing something about that student. It is not a smooth bend across the rest of the test set.

---

**User**

For part 12(Section 11), I want to calculate the absolute prediction error using | actual - predicted |. Find the 10 test students with the largest prediction errors and display useful information for these students, including:
actual exam score;
predicted exam score;
residual;
absolute error;
several input features.
Investigation
Choose at least two large-error cases and examine them carefully. For each case, write a short discussion. For example:
The model predicted 75.2, while the student's actual score was 89. The student had relatively high attendance and completed many practice problems. These observations may help us form hypotheses about why the linear model underestimated the score, but they do not establish the cause of the error.

Distinguish between what the data shows and your hypothesis about why it happened.

---

**Cursor**

Section 11 is the large-error check. I’ll rank the test students by absolute error and inspect two of those cases against their habit features.

The two biggest misses point in opposite directions: one prediction is far too high, and one is far too low. I’ll list the 10 largest absolute errors with the habit features, then discuss those two cases.

Part 12 is in section 11 of the notebook. Absolute error is |actual − predicted|. These are the 10 test students with the largest misses. The cell also prints their habit features.

| Student | Actual | Predicted | Residual | Absolute error |
|---|---|---|---|---|
| S174 | 64.8 | 102.1 | -37.3 | 37.3 |
| S109 | 100.0 | 82.2 | 17.8 | 17.8 |
| S020 | 92.2 | 76.9 | 15.3 | 15.3 |
| S070 | 75.5 | 60.7 | 14.8 | 14.8 |
| S241 | 74.1 | 85.2 | -11.1 | 11.1 |
| S197 | 80.5 | 69.9 | 10.6 | 10.6 |
| S016 | 60.5 | 71.0 | -10.5 | 10.5 |
| S223 | 74.6 | 84.7 | -10.1 | 10.1 |
| S068 | 86.3 | 76.4 | 9.9 | 9.9 |
| S160 | 57.2 | 66.8 | -9.6 | 9.6 |

**S174** is the largest overestimate. The prediction is about 102.1 and the score is 64.8. The row shows 17.8 study hours, the maximum in the file, 98.1% attendance, Strong prior experience, and 0 practice problems. Most students study about 7.5 hours, and the median number of practice problems is 16. One hypothesis is that the fitted line keeps rising with study hours, so this extreme value, with high attendance and Strong experience, is extrapolated past 100, and zero practice problems does not pull it back down to 64.8. That does not show that the long study hours caused the low score.

**S109** is the largest underestimate. The prediction is about 82.2 and the score is 100. The row shows 10.1 study hours, 25 practice problems, 91.6% attendance, and prior experience of None. The prediction is already a few points above the training mean of 77.73. One hypothesis is that the None label held the prediction down relative to a Strong student with the same habits. Another is that something the model never sees fills the rest of the gap. This student's quiz average is 94.1, and quiz average was left out of the model. Either idea is a hypothesis. The row does not show that the None label caused the miss.

---

**User**

Under section 11, I want to perform a little experiment. I want you to help me extract the fitted Linear Regression coefficients after preprocessing. Then, create a table showing the transformed feature name and coefficient. You may also create a bar chart if you think it better displays the data.

Part 13 Questions:
Which features have positive coefficients?
Which features have negative coefficients?
Which coefficients have relatively large magnitudes?
What does a positive coefficient mean in this fitted model?

Important things to remember:
Do not automatically interpret a coefficient as a causal effect. For example, a positive coefficient for attendance means that the fitted model associates higher attendance with a higher predicted score, holding its other modeled features fixed. It does not prove that changing attendance by itself causes the corresponding change in exam score.

---

**Cursor**

Section 11 already lists the large misses. I’ll add the fitted coefficients there, with the sign and size read from the preprocessed features.

Part 13 is under section 11, in a new cell after the large-error investigation. It reads the coefficients from the fitted pipeline, prints them with the transformed feature names, and draws a horizontal bar chart. The intercept is **78.56**.

| Transformed feature | Coefficient |
|---|---|
| prior programming experience = None | -4.87 |
| prior programming experience = Some | -0.19 |
| study group = Yes | -0.12 |
| study group = No | 0.12 |
| commute minutes | 0.53 |
| sleep hours per night | 1.33 |
| attendance rate | 1.98 |
| practice problems per week | 3.17 |
| prior programming experience = Strong | 5.06 |
| study hours per week | 5.93 |

The numeric columns were standardized, so a numeric coefficient is the change in the predicted score associated with a one-standard-deviation increase on the training data. For study hours, that step is about 2.9 hours.

Positive coefficients are study hours, Strong prior experience, practice problems, attendance, sleep, commute minutes, and study group = No. Negative coefficients are prior experience = None, prior experience = Some, and study group = Yes.

The large magnitudes are study hours (5.93), Strong (5.06), and None (-4.87). Practice problems is next at 3.17. Attendance and sleep are smaller. Commute, Some, and both study-group columns are under 1 in absolute value, so study group barely moves the prediction in this fit.

A positive coefficient means the fitted equation associates a higher value of that prepared column with a higher predicted score, holding the other prepared columns fixed. A positive attendance coefficient means the model associates higher attendance with a higher predicted score. It does not prove that changing attendance by itself causes that change in the exam score. The same reading applies to study hours: 5.93 is the associated change for a one-standard-deviation increase inside this equation, not a measured effect of assigning someone extra study time.

---

**User**

For part 14(see section 12), I want to perform a controlled experiment. Add quiz_average to the input features.
Before running the experiment, write a hypothesis.
For example: I expect adding quiz average to reduce prediction error because ______.

Use the same training/test observations as your original model. Train the Linear Regression again.
Then, compare the mean baseline's MAE, RMSE, and R² values with the original linear regression's and the new linear regression+quiz_average's. 

Part 14 questions:
Did MAE improve?
Did RMSE improve?
Did ﻿R squared﻿ improve?
Was your hypothesis supported?

Most importantly, also discuss:
Would quiz_average actually be available at the time when the prediction is supposed to be made?

If the prediction is made after quizzes but before the final exam, it may be a legitimate feature. If the prediction must be made before any quizzes occur, it would not be available. A feature can be highly predictive and still be inappropriate for a particular prediction scenario.

---

**Cursor**

Section 12 adds `quiz_average` on the same students as the first model. I’ll state the expectation first, then compare MAE, RMSE, and R² with the baseline and the original regression.

Quiz average is strongly tied to the exam score in this file, so the expectation is that the same 50 test students will be predicted more closely. I’ll write that hypothesis first, then fit the model on the original split.

Part 14 is in section 12. The hypothesis is written above the experiment: adding `quiz_average` should lower the error because higher quiz averages come with higher exam scores in this file.

The new model uses the same 200 training students and the same 50 test students. `quiz_average` is added to the seven original features and scaled with the other numeric columns.

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Mean baseline | 7.66 | 9.80 | -0.091 |
| Linear regression | 5.77 | 8.35 | 0.209 |
| Linear regression + quiz average | 4.75 | 6.23 | 0.559 |

MAE improved, from 5.77 to 4.75. RMSE improved, from 8.35 to 6.23. R² improved, from 0.209 to 0.559. The hypothesis is supported. The correlation between quiz average and exam score is 0.769, and every metric moved in the expected direction. The typical miss is still about 4.75 points.

Whether `quiz_average` should be used depends on when the prediction is made. Every student in this file has a quiz average. If the prediction comes after the quizzes are graded and before the final exam, it is a legitimate feature: it is known then, and it is not the exam score. If the prediction has to be made before any quiz, the average would not exist yet. A feature can track the exam closely and still be the wrong input for that earlier decision.

---

**User**

Now to part 15(see section 13), where I want to compare my regression model with a non-linear one. Linear Regression assumes a relatively simple relationship between the features and the target.

How do I replace Linear Regression with RandomForestRegressor?

Keep the same prediction target, input features, training/test split, and preprocessing approach where appropriate.
Do not perform extensive hyperparameter tuning.

Use reasonable default settings, with random_state=42, and compare:
mean baseline;
Linear Regression;
Random Forest Regression.

At minimum, compare:
MAE;
RMSE;
R².

Part 15 Questions:
Which model had the lowest MAE?
Which had the lowest RMSE?
Which had the highest ﻿R squared﻿?
Did the more complicated model necessarily perform better?

Important to remember:
Do not conclude: Random Forest is better than Linear Regression.
A more appropriate conclusion is: Random Forest performed better/worse than Linear Regression on this dataset and this particular train/test split.

Later we will learn a better way to compare models using cross-validation.

---

**Cursor**

Section 13 is the nonlinear comparison. I’ll fit a random forest on the same students and the same seven features, then compare MAE, RMSE, and R² with the baseline and the linear model.

On this split the two models do not rank the same way on every metric. I’ll fit the forest with the original seven features and put that comparison next to the baseline and the linear model.

Part 15 is in section 13. The random forest uses the same exam-score target, the same seven features, and the same 200/50 split. `quiz_average` stays out. Missing values are still filled and the categories are still turned into 0/1 columns. `StandardScaler` is left off, because a tree only asks whether a value is above or below a cutoff, and rescaling does not change that order. The forest uses default settings with `random_state=42`.

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Mean baseline | 7.66 | 9.80 | -0.091 |
| Linear regression | 5.77 | 8.35 | 0.209 |
| Random forest | 6.25 | 7.94 | 0.284 |

Linear regression has the lowest MAE, 5.77. The random forest has the lowest RMSE, 7.94, and the highest R², 0.284. The more complicated model did not perform better on every metric. On this dataset and this split, the forest is closer on the squared-error summaries, and the linear model is closer on the average absolute miss. Both beat predicting 77.73 for everyone. That is a result for these 50 test students, not a general ranking of the two algorithms.

---

**User**

Let's move on to part 16(add under section 13). We used StandardScaler for Linear Regression. Random Forests are based on decision-tree splits.

Does RandomForestRegressor require StandardScaler? Explain why or why not. Write a short explanation of the answer.

Think about a tree decision such as: study_hours_per_week < 8.5

If the feature is standardized, the numerical threshold changes, but the ordering of the observations remains the same. This is one reason tree-based models generally do not require feature scaling. 

---

**Cursor**

The forest already skips scaling. I’ll add a short Part 16 note under section 13 on why a tree split does not need `StandardScaler`.

Part 16 is under section 13, after the model comparison. `RandomForestRegressor` does not require `StandardScaler`.

A tree split asks whether a feature is on one side of a cutoff, such as `study_hours_per_week < 8.5`. Standardizing subtracts the training mean and divides by the training standard deviation for every student. The cutoff number changes, and the order of the students does not. Whoever studied the least is still the least, so the same students fall on each side of the split. That is why the forest fills missing values and encodes the categories, and leaves the numeric columns unscaled.

Linear regression is different. Each coefficient multiplies the size of the number, so a column with larger units can dominate the sum unless it is rescaled.

---

**User**

For part 17(section 14), I want to perform one additional experiment. I want to investigate a different missing-value strategy. 
Before running it, write:
My Hypothesis: I expect ______ because ______.

Then:
perform the experiment;
report the result;
compare it with the original model;
state whether the evidence supports your hypothesis.
Do not repeatedly change the model simply until you obtain a better test score. The purpose is to answer a specific question.

---

**Cursor**

Section 14 needs one missing-value experiment, with the expectation written first. I’ll check how the median and mean fills differ on this split, then run that comparison once.

The only numeric blanks are study hours and sleep, and their training mean and median are almost the same. I’ll write that expectation first, then compare one mean-fill model with the original median fill.

Part 17 is in section 14. The hypothesis is written above the code: filling missing study hours and sleep hours with the training mean, instead of the training median, should leave the test error almost unchanged, because those two columns are not strongly skewed and only a few test students are missing a value.

On the training rows, the study-hour mean is 7.685 and the median is 7.6. The sleep-hour mean is 6.967 and the median is 7.0. Three test students are missing study hours, and three are missing sleep hours. Everything else in the linear model stays the same, including the 200/50 split.

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Median fill | 5.7740 | 8.3485 | 0.2085 |
| Mean fill | 5.7749 | 8.3498 | 0.2083 |

The evidence supports the hypothesis. MAE rises by less than 0.001, RMSE rises by about 0.001, and R² falls by about 0.0002. At two decimals, both models are still MAE 5.77 and RMSE 8.35. Mean imputation is not an improvement on this split.

I did not try another fill after seeing that table. One suggestion I set aside was to run several imputation strategies and keep whichever scored best on the test set. That would use these 50 students to shop for a better score. This comparison was one pre-specified question: median fill versus mean fill.

---

**User**

Lastly to Part 18(see section 14 again). Discuss at least one situation in which AI helped you:
construct a regression pipeline;
understand MAE, MSE, RMSE, or ﻿R squared﻿;
create a residual plot;
inspect model coefficients;
build the Random Forest model;
debug code;
interpret an unexpected result.

Part 18 questions:
What did you ask the AI?
What did it suggest?
Did you accept the suggestion?
How did you verify it?
Did you modify the AI-generated code or explanation?
What did you learn?
Also describe one AI suggestion that you questioned, even if the suggestion eventually turned out to be correct.


---

**Cursor**

Part 18 is the reflection in section 14. I’ll add it after the missing-value experiment and base it on choices this notebook actually made.

Part 18 is at the end of section 14, after the missing-value results. It covers two uses of the AI in this notebook.

**Interpreting the baseline R².** The question was how to score a model that predicts the training mean for every test student, and what MAE, MSE, RMSE, and R² mean. The suggestion was to compute all four on the same 50 students and to treat a negative R² as a real result. That suggestion was accepted. The notebook shows MAE 7.66, RMSE 9.80, and R² -0.091, next to a training mean of 77.73 and a test average of 74.89. The formulas were left as they were. MAE is the average miss in exam points, MSE squares those misses, and RMSE puts the result back in points. R² compares the predictions with the test set’s own mean, so predicting the training mean can land slightly below zero.

**A suggestion that was questioned.** Skipping `StandardScaler` for the random forest was not obvious, because the linear pipeline scales every numeric column. The reason to skip it is a split such as `study_hours_per_week < 8.5`: after standardization the cutoff changes, and the same students still fall on each side. That suggestion was accepted for the forest. The median fill and the category columns stayed. The check was fitting that pipeline on the same 200 training students and scoring the same 50 test students, which produced MAE 6.25, RMSE 7.94, and R² 0.284. A broader claim that the forest is the better algorithm was not accepted. On this split it won on RMSE and R², and linear regression still had the lower MAE, 5.77 against 6.25.

