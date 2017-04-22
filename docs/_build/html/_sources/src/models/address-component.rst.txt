AddressComponent
================

This model should not be created manually. It is automatically created while saving an Address model. It can be used for advanced filtering. Read more at :doc:`Filtering <../filtering>`.


Fields
~~~~~~
::

    class AddressComponent(models.Model):
      long_name = models.CharField(max_length=400)
      short_name = models.CharField(max_length=400)
      types = models.ManyToManyField(AddressComponentType)
