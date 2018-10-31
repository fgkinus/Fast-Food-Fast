
let script = require('../static/js/script.js');
let expect = require('chai').expect;
let assert = require('chai').assert;


describe('fetch cookie', function() {
    it('should return the auth cookie', function() {
        assert.equal(script.getCookie('auth'),'')
    });
});