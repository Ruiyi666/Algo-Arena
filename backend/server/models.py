from django.db import models
from django.conf import settings

# Create your models here.
from django.utils.translation import gettext_lazy as _


class Strategy(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="strategies",
        verbose_name=_("User"),
    )
    name = models.CharField(_("Name"), max_length=150)
    description = models.TextField(_("Description"))
    is_mannual = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Player(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="players",
        verbose_name=_("Game"),
    )
    strategy = models.ForeignKey(
        Strategy,
        on_delete=models.CASCADE,
        related_name="players",
        verbose_name=_("Strategy"),
    )


class FrameAction(models.Model):
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="frame_actions",
        verbose_name=_("Player"),
    )
    frame = models.IntegerField(
        _("Frame"),
    )
    action = models.JSONField(
        _("Action"),
    )


class FrameState(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="frame_states",
        verbose_name=_("Game"),
    )
    frame = models.IntegerField(
        _("Frame"),
    )
    state = models.JSONField(
        _("State"),
    )
