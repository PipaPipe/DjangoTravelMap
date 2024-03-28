// Получаю все маркеры, для каждого свой drag and drop
let markers = document.querySelector(".leaflet-marker-pane")

// Array.prototype.forEach.call(markers.children, marker => {
//   marker.addEventListener('click', () => {
//      setTimeout(checkDragAndDrop, 10)
//    });
// });


// Массив ссылок на фото
let arrayOfPhotos = []

// Функция удаления фото для актуальности массива
function removePhotoFromArray(e) {
  photoToRemove = e.children[0].currentSrc

  arrayOfPhotos = arrayOfPhotos.filter(photo => photo !== photoToRemove);
  e.remove()
}


// Функция для drag and drop
function checkDragAndDrop() {
   // Select relevant DOM elements using querySelector
  let dropArea = document.querySelector("#drop-area");
  
  dropArea.addEventListener("dragenter", (ev) => {
    // Highlighting the drop area's border.
    dropArea.classList.add("highlight");
    // Preventing the browser's default action.
    ev.preventDefault();
  });

  dropArea.addEventListener("dragover", (ev) => {
    // Highlighting the drop area's border.
    dropArea.classList.add("highlight");
    // Preventing the browser's default action.
    ev.preventDefault();
  });

  dropArea.addEventListener("dragleave", (ev) => {
    // Remove the border highlight when leaving the drop area
    dropArea.classList.remove("highlight");
    // Preventing the browser's default action.
    ev.preventDefault();
  });

  // Add a drop event listener to handle dropped files
  dropArea.addEventListener("drop", (ev) => {
    // Remove the border highlight when dropping the files
    dropArea.classList.remove("highlight");
   
    // Preventing the browser's default action.
    ev.preventDefault();

    // Using the dataTransfer object to access the files being dragged.
    if (ev.dataTransfer.files) {
      // If there are being files dragged and dropped, we store
      // this files in the 'transferredFiles' variable.
      let transferredFiles = ev.dataTransfer.files;

      // Call the previewFiles function with the dropped files
      // to preview them
      previewFiles(transferredFiles);
    }
  });
}


// Функция для отображения фотографий
function previewFiles(files) {
  let previewContainer = document.querySelector(".preview-container");
  let error = document.querySelector(".error");
   // Hide any previous error messages
   error.style.display = "none";

   let allowedImageTypes = ["image/jpeg", "image/gif", "image/png"];
   
  
   // Check each dropped file against the allowed image types
   for (let file of files) {
     if (!allowedImageTypes.includes(file.type)) {
       // Display an error message for disallowed file types
       error.style.display = "block";
       error.innerHTML = "Only .jpg, .png, .gif files are allowed";

       // Hide the error message after 5 seconds
       setTimeout(() => {
         error.style.display = "none";
       }, 5000);

       // Return false to stop processing and prevent image preview
       return false;
     }
   }


   // If all files are allowed, proceed to preview each image
   for (let file of files) {
     // Create a FileReader to read the file content
     let reader = new FileReader();

     // Read the file as a data URL (base64 encoded)
     reader.readAsDataURL(file);

     // When the browser finishes reading the file, the
     // onload event listener will trigger a function.
     reader.onload = function () {
       // Create an image element..
       let image = new Image();
       // ..and set its source to the result of FileReader
       image.src = this.result;
       arrayOfPhotos.push(image.src)

       // Create a container for the image
       let imageContainer = document.createElement("div");
       imageContainer.setAttribute("class", "image-container");
       imageContainer.appendChild(image);
       previewContainer.appendChild(imageContainer);

       // Create a paragraph element to display the file name
       let imageName = document.createElement("span");
       imageName.setAttribute("class", "info");
       imageName.innerHTML = file.name;
       imageContainer.appendChild(imageName);

       // Create a remove button with an onclick event
       // to remove the image
       let removeButton = document.createElement("button");
       removeButton.setAttribute("class", "remove-button");
       removeButton.setAttribute("onclick", "removePhotoFromArray(this.parentElement)");
       removeButton.innerText = "x";
       imageContainer.appendChild(removeButton);
     };
   }
 }