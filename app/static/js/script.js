function renderMedicineToTable(data = []) {
    const html = Object.values(data).map(m => `<tr>
        <td>${ m.name }</td>
        <td>${ m.quantity }</td>
        <td>${ m.unit }</td>
        <td>${ m.direction }</td>
        <td>
          <button class="btn btn-info detail-btn" onclick="deleteMedicine('${m.id}')">Xóa</button>
        </td>
      </tr>`)
      .join('')
    document.getElementById('tbody').innerHTML = html;
}

function deleteMedicine(id) {
    fetch("/api/medicine/delete", {
        method: "post",
        body: JSON.stringify({ id }),
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(function (res) {
        return res.json();
    })
    .then(function (data) {
        console.log(data);
        renderMedicineToTable(data);
    });
}
function renderHistoryToTable(data = []) {
    const html = Object.values(data).map(m => `<tr>
        <td>${ m.examination_date }</td>
        <td>${ m.symptom }</td>
        <td>${ m.prediction }</td>
      </tr>`)
      .join('')
    document.getElementById('tbodyHistory').innerHTML = html;
}

function getHistoryById(userId) {
    fetch(`/api/history/${userId}`)
    .then(function (res) {
        return res.json();
    })
    .then(function (data) {
        console.log(data);
        renderHistoryToTable(data)
    });
}


function addMedicineToBill(id, price, quantity, name, direction, unit) {
    console.log(JSON.stringify({
      id,
      price,
      quantity,
      name,
      direction,
      unit
    }))
    fetch("/api/medicine", {
        method: "post",
        body: JSON.stringify({
          id,
          price,
          quantity, name, direction, unit
        }),
        headers: {
          "Content-Type": "application/json",
        },
    })
    .then(function (res) {
      return res.json();
    })
    .then(function (data) {
    console.log(data);
    renderMedicineToTable(data)
    });
}

function saveMedicineBill(symptom, prediction, patient_id, form_id) {
    console.log(JSON.stringify({
        symptom, prediction, patient_id, form_id
    }))
    fetch("/api/medicine/save", {
        method: "post",
        body: JSON.stringify({
         symptom, prediction, patient_id, form_id
        }),
        headers: {
          "Content-Type": "application/json",
        },
    })
    .then(function (res) {
        return res.json();
    })
    .then(function (data) {
        console.log(data);
        location.href = '/nurse/examination/'
    });
}
