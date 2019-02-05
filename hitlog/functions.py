from hitlog.models import PageHit, ArticleEntry


def parse_csv_and_create_hit_list(csv_reader):
    """
    Uses the csv_reader and creates a generator of hits
    :param csv_reader:
    :return list:
    """

    headers = next(csv_reader, None)
    header_length = len(headers)

    for row in csv_reader:
        if len(row) == header_length:
            yield PageHit(*row)


def group_hits_in_user_navigation(hit_list):
    """
    Groups the site hits by user_id, creating an user navigation from the input file
    :param hit_list:

    :return dict: with key: user_id and value is the list of the user page hits
    """
    navigation_by_user_id = {}

    for page_hit in hit_list:
        if not navigation_by_user_id.get(page_hit.user_id):
            navigation_by_user_id[page_hit.user_id] = []

        navigation_by_user_id[page_hit.user_id].append(page_hit)

    return navigation_by_user_id


def extract_completed_journeys(navigation):
    """
    Generates a list of completed journeys
    A complete journey is a subset of the navigation. it's a list of hit that ends with registration.

    :param list navigation: list of hit

    :return: a list of journeys (navigation steps)that ends with a registration
    """
    list_of_completed_journey = []

    current_journey = []
    for hit in navigation:

        current_journey.append(hit)

        if hit.page.is_register():
            list_of_completed_journey.append(current_journey)
            current_journey = []

    return list_of_completed_journey


def rank_article_on_journey_occurrences(completed_journeys):
    """
    Counts article occurrences in completed journeys and create a ranked list

    :param completed_journeys:
    :return : dictionary with articles as key and occurrences as values
    """
    article_list = {}

    for journey in completed_journeys:
        for hit in filter(is_article, journey):
            article_key = ArticleEntry(hit.page.name, hit.page.url)

            if not article_list.get(article_key):
                article_list[article_key] = 0

            article_list[article_key] += 1

    return article_list


def is_article_or_registration(page_hit):
    return page_hit.page.is_article() or page_hit.page.is_register()


def is_article(page_hit):
    return page_hit.page.is_article()