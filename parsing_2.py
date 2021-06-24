import pandas as pd
import parsing

class KinavoBot:
    help_text = '''
    /categories выдать названия всех категорий
    /categories_name {название категории} выдать товары этой категории
    /product {название продукта} выдать информацию о данном товаре
    '''
    __sales = pd.read_csv('kinavo.csv')
    categoriesset = set(__sales.category)
    productset = set(__sales.title)
   
     

    def category_from_kinavo(self, args):
        if len(args) <= 0:
            return '\n'.join(self.categoriesset)
        else:
            if args not in self.categoriesset:
                return f'Категории {args} нет в списке'
            else:   
                z = self.__sales[self.__sales.category == args]
                cat = z[['title', 'link']].to_string()
                return cat

    def product_from_kinavo(self, args):

        if len(args) <= 0:
            return '\n'.join(self.productset)
        else:
            if args not in self.productset:
                return f'Продукта {args} нет в категории '
            else:   
                z = self.__sales[self.__sales.title == args]
                cat = z[['category','title', 'link']].to_string()
                return cat