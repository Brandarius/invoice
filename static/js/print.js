function handlePrint() {
    document.getElementById('printButton').addEventListener('click', function() {
        window.print();
    });
}
document.addEventListener('DOMContentLoaded', handlePrint);
