import csv
import os
from collections import Iterable

from hitlog.models import PageHit, ArticleEntry
from hitlog.functions import parse_csv_and_create_hit_list, group_hits_in_user_navigation, extract_completed_journeys, \
    is_article_or_registration, is_article, rank_article_on_journey_occurrences
from tests import RESOURCE_DIR

input_file = os.path.join(RESOURCE_DIR, 'sample_input.csv')


def test_read_csv():

    with open(input_file) as csv_file:
        reader = csv.reader(csv_file, quoting=csv.QUOTE_NONE)

        page_hits = parse_csv_and_create_hit_list(reader)
        assert isinstance(page_hits, Iterable)

        page_hit = next(page_hits)

        assert isinstance(page_hit, PageHit)


def test_group_hits_by_user_id():

    hit_list = [
        PageHit('Article Title', '/articles/article-title', '100001', '1515355938'),
        PageHit('Article Title', '/articles/article-title', '100002', '1515355938'),
        PageHit('Article Title', '/articles/article-title-2', '100002', '1515355940'),
        PageHit('Article Title', '/articles/article-title', '100003', '1515355945')
    ]

    grouped_hits = group_hits_in_user_navigation(hit_list)

    assert set(grouped_hits.keys()) == {'100001', '100002', '100003'}

    assert len(grouped_hits['100002']) == 2
    assert len(grouped_hits['100001']) == 1
    assert len(grouped_hits['100003']) == 1


def test_extract_completed_journeys():

    completed_journey = extract_completed_journeys([
        PageHit('Article Title', '/articles/article-title', '100001', '1515355938'),
        PageHit('Article Title', '/articles/article-title', '100001', '1515355939'),
        PageHit('Article Title', '/register', '100001', '1515355940'),
        PageHit('Article Title', '/articles/article-title', '100001', '1515355941'),
        PageHit('Article Title', '/register', '100001', '1515355942'),
        PageHit('Article Title', '/articles/article-title', '100001', '1515355943'),
        PageHit('Article Title', '/articles/article-title', '100001', '1515355944')
    ])

    assert len(completed_journey) == 2

    assert len(completed_journey[0]) == 3
    assert len(completed_journey[1]) == 2


def test_rank_article_on_journey_occurrences():

    completed_journeys = [
        [
            PageHit('Article Title', '/articles/article-title', '100001', '1515355938'),
            PageHit('Article Title 2', '/articles/article-title-2', '100001', '1515355939'),
            PageHit('Register', '/register', '100001', '1515355940'),
        ],
        [
            PageHit('Article Title', '/articles/article-title', '100001', '1515355941'),
            PageHit('Register', '/register', '100001', '1515355942'),
        ],
        [
            PageHit('Article Title 2', '/articles/article-title-2', '100001', '1515355938'),
            PageHit('Article Title 3', '/articles/article-title-3', '100001', '1515355939'),
            PageHit('Register', '/register', '100001', '1515355940'),
        ],
        [
            PageHit('Article Title 5', '/articles/article-title-5', '100001', '1515355939'),
            PageHit('Article Title 2', '/articles/article-title-2', '100001', '1515355940'),
            PageHit('Article Title 6', '/articles/article-title-6', '100001', '1515355941'),
            PageHit('Article Title', '/register', '100001', '1515355942'),
        ],
    ]

    rank = rank_article_on_journey_occurrences(completed_journeys)

    for article, value in rank.iteritems():
        assert isinstance(article, ArticleEntry)

    assert rank[ArticleEntry('Article Title 2', '/articles/article-title-2')] == 3
    assert rank[ArticleEntry('Article Title', '/articles/article-title')] == 2
    assert rank[ArticleEntry('Article Title 5', '/articles/article-title-5')] == 1
    assert rank[ArticleEntry('Article Title 3', '/articles/article-title-3')] == 1


def test_is_article_and_registration():

    article_hit = PageHit('Article Title', '/articles/article-title', '100001', '1515355938')

    registration_hit = PageHit('Registration Title', '/register', '100001', '1515355938')

    assert is_article_or_registration(article_hit)
    assert is_article_or_registration(registration_hit)

    assert not is_article_or_registration(PageHit('Page Title', '/something', '100005', '1515355938'))


def test_is_article():

    assert is_article(PageHit('Article Title', '/articles/article-title', '100001', '1515355938'))

    assert not is_article(PageHit('Registration Title', '/register', '100001', '1515355938'))
