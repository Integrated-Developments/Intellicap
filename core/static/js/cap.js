const socket = io();
socket.on('update_total', function (data) {
    document.getElementById('totalValue').innerText = data.total;
});
