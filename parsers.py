from urllib.parse import urlparse
from constants import LESSON_ABBREV_TYPE



def parse_url(url:str) -> tuple:
    """Parses a given URL to return a tuple where the first element is the 
      semester and the second element is a list that contains the module data
      returned by calling parse_module_data.

    :param url: The given URL.
    :type url: str
    :return: A tuple containing the semester and the module data.
    :rtype: tuple
    """
    prs_rslt = urlparse(url)
    if prs_rslt.netloc != 'nusmods.com':
        # TODO: Throw an error here
        pass
    semester = int(prs_rslt.path.split('-')[1][0])
    module_list_string = prs_rslt.query.split("&")
    module_data_list = [parse_module_data(mod) for mod in module_list_string]
    return (semester, module_data_list)


  
def parse_module_data(module_data:str) -> dict:
    """Parses module data from a given section of an NUSMODS URL string.

    :param module_data: The given NUSMODS URL string.
    :type module_data: str
    :return: A dictionary containing the module code and the classes in 
    dictionary form
    :rtype: dict
    """
    module_lesson_split = module_data.split("=")
    module_code = module_lesson_split[0]
    lesson_split = module_lesson_split[1].split(",")
    lessons = {LESSON_ABBREV_TYPE[k.split(":")[0]] : k.split(":")[1] for k in lesson_split}

    module_data_parsed = {"moduleCode" : module_code, 
                          "classes" : lessons}
    return module_data_parsed





if __name__ == "__main__":
    print(parse_url("https://nusmods.com/timetable/sem-2/share?ES1000=SEC:G03&PC2032=LEC:1&ST2334=TUT:16,LEC:2"))