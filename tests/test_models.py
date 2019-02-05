from hitlog.models import Page, PageHit


def test_page():

    page = Page('Page Title', '/articles/article-title')

    assert page.is_article()
    assert not page.is_register()

    page = Page('Register', '/register')
    assert page.is_register()
    assert not page.is_article()


def test_page_hit():

    page_hit = PageHit('Page Title', '/articles/article-title', '100001', '12312313')

    assert isinstance(page_hit.page, Page)