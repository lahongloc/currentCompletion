const takeCartInfo = (id, image, name, price) => {
    event.preventDefault()

    fetch('/api/add-cart', {
        method: 'POST',
        body: JSON.stringify({
            id,
            image,
            name,
            price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            document.getElementById('cart-quantity').innerText = data.total_quantity
        })
        .catch(err => {
            console.error(err)
        })
}

const pay = () => {
	if (confirm('Are you sure to pay?') == true) {
		fetch('/api/pay', {
				method: 'post'
			})
			.then(res => res.json())
			.then(data => {
				if (data.code == 200)
					location.reload()
			})
			.catch(err => console.error(err))
	}

}