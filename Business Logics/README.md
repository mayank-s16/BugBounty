## Business logic vulnerabilities
### Excessive trust in client-side controls [Price Manipulation while adding to cart]
While adding items to the cart, send this request to repeater. Manipulated the price value and refresh your cart on UI.
* price=0 (Didn't work)
* price=1 (Worked)
### High-level logic vulnerability [Price Manipulation while adding to cart]
This time price is not visible in the request, we do have the parameters like below, while we add the item in the cart.
```
productId=1&redir=PRODUCT&quantity=1
```
Lets play with quantity.
```
productId=1&redir=PRODUCT&quantity=-1 
```
We do have -1 item in the cart if we refresh on the page and the total amount would be -1*price. But while we checkout it says we cannot have negative total. Add the leather jacket to your cart as normal. Add a suitable negative quantity of the another item to reduce the total price to less than your remaining store credit.
### Inconsistent security controls
Flawed logic allows arbitrary users to access administrative functionality that should only be available to company employees. Lets try to browse admin page directly https://test[.]com/admin We got the below error.
```
Admin interface only available if logged in as a DontWannaCry user
```
* Register in the app using test@test[.]com
* Do have email update feature post login
* Update the email to test@Dontwannacry[.]com since the accounts with this domain would have admin privs.
* Didnt require any email verification,
Now we can access /admin page.
### Flawed enforcement of business rules [Price manipulation by abusing coupon code]
Discount coupon can be applied this time. Below are the test cases we performed
* Can same coupon be applied multiple times? Didn't work
* Can multiple different coupons applied? Yes (but it is not a vulnerability)
* Using repeater, Apply coupon1 first, then apply coupon 2, then apply coupon 1 and continues since the app was checking the last coupon applied to check for duplicate coupons. Refresh on UI and see the price changes.

