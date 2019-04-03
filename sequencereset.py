from django.core.management.color import no_style
from django.db import connection
from recommender.models import Movie


sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Movie])
with connection.cursor() as cursor:
    for sql in sequence_sql:
        cursor.execute(sql)