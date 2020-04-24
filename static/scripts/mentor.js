function generateOpportunityHTML(opportunityNumber) {
    return `<p>Opportunity</p>
    <div class="form-group">
        <label for="opportunity${opportunityNumber}date">Date</label>
        <input type="date" class="form-control" name="opportunity${opportunityNumber}date" id="opportunity${opportunityNumber}date">
    </div>
    <div class="form-group">
        <label for="opportunity${opportunityNumber}session">Session</label>
        <select name="opportunity${opportunityNumber}session" class="form-control" id="opportunity${opportunityNumber}session">
            <option value="am">A.M. Session</option>
            <option value="pm">P.M. Session</option>
            <option value="full">Full Day Session</option>
        </select>
    </div>
    <button type="button" onclick="removeOpportunity(${opportunityNumber});" class="btn btn-danger">Remove</button>
    <hr />
    `
}

function addOpportunity(opportunityNumber) {
    let container = document.createElement('div')
    container.id = 'opportunity' + opportunityNumber
    container.innerHTML = generateOpportunityHTML(opportunityNumber)
    document.getElementById('opportunities').appendChild(container)
    document.getElementById('add-opportunity').setAttribute('onclick', 'addOpportunity(' + (opportunityNumber + 1) + ')')
}

function removeOpportunity(opportunityNumber) {
    document.getElementById('opportunity' + opportunityNumber).remove()
}