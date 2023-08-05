"""
General models.
"""
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .audit import (
    get_dictionary_audit_mixin
)

AUDIT_MIXIN = get_dictionary_audit_mixin()


class Language(AUDIT_MIXIN, models.Model):
    """Language entity.

    Attributes:
        code1 (str or None): ISO 639-1 code of language (2 letters).
        code2 (str): ISO 639-2 code of language (3 letters).
        name (str): English name of language.
    """
    code1 = models.CharField(
        max_length=2,
        verbose_name=_('Language code (ISO 639-1)'),
        null=True
    )
    code2 = models.CharField(
        max_length=3,
        verbose_name=_('Language code (ISO 639-2)'),
        primary_key=True
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('Language name (English)')
    )

    @classmethod
    def get_default(cls):
        """Get default Language.

        Returns:
            :class:`~.Language`: Default language.
        """
        return cls.objects.get_or_create(
            code2='eng',
            defaults={
                'code1': 'en',
                'name': 'English'
            }
        )[0]

    def __str__(self):
        return '{0} {1}'.format(
            self.code2, self.name
        )

    class Meta:
        ordering = ('code2',)
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        db_table = 'language'
        index_together = ('code1', 'code2', 'name')


class Timezone(AUDIT_MIXIN, models.Model):
    """Timezone entity.

    Attributes:
        name (str): Timezone name.
        utc_offset (datetime.time): UTC offset time,
            negative/positive should be specified in is_positive_offset field.
        is_positive_offset (bool): Indicates if offset is positive.
        coordinates (str or None): Coordinates of timezone.

    """
    name = models.CharField(
        max_length=100,
        verbose_name=_('Timezone name'),
        unique=True,
        db_index=True
    )
    utc_offset = models.TimeField(
        verbose_name=_('UTC offset time (for standard time)'),
        help_text=_('Negative / positive should be '
                    'specified in `is_positive_offset` field')
    )
    is_positive_offset = models.BooleanField(
        default=True,
        verbose_name=_('Positive / negative offset')
    )
    coordinates = models.CharField(
        max_length=20,
        verbose_name=_('Coordinates'),
        null=True
    )

    @property
    def offset(self):
        """str: offset string representation"""
        return '{0}{1}'.format(
            '+' if self.is_positive_offset else '-',
            '{0}:{1}'.format(
                str(self.utc_offset.hour).zfill(2),
                str(self.utc_offset.minute).zfill(2)
            )
        )

    @classmethod
    def get_default(cls):
        """Get default Timezone.

        Returns:
            :class:`~.Timezone`: Default Timezone.
        """
        return cls.objects.get_or_create(
            name='UTC',
            defaults={
                'utc_offset': datetime.time(0, 0)
            }
        )[0]

    def __str__(self):
        return '{0} {1}{2}'.format(
            self.name,
            '+' if self.is_positive_offset else '-',
            '{0}:{1}'.format(
                str(self.utc_offset.hour).zfill(2),
                str(self.utc_offset.minute).zfill(2)
            )
        )

    class Meta:
        ordering = ('name',)
        verbose_name = _('Timezone')
        verbose_name_plural = _('Timezones')
        db_table = 'timezone'


class Country(AUDIT_MIXIN, models.Model):
    """Country entity.

    Attributes:
        code2 (str or None): ISO 3166-1 alpha-2 code of the country (2 letters).
        code3 (str): ISO 3166-1 alpha-3 code of the country (3 letters).
        numeric_code (str): ISO 3166-1 numeric code (3 digits).
        name (str): English name of the country.
        languages (list of :class:`~.Language`): Official languages in country.
        timezones (list of :class:`~.Timezone`): Timezones of the country.
    """
    code2 = models.CharField(
        max_length=2,
        verbose_name=_('Country code (ISO 3166-1 alpha-2)'),
        primary_key=True
    )
    code3 = models.CharField(
        max_length=3,
        verbose_name=_('Country code (ISO 3166-1 alpha-3)'),
        unique=True
    )
    numeric_code = models.CharField(
        max_length=3,
        verbose_name=_('Country numeric code (ISO 3166-1 numeric)'),
        unique=True
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('Country name (English)')
    )
    languages = models.ManyToManyField(
        Language,
        verbose_name=_('Country languages'),
        blank=True,
        related_name='countries'
    )
    timezones = models.ManyToManyField(
        Timezone,
        verbose_name=_('Country timezones'),
        blank=True,
        related_name='countries'
    )

    @classmethod
    def get_default(cls):
        """Get default Country.

        Returns:
            :class:`~.Country': Default Country.
        """
        country = cls.objects.get_or_create(
            code2='US',
            defaults={
                'code3': 'USA',
                'numeric_code': '840',
                'name': 'United States of America',
            }
        )[0]
        return country

    def __str__(self):
        return '{0} {1}'.format(
            self.code2, self.name
        )

    class Meta:
        ordering = ('code3',)
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        db_table = 'country'
        index_together = ('code2', 'code3', 'name', 'numeric_code')


def get_default_country():
    """Get default country.

    Returns:
        int: Country primary key
    """
    return Country.get_default().pk


def get_default_timezone():
    """Get default timezone.

    Returns:
        int: Timezone primary key
    """
    return Timezone.get_default().pk


def get_default_language():
    """Get default language.

    Returns:
        int: Language primary key
    """
    return Language.get_default().pk
