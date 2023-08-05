import attr


@attr.s(repr=False)
class CSPObject:
    default_src = attr.ib(convert=frozenset, default=frozenset())

    # The following fall back to default_src
    child_src = attr.ib(convert=frozenset, default=frozenset())
    connect_src = attr.ib(convert=frozenset, default=frozenset())
    font_src = attr.ib(convert=frozenset, default=frozenset())
    img_src = attr.ib(convert=frozenset, default=frozenset())
    manifest_src = attr.ib(convert=frozenset, default=frozenset())
    media_src = attr.ib(convert=frozenset, default=frozenset())
    object_src = attr.ib(convert=frozenset, default=frozenset())
    script_src = attr.ib(convert=frozenset, default=frozenset())
    style_src = attr.ib(convert=frozenset, default=frozenset())

    # The following fall back to child_src (then default_src)
    frame_src = attr.ib(convert=frozenset, default=frozenset())
    worker_src = attr.ib(convert=frozenset, default=frozenset())

    # The following fail open (don't fall back to default_src)
    base_uri = attr.ib(convert=frozenset, default=frozenset())
    form_action = attr.ib(convert=frozenset, default=frozenset())
    frame_ancestors = attr.ib(convert=frozenset, default=frozenset())

    # The following are not source lists (and so cannot fall back to
    # default_src)
    block_all_mixed_content = attr.ib(convert=bool, default=False)
    plugin_types = attr.ib(convert=frozenset, default=frozenset())
    referrer = attr.ib(default=None)
    report_uri = attr.ib(default=None)
    require_sri_for = attr.ib(convert=frozenset, default=frozenset())
    # TODO: proper handling of sandbox
    sandbox = attr.ib(convert=bool, default=False)
    sandbox_allow = attr.ib(convert=frozenset, default=frozenset())
    upgrade_insecure_requests = attr.ib(convert=bool, default=False)

    def __repr__(self):
        rv = []
        for k, v in attr.asdict(self).items():
            if not v:
                continue

            if isinstance(v, bool):
                rv.append("{}=True".format(k))

            elif isinstance(v, frozenset):
                rv.append("{}={{{}}}".format(
                    k, ', '.join(repr(vi) for vi in v)))

            else:
                rv.append("{}={}".format(k, repr(v)))
        return 'CSPObject({})'.format(', '.join(rv))

    def __str__(self):
        rv = []
        for k, v in attr.asdict(self).items():
            key = k.replace('_', '-')

            if not v:
                continue

            if isinstance(v, bool):
                rv.append(key)

            elif isinstance(v, frozenset):
                rv.append("{} {}".format(key, ' '.join(v)))

            else:
                rv.append("{} {}".format(key, v))
        return '; '.join(rv)

    def _fallback_union(self, other, the_attr, child_src=False):
        self_v = getattr(self, the_attr)
        other_v = getattr(other, the_attr)
        if not (self_v or other_v):
            return frozenset()
        self_fb = self_v or (child_src and self.child_src) or self.default_src
        other_fb = other_v or (
            child_src and other.child_src) or other.default_src
        return self_fb.union(other_fb)

    def union(self, other):
        if self.referrer and other.referrer:
            raise ValueError("Cannot union two CSPObjects that both have the "
                             "(deprecated) referrer directive set")
        if self.report_uri and other.report_uri and self.report_uri != other.report_uri:
            raise ValueError("Cannot union two CSPObjects that both have the "
                             "report-uri directive set to different values")

        return CSPObject(
            default_src=self.default_src.union(other.default_src),
            child_src=self._fallback_union(other, 'child_src'),
            connect_src=self._fallback_union(other, 'connect_src'),
            font_src=self._fallback_union(other, 'font_src'),
            img_src=self._fallback_union(other, 'img_src'),
            manifest_src=self._fallback_union(other, 'manifest_src'),
            media_src=self._fallback_union(other, 'media_src'),
            object_src=self._fallback_union(other, 'object_src'),
            script_src=self._fallback_union(other, 'script_src'),
            style_src=self._fallback_union(other, 'style_src'),
            frame_src=self._fallback_union(other, 'frame_src', child_src=True),
            worker_src=self._fallback_union(
                other, 'worker_src', child_src=True),
            base_uri=self.base_uri.union(other.base_uri),
            form_action=self.form_action.union(other.form_action),
            frame_ancestors=self.frame_ancestors.union(other.frame_ancestors),
            block_all_mixed_content=self.block_all_mixed_content and other.block_all_mixed_content,
            plugin_types=self.plugin_types.union(other.plugin_types),
            referrer=self.referrer or other.referrer,
            sandbox=self.sandbox and other.sandbox,
            sandbox_allow=self.sandbox_allow.union(other.sandbox_allow),
            upgrade_insecure_requests=self.upgrade_insecure_requests and other.upgrade_insecure_requests,
        )

    def __and__(self, other):
        if not isinstance(other, CSPObject):
            raise TypeError("Expected CSPObject, got {}".format(type(other)))
        return self.union(other)
