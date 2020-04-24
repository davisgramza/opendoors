function confirmStudentEmail(numberOfStudents) {
    return confirm('Are you sure you want to send this bulk email reminder to all ' + numberOfStudents + ' students with approved mentor sessions (and their parents if selected)?')
}

function confirmMentorEmail() {
    return confirm('Are you sure you want to send this bulk email to all selected mentors?')
}

function requireFirstOption() {
    if (document.getElementById('registered-mentors-only').checked) {
        document.getElementById('include-registered-students').disabled = false
    }
    else {
        document.getElementById('include-registered-students').disabled = true
    }
    document.getElementById('include-registered-students').checked = false
}