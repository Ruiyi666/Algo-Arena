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
    name = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_mannual = models.BooleanField(default=False)


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def winner(self):
        return self.game_players.order_by("-score").first()


class GamePlayer(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="game_players",
        verbose_name=_("Game"),
    )
    strategy = models.ForeignKey(
        Strategy,
        on_delete=models.CASCADE,
        related_name="game_players",
        verbose_name=_("Strategy"),
    )
    score = models.IntegerField(default=0)


class FrameAction(models.Model):
    game_player = models.ForeignKey(
        GamePlayer,
        on_delete=models.CASCADE,
        related_name="frame_actions",
        verbose_name=_("Actions"),
    )
    frame = models.IntegerField(
        _("Frame"),
    )
    action = models.JSONField(
        _("Action"),
    )
