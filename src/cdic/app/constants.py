# coding: utf-8


class SourceType(object):

    LOCAL_TEXT = "local_text"
    GIT_URL = "git_url"

    @classmethod
    def get_all_options(cls):
        return [cls.LOCAL_TEXT, cls.GIT_URL]


class EventType(object):

    BUILD_REQUESTED = "build_requested"
    WEBHOOK_CALLED = "webhook_called"

