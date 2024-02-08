const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');
const productTitleElements = document.querySelectorAll('.card-title');
const productPriceElements = document.querySelectorAll('.card-subtitle');
const quantityInputs = document.querySelectorAll('.input-qty-selector');
const sessionId = document.getElementById('session-id').value;
const urlSegments = window.location.pathname.split('/');
const id = urlSegments[urlSegments.length - 2];
addToCartBtns.forEach((btn, index) => {
    btn.addEventListener("click", () => {
        const productName = productTitleElements[index].textContent;
        const productPrice = productPriceElements[index].textContent;
        const quantity = quantityInputs[index].value;

        // Send data to backend using your preferred method (e.g., AJAX fetch)
        fetch(`http://127.0.0.1:5001/${id}/cart`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            sessionId: sessionId,
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
