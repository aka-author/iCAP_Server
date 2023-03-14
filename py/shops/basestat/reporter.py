
import sys, os, pathlib

sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.parent.absolute()) + "/kernel"))

import shops


class ShopReporter(shops.Shop):

   def __init__(self, chief):

      super().__init__(chief)


def new_shop(chief):

   return ShopReporter(chief)




