-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_grading_count AS (
    SELECT teacher_id, COUNT(*) AS grading_count
    FROM assignments
    GROUP BY teacher_id
),
top_teacher AS (
    SELECT teacher_id
    FROM teacher_grading_count
    ORDER BY grading_count DESC
    LIMIT 1
)
SELECT a.teacher_id, COUNT(*) AS grade_a_count
FROM assignments a
JOIN top_teacher t ON a.teacher_id = t.teacher_id
WHERE a.grade = 'A'
GROUP BY a.teacher_id;


