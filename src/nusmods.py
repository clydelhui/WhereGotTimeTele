import requests
from datetime import datetime
from modules import SemModule, Lesson
import parsers


def get_module(acad_year:str, module_code:str, semester:int, lesson_list:list[dict]) -> SemModule:
    """ Gets module data from NUSMODS and returns a SemModule object

    :param acad_year: Desired academic year with the slash replaced by a dash
    :type acad_year: str
    :param module_code: Desired module code
    :type module_code: str
    :param semester: Desired Semester
    :type semester: int
    :param lesson_list: List of lessons to be included in the SemModule
    :type lesson_list: list[dict]
    :return: A SemModule object containing the requested data from NUSMODS
    :rtype: SemModule
    """
    r = requests.get(f"https://api.nusmods.com/v2/{acad_year}/modules/{module_code}.json")
    if r.status_code != 200:
        print("HTTP request to NUSMODS failed.")
        return
    retrieved_data = r.json()
    title = retrieved_data['title']
    sem_mod_lessons = next(k['timetable'] \
                           for k in retrieved_data['semesterData'] \
                            if k['semester'] == semester)
    
    matched_lessons = [Lesson(k['classNo'], datetime.strptime(k['startTime'], "%H%M").time(), \
                              datetime.strptime(k['endTime'], "%H%M").time(),
                              k['weeks'], k['venue'], k['day'],
                              k['lessonType']) for k in sem_mod_lessons \
                       if k['lessonType'] in lesson_list \
                        and lesson_list[k['lessonType']] == k['classNo']]

    
    return SemModule(acad_year, module_code, semester, title, matched_lessons)


if __name__ == "__main__":
    semester, module_data_list = parsers.parse_url('https://nusmods.com/timetable/sem-1/share?GEC1015=LEC:3&LSM2233=LEC:1&LSM3228=LEC:1,LAB:1&LSM3232=LEC:1,LAB:1,TUT:1&PL1101E=LEC:1,TUT:E19')
    print(module_data_list)
    for i in module_data_list:
        print(get_module('2023-2024', i['moduleCode'], semester, i['classes']))
    print(get_module('2022-2023', 'ST2334', semester, module_data_list[2]['classes']))
    