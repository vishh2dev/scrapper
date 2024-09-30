
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AmazonScraperPipeline:
    def process_item(self, item, spider):
        adaptor = ItemAdapter(item)
        fields = adaptor.field_names()

        for field in fields:
            if field == "name":
                value = adaptor.get(field)
                if value:
                    # Strip leading/trailing whitespace if the value is not None
                    adaptor[field] = value.strip()
                else:
                    # Assign an empty string if the value is None
                    adaptor[field] = ""
                    
        return item
