// static/js/pedidos.js

function mostrarDatosCliente() {
    var select = document.getElementById("cliente_id");
    var selectedOption = select.options[select.selectedIndex];
    document.getElementById("direccion").value = selectedOption.getAttribute("data-direccion");
    document.getElementById("telefono").value = selectedOption.getAttribute("data-telefono");
}
