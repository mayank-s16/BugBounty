### Reflected XSS into HTML context with nothing encoded
**Vulnerable Parameter/Location:** Search field<br>
Reflection Point is given below.
```html
<h1>0 search results for '11111'</h1>
```
**Payload Used:** <script>alert()</script>
