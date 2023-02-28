from haystack import indexes
from indexing_project.models import Products

class ProductsIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	name = indexes.CharField(model_attr='name', faceted=True)
	
	def get_model(self):
		return Products

	def index_queryset(self,using=None):
		return self.get_model().objects.all()