function onRemoveInactiveMentorsClick() {
    if (document.getElementById('remove-inactive-mentors').checked) {
        document.getElementById('remove-mentors').checked = false
        document.getElementById('remove-mentors').disabled = true
    } else {
        document.getElementById('remove-mentors').disabled = false
        document.getElementById('remove-inactive-mentors').disabled = false
    }
}

function onRemoveMentorsClick() {
    if (document.getElementById('remove-mentors').checked) {
        document.getElementById('remove-inactive-mentors').checked = false
        document.getElementById('remove-inactive-mentors').disabled = true
    } else {
        document.getElementById('remove-mentors').disabled = false
        document.getElementById('remove-inactive-mentors').disabled = false
    }
}