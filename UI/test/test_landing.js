describe('test landing page components', function () {
    let page;
    const script = require('../static/js/script');

    // set up tests
    before(async function () {
        page = await browser.newPage();
        await page.goto('http://127.0.0.1:5000/landing.html');
    });

    // tear down asset
    after(async function () {
        await page.close();
    });


    it('should load view items button', async function () {
        let btn_text = await page.evaluate(() => {
            let text = document.querySelector('.btn').textContent;
            return text;
        });

        expect(btn_text).to.eql('our Menu');
    });

    it('should load a menu item list', async function () {
        let list = await page.evaluate(() => {
            let list_content = document.querySelector('#popup-list-content').childElementCount;
            return list_content;
        });
    });
    it('should test sum',async function () {
        expect(await script.sum(1,2)).to.eql(3);
    });

    it('should load the api endpoints',async function () {
        expect(await script.urls).to.exist;
    });

    it('should should not have auth token',async function () {
        let token  = await page.evaluate(()=>{
            let tok =  getCookie('auth');
            return tok;
        });
        expect(token).to.eql('');
    });
});