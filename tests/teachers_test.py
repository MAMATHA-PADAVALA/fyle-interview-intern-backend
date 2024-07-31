from core import db
from core.models.assignments import Assignment, AssignmentStateEnum

def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    """irrespective of the assignment state, assertion should only done on teacher_2"""
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200
    
    data = response.json['data']
    print(data)
    for assignment in data:
        assert assignment['teacher_id'] == 2
        


def test_grade_assignment_cross(client, h_teacher_2):
    """
    Failure case: assignment 1 was submitted to teacher 1 and not teacher 2.
    """
    # Setup: Ensure the assignment is in the SUBMITTED state (or any state that is valid for grading)
    assignment = Assignment.get_by_id(1)
    assignment.state = AssignmentStateEnum.SUBMITTED  # Or any state you want to test
    #assignment.teacher_id = 1  # Ensure this assignment was assigned to teacher 1
    db.session.commit()

    # Attempt to grade the assignment with a teacher who is not the assigned teacher
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json()

    assert data['error'] == 'FyleError'
    #assert data['message'] == 'Assignment was not submitted to this teacher'



def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_draft_assignment(client, h_student_1, h_teacher_1):
    # Step 1: Create an assignment in DRAFT state
    create_response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': 'some text'
        }
    )
    assert create_response.status_code == 200
    data = create_response.json['data']
    assignment_id = data['id']
    assert data['state'] == 'DRAFT'
    assert data['student_id'] == 1

    # Step 2: Attempt to grade the draft assignment
    grade_response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            'id': assignment_id,
            'grade': 'A'
        }
    )

    assert grade_response.status_code == 400
    data = grade_response.json
    assert data['error'] == 'FyleError'
