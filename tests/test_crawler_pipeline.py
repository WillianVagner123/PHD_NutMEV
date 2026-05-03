from crawler_pipeline import extract_candidate_links_from_html


class FakeA:
    def __init__(self, href, text):
        self._href = href
        self._text = text
    def __getitem__(self, k):
        if k == 'href':
            return self._href
        raise KeyError(k)
    def get_text(self, sep=' ', strip=True):
        return self._text


class FakeSoup:
    def __init__(self, links):
        self.links = links
    def find_all(self, tag, href=True):
        return self.links


def test_extract_candidate_links_filters_and_limits():
    soup = FakeSoup([
        FakeA('/doc1.pdf', 'Doc 1'),
        FakeA('/login', 'Login'),
        FakeA('/page.html', 'Guide page'),
    ])

    rows = extract_candidate_links_from_html(
        base_url='https://example.org/start',
        html_soup=soup,
        page_title='Title',
        page_text_excerpt='Excerpt',
        workstream='ws1',
        source_name='src',
        seed_url='seed',
        looks_like_relevant_link=lambda href, text: True,
        detect_extension_from_response=lambda href, _: '.pdf' if href.endswith('.pdf') else ('.html' if href.endswith('.html') else ''),
        downloadable_ext={'.pdf'},
        paywall_hints=['login'],
        max_links_per_page=10,
    )
    urls = [r['link_url'] for r in rows]
    assert any(u.endswith('doc1.pdf') for u in urls)
    assert any(u.endswith('page.html') for u in urls)
    assert not any('login' in u for u in urls)
