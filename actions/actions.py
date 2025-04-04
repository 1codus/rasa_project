import json
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

#단과대학 정보 조회 
class ActionFetchFacultyInfo(Action):
    def name(self):
        return "action_fetch_faculty_info"

    def run(self, dispatcher, tracker, domain):
        # JSON 파일 로드
        with open('university_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        faculty = next((f for f in data["university"]["faculties"] if f["name"] == tracker.get_slot("faculty")), None)
        if faculty:
            dispatcher.utter_message(text=f"{faculty['name']}에는 다음과 같은 학과들이 있습니다: {', '.join([d['name'] for d in faculty['departments']])}")
        else:
            dispatcher.utter_message(text="해당 단과대학 정보를 찾을 수 없습니다.")
        return []

#교수 정보 조회
class ActionFetchProfessorInfo(Action):
    def name(self):
        return "action_fetch_professor_info"

    def run(self, dispatcher, tracker, domain):
        with open('university_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        department = tracker.get_slot("department")
        professor_name = tracker.get_slot("professor")

        professor_info = None
        for faculty in data["university"]["faculties"]:
            for dept in faculty["departments"]:
                if dept["name"] == department:
                    professor_info = next((p for p in dept["professors"] if p["name"] == professor_name), None)
                    if professor_info:
                        break
            if professor_info:
                break

        if professor_info:
            dispatcher.utter_message(text=f"{professor_info['name']} 교수님의 전공은 {professor_info['specialization']}입니다.")
        else:
            dispatcher.utter_message(text="해당 교수님 정보를 찾을 수 없습니다.")
        return []

#과목 정보 조회
class ActionFetchCourseInfo(Action):
    def name(self):
        return "action_fetch_course_info"

    def run(self, dispatcher, tracker, domain):
        with open('university_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        department = tracker.get_slot("department")
        course_name = tracker.get_slot("course")

        course_info = None
        for faculty in data["university"]["faculties"]:
            for dept in faculty["departments"]:
                if dept["name"] == department:
                    course_info = next((c for c in dept["courses"] if c["name"] == course_name), None)
                    if course_info:
                        break
            if course_info:
                break

        if course_info:
            dispatcher.utter_message(text=f"{course_info['name']} 과목은 {course_info['credits']} 학점입니다.")
        else:
            dispatcher.utter_message(text="해당 과목 정보를 찾을 수 없습니다.")
        return []
