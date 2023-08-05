"""
Utilities for Country, Language, Timezone models. Generating data for them.
"""
import logging
import datetime

import pytz

from django.db import transaction

from babel.languages import get_territory_language_info,\
                            get_official_languages
from pycountry import countries, languages

from django_asservio_core.models import (
    Country, Language, Timezone
)

logger = logging.getLogger(__name__)


def get_utc_offset_for_tz(tz_name):
    """
    Args:
        tz_name (str): Timezone name.

    Returns:
        tuple(datetime.time, bool): UTC offset for tz and offset sign boolean.
    """
    tz = pytz.timezone(tz_name)
    offset = tz.localize(datetime.datetime(datetime.datetime.now().year, 1, 1))\
        .strftime('%z')
    utc_offset = datetime.time(hour=int(offset[1:3]), minute=int(offset[3:]))
    return utc_offset, True if offset[0] == '+' else False


def load_countries_iso3166():
    """Populate to database all countries in ISO3166.
    
    Returns:
        int: Quantity of country populated.
    """
    result_countries = []
    for country in countries:
        query = Country.objects.filter(code2=country.alpha_2)
        if not query.exists():
            new_country = Country(
                code2=country.alpha_2,
                code3=country.alpha_3,
                numeric_code=country.numeric,
                name=country.name
            )
            result_countries.append(new_country)
    Country.objects.bulk_create(result_countries)
    return len(result_countries)


def load_languages_iso639():
    """Populate to database all languages in ISO369.
    
    Returns:
        int: Quantity of languages populated.
    """
    result_languages = []
    for language in languages:
        query = Language.objects.filter(code2=language.alpha_3)
        if not query.exists():
            new_language = Language(code2=language.alpha_3, name=language.name)
            try:
                new_language.code1 = language.alpha_2
            except AttributeError:
                pass
            result_languages.append(new_language)
    Language.objects.bulk_create(result_languages)
    return len(result_languages)


def load_timezone_utc():
    """Populate to database all timezones.
    
    Returns:
        int: Quantity of timezones populated.    
    """
    result_timezones = []
    for timezone in pytz.all_timezones:
        query = Timezone.objects.filter(name=timezone)
        if not query.exists():
            utc_offset, sign = get_utc_offset_for_tz(timezone)
            new_timezone = Timezone(name=timezone, utc_offset=utc_offset,
                                    is_positive_offset=sign)
            result_timezones.append(new_timezone)
    Timezone.objects.bulk_create(result_timezones)
    return len(result_timezones)


def get_languages_for_country(code2):
    """Get official or most popular languages in country.

    Args:
        code2: ISO3166 code for country

    Returns:
        List of Language objects.
    """
    language_codes = get_official_languages(code2)
    if not language_codes:
        language_info = get_territory_language_info(code2)
        most_popular_language \
            = max(language_info,
                  key=(lambda key: language_info[key]['population_percent']))
        language_codes = tuple(most_popular_language)

    country_languages = []
    for language_code in language_codes:
        if len(language_code) == 2:
            query = Language.objects.filter(code1=language_code)
        elif len(language_code) == 3:
            query = Language.objects.filter(code2=language_code)
        else:
            logger.warning('Unexpected language code length returned '
                           'with length of %s symbols.', len(language_code),
                           extra={
                            'language_code': language_code
                           })
            continue
        if query.exists():
            language = query.first()
            country_languages.append(language)
        else:
            logger.warning('Language %s does not exist in our database.',
                           language_code, extra={
                            'language_code': language_code
                           })
    return country_languages


def set_languages_for_countries():
    """Set official or most popular language for country."""
    countries_qs = Country.objects.all()
    for country in countries_qs:
        language = get_languages_for_country(country.code2)
        country.languages.add(*language)


def get_timezones_for_country(code2):
    """
    Args:
        code2: ISO3166 code for country.

    Returns:
        List of Timezones objects.
    """
    timezones = pytz.country_timezones.get(code2)

    if not timezones:
        return []

    country_timezones = []
    for timezone_name in timezones:
        query = Timezone.objects.filter(name=timezone_name)
        if query.exists():
            timezone = query.first()
            country_timezones.append(timezone)
        else:
            logger.warning('Timezone %s does not exist in our database.',
                           timezone_name, extra={
                            'timezone_name': timezone_name
                           })
    return country_timezones


def set_timezones_for_countries():
    """Set official timezone for country."""
    countries_qs = Country.objects.all()
    for country in countries_qs:
        timezones = get_timezones_for_country(country.code2)
        if timezones:
            country.timezones.add(*timezones)


def seed_database():
    """Seeding database.
    
    Returns:
        tuple(int, int, int): Count of populated countries, languages 
            and timezones.
    """
    logger.info('Began seeding database with country, '
                'language and timezone data.')
    with transaction.atomic():
        countries_count = load_countries_iso3166()
        languages_count = load_languages_iso639()
        timezones_count = load_timezone_utc()
        set_languages_for_countries()
        set_timezones_for_countries()
    logger.info('Finished seeding database with country, '
                'language and timezone data.', extra={
                    'countries_count': countries_count,
                    'languages_count': languages_count,
                    'timezones_count': timezones_count
                })
    return countries_count, languages_count, timezones_count
