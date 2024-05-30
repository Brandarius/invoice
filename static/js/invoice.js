function calculatePrice(input) {
    var index = input.dataset.index;
    var amount = document.getElementById('amount_' + index).value;
    var quantity = document.getElementById('quantity_' + index).value;
    var price = document.getElementById('price_' + index);
    price.value = amount * quantity;
}
function calculateTotal() {
    var total = 0;
    var rowCount = document.getElementById('invoice_table').rows.length;
    
    for (var i = 1; i < rowCount; i++) {
        var price = parseFloat(document.getElementById('price_' + i).value);
        total += price;
    }
    
    document.getElementById('amount').value = total;
}



