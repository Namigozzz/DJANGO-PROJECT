import pytest
from rest_framework.test import APIClient

from students.models import Course, Student
from model_bakery import baker


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student():
    return Student.objects.create(name='Student 1', birth_date='2000-01-01')


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == course.id and data['name'] == course.name


@pytest.mark.django_db
def test_get_all_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    url = '/api/v1/courses/'

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert {course.id for course in courses} == {course['id'] for course in data}


@pytest.mark.django_db
def test_get_filtered_courses_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    url = f'/api/v1/courses/?id={courses[0].id}'

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert courses[0].id == data[0]['id']


@pytest.mark.django_db
def test_get_filtered_courses_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    url = f'/api/v1/courses/?name={courses[0].name}'

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert courses[0].name == data[0]['name']


@pytest.mark.django_db
def test_create_course(client, student):
    url = '/api/v1/courses/'
    data = {'name': 'Course 1', 'students': [student.id]}

    response = client.post(url, data)

    assert response.status_code == 201
    result = response.json()
    assert result['name'] == data['name']
    assert result['students'] == [student.id]


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'
    data = {'name': 'Test Course'}

    response = client.patch(url, data)

    assert response.status_code == 200
    result = response.json()
    assert data['name'] == result['name']
    assert course.id == result['id']

    course.refresh_from_db()
    assert course.name == result['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'

    response = client.delete(url)

    assert response.status_code == 204
    assert Course.objects.count() == 0


@pytest.mark.parametrize(
    'students_count, http_response_code',
    [
        (10, 201),
        (21, 400)
    ]
)
@pytest.mark.django_db
def test_create_course_with_students_count(client, student_factory, settings, students_count, http_response_code):
    settings.MAX_STUDENTS_PER_COURSE = 10

    students = student_factory(_quantity=students_count)
    url = '/api/v1/courses/'
    data = {'name': 'Course 1', 'students': [student.id for student in students]}

    response = client.post(url, data)

    assert response.status_code == http_response_code
