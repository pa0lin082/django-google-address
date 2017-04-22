AddressComponentType
====================

This model should not be created manually. It is automatically created while saving an Address model. It can be used for advanced filtering. Read more at :doc:`Filtering <../filtering>`.


Fields
~~~~~~
::

    class AddressComponentType(models.Model):
      name = models.CharField(max_length=100)
