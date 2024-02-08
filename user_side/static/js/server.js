const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');
const productTitleElements = document.querySelectorAll('.card-title');
const productPriceElements = document.querySelectorAll('.card-subtitle');
const quantityInputs = document.querySelectorAll('.input-qty-selector');
console.log(addToCartBtns)
addToCartBtns.forEach((btn, index) => {
    console.log(btn)
    btn.addEventListener("click", () => {
        const productName = productTitleElements[index].textContent;
        console.log(productName);
        const productPrice = productPriceElements[index].textContent;
        console.log(productPrice);
        const quantity = quantityInputs[index].value;
        console.log(quantity);
        // Send data to backend using your preferred method (e.g., AJAX fetch)
        fetch("http://127.0.0.1:5001/cart", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            productName,
            productPrice,
            quantity,
            index
          }),
        })
          .then((response) => {
            // Handle successful response
            console.log("Product added to cart successfully!");
            // You might want to display a success message or update the UI
          })
          .catch((error) => {
            // Handle errors
            console.error("Error adding product to cart:", error);
          });
      });      
})
