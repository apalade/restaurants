const test_email = 'test-user-' + Math.floor(Math.random() * 1000000) + '@gmail.com'
const test_passwd = '123'

module.exports = {
    'Register' : function (browser) {
      browser
        .url('http://127.0.0.1:8080/#/register')
        .setValue('input[id="email"]', test_email)
        .setValue('input[id="password"]', test_passwd)
        .setValue('input[id="password2"]', test_passwd)
        .click('input[id="owner"]')
        .submitForm('form')
        .assert.urlContains('/login')
        .url('http://127.0.0.1:8080/#/register')
        .setValue('input[id="email"]', test_email)
        .setValue('input[id="password"]', test_passwd)
        .setValue('input[id="password2"]', test_passwd)
        .click('input[id="owner"]')
        .submitForm('form')
        .waitForElementVisible('#global-message')
        .end();
    },
    'Logging in' : function (browser) {
      browser
        .url('http://127.0.0.1:8080/#/login')
        .setValue('input[id="email"]', test_email)
        .setValue('input[id="password"]', test_passwd + 'wrong')
        .submitForm('form')
        .waitForElementVisible('#global-message')
        .clearValue('input[id="password"]')
        .setValue('input[id="password"]', test_passwd)
        .submitForm('form')
        .assert.urlEquals('http://127.0.0.1:8080/#/')
        .end();
    }
  };