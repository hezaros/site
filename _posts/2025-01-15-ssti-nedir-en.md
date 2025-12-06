---
title: "What is SSTI Vulnerability?"
date: 2025-01-15 12:00:00 +0300
lang: en
slug: ssti-nedir
---

# What is SSTI Vulnerability?

Today, most websites use dynamic web pages. Dynamic pages generate content on the server-side or client-side according to the user. During this generation process, template engines come into play. Server-side attacks target an application or service provided by a server, while Client-side attacks occur on the client's machine, not on the server itself. Where and on which side the content is generated reveals the fundamental difference between SSTI and CSTI vulnerabilities.

In SSTI vulnerabilities, as mentioned above, the content is rendered by a template engine running on the server-side and the output is sent to the client as HTML. If inputs are passed directly to the template engine without sufficient filtering, these expressions can be interpreted by the template engine as template expressions or function calls rather than variables. The commonly encountered `{{7*7}}` expression has become:

A well-known payload to determine whether the template engine interprets the input as a variable as it should, or whether injection can be performed.

In CSTI, the template processing is performed on the user's browser. Many frontend frameworks used today can also perform template rendering on the client-side. Therefore, CSTI vulnerabilities can arise through user inputs containing template expressions.

## Secure Code Example

For example, a secure template example in jinja2:

![Secure Code Example](/arda.tc/images/ssti-nedir/page_1_img_1.jpeg)

```python
The template sent to the render() function "Hello {{name}}" is a static value, the input
"Arda" is only assigned as the value of the variable named "name".
```

The output of this code will be `Hello Arda` and the `{{7*7}}` expression will not work here.

![Secure Code Output](/arda.tc/images/ssti-nedir/page_1_img_2.jpeg)

## Vulnerable Code Example

The vulnerable code example is as follows:

![Vulnerable Code Example](/arda.tc/images/ssti-nedir/page_2_img_1.jpeg)

```python
template = "Hello " + user_input
render_template_string(template)
```

In this code, the dangerous part is that the template that render() will receive will not be just `{{7*7}}` but `"Hello {{7*7}}"`. This gives the output as `Hello 49`. This and similar situations cause SSTI vulnerabilities.

# SSTI Attack Methodology

The existence of this vulnerability in the target system is revealed when we interpret error codes or whether the input we sent is rendered. Different template engines may use slightly different syntaxes.

## SSTI Detection

The process of detecting SSTI is similar to detecting other injections. To create an error message on the other side or to see which special characters it renders:

```
${{<%[%'"}}\.
```

We give this payload as input. This is similar to breaking the SQL query syntax and encountering an error by giving a single quote (') input in SQL injection detections. After giving this payload, I either expect an error and try to get information about whether there is a Template injection, and if so, which template type it uses, or I put a marker in a certain part, for example arda:

```
${{<%[arda%'"}}\.
```

In this way, we look at where this template writes the output on the page and see which special characters it rendered, and in this direction, we try to understand which template engine was used.

When we compare the input we gave and the output, we see that the special characters `<%` are missing.

![SSTI Detection Example](/arda.tc/images/ssti-nedir/page_3_img_1.jpeg)

## ATTACK SCENARIO 1

When we research this behavior on the internet (book.hacktricks.wiki is recommended and can be used), we see that it is related to commonly used template engines such as ERB (Ruby), Mako (Python).

When we try to read the passwd file with ERB as an example:

```erb
<%= system('cat /etc/passwd') %>
```

![ERB Attack Example](/arda.tc/images/ssti-nedir/page_3_img_2.jpeg)

We succeed in this system. If we had not been successful, we would try other template engines that use (`<%`) or if we are sure that ERB template is used in this system and we think there is a vulnerability, we think that access to command execution functions in the system is blocked. However, thanks to Ruby and other OOP languages, we can try different ways because in OOP everything is an object. So our way of thinking is that every object has a class, we can access methods coming from that class, and with some methods we can reach other classes and methods.

We can think of it as a chain like `Object → Class → Method → Execute`.

## ATTACK SCENARIO 2

After understanding that there is a Template injection in the system:

First, we write `<%= "arda".class %>` and see its output, this is the first step. Since we know where we are now and that every class in Ruby is derived from another class, this is the first stage of the chain. After this, we will go up to a parent class.

![Attack Scenario 2 - Step 1](/arda.tc/images/ssti-nedir/page_4_img_1.jpeg)

In the other stage, we will go up to the superclass, when we write `<%= "arda".class.superclass %>` we get the output `Object`. The Object class is the most basic class in Ruby and contains many methods that can be useful for us.

![Attack Scenario 2 - Step 2](/arda.tc/images/ssti-nedir/page_4_img_2.jpeg)

In the method stage, we use the input `<%= Object.methods %>` to see the methods. Here we get a long method output.

Especially the methods I underlined above are powerful methods for executing commands and doing RCE:

- `:send`
- `:__send__`
- `:instance_eval`
- `:instance_exec`

We can try to read the passwd file with the information we gathered from above:

```erb
<%= Object.const_get("File").read("/etc/passwd") %>
```

![Attack Scenario 2 - Final](/arda.tc/images/ssti-nedir/page_4_img_3.jpeg)

If we could not read the passwd file directly as `<%= system('cat /etc/passwd') %>`, we went through the scenario and read it with the payload we used at the end.

---

> **Note**: This article has been converted from PDF content. Click [here](/arda.tc/pdfs/ssti-nedir.pdf) for the original PDF file.

