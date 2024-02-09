var UpdateBtns = document.getElementsByClassName("update-cart");

for (var i = 0; i < UpdateBtns.length; i++) {
    UpdateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action; // Corrected variable name to 'action'
        console.log("product id:", productId, "action:", action);

        console.log("User", user);
        if (user === 'AnonymousUser') {
            // Handle anonymous user
        } else {
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action) {
    console.log('user is logged in, sending data...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then(response => response.json())
    .then(data => {
        console.log('data:', data);
        location.reload()
    })
    .catch(error => {
        console.error('Error:', error);
    });
}