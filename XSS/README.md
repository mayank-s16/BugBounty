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
### 3. DOM XSS in document.write sink using source location.search
**Vulnerable Parameter/Location:** Search field<br>
User's input is getting reflected back in DOM at two places as given below.
```html
<h1>0 search results for '111111'</h1>
```
```html
<img src="/resources/images/tracker.gif?searchTerms=111111">
```
First reflection point is also visible when we view Source code, but the second one is not visible in source code. Because this does not exist in source code, the server didn't send it. Instead, a client-side JavaScript file grabbed your input (from a Source like location.search, location.hash, or document.referrer) and dynamically wrote it into the page (into a Sink) after the initial page loaded. Lets view the source code again to check for any vulnerable javascript that might be generating the link in second reflection point
```js
function trackSearch(query) {
	document.write('<img src="/resources/images/tracker.gif?searchTerms=' + query + '">');
}
var query = (new URLSearchParams(window.location.search)).get('search');
if (query) {
	trackSearch(query);
}
```
Nice, means we can use the below payload to execute XSS. In the above js code query parameter would be replaced by user's input. So the final payload would be according to the reflection in DOM (Inspect Element).<br>
**Payload**: "><script>alert()</script>

