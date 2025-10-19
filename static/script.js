const scanForm = document.getElementById('scan-form');

scanForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(scanForm);
    const domain = formData.get('domain');

    console.log('Tarama isteği gönderiliyor:', domain);

    fetch('/scan',{
        method: 'POST',
        headers: {'Content-type': 'application/json'},
        body: JSON.stringify({domain: domain})
    })
    .then(response => response.json())
    .then(data => {
        console.log('sunucudan gelen cevap: ',data)
    })
    .catch (error=>{
        console.error('fetch hatası: ',error)

    })


})