// credit for code : https://medium.com/@ankit_m/ui-testing-with-puppeteer-and-mocha-part-1-getting-started-b141b2f9e21

// set up the tests
const puppeteer = require('puppeteer');
const { expect } = require('chai');
const _ = require('lodash');
const globalVariables = _.pick(global, ['browser', 'expect']);

const script = require('../static/js/script.js');

// puppeteer options
const opts = {
  headless: true,
  slowMo: 100,
  timeout: 10000
};

before (async function () {
  global.expect = expect;
  global.browser = await puppeteer.launch(opts);
  global.script = script;
});

// tear down the test
after (function () {
  browser.close();

  global.browser = globalVariables.browser;
  global.expect = globalVariables.expect;
});