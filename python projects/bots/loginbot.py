from webbot import Browser

web = Browser()


web.go_to("google.com")
web.type('hello')
# web.click('Log in')