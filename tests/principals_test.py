from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    """Implemented functionality"""
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_student_1, h_principal):
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

    # Step 2: Submit the assignment to change its state to SUBMITTED
    submit_response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': assignment_id,
            'teacher_id': 2
        }
    )
    assert submit_response.status_code == 200
    data = submit_response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2

    # Step 3: Grade the assignment
    grade_response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment_id,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )
    assert grade_response.status_code == 200
    data = grade_response.json['data']
    assert data['state'] == AssignmentStateEnum.GRADED.value
    assert data['grade'] == GradeEnum.C.value




def test_regrade_assignment(client, h_student_1, h_principal):
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

    # Step 2: Submit the assignment to change its state to SUBMITTED
    submit_response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': assignment_id,
            'teacher_id': 2
        }
    )
    assert submit_response.status_code == 200
    data = submit_response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2

    # Step 3: Grade the assignment
    grade_response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment_id,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )
    assert grade_response.status_code == 200
    data = grade_response.json['data']
    assert data['state'] == AssignmentStateEnum.GRADED.value
    assert data['grade'] == GradeEnum.C.value

    # Step 4: Re-grade the assignment
    regrade_response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment_id,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )
    assert regrade_response.status_code == 200
    data = regrade_response.json['data']
    assert data['state'] == AssignmentStateEnum.GRADED.value
    assert data['grade'] == GradeEnum.B.value
