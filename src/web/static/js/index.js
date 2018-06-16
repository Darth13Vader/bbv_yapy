function RadioButtonReal() {
    document.getElementById('temperature').disabled = true;
    document.getElementById('precip').disabled = true;
    document.getElementById('intens').disabled = true;
    document.getElementById('holidays').disabled = true;
    document.getElementById('news').disabled = true;
    document.getElementById('cars-speed').disabled = true;

    document.getElementById('temperature').value = "";
    document.getElementById('holidays').value = '';
    document.getElementById('news').value = '';
    document.getElementById('precip').selectedIndex = 0;
    document.getElementById('intens').selectedIndex = 0;
    document.getElementById("intens").selectedIndex = 0;
    document.getElementById('cars-speed').value = '';

}

function RadioButtonModel() {
    document.getElementById('temperature').disabled = false;
    document.getElementById('precip').disabled = false;
    document.getElementById('holidays').disabled = false;
    document.getElementById('news').disabled = false;
    document.getElementById('cars-speed').disabled = false;
}


function OpenIntens(f) {
    let intens = f.precip.selectedIndex;
    if (intens === 2 || intens === 3) {
        document.getElementById('intens').disabled = false;
    }
    else {
        document.getElementById('intens').disabled = true;
        document.getElementById("intens").selectedIndex = 0
    }
}