document.getElementById('lend').addEventListener('submit', function(){
    var elements = this.elements;
    for (var i = 0; i < elements.length; i++) {
        if (elements[i].type == 'submit') {
            elements[i].disabled = true;
        }
    }
});