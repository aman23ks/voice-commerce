const addToCartBtns = document.querySelectorAll("addToCartBtn");
console.log(addToCartBtns)
addToCartBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        const productName = document.querySelector(".card-title").textContent;
        const productPrice = document.querySelector(".card-subtitle").textContent;
        const quantity = document.getElementById("inputQuantitySelector").value;
        console.log(productName);
        console.log(productPrice);
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
