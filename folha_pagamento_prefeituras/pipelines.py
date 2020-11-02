# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import ssl
import io

import tabula
from scrapy.exceptions import DropItem


ssl._create_default_https_context = ssl._create_unverified_context


class AracajuPipeline:
    def process_item(self, item, spider):
        empresa = item.get('empresa', None)

        if empresa:
            folha = item.get('folha').split("location.href='")[-1].split("';")[0]
            tabula.convert_into(folha, f"outputs/{empresa.replace('Aracaju ', '')}.csv",
                                output_format='csv', stream=True, pages='all')

            return item
        else:
            raise DropItem(f'Item inexistente')
