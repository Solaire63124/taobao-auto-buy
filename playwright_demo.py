import json
import os
from playwright.sync_api import Page, expect, sync_playwright, Playwright, Locator
import pytest
from const import *

@pytest.fixture(scope="function", autouse=True)
def login_taobao(page: Page):
    page.goto(TAOBAO_URL)
    page.get_by_role('link', name='亲，请登录').click()
    qr_code_image = page.locator('canvas')
    cookies = []
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, 'r') as f:
            cookies = json.loads(f.read())
        page.context.add_cookies(cookies)
        page.reload()
        expect(qr_code_image, 'Login failed!').to_be_hidden()
    else:
        attempts = 0
        # Wait for QR scan.
        while attempts < LOGIN_RETRYS:
            attempts += 1
            if qr_code_image.is_visible():
                print(f'Login attempt {attempts} failed.')
            else:
                break
            page.wait_for_timeout(LOGIN_TIMEOUT)
        expect(qr_code_image, 'Login failed!').to_be_hidden()
        # Click the button to save the login status.
        page.get_by_role("button", name="保持", exact=True).click()
        cookies = page.context.cookies()
        os.makedirs(COOKIE_SAVE_PATH, exist_ok=True)
        with open(COOKIE_FILE, 'w') as f:
            f.write(json.dumps(cookies))
    expect(qr_code_image, 'Login failed!').to_be_hidden()
    page.get_by_role("link", name=" 购物车").click()


def test_buy_cart_items(page: Page):
    select_all_btn = page.locator("span#J_SelectAll1")
    submit_btn = page.get_by_label("请注意如果没有选择宝贝，将无法结算")
    pay_btn = page.get_by_role("button", name="提交订单")

    while 'select-all-disabled' in class_list(select_all_btn):
        page.reload()
        page.wait_for_timeout(500)
    
    while 'selected' not in class_list(select_all_btn):
        select_all_btn.click(force=True)

    while 'submit-btn-disabled' in class_list(submit_btn):
        submit_btn.click(force=True)
    
    while True:
        pay_btn.click() 


def class_list(locator: Locator):
    return locator.get_attribute('class')
