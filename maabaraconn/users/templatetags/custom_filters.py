# your_app/templatetags/custom_filters.py
from users.models import StudentResponse
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# templatetags/custom_filters.py


register = template.Library()


@register.filter
def get_response_for_section(responses, section_id):
    try:
        return responses.get(section_id=section_id).response_text
    except StudentResponse.DoesNotExist:
        return ''


@register.filter
def get_awarded_marks_for_section(responses, section_id):
    try:
        return responses.get(section_id=section_id).awarded_marks
    except StudentResponse.DoesNotExist:
        return 0
# templatetags/custom_filters.py


@register.filter
def get_response(student_responses, section_id):
    response = student_responses.filter(section_id=section_id).first()
    return response.response_text if response else 'No response'
