@app.route('/students_list')
def students_list():
    # Get all students
    c.execute("SELECT * FROM students")
    students = c.fetchall()

    # Get all subjects
    c.execute("SELECT DISTINCT subject FROM attendance")
    subjects = c.fetchall()

    students_data = []
    for student in students:
        student_id = student[0]
        name = student[1]
        roll_no = student[2]

        attendance_data = []
        for subject in subjects:
            subject_name = subject[0]

            # Calculate attendance for each subject
            c.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND subject=? AND status='Present'",
                      (student_id, subject_name))
            present_attendance = c.fetchone()[0]

            c.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND subject=?",
                      (student_id, subject_name))
            total_attendance = c.fetchone()[0]

            # Calculate attendance percentage
            attendance_percentage = (present_attendance / total_attendance) * 100 if total_attendance != 0 else 0

            attendance_data.append({
                'subject': subject_name,
                'present_attendance': present_attendance,
                'total_attendance': total_attendance,
                'attendance_percentage': round(attendance_percentage, 2)  # Round to 2 decimal places
            })

        students_data.append({
            'name': name,
            'roll_no': roll_no,
            'attendance_data': attendance_data
        })

    return render_template('students_list.html', students_data=students_data, subjects=subjects)

