from disnake.ext import commands

from .context import Context
from .constants import StaffRoles

__all__ = (
    'is_owner',
    'is_admin',
    'is_mod',
)


def _is_owner(ctx: Context, *, owner_only: bool = False):
    if owner_only is True:
        if ctx.author.id == 1102653969483976725:
            return True
        raise commands.NotOwner

    if ctx.author.id == 1102653969483976725:
        return True
    elif StaffRoles.owner in (role.id for role in ctx.author.roles):
        return True
    return False


def is_owner(*, owner_only: bool = False):
    """
    A special check for checking if the author has the owner role.

    If ``owner_only`` is set to `True` it will only check if the owner is the bot owner.
    """

    async def pred(ctx: Context):
        return _is_owner(ctx, owner_only=owner_only)
    return commands.check(pred)


def _is_admin_or_owner(ctx):
    res = _is_owner(ctx)
    if res is False:
        if StaffRoles.admin in (role.id for role in ctx.author.roles):
            return True
    else:
        return res
    return False


def is_admin():
    """A special check for checking if the author is an admin."""

    async def pred(ctx: Context):
        return _is_admin_or_owner(ctx)
    return commands.check(pred)


def is_mod():
    """A special check for checking if the author is a moderator."""

    async def pred(ctx: Context):
        res = _is_admin_or_owner(ctx)
        if res is False:
            if StaffRoles.moderator in (role.id for role in ctx.author.roles):
                return True
        else:
            return res
        return False
    return commands.check(pred)
