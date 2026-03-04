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
### Low-level logic flaw
This time we need to add enough items in cart that would exceed the integer or float value of price so that it loops and becomes negative.
Since the negative number is not accepted by the application, loop back until it becomes and settle down the price by including other item between 1 and 100$ since 100$ is the max money you have and the items cost more than 100. The steps to reproduce are given below.
* In Burp Repeater while adding item to cart, notice that you can only add a 2-digit quantity with each request. Quantity parameter was also there in the rquest. Send the request to Burp Intruder.
* Go to Intruder and set the quantity parameter to 99.
* In the Payloads side panel, select the payload type Null payloads. Under Payload configuration, select Continue indefinitely. Send max request 1 by configuring the resource pool. Start the attack.
* While the attack is running, go to your cart. Keep refreshing the page every so often and monitor the total price. Eventually, notice that the price suddenly switches to a large negative integer and starts counting up towards 0.
* In the next few steps, we'll try to add enough units so that the price loops back around and settles between $0 and the $100 of your remaining store credit. This is not mathematically possible using only the leather jacket. Add leather jacket by doing some maths like TOTAL_PRICE/ITEM_PRICE. This would be the number of items you should to become it 0. You should do -1 from it to be safe. Because 0 is also not acceptable.
* Now add another item of different price to keep the price in 0 to 100 and then buy it.
 ### Inconsistent handling of exceptional input during registration process
 * Try to browse to /admin. Although you don't have access, an error message indicates that DontWannaCry users do
 * Go to the account registration page. We need to register with DontWannaCry domain somehow but it requires activation of account using the link sent on email and we dont have access to mailbox.
 * Try register with an exceptionally long email address in the format: very-long-string@.web-security-academy.net as you have access to mailbox of web-security-academy.net Complete the registration process by activating the account and login using this account
 * Log in and go to the "My account" page. Notice that your email address has been truncated to 255 characters.
 * Register a new account with another long email address, but this time include dontwannacry.com as a subdomain in your email address as follows:
  ```
   very-long-string@dontwannacry.com.YOUR-EMAIL-ID.web-security-academy.net
  ```
* Make sure that the very-long-string is the right number of characters so that the "m" at the end of @dontwannacry.com is character 255 exactly.
* Activate this account by clicking on activation link sent on email and log in to your new account and notice that you now have access to the admin panel
