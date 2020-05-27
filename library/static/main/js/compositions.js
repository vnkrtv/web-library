function setComposition(id, name) {
    const header = document.getElementById('header');
    header.innerHTML = name + ' - новый перевод';
    const composition_id = document.getElementById('composition_id');
    composition_id.value = id;
}
