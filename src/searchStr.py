#constants for find and replace in other parts of the program
class SearchStr:
    CMakeUserIncludes = "target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE"
    CMakeUserSources = "target_sources(${CMAKE_PROJECT_NAME} PRIVATE"
    mainUserHeaders = '''/* USER CODE BEGIN Header */'''
    mainUserCodeLoop = '''/* USER CODE BEGIN 3 */'''
