// Map initialization
function createMap(){
    var map = L.map("map").setView([50, 20], 3);

    // Стиль google maps
    googleStreets = L.tileLayer(
      "http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
      {
        maxZoom: 20,
        subdomains: ["mt0", "mt1", "mt2", "mt3"],
      }
    );
    googleStreets.addTo(map);
    return map
}


// Иконка для всех маркеров
var myIcon = L.icon({
  iconUrl: "static/img/red_marker.png",
  iconSize: [40, 40],
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function makeRequest(url, method, body){
    let headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'content-type': 'application/json'
    }

    if (method == 'POST'){
        const csrf = getCookie('csrftoken')
        headers['X-CSRFToken'] = csrf
    }

    let response = await fetch(url, {
        method: method,
        headers: headers,
        body: body
    })

    return await response.json()
}

console.log(getCookie('csrftoken'))

// Функция создания маркера на карте
async function addMarker(coordinates) {
  L.marker([coordinates.lat, coordinates.lng], { icon: myIcon, }).addTo(map)
   makeRequest('/', 'POST', JSON.stringify({'lat': coordinates.lat}))
//  let response = await fetch('http://127.0.0.1:8000/', {
//    method: 'POST',
//    headers: {
//        //'X-Requested-With': 'XMLHttpRequest',
//        'X-CSRFToken': getCookie('csrftoken'),
//        'content-type': 'application/json'
//    },
//    body:{
//        'lat':123,
//        'lng':'abobus'
//    }
//  })
//  //response.then(d => console.log(d)).catch(e => console.log(e))
//
//  console.log(getCookie('csrftoken'))
//  console.log(response.body)
//  return response
}



// Добавление маркера по нажатию ПКМ. Всплывает модальное окно для заполнения всей инфы по данному месту.
// При нажатии кнопки "Добавить место" данные должны улетать на бэк. 
// Потом фронт должен автоматически обновляться и рисовать на карте последний добавленный в бд маркер.
map.on("contextmenu", function (e) {
  coordinates = e.latlng
  L.popup()
    .setLatLng(coordinates)
    .setContent(`<form id="myForm" onsubmit="return false">
        <label for="name">Название:</label>
        <input type="text" id="name" name="name">
        <label for="description">Описание:</label>
        <textarea id="description" name="description"></textarea>
        <div id="drop-area">
            <p class="instructions">Drag & Drop one or more files or click to select</p>
            <p class="instructions">Only .jpeg, .png, .gif images allowed</p>
            <label class="input-file">
	   	        <input onchange="previewFiles(this.files)" type="file"  multiple>		
	   	        <span>Выберите файл</span>
 	          </label>
            <p class="error"></p>
        </div>
        <div class="preview-container"></div>
        <button onclick="addMarker(coordinates)">Добавить</button>
      </form>`)
    .openOn(map);
  setTimeout(checkDragAndDrop(), 10)
  // console.log(name)
  // console.log(description)
  // console.log(photos)
});

document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var xhr = new XMLHttpRequest();
    var url = "/";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    var formData = new FormData(this);
    xhr.send(new URLSearchParams(formData));

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(JSON.parse(xhr.responseText));
        }
    };
});
// 2 Тестовых предзаполненных маркера
//var singleMarker = L.marker([28.3949, 84.124], {
//  icon: myIcon,
//}).addTo(map)
//
//var secondMarker = L.marker([60.3949, 0.124], {
//  icon: myIcon,
//}).addTo(map)


let fillContent = ((name, description) => {
  let content = `<h2 class="popup-title">${name}</h2>
  <div class="photo-section">
  <div class="photo-block"></div>
  </div>
  <div class="content_description">${description}</div>
  <div class="preview-container"><div class="image-container"><img src=""></div></div></div>`
  return content
})

//singleMarker.bindPopup(fillContent('Маркер 1', 'Какой-то текст с описанием'))
//
//secondMarker.bindPopup(fillContent('Маркер 2', 'Какой-то текст с описанием'));

// secondMarker.setPopupContent(`<p>LOLODFDF</p>`) записать html в popup
// console.log(secondMarker.getPopup().getContent()) получить html из popup
// console.log(singleMarker.getLatLng());
