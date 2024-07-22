from datetime import time

class Lesson:
    """A class that represents the information about a particular lesson 
    retrieved from the NUSMODS API
    """
    def __init__(self, class_no:str, start_time:time, end_time:time, weeks:list[int], \
                 venue:str, day:str, lesson_type:str) -> None:
        self.class_no = class_no
        self.start_time = start_time
        self.end_time = end_time
        self.weeks = weeks
        self.venue = venue
        self.day = day
        self.lesson_type = lesson_type

    def __str__(self) -> str:
        return f"{self.lesson_type} {self.class_no} on {self.day} on weeks\
            {', '.join([str(k) for k in self.weeks])} from {self.start_time} \
              to {self.end_time}"

class SemModule:
    """A class that represents the information about a particular module from a 
    particular academic year and semester that a particular student is taking
    """
    def __init__(self, acad_year:str, module_code:str, semester:int, title:str, \
                 lesson_list:list[Lesson]) -> None:
        self.acad_year = acad_year
        self.module_code = module_code
        self.semester = semester
        self.module_title = title
        self.lesson_list = lesson_list
        
    def __hash__(self) -> int:
        return hash(self.module_code)
    
    def __str__(self) -> str:
        lesson_string = "\n".join([str(k) for k in self.lesson_list])
        return f"{self.module_code} {self.module_title}: \n{lesson_string}\n"