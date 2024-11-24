from pycaret.classification import *
import pandas as pd
import os

# load data
data = pd.read_csv('Student_performance_data _.csv')

# Set up the classification environment
clf = setup(data, target='GradeClass', session_id=123,
            numeric_features=['Age', 'StudyTimeWeekly', 'Absences'],
            categorical_features=['Gender', 'Ethnicity', 'ParentalEducation', 'Tutoring',
            'ParentalSupport', 'Extracurricular', 'Sports', 'Music', 'Volunteering'],
            ignore_features=['StudentID', 'GPA'])

# cmopare all models
best_model = compare_models()


os.makedirs('student_performance_api', exist_ok=True)

# save the best model
save_model(best_model, 'student_performance_api_model')

create_api(best_model, 'student_performance_api')


