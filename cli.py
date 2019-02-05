import csv
import click

from hitlog.functions import (parse_csv_and_create_hit_list,
                              group_hits_in_user_navigation,
                              extract_completed_journeys,
                              rank_article_on_journey_occurrences,
                              is_article_or_registration)


@click.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w'))
def cli(input_file, output_file):

    csv_reader = csv.reader(input_file, quoting=csv.QUOTE_NONE)
    hits_generator = parse_csv_and_create_hit_list(csv_reader)

    hit_list = filter(is_article_or_registration, hits_generator)

    sorted_hit_list = sorted(hit_list, key=lambda x : x.timestamp)

    completed_journeys = []
    for user_id, hits in group_hits_in_user_navigation(sorted_hit_list).iteritems():
        completed_journeys += extract_completed_journeys(hits)

    article_rank = rank_article_on_journey_occurrences(completed_journeys)

    article_rank = sorted(article_rank.iteritems(), key=lambda (k, v): (v, k), reverse=True)

    csv_writer = csv.writer(output_file)
    csv_writer.writerow(['page_name', 'page_url', 'total'])

    for article, total in article_rank[:3]:
        csv_writer.writerow([
            article.page_name,
            article.page_url,
            total
        ])









