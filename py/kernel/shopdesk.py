
import workers, apps, shops


class ShopDesk(workers.Work):

    def __init__(self, chief: apps.Application):

        super().__init__(chief)


    def get_shop(report_name: str) -> shops.Shop:

        import None