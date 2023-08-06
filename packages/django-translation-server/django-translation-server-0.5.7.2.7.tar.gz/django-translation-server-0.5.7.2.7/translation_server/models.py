from django.db import models
from django.utils.translation import ugettext_lazy as _


class TranslationType(models.Model):
    created = models.DateTimeField(_('DTSM1'), auto_now_add=True, null=True, blank=True, help_text=_('DTST1'))
    updated = models.DateTimeField(_('DTSM2'), auto_now=True, null=True, blank=True, help_text=_('DTST2'))
    tag = models.CharField(_('DTSM3'), help_text=_('DTST3'), max_length=20, unique=True)
    name = models.TextField(_('DTSM4'), help_text=_('DTST4'))
    has_auxiliary_text = models.BooleanField(_('DTSM5'), help_text=_('DTST5'), default=True)
    auxiliary_tag = models.CharField(_('DTSM6'), help_text=_('DTST6'), max_length=20, unique=True, blank=True,
                                     default=False, null=True)

    class Meta:
        verbose_name = _('DTSMT1')
        verbose_name_plural = _('DTSMTP1')

    def __str__(self):
        return "%s - %s" % (self.tag, self.name)

    def __unicode__(self):
        return "%s - %s" % (self.tag, self.name)


class Translation(models.Model):
    created = models.DateTimeField(_('DTSM1'), auto_now_add=True, null=True, blank=True, help_text=_('DTST1'))
    updated = models.DateTimeField(_('DTSM2'), auto_now=True, null=True, blank=True, help_text=_('DTST2'))
    type = models.ForeignKey(TranslationType, on_delete=None, related_name="translation_translation_type",
                             verbose_name=_('DTSM7'), help_text=_('DTST7'))
    tag = models.CharField(_('DTSM8'), help_text=_('DTST8'), max_length=20, unique=True)
    text = models.TextField(_('DTSM9'), help_text=_('DTST9'))
    auxiliary_tag = models.CharField(_('DTSM10'), help_text=_('DTST10'), max_length=20, blank=True, null=True)
    auxiliary_text = models.TextField(_('DTSM11'), help_text=_('DTST11'), blank=True, null=True)
    migration_created = models.BooleanField(_('DTSM12'), help_text=_('DTST12'), default=False)

    class Meta:
        verbose_name = _('DTSMT2')
        verbose_name_plural = _('DTSMTP2')

    def __str__(self):
        return "%s" % self.tag

    def __unicode__(self):
        return "%s" % self.tag


# @receiver(post_save, sender=Translation, dispatch_uid="update_stock_count")
# def update_translation(sender, instance, **kwargs):
#     from django.core.management import call_command
#     call_command('make_translation')

class LastTranslationTag(object):
    translation_tag = None

    def __init__(self, translation_tag, *args, **kwargs):
        self.translation_tag = translation_tag

    def return_last_tag(self):
        if self.translation_tag and len(self.translation_tag) > 0:
            from django.db import connection
            # todo: add suport to multiple databases
            query = "SELECT tag FROM %(translation_table)s WHERE tag LIKE '%(translation_tag)s%%' ORDER BY NULLIF(regexp_replace(TAG, E'\\\\D', '', 'g'), '')::int DESC LIMIT 1" % {
                'translation_tag': self.translation_tag,
                'translation_table': Translation._meta.db_table
            }
            cursor = connection.cursor()
            try:
                cursor.execute(query)
            except Exception as err:
                raise err
            else:
                result = []
                for row in cursor.fetchall():
                    result = row[0]
                if result:
                    import re
                    tag = Translation.objects.get(tag=result)
                    return dict(result=dict(last_tag=result, last_id=re.findall("(\d+)", result)[0], type=tag.type.name,
                                            has_auxiliary_text=tag.type.has_auxiliary_text,
                                            auxiliary_tag=tag.type.auxiliary_tag, tag=tag.type.tag))
                else:
                    return dict(result=dict())
        else:
            return dict(result=dict())
