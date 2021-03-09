import json

teachers_file = open("teachers.json")
teachers = json.load(teachers_file)
teachers = teachers["teachers"]

'''
format of file:
    "teachers" : {
        teacher_code : {
            day1 : 
                {
                    "1" : {"class" : "foo", "availability" : "unav/free/assembly"},
                    2...
            },
            day2 ...          
        }
    }
'''


