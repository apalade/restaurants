const test_email = 'test-user-' + Math.floor(Math.random() * 1000000) + '@gmail.com'
const test_passwd = '123'
const test_restaurant =  {name: 'Restaurant Test', description: 'Restaurant Description'}
const test_meal =  {name: 'Meal Test', description: 'Meal Description', price: 2.3}

module.exports = {
    'Order' : function (browser) {
      browser
        // Create user and login
        .url('http://127.0.0.1:8080/#/register')
        .setValue('input[id="email"]', test_email)
        .setValue('input[id="password"]', test_passwd)
        .setValue('input[id="password2"]', test_passwd)
        .click('input[id="owner"]')
        .submitForm('form')
        .assert.urlContains('/login')
        .setValue('input[id="email"]', test_email)
        .setValue('input[id="password"]', test_passwd)
        .submitForm('form')
        .pause(500)

        // Restaurant CRUD
        .url('http://127.0.0.1:8080/#/restaurant/add')
        .setValue('input[id="name"]', test_restaurant.name)
        .click('#button')
        .waitForElementVisible('#global-message')
        .setValue('input[id="description"]', test_restaurant.description)
        .click('#button')
        .assert.urlContains('/restaurants')
        .assert.containsText('div.card-body', test_restaurant.name)
        .assert.containsText('div.card-body', test_restaurant.description)
        .click('div.card div a:nth-child(1)') // Edit
        .pause(100)
        .setValue('div.card-body input:nth-child(2)', '1')
        .setValue('div.card-body input:nth-child(3)', '1')
        .click('div.card div a:nth-child(1)') // Save
        .assert.containsText('div.card-body', test_restaurant.name + '1')
        .assert.containsText('div.card-body', test_restaurant.description + '1')
        .click('div.card div a:nth-child(2)') // Delete
        .pause(100)
        .assert.not.elementPresent('div.card-body')
        
        // Meal CRUD
        .url('http://127.0.0.1:8080/#/restaurant/add')
        .setValue('input[id="name"]', test_restaurant.name)
        .setValue('input[id="description"]', test_restaurant.description)
        .click('#button')
        .pause(100)
        .url('http://127.0.0.1:8080/#/meal/add')
        .setValue('input[id="name"]', test_meal.name)
        .setValue('input[id="description"]', test_meal.description)
        .setValue('input[id="price"]', test_meal.price)
        .click('#button')
        .waitForElementVisible('#global-message')
        .click('#restaurant_id')
        .keys(['\uE015', '\uE006'])
        .click('#button')
        .assert.urlContains('/meals')
        .assert.containsText('div.card-body', test_meal.name)
        .assert.containsText('div.card-body', test_meal.description)
        .assert.containsText('div.card-body', test_meal.price)
        .assert.containsText('div.card-body', test_restaurant.name)
        .click('div.card div a:nth-child(1)') // Edit
        .pause(100)
        .setValue('div.card-body input:nth-child(2)', '1')
        .setValue('div.card-body input:nth-child(3)', '1')
        .setValue('div.card-body input:nth-child(4)', '1')
        .click('div.card div a:nth-child(1)') // Save
        .pause(100)
        .assert.containsText('div.card-body', test_meal.name + '1')
        .assert.containsText('div.card-body', test_meal.description + '1')
        .assert.containsText('div.card-body', test_meal.price.toString() + '1')
        .click('div.card div a:nth-child(2)') // Delete
        .pause(100)
        .assert.not.elementPresent('div.card-body')

        // Order
        .url('http://127.0.0.1:8080/#/meal/add')
        .setValue('input[id="name"]', test_meal.name)
        .setValue('input[id="description"]', test_meal.description)
        .setValue('input[id="price"]', test_meal.price)
        .click('#restaurant_id')
        .keys(['\uE015', '\uE006'])
        .click('#button')
        .pause(100)
        .url('http://127.0.0.1:8080/#/')
        .useXpath()
        .click(`(//h5[contains(text(), "${test_meal.name}")])[last()]/following-sibling::a`) // Order now
        .useCss()
        .waitForElementVisible('div.container.cart')
        .click('div.container.cart a:nth-child(4)') // Confirm
        .waitForElementNotVisible('div.container.cart')
        .pause(100)
        .assert.urlContains('/orders')
        .assert.containsText('tr td', test_meal.name)

        // Delete the meal and check if line from the order is gone, 
        // but the restaurant is still there
        .url('http://127.0.0.1:8080/#/meals')
        .click('div.card div a:nth-child(2)') // Delete
        .pause(100)
        .assert.not.elementPresent('div.card-body')
        .url('http://127.0.0.1:8080/#/orders')
        .assert.not.containsText('tr td', test_meal.name)
        .url('http://127.0.0.1:8080/#/restaurants')
        .assert.containsText('div.card-body', test_restaurant.name)
        .assert.containsText('div.card-body', test_restaurant.description)

        // Now delete the restaurant and check if the entire order is gone
        .click('div.card div a:nth-child(2)') // Delete
        .waitForElementNotPresent('div.card-body')
        .url('http://127.0.0.1:8080/#/orders')
        .assert.not.elementPresent('table')

        


















        






        .end();
    },
  };