from bingads.v10.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v10.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V10

from .common import *
from bingads.internal.extensions import *
from .common import _BulkAdExtensionBase
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAdGroupAdExtensionAssociation


_ImageAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V10.create('ImageAdExtension'))


class BulkImageAdExtension(_BulkAdExtensionBase):
    """ Represents a image ad extension.

    This class exposes the :attr:`image_ad_extension` property that can be read and written
    as fields of the Image Ad Extension record in a bulk file.

    For more information, see Image Ad Extension at http://go.microsoft.com/fwlink/?LinkID=620277.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _ImageAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'ImageAdExtension'
            ))
        super(BulkImageAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def image_ad_extension(self):
        """ The image ad extension.

        see Image Ad Extension at http://go.microsoft.com/fwlink/?LinkID=620277.
        """

        return self._ad_extension

    @image_ad_extension.setter
    def image_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.DestinationUrl,
            field_to_csv=lambda c: bulk_optional_str(c.image_ad_extension.DestinationUrl),
            csv_to_field=lambda c, v: setattr(c.image_ad_extension, 'DestinationUrl', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.AltText,
            field_to_csv=lambda c: c.image_ad_extension.AlternativeText,
            csv_to_field=lambda c, v: setattr(c.image_ad_extension, 'AlternativeText', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.MediaIds,
            #field_to_csv=lambda c: bulk_str(c.image_ad_extension.ImageMediaIds),
            field_to_csv=lambda c: field_to_csv_MediaIds(c.image_ad_extension),
            #csv_to_field=lambda c, v: setattr(c.image_ad_extension, 'ImageMediaIds', int(v))
            csv_to_field=lambda c, v: csv_to_field_MediaIds(c.image_ad_extension, v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.image_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V10.create('ImageAdExtension')
        self.image_ad_extension.Type = 'ImageAdExtension'
        super(BulkImageAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkImageAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.image_ad_extension, 'image_ad_extension')
        super(BulkImageAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkImageAdExtension._MAPPINGS)


class BulkCampaignImageAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents an campaign level image ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Image Ad Extension record in a bulk file.

    For more information, see Campaign Image Ad Extension at http://go.microsoft.com/fwlink/?LinkID=620276.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass


class BulkAdGroupImageAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level image ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Image Ad Extension record in a bulk file.

    For more information, see Ad Group Image Ad Extension at http://go.microsoft.com/fwlink/?LinkID=620261.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
