try:
    from safedelete.models import safedelete_mixin_factory
    from safedelete.utils import DELETED_VISIBLE_BY_PK, SOFT_DELETE

    SafeDeleteMixin = safedelete_mixin_factory(policy=SOFT_DELETE, visibility=DELETED_VISIBLE_BY_PK)
except ImportError:
    from safedelete.models import SafeDeleteMixin as SafeDeleteMixinBase, SOFT_DELETE
    from safedelete.config import DELETED_VISIBLE_BY_FIELD

    class SafeDeleteMixin(SafeDeleteMixinBase):
        _safedelete_policy = SOFT_DELETE
    SafeDeleteMixin.objects._safedelete_visibility = DELETED_VISIBLE_BY_FIELD
