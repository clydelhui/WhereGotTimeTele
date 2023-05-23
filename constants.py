'''
Constants that need to be updated periodically
'''

current_ay = '2022-2023'
current_semester = 2


'''
Constants that do not change over time.
'''
LESSON_TYPE_ABBREV = {
  'Design Lecture': 'DLEC',
  'Laboratory': 'LAB',
  'Lecture': 'LEC',
  'Packaged Lecture': 'PLEC',
  'Packaged Tutorial': 'PTUT',
  'Recitation': 'REC',
  'Sectional Teaching': 'SEC',
  'Seminar-Style Module Class': 'SEM',
  'Tutorial': 'TUT',
  'Tutorial Type 2': 'TUT2',
  'Tutorial Type 3': 'TUT3',
  'Workshop': 'WS',
}

LESSON_ABBREV_TYPE = {v: k for k, v in LESSON_TYPE_ABBREV.items()}