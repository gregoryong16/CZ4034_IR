# from haystack import indexes
# from indexing_project.models import Products

# class ProductsIndex(indexes.SearchIndex, indexes.Indexable):
# 	text = indexes.CharField(document=True, use_template=True)
# 	name = indexes.CharField(model_attr='name')
# 	rating_star = indexes.DecimalField(model_attr= "rating_star", faceted=True)
	
# 	def get_model(self):
# 		return Products

# 	def index_queryset(self,using=None):
# 		return self.get_model().objects.all()

from django.contrib.auth.models import User
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from indexing_project.models import Products


@registry.register_document
class ProductsDocument(Document):
    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Products
        fields = [
            "shop_id",
			"item_id",
			"product_url", 
			"product_name",
			"product_price",
			"description",
			"rating",
			"image_url",
			"shop_location",
			"shop_ratings",
			"shop_name"
        ]

