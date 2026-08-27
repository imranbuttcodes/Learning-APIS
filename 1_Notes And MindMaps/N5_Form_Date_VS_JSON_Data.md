Think of **Form Data** as the original, old-school way the internet was built to send information. When you type your name into an HTML `<form>` on a website and hit "Submit," the browser naturally packages and sends the information as Form Data.

Here is the exact visual difference between the two formats when they travel across the internet to your server:

**The JSON Way (Modern APIs)**
This is what your normal Pydantic schemas expect to read. It sends data as a neat, structured dictionary.

```json
{
  "username": "test@test.com",
  "password": "123"
}

```

**The Form Data Way (The OAuth2 Standard)**
This is what `OAuth2PasswordRequestForm` expects to read. It glues the keys and values together with equal signs (`=`) and separates them with ampersands (`&`), almost exactly like a web URL.

```text
username=test%40test.com&password=123

```

*(Notice how the `@` symbol in the email got converted to `%40`? That is Form Data automatically encoding special characters so they don't break the internet.)*

**The FastAPI Connection**
FastAPI handles these two formats completely differently:

* **Pydantic Model:** If you inject a normal schema (e.g., `user: UserLogin`), FastAPI explicitly blocks Form Data and demands a JSON dictionary.
* **OAuth2 Form:** If you inject `OAuth2PasswordRequestForm`, FastAPI explicitly blocks JSON and demands traditional Form Data.

Because the creators of the OAuth2 security standard wrote the official rulebook a long time ago, they mandated that secure password flows must use this traditional Form Data format. FastAPI provides that built-in form class so you can easily obey the standard without having to write a custom Form Data parser yourself.