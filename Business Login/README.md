## Business logic vulnerabilities
### Excessive trust in client-side controls
While adding items to the cart, send this request to repeater. Manipulated the price value and refresh your cart on UI.
* price=0 (Didn't work)
* price=1 (Worked)

