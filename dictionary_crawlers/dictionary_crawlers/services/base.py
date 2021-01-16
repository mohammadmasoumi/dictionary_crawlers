__all__ = ('BaseService',)


class BaseService:
    @staticmethod
    def _join(iterables: list, strip=True):
        """

        :param iterables: list
        :return:
        """
        word = ''.join(filter(lambda x: not x.startswith('\\'), iterables))
        return word.strip() if strip else word

    @staticmethod
    def _first(iterables: list):
        """

        :param iterables:
        :return:
        """
        return iterables[0] if iterables else None

    @staticmethod
    def _join_url(base_url, href: list):
        """

        :param base_url:
        :param href:
        :return:
        """
        return ''.join([base_url, *href])
