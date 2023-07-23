function addMedia(event){
    let amount = document.getElementsByClassName("delete-button").length + 1;
    let newRow = document.createElement("div");
    newRow.className = "row";

    let inputColumn = document.createElement("div");
    inputColumn.className = "col";

    let input = document.createElement("input");
    input.setAttribute("type", "file");
    input.className = "form-control";
    input.setAttribute("name", "input-media-" + amount.toString());

    inputColumn.appendChild(input);
    newRow.appendChild(inputColumn)

    let buttonColumn = document.createElement("div");
    buttonColumn.className = "col";

    let button = document.createElement("button");
    button.className = "delete-button";
    button.innerText = "Delete";
    button.setAttribute("id", "button-delete-" + amount.toString())
    button.setAttribute("type", "button")

    button.onclick = deleteMedia;
    buttonColumn.appendChild(button);

    newRow.appendChild(buttonColumn);

    let medias = document.getElementById("medias");
    medias.appendChild(newRow);
}



function deleteMedia(event){
    let mediaNumber = event.currentTarget.id.split("-")[2];
    let medias = document.getElementById("medias");
    let child = medias.children[mediaNumber - 1];
    medias.removeChild(child);

}
