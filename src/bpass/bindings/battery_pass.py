"""Generated from Catena-X SAMM aspect models. Do not edit.

Aspect:    urn:samm:io.catenax.battery.battery_pass:6.1.0#BatteryPass

Generated from these pinned models:
    urn:samm:io.catenax.battery.battery_pass:6.1.0
    urn:samm:io.catenax.generic.digital_product_passport:5.0.0
    urn:samm:io.catenax.batch:3.0.0
    urn:samm:io.catenax.part_type_information:1.0.0
    urn:samm:io.catenax.serial_part:3.0.0
    urn:samm:io.catenax.shared.business_partner_number:2.0.0
    urn:samm:io.catenax.shared.part_classification:1.0.0
    urn:samm:io.catenax.shared.quantity:2.0.0
    urn:samm:io.catenax.shared.uuid:2.0.0

Regenerate with:

    python -m bpass.samm.generate

Every field carries its semantic URN in json_schema_extra, and its payload
name as an alias. Dump with by_alias=True to reproduce a Catena-X payload.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SerialPartKeyValueList(BaseModel):
    """Key Value List.

    A list of key value pairs for local identifiers, which are composed of a key and a
    corresponding value.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    key: str = Field(
        alias='key',
        description=(
            'The key of a local identifier. Constrained upstream by KeyRegularExpression; '
            'not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.serial_part:3.0.0#key'},
    )

    value: str = Field(
        alias='value',
        description='The value of an identifier.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.serial_part:3.0.0#value'},
    )


class BatchKeyValueList(BaseModel):
    """Key Value List.

    A list of key value pairs for local identifiers, which are composed of a key and a
    corresponding value.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    key: str = Field(
        alias='key',
        description=(
            'The key of a local identifier. Constrained upstream by KeyRegularExpression; '
            'not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.batch:3.0.0#key'},
    )

    value: str = Field(
        alias='value',
        description='The value of an identifier.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.batch:3.0.0#value'},
    )


class PartTypeEntity(BaseModel):
    """Part Type Entity.

    Entity for the part type with manufacturer id and name.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    manufacturer_part_id: str = Field(
        alias='manufacturerPartId',
        description=(
            'Part ID as assigned by the manufacturer of the part. The part ID identifies '
            'the part in the manufacturer`s dataspace. The part ID references a specific '
            'version of a part. The version number must be included in the part ID if it '
            'is available. The part ID does not reference a specific instance of a part '
            'and must not be confused with the serial number.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.part_type_information:1.0.0#manufacturerPartId'},
    )

    name_at_manufacturer: str = Field(
        alias='nameAtManufacturer',
        description='Name of the part as assigned by the manufacturer.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.part_type_information:1.0.0#nameAtManufacturer'},
    )


class CodeEntity(BaseModel):
    """Code Entity.

    Code entity with code key and value.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    code_key: str = Field(
        alias='key',
        description=(
            'The code key for the identification of the product. Examples are GTIN, hash, '
            'DID, ISBN, TARIC. This attribute is mentioned in the ESPR proposal from '
            'March 30th, 2022 ANNEX III: (b) the unique product identifier at the level '
            'indicated in the applicable delegated act adopted pursuant to Article 4; (c) '
            'the Global Trade Identification Number as provided for in standard ISO/IEC '
            '15459-6 or equivalent of products or their parts; (d) relevant commodity '
            'codes, such as a TARIC code as defined in Council Regulation (EEC) No '
            '2658/87.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#codeKey'},
    )

    code_value: str = Field(
        alias='value',
        description=(
            'The code value for the identification of the product in regard to the chosen '
            'code name.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#codeValue'},
    )


class DataCarrierEntity(BaseModel):
    """Data Carrier Entity.

    Data Carrier Entity with type and layout of the data carrier.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    carrier_type: str = Field(
        alias='carrierType',
        description=(
            'The type of data carrier such as a QR code on the product. This attribute is '
            'mentioned in the ESPR proposal from March 30th, 2022 Article 8: (2) (b) the '
            'types of data carrier to be used.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#carrierType'},
    )

    carrier_layout: str = Field(
        alias='carrierLayout',
        description=(
            'The positioning of data carrier on the product. This attribute is mentioned '
            'in the ESPR proposal from March 30th, 2022 Article 8: (2) (c) the layout in '
            'which the data carrier shall be presented and its positioning.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#carrierLayout'},
    )


class ClassificationEntity(BaseModel):
    """ClassificationEntity.

    Encapsulates data related to the classification of the part.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    classification_standard: str = Field(
        alias='classificationStandard',
        description='Identified classification standards that align to the Catena-X needs.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.shared.part_classification:1.0.0#classificationStandard'},
    )

    classification_id: str = Field(
        alias='classificationID',
        description=(
            'The classification ID of the part type according to the corresponding '
            'standard definition mentioned in the key value pair.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.shared.part_classification:1.0.0#classificationID'},
    )

    classification_description: str | None = Field(
        alias='classificationDescription',
        default=None,
        description='Optional property describing the classification standard.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.shared.part_classification:1.0.0#classificationDescription'},
    )


class DigitalProductPassportIdentificationEntity(BaseModel):
    """Identification Entity.

    Entity with identification information of the product with part type information,
    local identifiers, other codes and the data carrier.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    serial_information: list[SerialPartKeyValueList] | None = Field(
        alias='serial',
        default=None,
        description=(
            'Identifier for a serial part if available. This is mentioned in the ESPR '
            "provisional agreement from January 9th, 2024 Recital (27): [...] an 'item' "
            'usually means a single unit of a model.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#serialInformation'},
    )

    batch_information: list[BatchKeyValueList] | None = Field(
        alias='batch',
        default=None,
        description=(
            'Identifier for a batch part if available. Identifier for a serial part if '
            'available. This is mentioned in the ESPR provisional agreement from January '
            "9th, 2024 Recital (27): [...] a 'batch' usually means a subset of a specific "
            'model composed of all products produced in a specific manufacturing plant at '
            'a specific moment in time [...].'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#batchInformation'},
    )

    part_type_information: PartTypeEntity = Field(
        alias='type',
        description=(
            'Identifier on the level of a part model or type. Identifier for a serial '
            'part if available. This is mentioned in the ESPR provisional agreement from '
            "January 9th, 2024 Recital (27): [...] A 'model' usually means a version of a "
            'product of which all units share the same technical characteristics relevant '
            'for the ecodesign requirements and the same model identifier [...].'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#partTypeInformation'},
    )

    codes: list[CodeEntity] = Field(
        alias='codes',
        description='Codes for identification.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#codes'},
    )

    data_carrier: DataCarrierEntity = Field(
        alias='dataCarrier',
        description=(
            'The type and layout of the data carrier on the product. These are mentioned '
            'in the ESPR proposal from March 30th, 2022 Article 8: (b) the types of data '
            'carrier to be used; (c) the layout in which the data carrier shall be '
            "presented and its positioning; Article 2 defines: (30) 'data carrier' means "
            'a linear bar code symbol, a two-dimensional symbol or other automatic '
            'identification data capture medium that can be read by a device.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#dataCarrier'},
    )

    part_classification: list[ClassificationEntity] = Field(
        alias='classification',
        description='Property describing the classification of a part.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.shared.part_classification:1.0.0#partClassification'},
    )


class BatteryPassIdentificationEntity(BaseModel):
    """Identification Entity.

    Entity for the identification of the battery.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    battery_category: Literal['SLI', 'LMT', 'EV', 'industrial', 'portable', 'incorporated'] = Field(
        alias='category',
        description=(
            'The battery category, which can be a portable battery; starting, lighting '
            'and ignition battery (SLI); light means of transport battery (LMT); electric '
            'vehicle battery (EV), industrial battery and incorporated battery. This '
            'attribute is mentioned in the Battery regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (1) (a) and refers to ANNEX VI Part A: 2. the battery category '
            'and information identifying the battery in accordance with Article 38(6).'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#batteryCategory'},
    )

    id_dmc: str = Field(
        alias='idDmc',
        description=(
            'The unique identifier of the product, when it is placed on the market. '
            'Through this identifier a web link can be accessed. This attribute is '
            'mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Article '
            '77: 3. The battery passport shall be accessible through the QR code referred '
            'to in Article 13(6) which links to a unique identifier that the economic '
            'operator placing the battery on the market shall attribute to it. The QR '
            'code and the unique identifier shall comply with the ISO/IEC standards '
            '15459-1:2014, 15459-2:2015, 15459-3:2014, 15459-4:2014, 15459-5:2014 and '
            '15459-6:2014 or their equivalent. Defined is the QR code in Article 3: (24) '
            '"QR code" means a machine-readable matrix code that links to information as '
            'required by this Regulation. (66) "unique identifier" means a unique string '
            'of characters for the identification of batteries that also enables a web '
            'link to the battery passport.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#idDmc'},
    )

    battery_chemistry: str = Field(
        alias='chemistry',
        description=(
            'Battery chemistry refers to the specific chemical composition and reactions '
            'that occur within a battery to produce and store electrical energy. The '
            'chemistry has to be stated as detailed as possible for example: the Nickel '
            "Cobalt Manganese battery 'NCM'. This attribute is mentioned in the Battery "
            'regulation 2023/1542 from 12 July 2023 in Annex XIII (1) (a) and refers to '
            'ANNEX VI Part A: 7. the chemestry.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#batteryChemistry'},
    )

    identification: DigitalProductPassportIdentificationEntity = Field(
        alias='identification',
        description=(
            'Identification information of the product, especially identifiers and codes. '
            'These are mentioned in the ESPR provisional agreement from January 9th, 2024 '
            'ANNEX III: (b) the unique product identifier at the level indicated in the '
            'applicable delegated act adopted pursuant to Article 4. Additionally in '
            'Article 9 regarding general requirements for the product passport is stated '
            'that: A product passport shall meet the following conditions: (a) it shall '
            'be connected through a data carrier to a persistent unique product '
            'identifier; (e) the information included in the product passport shall refer '
            'to the product model, batch, or item as specified in the delegated act '
            "adopted pursuant to Article 4. Article 2 Definitions: (31) 'unique product "
            "identifier' means a unique string of characters for the identification of "
            'products that also enables a web link to the product passport; Recital (27): '
            "A 'model' usually means a version of a product of which all units share the "
            'same technical characteristics relevant for the ecodesign requirements and '
            "the same model identifier, a 'batch' usually means a subset of a specific "
            'model composed of all products produced in a specific manufacturing plant at '
            "a specific moment in time and an 'item' usually means a single unit of a "
            'model.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#identification'},
    )


class FacilityEntity(BaseModel):
    """Facility Entity.

    The entity for a facility with the BPNA identifier.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    facility: str = Field(
        alias='facility',
        description=(
            'The identifier used for a location. This attribute is mentioned in the ESPR '
            'provisional agreement from January 9th 2024 Annex III: (i) unique facility '
            "identifiers; Article 2 Definitions: (33) 'unique facility identifier' means "
            'a unique string of characters for the identification of locations or '
            'buildings involved in the value chain of a product or used by actors '
            'involved in the value chain of a product. Constrained upstream by '
            'BpnaRegularExpression; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#facility'},
    )


class ManufacturerEntity(BaseModel):
    """Manufacturer Entity.

    Manufacturing Entity with the identification of the main manufacturer and the
    facility location as well as the manufacturing date.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    facility_identification: list[FacilityEntity] = Field(
        alias='facility',
        description=(
            'The identifier used for a location. In the CATENA-X use case, the BPNA can '
            'be stated. This attribute is mentioned in the ESPR provisional agreement '
            'from January 9th 2024 Annex III: (i) unique facility identifiers; Article 2 '
            "Definitions: (33) 'unique facility identifier' means a unique string of "
            'characters for the identification of locations or buildings involved in the '
            'value chain of a product or used by actors involved in the value chain of a '
            'product.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#facilityIdentification'},
    )

    manufacturer_identification: str = Field(
        alias='manufacturer',
        description=(
            'The main manufacturer, if different from the passport owner, represented by '
            'an identification number. In the Catena-X use case, the BPNL can be stated. '
            'This attribute is mentioned in the ESPR provisional agreement from January '
            '9th 2024 Annex III: (h) unique operator identifiers other than that of the '
            'manufacturer; (k) the name, contact details and unique operator identifier '
            'code of the economic operator established in the Union responsible for '
            'carrying out the tasks set out in Article 4 of Regulation (EU) 2019/1020, or '
            'Article 15 of Regulation (EU) [.../...] on general product safety, or '
            'similar tasks pursuant to other EU legislation applicable to the product. '
            'Constrained upstream by BpnlRegularExpression; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#manufacturerIdentification'},
    )

    manufacturing_date: str | None = Field(
        alias='manufacturingDate',
        default=None,
        description=(
            'The timestamp in the format (yyyy-mm-dd) of the manufacturing date as the '
            'final step in production process (e.g. final quality check, '
            'ready-for-shipment event). Constrained upstream by DateConstraint; not '
            'enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#manufacturingDate'},
    )


class OperationEntity(BaseModel):
    """Operation Entity.

    Entity which includes details such as the manufacturer's identification and the date
    of production. The date of the putting into service is optional.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    into_service_date: str | None = Field(
        alias='intoServiceDate',
        default=None,
        description=(
            'Putting into service is the transition from a state of readiness to actual '
            'use or operation. The date should be formatted as yyyy-mm-dd. This attribute '
            'is mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'VII Part B: 1.the date of manufacture of the battery and, where appropriate, '
            'the date of putting into service; Defined is "putting into service" in '
            'Article 3: (18) "putting into service" means the first use, for its intended '
            'purpose, in the Union, of a battery, without having been previously placed '
            'on the market. Constrained upstream by DateConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#intoServiceDate'},
    )

    manufacturer: ManufacturerEntity = Field(
        alias='manufacturer',
        description=(
            'Manufacturing information of the product. In the CATENA-X use case, the BPNL '
            'and BPNA can be stated. These attributes are mentioned in the ESPR '
            'provisional agreement from January 9th 2024 Annex III: (h) unique operator '
            'identifiers other than that of the manufacturer; (k) the name, contact '
            'details and unique operator identifier code of the economic operator '
            'established in the Union responsible for carrying out the tasks set out in '
            'Article 4 of Regulation (EU) 2019/1020, or Article 15 of Regulation (EU) '
            '[.../...] on general product safety, or similar tasks pursuant to other EU '
            'legislation applicable to the product.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#manufacturer'},
    )


class WarrantyEntity(BaseModel):
    """Warranty Entity.

    Entity for the warranty with a value and unit.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    life_value: int = Field(
        alias='lifeValue',
        description='The value as an integer for the respective lifespan.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#lifeValue'},
    )

    life_unit: Literal['unit:day', 'unit:month', 'unit:year', 'unit:cycle', 'unit:runningOrOperatingHour'] = Field(
        alias='lifeUnit',
        description=(
            'The unit of the respective lifespan expressed through the possible units '
            'day, month, cycle, year and runningOrOperatingHour.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#lifeUnit'},
    )


class LinearEntity(BaseModel):
    """Linear Entity.

    Entity for linear measurements of an item with an unit and value.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    quantity_value: float = Field(
        alias='value',
        description='The quantity value associated with the unit.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.shared.quantity:2.0.0#quantityValue'},
    )

    linear_unit: Literal['unit:millimetre', 'unit:centimetre', 'unit:metre', 'unit:kilometre', 'unit:inch', 'unit:foot', 'unit:yard'] = Field(
        alias='unit',
        description='The unit of a linear attribute.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.shared.quantity:2.0.0#linearUnit'},
    )


class MassEntity(BaseModel):
    """Mass Entity.

    Entity for mass measurements of an item with an unit and value.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    quantity_value: float = Field(
        alias='value',
        description='The quantity value associated with the unit.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.shared.quantity:2.0.0#quantityValue'},
    )

    mass_unit: Literal['unit:gram', 'unit:kilogram', 'unit:tonneMetricTon', 'unit:tonUsOrShortTonUkorus', 'unit:ounceAvoirdupois', 'unit:pound'] = Field(
        alias='unit',
        description='The unit of a mass related attribute.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.shared.quantity:2.0.0#massUnit'},
    )


class PhysicalDimensionEntity(BaseModel):
    """Physical Dimension Entity.

    Entity for the physical dimension with weight, volume and other optional values.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    height: LinearEntity | None = Field(
        alias='height',
        default=None,
        description=(
            'The height of the item measured in a specific linear unit which can be '
            'declared in the corresponding unit attribute.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#height'},
    )

    length: LinearEntity | None = Field(
        alias='length',
        default=None,
        description=(
            'The length of the item measured in a specific linear unit which can be '
            'declared in the corresponding unit attribute.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#length'},
    )

    width: LinearEntity | None = Field(
        alias='width',
        default=None,
        description=(
            'The width of the item measured in a specific linear unit which can be '
            'declared in the corresponding unit attribute.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#width'},
    )

    weight: MassEntity = Field(
        alias='weight',
        description=(
            'Weight of the product measured in a specific mass unit which can be declared '
            'in the corresponding unit attribute. This attribute is mentioned in the ESPR '
            'proposal from March 30th, 2022 Article 7: (2) (b) (i) information on the '
            'performance of the product in relation to the product parameters referred to '
            'in Annex I; Annex I (i) weight and volume of the product [...].'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#weight'},
    )


class CharacteristicsEntity(BaseModel):
    """Characteristics Entity.

    Entity for the product characteristics.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    warranty: WarrantyEntity = Field(
        alias='warranty',
        description=(
            'The warranty of the battery. This attribute is mentioned in the Battery '
            'regulation 2023/1542 from 12 July 2023 in ANNEX XIII: (m) period for which '
            'the commercial warranty for the calendar life applies.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#warranty'},
    )

    physical_dimension: PhysicalDimensionEntity = Field(
        alias='physicalDimension',
        description=(
            'The weight of the battery. For calculation of the energy density, the volume '
            'is also needed. The energy density of a battery is measured in watt-hours '
            'per kilogram (Wh/kg) and watt-hours per liter (Wh/L). These measures '
            'indicate how much energy a battery can store relative to its weight and '
            'volume, respectively. Other measurements are optional.These are mentioned in '
            'the Battery regulation 2023/1542 from 12 July 2023 in Annex XIII (1)(a) and '
            'refers to Annex VI Part A: 5. the weight.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#physicalDimension'},
    )


class DocumentationEntity(BaseModel):
    """Documentation Entity.

    Entity for a document with a header, type and content.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    content: str = Field(
        alias='content',
        description='The content of the document e.g a link.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#content'},
    )

    content_type: str = Field(
        alias='contentType',
        description=(
            'The type of content which can be expected in the "content" property. '
            'Examples are a link, restricted link, pdf, excel, etc.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#contentType'},
    )

    header: str = Field(
        alias='header',
        description=(
            'The header as a short description of the document with a maximum of 100 '
            'characters. Constrained upstream by HeaderConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#header'},
    )


class SustainabilityDocumentEntity(BaseModel):
    """Sustainability Document Entity.

    Sustainability Document Entity which encapsulates relevant information in the form
    of documents.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    separate_collection: list[DocumentationEntity] = Field(
        alias='separateCollection',
        description=(
            'Documentation about separate collection of batteries involve information on '
            'how to properly collect, handle, and recycle batteries to ensure '
            'environmental sustainability and compliance with regulations. This attribute '
            'is mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1) (s), refers to Article 74: 1. In addition to the information '
            'referred to in Article 8a(2) of Directive 2008/98/EC, producers or, where '
            'appointed in accordance with Article 57(1), producer responsibility '
            'organisations shall make available to end-users and distributors the '
            'following information regarding the prevention and management of waste '
            'batteries with regard to the categories of batteries that they supply within '
            'the territory of a Member State: (a) the role of end-users in contributing '
            'to waste prevention, including by information on good practices and '
            'recommendations concerning the use of batteries aimed at extending their use '
            'phase and the possibilities of re-use, preparation for re-use, preparation '
            'for repurposing, repurposing and remanufacturing; (b) the role of end-users '
            'in contributing to the separate collection of waste batteries in accordance '
            'with their obligations under Article 64 to allow their treatment; (c) the '
            'separate collection, take-back and collection points, preparation for '
            're-use, preparation for repurposing and treatment available for waste '
            'batteries; (d) the necessary safety instructions to handle waste batteries, '
            'including in relation to the risks associated with, and the handling of, '
            'batteries containing lithium; (e) the meaning of the labels and symbols on '
            'batteries in accordance with Article 13 or printed on their packaging or in '
            'the documents accompanying batteries; and (f) the impact of substances, in '
            'particular hazardous substances, present in batteries on the environment and '
            'on human health or the safety of persons, including the impact due to '
            'inappropriate discarding of waste batteries, such as littering or discarding '
            'as unsorted municipal waste.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#separateCollection'},
    )

    waste_prevention: list[DocumentationEntity] = Field(
        alias='wastePrevention',
        description=(
            'Documentation about waste prevention for batteries which include guidelines, '
            'recommendations, and information on minimizing the environmental impact '
            'associated with the use and disposal of batteries. This attribute is '
            'mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1) (s), refers to Article 74 (1) which call Article 8a of Directive '
            '2008/98/EC: 2. Member States shall take the necessary measures to ensure '
            'that the waste holders targeted by the extended producer responsibility '
            'schemes established in accordance with Article 8 (1), are informed about '
            'waste prevention measures, centres for re-use and preparing for re-use, '
            'take-back and collection systems, and the prevention of littering. Member '
            'States shall also take measures to create incentives for the waste holders '
            'to assume their responsibility to deliver their waste into the separate '
            'collection systems in place, notably, where appropriate, through economic '
            'incentives or regulations.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#wastePrevention'},
    )

    eu_taxonomy_disclosure_statement: list[DocumentationEntity] | None = Field(
        alias='euTaxonomyDisclosureStatement',
        default=None,
        description=(
            'Optional disclosure regarding the EU taxonomy, with the choice to '
            'voluntarily provide the EU Taxonomy disclosure through the battery passport.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#euTaxonomyDisclosureStatement'},
    )

    sustainability_report: list[DocumentationEntity] | None = Field(
        alias='sustainabilityReport',
        default=None,
        description=(
            'Voluntarily making the Sustainability Report available via the battery '
            'passport. A report containing the information concerning the sustainability '
            'in form of a document.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#sustainabilityReport'},
    )


class FootprintEntity(BaseModel):
    """Footprint Entity.

    Footprint Entity for the carbon and environmental footprint with the total value,
    unit, impact category type, lifecycle, rulebook, declaration, performance class and
    the facility.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    footprint_value: float = Field(
        alias='value',
        description=(
            'The value of the footprint of the product. This attribute is mentioned in '
            'the ESPR proposal from March 30th, 2022 Annex I: (l) the environmental '
            'footprint of the product, expressed as a quantification, in accordance with '
            "the applicable delegated act, of a product's life cycle environmental "
            'impacts, whether in relation to one or more environmental impact categories '
            'or an aggregated set of impact categories; (m) the carbon footprint of the '
            'product; (ma) the material footprint of the product. Constrained upstream by '
            'PositiveRangeConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#footprintValue'},
    )

    footprint_rulebook: list[DocumentationEntity] = Field(
        alias='rulebook',
        description='The applied rulebook for the environmental footprint of the product.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#footprintRulebook'},
    )

    footprint_lifecycle: str = Field(
        alias='lifecycle',
        description=(
            'The lifecycle stage, to which the environmental footprint corresponds. These '
            'could be for example "raw material acquisition and pre-processing", "main '
            'product production", "distribution" or "end of life and recycling".'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#footprintLifecycle'},
    )

    footprint_unit: str = Field(
        alias='unit',
        description=(
            'The unit of measurement of the environmental impact category. For each '
            'impact category a specific unit is used. If an aggregation is used, utilize '
            'the normalization and weighting methods used in the referenced rulebook.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#footprintUnit'},
    )

    footprint_type: Literal['Climate Change Total', 'Climate Change Fossil', 'Climate Change Biogenic Removals and Emissions', 'Climate Change Land Use and Land Use Change', 'Ozone Depletion', 'Acidification', 'Eutrophication Aquatic Freshwater', 'Eutrophication Fresh Marine', 'Eutrophication Terrestrial', 'Photochemical Ozone Formation', 'Abiotic Depletion- Minerals and Metals', 'Fossil Fuels', 'Water Use', 'Particulate Matter Emissions', 'Ionizing Radiation, Human Health', 'Eco-Toxicity', 'Human Toxicity, Cancer Effects', 'Human Toxicity, Non-Cancer Effects', 'Land Use Related Impacts/Soil Quality'] = Field(
        alias='type',
        description=(
            'The type of the environmental footprint of the product. This could be one of '
            'the environmental impact categories. This attribute is mentioned in the ESPR '
            'provisional agreement from January 9th 2024 Article 7: (2)(b)(i) information '
            'on the performance of the product in relation to one or more of the product '
            'parameters referred to in Annex I, including a scoring of reparability or '
            'durability, carbon footprint or environmental footprint; Annex I: (l) the '
            'environmental footprint of the product, expressed as a quantification, in '
            "accordance with the applicable delegated act, of a product's life cycle "
            'environmental impacts, whether in relation to one or more environmental '
            'impact categories or an aggregated set of impact categories. (m) the carbon '
            'footprint of the product; (ma) the material footprint of the product.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#footprintType'},
    )

    performance_class: str | None = Field(
        alias='performanceClass',
        default=None,
        description='The performance classification of the footprint.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#performanceClass'},
    )

    manufacturing_plant: list[FacilityEntity] = Field(
        alias='manufacturingPlant',
        description='The manufacturing plant of the footprint in the specific lifecycle phase.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#manufacturingPlant'},
    )

    declaration: list[DocumentationEntity] = Field(
        alias='declaration',
        description='The footprint declaration in the format of a link',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#declaration'},
    )


class SustainabilityEntity(BaseModel):
    """Sustainability Entity.

    Entity which includes information on the carbon footprint, sustainability documents
    and the status of the battery.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    sustainability_documents: SustainabilityDocumentEntity = Field(
        alias='documents',
        description='Sustainability documents of the battery.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#sustainabilityDocuments'},
    )

    carbon_footprint: list[FootprintEntity] = Field(
        alias='carbonFootprint',
        description=(
            'The carbon footprint of the battery calculated as kg of carbon dioxide '
            'equivalent per one kWh of the total energy provided by the battery over its '
            'expected service life. Relevant attributes are the value, the unit, the '
            'referenced rulebook, the lifecycle where applied, the declaration, the '
            'performance class, the type (PCF), the declaration and the facility. These '
            'attributes are mentioned in the Battery regulation 2023/1542 from 12 July '
            '2023 in several places. Annex XIII (1) (c) refers to Article 7 (2) which '
            'refers to Article 7 (1)(d): 1. For electric vehicle batteries, rechargeable '
            'industrial batteries with a capacity greater than 2 kWh and LMT batteries a '
            'carbon footprint declaration shall be drawn up for each battery model per '
            'manufacturing plant, in accordance with the implementing act referred to in '
            'the fourth subparagraph and containing, at least, the following information: '
            '[...] (d) the carbon footprint of the battery, calculated as kg of carbon '
            'dioxide equivalent per one kWh of the total energy provided by the battery '
            'over its expected service life; And as well in Article 7: 2. Electric '
            'vehicle batteries, rechargeable industrial batteries with a capacity greater '
            'than 2 kWh and LMT batteries shall bear a conspicuous, clearly legible and '
            'indelible label indicating the carbon footprint of the battery referred to '
            'in paragraph 1, first subparagraph, point (d) and declaring the carbon '
            'footprint performance class to which the relevant battery model per '
            'manufacturing plant corresponds. Further specified in Annex XIII (1) (c) and '
            'refers to Article 7 (1): [...] The Commission shall, by 18 February 2024 for '
            'electric vehicle batteries, 18 February 2025 for rechargeable industrial '
            'batteries, except those with external storage, 18 February 2027 for LMT '
            'batteries and 18 February 2029 for industrial batteries with external '
            'storage, adopt: (a) a delegated act in accordance with Article 89 to '
            'supplement this Regulation by establishing the methodology for the '
            'calculation and verification of the carbon footprint of the battery referred '
            'to in the first subparagraph, point (d), in accordance with the essential '
            'elements set out in Annex II; These parameters are defined by Article 3: '
            '(21) "carbon footprint" means the sum of greenhouse gas emissions and '
            'greenhouse gas removals in a product system, expressed as carbon dioxide '
            'equivalents and based on a Product Environmental Footprint (PEF) study using '
            'the single impact category of climate change; and defined by Annex II (2): '
            '(e) "life cycle" means the consecutive and interlinked stages of a product '
            'system, from raw material acquisition or generation from natural resources '
            'to final disposal (ISO 14040:2006 or an equivalent standard).'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#carbonFootprint'},
    )

    state: Literal['original', 'repurposed', 're-used', 'remanufactured', 'waste'] = Field(
        alias='status',
        description=(
            'The status of the product (original, repurposed, re-used, remanufactured or '
            'waste) to indicated, whether it is a used product. This attribute is '
            'mentioned in the ESPR proposal from March 30th, 2022 Annex I: (j) '
            'incorporation of used components.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#state'},
    )


class MaterialActiveEntity(BaseModel):
    """Material Active Entity.

    The information on the active material with the recycled share, location and
    supporting document(s).
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    location: str = Field(
        alias='location',
        description=(
            'The location of the substances of concern within the product. This attribute '
            'is mentioned in the ESPR proposal from March 30th, 2022 Article 7: (5) (b) '
            'the location of the substances of concern within the product.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#location'},
    )

    recycled: float = Field(
        alias='recycled',
        description=(
            'The share of the material, which is recovered recycled content from the '
            'product. This attribute is mentioned in the ESPR provisional agreement from '
            'January 9th, 2024 Annex I: (h) use or content of recycled materials and '
            'recovery of materials, including critical raw materials; Unit: percent. '
            'Constrained upstream by PercentageConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#recycled'},
    )

    documentation: list[DocumentationEntity] = Field(
        alias='documentation',
        description='Documentation accompanying the material.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#documentation'},
    )

    critical: bool = Field(
        alias='critical',
        description=(
            'A flag, if the material is a critical raw material. This attribute is '
            'mentioned in the ESPR provisional agreement from January 9th, 2024 Annex I: '
            '(h) use or content of recycled materials and recovery of materials, '
            'including critical raw materials; In Annex II of the connected proposal Act '
            'of Critical Raw Materials, a list of critical raw materials can be found.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#critical'},
    )


class LeadEntity(BaseModel):
    """Lead Entity.

    Entity for lead.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    impact_of_substances: list[DocumentationEntity] = Field(
        alias='impactOfSubstances',
        description=(
            'An accumulation of documents that refer to the impact, especially hazardous '
            'substances, on the battery. This attribute is mentioned in the Battery '
            'regulation 2023/1542 from 12 July 2023 in Annex XIII (1) (s), refers to '
            'Article 74: 1. In addition to the information referred to in Article 8a(2) '
            'of Directive 2008/98/EC, producers or, where appointed in accordance with '
            'Article 57(1), producer responsibility organisations shall make available to '
            'end-users and distributors the following information regarding the '
            'prevention and management of waste batteries with regard to the categories '
            'of batteries that they supply within the territory of a Member State: [...] '
            '(f) the impact of substances, in particular hazardous substances, present in '
            'batteries on the environment and on human health or the safety of persons, '
            'including the impact due to inappropriate discarding of waste batteries, '
            'such as littering or discarding as unsorted municipal waste.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#impactOfSubstances'},
    )

    critical: bool = Field(
        alias='critical',
        description=(
            'A flag, if the material is a critical raw material. This attribute is '
            'mentioned in the ESPR provisional agreement from January 9th, 2024 Annex I: '
            '(h) use or content of recycled materials and recovery of materials, '
            'including critical raw materials; In Annex II of the connected proposal Act '
            'of Critical Raw Materials, a list of critical raw materials can be found.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#critical'},
    )

    documentation: list[DocumentationEntity] = Field(
        alias='documentation',
        description='Documentation accompanying the material.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#documentation'},
    )

    recycled: float = Field(
        alias='recycled',
        description=(
            'The share of the material, which is recovered recycled content from the '
            'product. This attribute is mentioned in the ESPR provisional agreement from '
            'January 9th, 2024 Annex I: (h) use or content of recycled materials and '
            'recovery of materials, including critical raw materials; Unit: percent. '
            'Constrained upstream by PercentageConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#recycled'},
    )

    location: str = Field(
        alias='location',
        description=(
            'The location of the substances of concern within the product. This attribute '
            'is mentioned in the ESPR proposal from March 30th, 2022 Article 7: (5) (b) '
            'the location of the substances of concern within the product.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#location'},
    )

    concentration: float = Field(
        alias='concentration',
        description=(
            'Concentration of the material at the level of the product. This attribute is '
            'specially mentioned for substances of concern mentioned in the ESPR proposal '
            'from March 30th, 2022 Article 7: (5) (c) the concentration, maximum '
            'concentration or concentration range of the substances of concern, at the '
            'level of the product [...]. Other substances are mentioned for the purpose '
            'of recycling in the ESPR provisional agreement from January 9th, 2024 Annex '
            'I: (d) design for recycling, ease and quality of recycling as expressed '
            'through: use of easily recyclable materials, safe, easy and non-destructive '
            'access to recyclable components and materials or components and materials '
            'containing hazardous substances and material composition and homogeneity, '
            'possibility for high-purity sorting, number of materials and components '
            'used, use of standard components, use of component and material coding '
            'standards for the identification of components and materials, number and '
            'complexity of processes and tools needed, ease of nondestructive disassembly '
            'and re-assembly, conditions for access to product data, conditions for '
            'access to or use of hardware and software needed. Constrained upstream by '
            'PositiveRangeConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#concentration'},
    )

    material_unit: Literal['unit:partPerMillion', 'unit:percent', 'unit:percentVolume', 'unit:partPerThousand', 'unit:partPerTrillionUs', 'unit:partPerBillionUs'] = Field(
        alias='materialUnit',
        description=(
            'The unit of concentration chosen from an enumeration: mass percent, volume '
            'percent, parts per thousand, parts per million, parts per billion and parts '
            'per trillion.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#materialUnit'},
    )


class MaterialIdEntity(BaseModel):
    """Material Id Entity.

    Id Entity with identifier, name and list type.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    chemical_id: str = Field(
        alias='id',
        description=(
            'The substance identification, in accordance with the specification in the '
            'attribute for the list type.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#chemicalId'},
    )

    list_type_id: Literal['CAS', 'EC', 'IUPAC'] = Field(
        alias='type',
        description=(
            'The type of standard used for the identification of the substances. Selected '
            'can be for example CAS, IUPAC or EC.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#listTypeId'},
    )

    chemical_name: str = Field(
        alias='name',
        description='The name of the material which is present in the product.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#chemicalName'},
    )


class OtherActiveMaterialsEntity(BaseModel):
    """Other Active Materials Entity.

    Entity for other active materials.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    location: str = Field(
        alias='location',
        description=(
            'The location of the substances of concern within the product. This attribute '
            'is mentioned in the ESPR proposal from March 30th, 2022 Article 7: (5) (b) '
            'the location of the substances of concern within the product.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#location'},
    )

    recycled: float = Field(
        alias='recycled',
        description=(
            'The share of the material, which is recovered recycled content from the '
            'product. This attribute is mentioned in the ESPR provisional agreement from '
            'January 9th, 2024 Annex I: (h) use or content of recycled materials and '
            'recovery of materials, including critical raw materials; Unit: percent. '
            'Constrained upstream by PercentageConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#recycled'},
    )

    documentation: list[DocumentationEntity] = Field(
        alias='documentation',
        description='Documentation accompanying the material.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#documentation'},
    )

    critical: bool = Field(
        alias='critical',
        description=(
            'A flag, if the material is a critical raw material. This attribute is '
            'mentioned in the ESPR provisional agreement from January 9th, 2024 Annex I: '
            '(h) use or content of recycled materials and recovery of materials, '
            'including critical raw materials; In Annex II of the connected proposal Act '
            'of Critical Raw Materials, a list of critical raw materials can be found.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#critical'},
    )

    material_identification: list[MaterialIdEntity] = Field(
        alias='materialIdentification',
        description=(
            'The chemical material name and identification, in accordance with the '
            'specification in the attribute for the list type. Preference is given to the '
            'IUPAC name. This attribute is mentioned in the ESPR provisional agreement '
            'from January 9th, 2024 Article 7: (5) (a) the name of the substances of '
            'concern present in the product, as follows: - name(s) in the International '
            'Union of Pure and Applied Chemistry (IUPAC) nomenclature, or another '
            'international name when IUPAC name is not available; - other names (usual '
            'name, trade name, abbreviation); - European Community (EC) number, as '
            'indicated in the European Inventory of Existing Commercial Chemical '
            'Substances (EINECS), the European List of Notified Chemical Substances '
            '(ELINCS) or the No Longer Polymer (NLP) list or assigned by the European '
            'Chemicals Agency (ECHA), if available; - the Chemical Abstract Service (CAS) '
            'name(s) and number(s), if available; .'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#materialIdentification'},
    )


class ActiveMaterialEntity(BaseModel):
    """Active Material Entity.

    Entity for the active materials included in the battery. Mandatory are nickel,
    lithium, cobalt and lead.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    nickel: MaterialActiveEntity = Field(
        alias='nickel',
        description=(
            'Information about the percentage of recovered nickel from waste. These '
            'attribute are mentioned in the Battery regulation 2023/1542 from 12 July '
            '2023 in Annex XIII (1)(e) refers to Article 8: 1. From 18 August 2028 or 24 '
            'months after the date of entry into force of the delegated act referred to '
            'in the third subparagraph, whichever is the latest, industrial batteries '
            'with a capacity greater than 2 kWh, except those with exclusively external '
            'storage, electric vehicle batteries and SLI batteries that contain cobalt, '
            'lead, lithium or nickel in active materials, shall be accompanied by '
            'documentation containing information about the percentage share of cobalt, '
            'lithium or nickel that is present in active materials and that has been '
            'recovered from battery manufacturing waste or post-consumer waste, and the '
            'percentage share of lead that is present in the battery and that has been '
            'recovered from waste, for each battery model per year and per manufacturing '
            'plant.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#nickel'},
    )

    lithium: MaterialActiveEntity = Field(
        alias='lithium',
        description=(
            'Information about the percentage of recovered lithium from waste. These '
            'attribute are mentioned in the Battery regulation 2023/1542 from 12 July '
            '2023 in Annex XIII (1)(e) refers to Article 8: 1. From 18 August 2028 or 24 '
            'months after the date of entry into force of the delegated act referred to '
            'in the third subparagraph, whichever is the latest, industrial batteries '
            'with a capacity greater than 2 kWh, except those with exclusively external '
            'storage, electric vehicle batteries and SLI batteries that contain cobalt, '
            'lead, lithium or nickel in active materials, shall be accompanied by '
            'documentation containing information about the percentage share of cobalt, '
            'lithium or nickel that is present in active materials and that has been '
            'recovered from battery manufacturing waste or post-consumer waste, and the '
            'percentage share of lead that is present in the battery and that has been '
            'recovered from waste, for each battery model per year and per manufacturing '
            'plant.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#lithium'},
    )

    cobalt: MaterialActiveEntity = Field(
        alias='cobalt',
        description=(
            'Information about the percentage of recovered cobalt from waste. These '
            'attribute are mentioned in the Battery regulation 2023/1542 from 12 July '
            '2023 in Annex XIII (1)(e) refers to Article 8: 1. From 18 August 2028 or 24 '
            'months after the date of entry into force of the delegated act referred to '
            'in the third subparagraph, whichever is the latest, industrial batteries '
            'with a capacity greater than 2 kWh, except those with exclusively external '
            'storage, electric vehicle batteries and SLI batteries that contain cobalt, '
            'lead, lithium or nickel in active materials, shall be accompanied by '
            'documentation containing information about the percentage share of cobalt, '
            'lithium or nickel that is present in active materials and that has been '
            'recovered from battery manufacturing waste or post-consumer waste, and the '
            'percentage share of lead that is present in the battery and that has been '
            'recovered from waste, for each battery model per year and per manufacturing '
            'plant.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#cobalt'},
    )

    lead: LeadEntity = Field(
        alias='lead',
        description=(
            'Information about the lead in the battery. As this is an active and '
            'hazardous material, all properties for hazardous as well as active materials '
            'are required. These attribute are mentioned in the Battery regulation '
            '2023/1542 from 12 July 2023 in Annex XIII (1)(e) refers to Article 8: 1. '
            'From 18 August 2028 or 24 months after the date of entry into force of the '
            'delegated act referred to in the third subparagraph, whichever is the '
            'latest, industrial batteries with a capacity greater than 2 kWh, except '
            'those with exclusively external storage, electric vehicle batteries and SLI '
            'batteries that contain cobalt, lead, lithium or nickel in active materials, '
            'shall be accompanied by documentation containing information about the '
            'percentage share of cobalt, lithium or nickel that is present in active '
            'materials and that has been recovered from battery manufacturing waste or '
            'post-consumer waste, and the percentage share of lead that is present in the '
            'battery and that has been recovered from waste, for each battery model per '
            'year and per manufacturing plant. And for hazardous materials this is '
            'mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1) (a) refers to Annex VI Part A: 8. the hazardous substances present '
            'in the battery, other than mercury, cadmium or lead; Additionally in Article '
            '13: 5. All batteries containing more than 0,002 % cadmium or more than 0,004 '
            '% lead, shall be marked with the chemical symbol for the metal concerned: Cd '
            'or Pb. Defined in Article 3: (52) "hazardous substance" means a substance '
            'classified as hazardous pursuant to Article 3 of Regulation (EC) No '
            '1272/2008.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#lead'},
    )

    other_active_materials: list[OtherActiveMaterialsEntity] | None = Field(
        alias='other',
        default=None,
        description='Other active materials in the battery.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#otherActiveMaterials'},
    )


class HazardousEntity(BaseModel):
    """Hazardous Entity.

    Material Entity to describe the material composition for hazardous materials.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    impact_of_substances: list[DocumentationEntity] = Field(
        alias='impactOfSubstances',
        description=(
            'An accumulation of documents that refer to the impact, especially hazardous '
            'substances, on the battery. This attribute is mentioned in the Battery '
            'regulation 2023/1542 from 12 July 2023 in Annex XIII (1) (s), refers to '
            'Article 74: 1. In addition to the information referred to in Article 8a(2) '
            'of Directive 2008/98/EC, producers or, where appointed in accordance with '
            'Article 57(1), producer responsibility organisations shall make available to '
            'end-users and distributors the following information regarding the '
            'prevention and management of waste batteries with regard to the categories '
            'of batteries that they supply within the territory of a Member State: [...] '
            '(f) the impact of substances, in particular hazardous substances, present in '
            'batteries on the environment and on human health or the safety of persons, '
            'including the impact due to inappropriate discarding of waste batteries, '
            'such as littering or discarding as unsorted municipal waste.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#impactOfSubstances'},
    )

    concentration: float = Field(
        alias='concentration',
        description=(
            'Concentration of the material at the level of the product. This attribute is '
            'specially mentioned for substances of concern mentioned in the ESPR proposal '
            'from March 30th, 2022 Article 7: (5) (c) the concentration, maximum '
            'concentration or concentration range of the substances of concern, at the '
            'level of the product [...]. Other substances are mentioned for the purpose '
            'of recycling in the ESPR provisional agreement from January 9th, 2024 Annex '
            'I: (d) design for recycling, ease and quality of recycling as expressed '
            'through: use of easily recyclable materials, safe, easy and non-destructive '
            'access to recyclable components and materials or components and materials '
            'containing hazardous substances and material composition and homogeneity, '
            'possibility for high-purity sorting, number of materials and components '
            'used, use of standard components, use of component and material coding '
            'standards for the identification of components and materials, number and '
            'complexity of processes and tools needed, ease of nondestructive disassembly '
            'and re-assembly, conditions for access to product data, conditions for '
            'access to or use of hardware and software needed. Constrained upstream by '
            'PositiveRangeConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#concentration'},
    )

    location: str = Field(
        alias='location',
        description=(
            'The location of the substances of concern within the product. This attribute '
            'is mentioned in the ESPR proposal from March 30th, 2022 Article 7: (5) (b) '
            'the location of the substances of concern within the product.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#location'},
    )

    material_unit: Literal['unit:partPerMillion', 'unit:percent', 'unit:percentVolume', 'unit:partPerThousand', 'unit:partPerTrillionUs', 'unit:partPerBillionUs'] = Field(
        alias='materialUnit',
        description=(
            'The unit of concentration chosen from an enumeration: mass percent, volume '
            'percent, parts per thousand, parts per million, parts per billion and parts '
            'per trillion.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#materialUnit'},
    )

    critical: bool = Field(
        alias='critical',
        description=(
            'A flag, if the material is a critical raw material. This attribute is '
            'mentioned in the ESPR provisional agreement from January 9th, 2024 Annex I: '
            '(h) use or content of recycled materials and recovery of materials, '
            'including critical raw materials; In Annex II of the connected proposal Act '
            'of Critical Raw Materials, a list of critical raw materials can be found.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#critical'},
    )

    documentation: list[DocumentationEntity] = Field(
        alias='documentation',
        description='Documentation accompanying the material.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#documentation'},
    )


class OtherHazardousMaterialEntity(BaseModel):
    """Other HazardousMaterial Entity.

    Entity for other hazardous materials.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    impact_of_substances: list[DocumentationEntity] = Field(
        alias='impactOfSubstances',
        description=(
            'An accumulation of documents that refer to the impact, especially hazardous '
            'substances, on the battery. This attribute is mentioned in the Battery '
            'regulation 2023/1542 from 12 July 2023 in Annex XIII (1) (s), refers to '
            'Article 74: 1. In addition to the information referred to in Article 8a(2) '
            'of Directive 2008/98/EC, producers or, where appointed in accordance with '
            'Article 57(1), producer responsibility organisations shall make available to '
            'end-users and distributors the following information regarding the '
            'prevention and management of waste batteries with regard to the categories '
            'of batteries that they supply within the territory of a Member State: [...] '
            '(f) the impact of substances, in particular hazardous substances, present in '
            'batteries on the environment and on human health or the safety of persons, '
            'including the impact due to inappropriate discarding of waste batteries, '
            'such as littering or discarding as unsorted municipal waste.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#impactOfSubstances'},
    )

    material_unit: Literal['unit:partPerMillion', 'unit:percent', 'unit:percentVolume', 'unit:partPerThousand', 'unit:partPerTrillionUs', 'unit:partPerBillionUs'] = Field(
        alias='materialUnit',
        description=(
            'The unit of concentration chosen from an enumeration: mass percent, volume '
            'percent, parts per thousand, parts per million, parts per billion and parts '
            'per trillion.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#materialUnit'},
    )

    concentration: float = Field(
        alias='concentration',
        description=(
            'Concentration of the material at the level of the product. This attribute is '
            'specially mentioned for substances of concern mentioned in the ESPR proposal '
            'from March 30th, 2022 Article 7: (5) (c) the concentration, maximum '
            'concentration or concentration range of the substances of concern, at the '
            'level of the product [...]. Other substances are mentioned for the purpose '
            'of recycling in the ESPR provisional agreement from January 9th, 2024 Annex '
            'I: (d) design for recycling, ease and quality of recycling as expressed '
            'through: use of easily recyclable materials, safe, easy and non-destructive '
            'access to recyclable components and materials or components and materials '
            'containing hazardous substances and material composition and homogeneity, '
            'possibility for high-purity sorting, number of materials and components '
            'used, use of standard components, use of component and material coding '
            'standards for the identification of components and materials, number and '
            'complexity of processes and tools needed, ease of nondestructive disassembly '
            'and re-assembly, conditions for access to product data, conditions for '
            'access to or use of hardware and software needed. Constrained upstream by '
            'PositiveRangeConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#concentration'},
    )

    material_identification: list[MaterialIdEntity] = Field(
        alias='materialIdentification',
        description=(
            'The chemical material name and identification, in accordance with the '
            'specification in the attribute for the list type. Preference is given to the '
            'IUPAC name. This attribute is mentioned in the ESPR provisional agreement '
            'from January 9th, 2024 Article 7: (5) (a) the name of the substances of '
            'concern present in the product, as follows: - name(s) in the International '
            'Union of Pure and Applied Chemistry (IUPAC) nomenclature, or another '
            'international name when IUPAC name is not available; - other names (usual '
            'name, trade name, abbreviation); - European Community (EC) number, as '
            'indicated in the European Inventory of Existing Commercial Chemical '
            'Substances (EINECS), the European List of Notified Chemical Substances '
            '(ELINCS) or the No Longer Polymer (NLP) list or assigned by the European '
            'Chemicals Agency (ECHA), if available; - the Chemical Abstract Service (CAS) '
            'name(s) and number(s), if available; .'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#materialIdentification'},
    )

    documentation: list[DocumentationEntity] = Field(
        alias='documentation',
        description='Documentation accompanying the material.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#documentation'},
    )

    critical: bool = Field(
        alias='critical',
        description=(
            'A flag, if the material is a critical raw material. This attribute is '
            'mentioned in the ESPR provisional agreement from January 9th, 2024 Annex I: '
            '(h) use or content of recycled materials and recovery of materials, '
            'including critical raw materials; In Annex II of the connected proposal Act '
            'of Critical Raw Materials, a list of critical raw materials can be found.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#critical'},
    )

    location: str = Field(
        alias='location',
        description=(
            'The location of the substances of concern within the product. This attribute '
            'is mentioned in the ESPR proposal from March 30th, 2022 Article 7: (5) (b) '
            'the location of the substances of concern within the product.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#location'},
    )


class HazardousSubstanceEntity(BaseModel):
    """Hazardous Substance Entity.

    Hazardous Substance Entity for hazardous chemical materials.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    hazardous_cadmium: HazardousEntity = Field(
        alias='cadmium',
        description=(
            'Information about the presence of cadmium in the battery. Therefore, a '
            'concentration and the location within the battery has to be given. This is '
            'mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1) (a) refers to Annex VI Part A: 8. the hazardous substances present '
            'in the battery, other than mercury, cadmium or lead; Defined in Article 3: '
            '(52) "hazardous substance" means a substance classified as hazardous '
            'pursuant to Article 3 of Regulation (EC) No 1272/2008. Additionally in '
            'Article 13: 5. All batteries containing more than 0,002 % cadmium or more '
            'than 0,004 % lead, shall be marked with the chemical symbol for the metal '
            'concerned: Cd or Pb.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#hazardousCadmium'},
    )

    hazardous_mercury: HazardousEntity = Field(
        alias='mercury',
        description=(
            'Information about the presence of mercury in the battery. Therefore, a '
            'concentration and the location within the battery has to be given. This is '
            'mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1) (a) refers to Annex VI Part A: 8. the hazardous substances present '
            'in the battery, other than mercury, cadmium or lead; Defined in Article 3: '
            '(52) "hazardous substance" means a substance classified as hazardous '
            'pursuant to Article 3 of Regulation (EC) No 1272/2008.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#hazardousMercury'},
    )

    other_hazardous_material: list[OtherHazardousMaterialEntity] | None = Field(
        alias='other',
        default=None,
        description='Other hazardous materials.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#otherHazardousMaterial'},
    )

    lead: LeadEntity = Field(
        alias='lead',
        description=(
            'Information about the lead in the battery. As this is an active and '
            'hazardous material, all properties for hazardous as well as active materials '
            'are required. These attribute are mentioned in the Battery regulation '
            '2023/1542 from 12 July 2023 in Annex XIII (1)(e) refers to Article 8: 1. '
            'From 18 August 2028 or 24 months after the date of entry into force of the '
            'delegated act referred to in the third subparagraph, whichever is the '
            'latest, industrial batteries with a capacity greater than 2 kWh, except '
            'those with exclusively external storage, electric vehicle batteries and SLI '
            'batteries that contain cobalt, lead, lithium or nickel in active materials, '
            'shall be accompanied by documentation containing information about the '
            'percentage share of cobalt, lithium or nickel that is present in active '
            'materials and that has been recovered from battery manufacturing waste or '
            'post-consumer waste, and the percentage share of lead that is present in the '
            'battery and that has been recovered from waste, for each battery model per '
            'year and per manufacturing plant. And for hazardous materials this is '
            'mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1) (a) refers to Annex VI Part A: 8. the hazardous substances present '
            'in the battery, other than mercury, cadmium or lead; Additionally in Article '
            '13: 5. All batteries containing more than 0,002 % cadmium or more than 0,004 '
            '% lead, shall be marked with the chemical symbol for the metal concerned: Cd '
            'or Pb. Defined in Article 3: (52) "hazardous substance" means a substance '
            'classified as hazardous pursuant to Article 3 of Regulation (EC) No '
            '1272/2008.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#lead'},
    )


class MaterialCompositionEntity(BaseModel):
    """Material Composition Entity.

    Entity for the material composition.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    material_identification: list[MaterialIdEntity] = Field(
        alias='id',
        description=(
            'The chemical material name and identification, in accordance with the '
            'specification in the attribute for the list type. Preference is given to the '
            'IUPAC name. This attribute is mentioned in the ESPR provisional agreement '
            'from January 9th, 2024 Article 7: (5) (a) the name of the substances of '
            'concern present in the product, as follows: - name(s) in the International '
            'Union of Pure and Applied Chemistry (IUPAC) nomenclature, or another '
            'international name when IUPAC name is not available; - other names (usual '
            'name, trade name, abbreviation); - European Community (EC) number, as '
            'indicated in the European Inventory of Existing Commercial Chemical '
            'Substances (EINECS), the European List of Notified Chemical Substances '
            '(ELINCS) or the No Longer Polymer (NLP) list or assigned by the European '
            'Chemicals Agency (ECHA), if available; - the Chemical Abstract Service (CAS) '
            'name(s) and number(s), if available; .'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#materialIdentification'},
    )

    concentration: float = Field(
        alias='concentration',
        description=(
            'Concentration of the material at the level of the product. This attribute is '
            'specially mentioned for substances of concern mentioned in the ESPR proposal '
            'from March 30th, 2022 Article 7: (5) (c) the concentration, maximum '
            'concentration or concentration range of the substances of concern, at the '
            'level of the product [...]. Other substances are mentioned for the purpose '
            'of recycling in the ESPR provisional agreement from January 9th, 2024 Annex '
            'I: (d) design for recycling, ease and quality of recycling as expressed '
            'through: use of easily recyclable materials, safe, easy and non-destructive '
            'access to recyclable components and materials or components and materials '
            'containing hazardous substances and material composition and homogeneity, '
            'possibility for high-purity sorting, number of materials and components '
            'used, use of standard components, use of component and material coding '
            'standards for the identification of components and materials, number and '
            'complexity of processes and tools needed, ease of nondestructive disassembly '
            'and re-assembly, conditions for access to product data, conditions for '
            'access to or use of hardware and software needed. Constrained upstream by '
            'PositiveRangeConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#concentration'},
    )

    material_unit: Literal['unit:partPerMillion', 'unit:percent', 'unit:percentVolume', 'unit:partPerThousand', 'unit:partPerTrillionUs', 'unit:partPerBillionUs'] = Field(
        alias='unit',
        description=(
            'The unit of concentration chosen from an enumeration: mass percent, volume '
            'percent, parts per thousand, parts per million, parts per billion and parts '
            'per trillion.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#materialUnit'},
    )

    critical: bool = Field(
        alias='critical',
        description=(
            'A flag, if the material is a critical raw material. This attribute is '
            'mentioned in the ESPR provisional agreement from January 9th, 2024 Annex I: '
            '(h) use or content of recycled materials and recovery of materials, '
            'including critical raw materials; In Annex II of the connected proposal Act '
            'of Critical Raw Materials, a list of critical raw materials can be found.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#critical'},
    )

    documentation: list[DocumentationEntity] = Field(
        alias='documentation',
        description='Documentation accompanying the material.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#documentation'},
    )

    recycled: float = Field(
        alias='recycled',
        description=(
            'The share of the material, which is recovered recycled content from the '
            'product. This attribute is mentioned in the ESPR provisional agreement from '
            'January 9th, 2024 Annex I: (h) use or content of recycled materials and '
            'recovery of materials, including critical raw materials; Unit: percent. '
            'Constrained upstream by PercentageConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#recycled'},
    )

    location: str = Field(
        alias='location',
        description=(
            'The location of the substances of concern within the product. This attribute '
            'is mentioned in the ESPR proposal from March 30th, 2022 Article 7: (5) (b) '
            'the location of the substances of concern within the product.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#location'},
    )

    renewable: float = Field(
        alias='renewable',
        description=(
            'The share of the material, which is from a renewable resource that can be '
            'replenished. Renewable resources are those that can be reproduced by '
            'physical, chemical, or mechanical processes. These are the kind of resources '
            'that can be regenerated throughout time. Forest wood, for example, can be '
            'grown through reforestation. This attribute is mentioned in the ESPR '
            'provisional agreement from January 9th, 2024 Annex I: (ha) use or content of '
            'sustainable renewable materials; Unit: percent. Constrained upstream by '
            'PercentageConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#renewable'},
    )


class ChemicalMaterialEntity(BaseModel):
    """Chemical Material Entity.

    Chemical Material Entity for the battery. Included are active, hazardous and
    critical materials as well as a material symbol. This is mentioned in the Battery
    regulation 2023/1542 from 12 July 2023 in Article 13: 5. All batteries containing
    more than 0,002 % cadmium or more than 0,004 % lead, shall be marked with the
    chemical symbol for the metal concerned: Cd or Pb.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    active_materials: ActiveMaterialEntity = Field(
        alias='active',
        description=(
            'The active materials included in the battery. Mandatory are nickel, lithium, '
            'cobalt and lead. Others are optional. Defined by the Battery regulation '
            '2023/1542 from 12 July 2023 in Article 3 Definitions: (5) ‘active material’ '
            'means a material which reacts chemically to produce electric energy when the '
            'battery cell discharges or to store electric energy when the battery is '
            'being charged.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#activeMaterials'},
    )

    hazardous_substance: HazardousSubstanceEntity = Field(
        alias='hazardous',
        description='Hazardous substances like lead, cadmium and mercury.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#hazardousSubstance'},
    )

    material_composition: list[MaterialCompositionEntity] = Field(
        alias='composition',
        description=(
            'The materials which are necessary to describe the material composition, '
            'especially if they are active, critical or hazardous. This can be redundant '
            'to the specifically mentioned active or hazardous materials. This is '
            'mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1): (b) the material composition of the battery, including its '
            'chemistry, hazardous substances present in the battery, other than mercury, '
            'cadmium or lead, and critical raw materials present in the battery; (f) the '
            'share of renewable content. and in Annex XIII (2): (a) detailed composition, '
            'including materials used in the cathode, anode and electrolyte; Definition '
            'from Article 3: (52) "hazardous substance" means a substance classified as '
            'hazardous pursuant to Article 3 of Regulation (EC) No 1272/2008: A substance '
            'or a mixture fulfilling the criteria relating to physical hazards, health '
            'hazards or environmental hazards, laid down in Parts 2 to 5 of Annex I is '
            'hazardous and shall be classified in relation to the respective hazard '
            'classes provided for in that Annex. Where, in Annex I, hazard classes are '
            'differentiated on the basis of the route of exposure or the nature of the '
            'effects, the substance or mixture shall be classified in accordance with '
            'such differentiation. Defined in Article 2 of Regulation (EC) No 1272/2008: '
            '1. hazard class" means the nature of the physical, health or environmental '
            'hazard.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#materialComposition'},
    )


class VoltageEntity(BaseModel):
    """Voltage Entity.

    Entity for voltage values.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    min_voltage: float = Field(
        alias='min',
        description=(
            'Minimum voltage refers to the lowest voltage the battery is able to reach. '
            'This attribute is mentioned in the Battery regulation 2023/1542 from 12 July '
            '2023 in Annex XIII (1): (h) minimal, nominal and maximum voltage, with '
            'temperature ranges when relevant. Unit: volt.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#minVoltage'},
    )

    max_voltage: float = Field(
        alias='max',
        description=(
            'Maximum voltage refers to the highest voltage the battery is able to reach. '
            'This attribute is mentioned in the Battery regulation 2023/1542 from 12 July '
            '2023 in Annex XIII (1): (h) minimal, nominal and maximum voltage, with '
            'temperature ranges when relevant. Unit: volt.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#maxVoltage'},
    )

    nominal_voltage: float = Field(
        alias='nominal',
        description=(
            'Nominal voltage is a standardized or average voltage value assigned to the '
            'battery. This attribute is mentioned in the Battery regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (1): (h) minimal, nominal and maximum '
            'voltage, with temperature ranges when relevant. Unit: volt.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#nominalVoltage'},
    )

    testing_temperature: float | None = Field(
        alias='temperature',
        default=None,
        description=(
            "Temperature refers to the temperature of the battery during it's cycle-life "
            'testing or as boundary condition for other rated values in celsius. Unit: '
            'degreeCelsius.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#testingTemperature'},
    )


class RatedRoundTripEfficiencyEntity(BaseModel):
    """Rated Round Trip Efficiency Entity.

    Entity for the rated round trip efficiency.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    depth_of_discharge: float = Field(
        alias='depthOfDischarge',
        description=(
            'Depth of discharge is a measure used to quantify the extent to which the '
            'battery has been discharged relative to its maximum capacity during its '
            'cycle-life testing. It represents the percentage of the total available '
            'capacity that has been drained or used during a particular discharge cycle. '
            'This attribute is mentioned in the Battery regulation 2023/1542 from 12 July '
            '2023 in Annex XIII (4) (a) refers to Article 10 (1), refers to Annex IV Part '
            'B: 3. Depth of discharge in the cycle-life test. Unit: percent.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#depthOfDischarge'},
    )

    initial_round_trip_efficiency: float = Field(
        alias='initial',
        description=(
            'The efficiency value of a battery refers to the ratio of useful output '
            'energy to the input energy, expressed as a percentage. It quantifies how '
            'effectively a battery can convert and deliver stored energy during the '
            'discharge process relative to the energy input during charging. This '
            'attribute is mentioned in the Battery regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (1): (n) initial round trip energy efficiency and at 50 % of '
            'cycle-life. Unit: percent.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#initialRoundTripEfficiency'},
    )

    round_trip_efficiency50_percent: float = Field(
        alias='50PercentLife',
        description=(
            'The round trip efficiency at 50 percent refers to the efficiency of a '
            "rechargeable battery's energy storage and retrieval process when the battery "
            'has undergone approximately half of its expected number of charge-discharge '
            'cycles. This attribute is mentioned in the Battery regulation 2023/1542 from '
            '12 July 2023 in Annex XIII (1): (n) initial round trip energy efficiency and '
            'at 50 % of cycle-life. Unit: percent.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#roundTripEfficiency50Percent'},
    )

    testing_temperature: float | None = Field(
        alias='temperature',
        default=None,
        description=(
            "Temperature refers to the temperature of the battery during it's cycle-life "
            'testing or as boundary condition for other rated values in celsius. Unit: '
            'degreeCelsius.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#testingTemperature'},
    )


class RatedEnergyEntity(BaseModel):
    """Rated Energy Entity.

    Entity for the rated energy.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    energy_value: float = Field(
        alias='value',
        description=(
            'Value describing the energy in a specific measurement period, expressed in '
            'kilowatt-hours. Unit: kilowattHour.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#energyValue'},
    )

    testing_temperature: float | None = Field(
        alias='temperature',
        default=None,
        description=(
            "Temperature refers to the temperature of the battery during it's cycle-life "
            'testing or as boundary condition for other rated values in celsius. Unit: '
            'degreeCelsius.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#testingTemperature'},
    )


class RatedResistanceEntity(BaseModel):
    """Rated Resistance Entity.

    Entity for rated resistance values of the battery on different levels.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    cell_resistance: float = Field(
        alias='cell',
        description=(
            'Cell resistance refers to the internal resistance of an individual battery '
            'cell in ohms. This attribute is mentioned in the Battery regulation '
            '2023/1542 from 12 July 2023 in Annex XIII (1): (o) internal battery cell and '
            'pack resistance; Definition from Annex IV: (5) "Internal resistance" means '
            'the opposition to the flow of current within a cell or a battery under '
            'reference conditions, that is, the sum of electronic resistance and ionic '
            'resistance to the contribution to total effective resistance including '
            'inductive/capacitive properties. Unit: ohm.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#cellResistance'},
    )

    module_resistance: float | None = Field(
        alias='module',
        default=None,
        description=(
            'The module resistance in ohms includes the internal resistance of each cell '
            'within the module as well as the resistance introduced by interconnecting '
            'components such as busbars, connectors, and thermal management systems. '
            'Unit: ohm.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#moduleResistance'},
    )

    pack_resistance: float = Field(
        alias='pack',
        description=(
            'Pack resistance refers to the overall electrical resistance within a battery '
            'pack in ohms. This resistance is a combination of the individual resistances '
            'in various components within the pack, including the electrodes, connectors, '
            'and other conductive elements. This attribute is mentioned in the Battery '
            'regulation 2023/1542 from 12 July 2023 in Annex XIII (1): (o) internal '
            'battery cell and pack resistance; Definition from Annex IV: (5) "Internal '
            'resistance" means the opposition to the flow of current within a cell or a '
            'battery under reference conditions, that is, the sum of electronic '
            'resistance and ionic resistance to the contribution to total effective '
            'resistance including inductive/capacitive properties. Unit: ohm.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#packResistance'},
    )

    testing_temperature: float | None = Field(
        alias='temperature',
        default=None,
        description=(
            "Temperature refers to the temperature of the battery during it's cycle-life "
            'testing or as boundary condition for other rated values in celsius. Unit: '
            'degreeCelsius.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#testingTemperature'},
    )


class RatedPowerEntity(BaseModel):
    """Rated Power Entity.

    Entity for rated power values.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    power_value: float = Field(
        alias='value',
        description=(
            'Value describing the power in a specific measurement period, expressed in '
            'watt. Unit: watt.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#powerValue'},
    )

    capability_at20_so_c: float = Field(
        alias='at20SoC',
        description=(
            "Capability at 20% SoC refers to the battery's capability at 80% State of "
            'Charge. This measurement is indicative of the immediate available energy in '
            'the battery. This attribute is mentioned in the Battery regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (4)(a) refers to Article 10 (1), refers to '
            'Annex IV Part B: 4. Power capability at 80 % and 20 % state of charge. Unit: '
            'watt.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#capabilityAt20SoC'},
    )

    capability_at80_so_c: float = Field(
        alias='at80SoC',
        description=(
            "Capability at 80% SoC refers to the battery's capability at 80% State of "
            'Charge. This measurement is indicative of the immediate available energy in '
            'the battery. This attribute is mentioned in the Battery regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (4)(a) refers to Article 10 (1), refers to '
            'Annex IV Part B: 4. Power capability at 80 % and 20 % state of charge Unit: '
            'watt.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#capabilityAt80SoC'},
    )

    testing_temperature: float | None = Field(
        alias='temperature',
        default=None,
        description=(
            "Temperature refers to the temperature of the battery during it's cycle-life "
            'testing or as boundary condition for other rated values in celsius. Unit: '
            'degreeCelsius.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#testingTemperature'},
    )


class RatedCapacityEntity(BaseModel):
    """Rated Capacity Entity.

    Entity for rated capacity values.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    capacity_value: float = Field(
        alias='value',
        description=(
            'Value describing the capacity in a specific measurement period, expressed in '
            'ampere-hours. Unit: ampereHour.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#capacityValue'},
    )

    capacity_threshold_exhaustion: float = Field(
        alias='thresholdExhaustion',
        description=(
            "Capacity threshold exhaustion refers to the condition where a battery's "
            'capacity diminishes to a level that is considered unacceptable for its '
            'intended use. The capacity threshold is a predetermined level below which '
            'the battery is considered to be no longer effective or reliable for the '
            'specific application. This attribute is mentioned in the Battery regulation '
            '2023/1542 from 12 July 2023 in Annex XIII (1): (k) capacity threshold for '
            'exhaustion (only for electric vehicle batteries). Unit: percent.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#capacityThresholdExhaustion'},
    )

    testing_temperature: float | None = Field(
        alias='temperature',
        default=None,
        description=(
            "Temperature refers to the temperature of the battery during it's cycle-life "
            'testing or as boundary condition for other rated values in celsius. Unit: '
            'degreeCelsius.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#testingTemperature'},
    )


class PerformanceTemperatureEntity(BaseModel):
    """Performance Temperature Entity.

    Entity for temperature values.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    lower_temperature_boundary: float = Field(
        alias='lower',
        description=(
            'The lower temperature boundary (in Celsius) refers to the minimum '
            'temperature at which a battery can effectively operate. This attribute is '
            'mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1): (l) temperature range the battery can withstand when not in use '
            '(reference test). Unit: degreeCelsius.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#lowerTemperatureBoundary'},
    )

    upper_temperature_boundary: float = Field(
        alias='upper',
        description=(
            'The upper temperature boundary (in Celsius) refers to the minimum '
            'temperature at which a battery can effectively operate. This attribute is '
            'mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1): (l) temperature range the battery can withstand when not in use '
            '(reference test). Unit: degreeCelsius.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#upperTemperatureBoundary'},
    )


class CycleLifeEntity(BaseModel):
    """Cycle Life Entity.

    Cycle Life Characteristic for the battery lifetime testing with the cycles,
    temperature, depth of discharge and applied c-rates.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    testing_temperature: float = Field(
        alias='temperature',
        description=(
            "Temperature refers to the temperature of the battery during it's cycle-life "
            'testing or as boundary condition for other rated values in celsius. Unit: '
            'degreeCelsius.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#testingTemperature'},
    )

    cycles: int = Field(
        alias='cycles',
        description=(
            'Cycle refers to one complete charging and discharging sequence. Either '
            "during the battery's cycle-life testing or as full equivalent while in use."
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#cycles'},
    )

    depth_of_discharge: float = Field(
        alias='depthOfDischarge',
        description=(
            'Depth of discharge is a measure used to quantify the extent to which the '
            'battery has been discharged relative to its maximum capacity during its '
            'cycle-life testing. It represents the percentage of the total available '
            'capacity that has been drained or used during a particular discharge cycle. '
            'This attribute is mentioned in the Battery regulation 2023/1542 from 12 July '
            '2023 in Annex XIII (4) (a) refers to Article 10 (1), refers to Annex IV Part '
            'B: 3. Depth of discharge in the cycle-life test. Unit: percent.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#depthOfDischarge'},
    )

    applied_charge_rate: float = Field(
        alias='appliedChargeRate',
        description=(
            'The applied charge rate (c rate) refers to the rate at which a battery is '
            'charged. This attribute is mentioned in the Battery regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (1): (p) c-rate of relevant cycle-life test; '
            'and Annex XIII (4)(a) refers to Article 10(1) refers to Annex IV Part B: 1. '
            'Applied discharge rate and charge rate.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#appliedChargeRate'},
    )

    applied_discharge_rate: float = Field(
        alias='appliedDischargeRate',
        description=(
            'The applied discharge rate (c rate) refers to the rate at which a battery is '
            'discharged. This attribute is mentioned in the Battery regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (1): (p) c-rate of relevant cycle-life test; '
            'and Annex XIII (4)(a) refers to Article 10(1) refers to Annex IV Part B: 1. '
            'Applied discharge rate and charge rate.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#appliedDischargeRate'},
    )


class LifeCycleEntity(BaseModel):
    """Life Cycle Entity.

    Life Cycle Entity with attributes for the lifetime evaluation of a battery such as
    expected years and cycles, if applicable.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    expected_years: int = Field(
        alias='expectedYears',
        description=(
            'The expected years refer to the expected life-time of the battery before it '
            'starts heavily degrading in its capacity and c-rate in calendar years. This '
            'attribute is mentioned in the Battery regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (4) (a) refers to the Article 10 (1) refers to Annex IV Part '
            'A: 5. The expected life-time of the battery under the reference conditions '
            'for which it has been designed, in terms of cycles, except for non-cycle '
            'applications, and calendar years.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#expectedYears'},
    )

    test_report: list[DocumentationEntity] = Field(
        alias='report',
        description=(
            'The test reports refer to the testing conducted during the determination of '
            'the rated values of the battery. This attribute is mentioned in the Battery '
            'regulation 2023/1542 from 12 July 2023 in Annex XIII (3): [...] results of '
            'test reports proving compliance with the requirements laid down in this '
            'Regulation or any delegated or implementing act adopted pursuant to this '
            'Regulation. And Annex XIII (4)(a) refers to Article 10(1) and refer to Annex '
            'IV Part B: 5. Any calculations performed with the measured parameters, if '
            'applicable.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#testReport'},
    )

    cycle_life_testing: CycleLifeEntity = Field(
        alias='cycleLifeTesting',
        description='The cycle life testing of the battery.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#cycleLifeTesting'},
    )


class RatedPerformanceEntity(BaseModel):
    """Rated Performance Entity.

    Entity for rated performance values of the battery.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    voltage: VoltageEntity = Field(
        alias='voltage',
        description=(
            'Voltage values are mandatory for the battery, with the option to include '
            'temperature values voluntarily. This attribute is mentioned in the Battery '
            'regulation 2023/1542 from 12 July 2023 in Annex XIII (1): (h) minimal, '
            'nominal and maximum voltage, with temperature ranges when relevant.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#voltage'},
    )

    rated_round_trip_efficiency: RatedRoundTripEfficiencyEntity = Field(
        alias='roundTripEfficiency',
        description=(
            'The efficiency value of a battery refers to the ratio of useful output '
            'energy to the input energy, expressed as a percentage. With the option to '
            'include temperature values voluntarily.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#ratedRoundTripEfficiency'},
    )

    rated_energy: RatedEnergyEntity | None = Field(
        alias='energy',
        default=None,
        description=(
            'Representation of the total amount of energy that the battery can store and '
            'subsequently deliver during its discharge cycle. It is necessary to '
            'calculate the SOCE.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#ratedEnergy'},
    )

    rated_resistance: RatedResistanceEntity = Field(
        alias='resistance',
        description=(
            'Rated resistance of the battery on the level of the pack, module (optional) '
            'and cell.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#ratedResistance'},
    )

    rated_power: RatedPowerEntity = Field(
        alias='power',
        description=(
            'The power value is the rate at which energy is delivered or consumed. It is '
            'measured in watts (W) and represents how quickly energy is transferred. This '
            'attribute is mentioned in the Battery regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (4)(a) refers to Article 10(1), refers to Annex IV Part A: 2. '
            'Power (in W) and power fade (in %). Definition from Annex IV: (3) "Power" '
            'means the amount of energy that a battery is capable of providing over a '
            'given period under reference conditions.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#ratedPower'},
    )

    rated_capacity: RatedCapacityEntity = Field(
        alias='capacity',
        description=(
            'Capacity value refers to the amount of electric charge that a battery can '
            'store and subsequently deliver when needed. It is a fundamental '
            'characteristic of a battery and is expressed in ampere-hours. This attribute '
            'is mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1): (g) rated capacity (in Ah); and in Annex XIII (4)(a) referring to '
            'Article 10 (1) and referring to Annex IV Part A: 1. Rated capacity (in Ah) '
            'and capacity fade (in %). And in Annex XIII (1)(a) referring to Annex VI '
            'Part A: 6. the capacity; Definition from Annex IV: (1) "Rated capacity" '
            'means the total number of ampere-hours (Ah) that can be withdrawn from a '
            'fully charged battery under reference conditions.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#ratedCapacity'},
    )

    performance_document: list[DocumentationEntity] | None = Field(
        alias='performanceDocument',
        default=None,
        description=(
            'The performance document lists information regarding the performance of the '
            'battery. This can be an overview about several rated performance attributes. '
            'This attribute is mentioned in the Battery regulation 2023/1542 from 12 July '
            '2023 in Annex XIII (3): [...] results of test reports proving compliance '
            'with the requirements laid down in this Regulation or any delegated or '
            'implementing act adopted pursuant to this Regulation. And Annex XIII (4)(a) '
            'refers to Article 10(1) and refer to Annex IV Part B: 5. Any calculations '
            'performed with the measured parameters, if applicable.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#performanceDocument'},
    )

    performance_temperature: PerformanceTemperatureEntity = Field(
        alias='temperature',
        description=(
            'The battery temperatures. This attribute is mentioned in the Battery '
            'regulation 2023/1542 from 12 July 2023 in Annex XIII (1): (l) temperature '
            'range the battery can withstand when not in use (reference test).'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#performanceTemperature'},
    )

    self_discharging_rate: float = Field(
        alias='selfDischargingRate',
        description=(
            'The self-discharge rate of a battery refers to the rate at which the battery '
            "loses its stored energy when not in use. It's the discharge of the battery "
            'that occurs internally without any external load recorded in percentage for '
            'every month. This attribute is mentioned in the Battery Regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (4) (b) refers to Article 14, refers to '
            'Annex VII Part A: 4. the evolution of self-discharging rates. Unit: percent.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#selfDischargingRate'},
    )

    test_report: list[DocumentationEntity] | None = Field(
        alias='testReport',
        default=None,
        description=(
            'The test reports refer to the testing conducted during the determination of '
            'the rated values of the battery. This attribute is mentioned in the Battery '
            'regulation 2023/1542 from 12 July 2023 in Annex XIII (3): [...] results of '
            'test reports proving compliance with the requirements laid down in this '
            'Regulation or any delegated or implementing act adopted pursuant to this '
            'Regulation. And Annex XIII (4)(a) refers to Article 10(1) and refer to Annex '
            'IV Part B: 5. Any calculations performed with the measured parameters, if '
            'applicable.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#testReport'},
    )

    lifetime: LifeCycleEntity = Field(
        alias='lifetime',
        description='Attributes for the lifetime evaluation of a battery.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#lifetime'},
    )


class RecordEntity(BaseModel):
    """Record Entity.

    Entity for a dynamic record with a value and timestamp.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    percent_value: float = Field(
        alias='value',
        description='A value as a percentage in the form of a double. Unit: percent.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#percentValue'},
    )

    data_record_time: datetime = Field(
        alias='time',
        description=(
            'The entry date and time corresponding to when a specific parameter was '
            'measured. This attribute is mentioned in the Battery regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (4): (d) information and data resulting from '
            'its use, including the number of charging and discharging cycles and '
            'negative events, such as accidents, as well as periodically recorded '
            'information on the operating environmental conditions, including '
            'temperature, and on the state of charge.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dataRecordTime'},
    )


class FullCycleEntity(BaseModel):
    """Full Cycle Entity.

    Entity for dynamic cycle values.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    data_record_time: datetime = Field(
        alias='time',
        description=(
            'The entry date and time corresponding to when a specific parameter was '
            'measured. This attribute is mentioned in the Battery regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (4): (d) information and data resulting from '
            'its use, including the number of charging and discharging cycles and '
            'negative events, such as accidents, as well as periodically recorded '
            'information on the operating environmental conditions, including '
            'temperature, and on the state of charge.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dataRecordTime'},
    )

    cycles: int = Field(
        alias='value',
        description=(
            'Cycle refers to one complete charging and discharging sequence. Either '
            "during the battery's cycle-life testing or as full equivalent while in use."
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#cycles'},
    )


class RemainingPowerEntity(BaseModel):
    """Remaining Power Entity.

    Entity for the remaining power.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    data_record_time: datetime = Field(
        alias='time',
        description=(
            'The entry date and time corresponding to when a specific parameter was '
            'measured. This attribute is mentioned in the Battery regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (4): (d) information and data resulting from '
            'its use, including the number of charging and discharging cycles and '
            'negative events, such as accidents, as well as periodically recorded '
            'information on the operating environmental conditions, including '
            'temperature, and on the state of charge.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dataRecordTime'},
    )

    power_value: float = Field(
        alias='value',
        description=(
            'Value describing the power in a specific measurement period, expressed in '
            'watt. Unit: watt.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#powerValue'},
    )


class DynamicPowerEntity(BaseModel):
    """Dynamic Power Entity.

    Entity for dynamic power values.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    power_fade: RecordEntity = Field(
        alias='fade',
        description=(
            'Power fade refers to a reduction in the power of the battery system over '
            'time expressed as a percentage in reference to the initial value. This '
            'attribute is mentioned in the Battery regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (4)(a) refers to Article 10 (1), refers to Annex IV Part A: 2. '
            'Power (in W) and power fade (in %). Definition from Annex IV: (4) "Power '
            'fade" means the decrease over time and upon usage in the amount of power '
            'that a battery can deliver at the rated voltage.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#powerFade'},
    )

    remaining_power: RemainingPowerEntity = Field(
        alias='remaining',
        description=(
            'The remaining power capability in the battery expressed in watt. This '
            'attribute is mentioned in the Battery Regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (4) (b) refers to Article 14, refers to Annex VII Part A: 2. '
            'where possible, the remaining power capability; Definition from Annex IV: '
            '(3) "Power" means the amount of energy that a battery is capable of '
            'providing over a given period under reference conditions.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#remainingPower'},
    )


class CapacityEntity(BaseModel):
    """Capacity Entity.

    Entity for dynamic capacity values such as the throughput and the remaining
    capacity.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    data_record_time: datetime = Field(
        alias='time',
        description=(
            'The entry date and time corresponding to when a specific parameter was '
            'measured. This attribute is mentioned in the Battery regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (4): (d) information and data resulting from '
            'its use, including the number of charging and discharging cycles and '
            'negative events, such as accidents, as well as periodically recorded '
            'information on the operating environmental conditions, including '
            'temperature, and on the state of charge.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dataRecordTime'},
    )

    capacity_value: float = Field(
        alias='value',
        description=(
            'Value describing the capacity in a specific measurement period, expressed in '
            'ampere-hours. Unit: ampereHour.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#capacityValue'},
    )


class DynamicCapacityEntity(BaseModel):
    """Dynamic Capacity Entity.

    Entity for dynamic capacity values.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    capacity_fade: RecordEntity = Field(
        alias='fade',
        description=(
            'Capacity fade refers to a reduction in the capacity of the battery system '
            'over time expressed as a percentage in reference to the initial value. This '
            'attribute is mentioned in the Battery regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (4)(a) refers to Article 10(1) and refer to Annex IV Part A: '
            '1. Rated capacity (in Ah) and capacity fade (in %). Definition from Annex '
            'IV: (2) "Capacity fade" means the decrease over time and upon usage in the '
            'amount of charge that a battery can deliver at the rated voltage, with '
            'respect to the original rated capacity.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#capacityFade'},
    )

    capacity_throughput: CapacityEntity = Field(
        alias='throughput',
        description=(
            'Capacity throughput refers to the total amount of energy that a battery has '
            'delivered over its lifetime. It represents the cumulative energy discharge '
            'and recharge cycles a battery has undergone. Capacity throughput is '
            'expressed in ampere-hours. This attribute is mentioned in the Battery '
            'regulation 2023/1542 from 12 July 2023 in Annex VII Part B: 3. the capacity '
            'throughput.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#capacityThroughput'},
    )

    remaining_capacity: CapacityEntity = Field(
        alias='capacity',
        description=(
            'The remaining capacity in the battery expressed in ampere hours. This '
            'attribute is mentioned in the Battery Regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (4) (b) refers to Article 14, refers to Annex VII Part A: 1. '
            'the remaining capacity.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#remainingCapacity'},
    )


class DynamicRoundTripEfficiencyEntity(BaseModel):
    """Dynamic Round Trip Efficiency Entity.

    Entity for dynamic round trip efficiency values.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    round_trip_efficiency_fade: RecordEntity = Field(
        alias='fade',
        description=(
            'Round trip efficiency fade refers to a reduction in the round trip '
            'efficiency of the battery system over time expressed as a percentage in '
            'reference to the initial value. This attribute is mentioned in the Battery '
            'regulation 2023/1542 from 12 July 2023 in Annex XIII (4)(a) refers to '
            'Article 10(1) and refers to Annex IV: 4. Where applicable, energy round trip '
            'efficiency and its fade (in %). Definition from Annex IV: (6) "Energy round '
            'trip efficiency" means the ratio of the net energy delivered by a battery '
            'during a discharge test to the total energy required to restore the initial '
            'state of charge by a standard charge.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#roundTripEfficiencyFade'},
    )

    remaining_round_trip_efficiency: RecordEntity = Field(
        alias='remaining',
        description=(
            'The remaining round trip efficiency in the battery expressed as percentage. '
            'This attribute is mentioned in the Battery Regulation 2023/1542 from 12 July '
            '2023 in Annex XIII (4) (b) refers to Article 14, refers to Annex VII Part A: '
            '3. where possible, the remaining round trip efficiency. Definition from '
            'Annex IV: (6) "Energy round trip efficiency" means the ratio of the net '
            'energy delivered by a battery during a discharge test to the total energy '
            'required to restore the initial state of charge by a standard charge.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#remainingRoundTripEfficiency'},
    )


class ResistanceIncreaseEntity(BaseModel):
    """Resistance Increase Entity.

    Entity for the increase of the battery resistance.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    pack_resistance_increase: RecordEntity = Field(
        alias='pack',
        description=(
            'Pack resistance increase refers to the overall electrical resistance within '
            'a battery pack. This resistance is a combination of the individual '
            'resistances in various components within the pack, including the electrodes, '
            'connectors, and other conductive elements. The rise in the pack resistance '
            'is expressed as a percentage in reference to the initial value. This '
            'attribute is mentioned in the Battery regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (4)(a) refers to Article 10(1) and refers to Annex IV Part A: '
            '3. Internal resistance (in ") and internal resistance increase (in %). '
            'Definition from Annex IV: (5) "Internal resistance" means the opposition to '
            'the flow of current within a cell or a battery under reference conditions, '
            'that is, the sum of electronic resistance and ionic resistance to the '
            'contribution to total effective resistance including inductive/capacitive '
            'properties.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#packResistanceIncrease'},
    )

    module_resistance_increase: RecordEntity | None = Field(
        alias='module',
        default=None,
        description=(
            'The module resistance increase includes the internal resistance of each cell '
            'within the module as well as the resistance introduced by interconnecting '
            'components such as busbars, connectors, and thermal management systems. The '
            'rise in the module resistance is expressed as a percentage in reference to '
            'the initial value.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#moduleResistanceIncrease'},
    )

    cell_resistance_increase: RecordEntity = Field(
        alias='cell',
        description=(
            'Cell resistance increase refers to the internal resistance of an individual '
            'battery cell. The rise in the cell resistance is expressed as a percentage '
            'in reference to the initial value. This attribute is mentioned in the '
            'Battery regulation 2023/1542 from 12 July 2023 in Annex XIII (4)(a) refers '
            'to Article 10(1) and refers to Annex IV Part A: 3. Internal resistance (in '
            'ohms) and internal resistance increase (in %). Definition from Annex IV: (5) '
            '"Internal resistance" means the opposition to the flow of current within a '
            'cell or a battery under reference conditions, that is, the sum of electronic '
            'resistance and ionic resistance to the contribution to total effective '
            'resistance including inductive/capacitive properties.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#cellResistanceIncrease'},
    )


class RemainingResistanceEntityRecord(BaseModel):
    """Remaining Resistance Entity Record.

    Entity for the remaining battery resistance with a timestamp and value.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    data_record_time: datetime = Field(
        alias='time',
        description=(
            'The entry date and time corresponding to when a specific parameter was '
            'measured. This attribute is mentioned in the Battery regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (4): (d) information and data resulting from '
            'its use, including the number of charging and discharging cycles and '
            'negative events, such as accidents, as well as periodically recorded '
            'information on the operating environmental conditions, including '
            'temperature, and on the state of charge.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dataRecordTime'},
    )

    remaining_resistance_value: float = Field(
        alias='value',
        description='The remaining resistance value expressed in ohms. Unit: ohm.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#remainingResistanceValue'},
    )


class RemainingResistanceEntity(BaseModel):
    """Remaining Resistance Entity.

    Entity for the remaining battery resistance.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    remaining_pack_resistance: RemainingResistanceEntityRecord = Field(
        alias='pack',
        description=(
            'Pack resistance refers to the overall electrical resistance within a battery '
            'pack. This resistance is a combination of the individual resistances in '
            'various components within the pack, including the electrodes, connectors, '
            'and other conductive elements. This attribute is mentioned in the Battery '
            'Regulation 2023/1542 from 12 July 2023 in Annex XIII (4) (b) refers to '
            'Article 14, refers to Annex VII Part A: 5. where possible, the ohmic '
            'resistance.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#remainingPackResistance'},
    )

    remaining_module_resistance: RemainingResistanceEntityRecord | None = Field(
        alias='module',
        default=None,
        description=(
            'Module resistance in ohms includes the internal resistance of each cell '
            'within the module as well as the resistance introduced by interconnecting '
            'components such as busbars, connectors, and thermal management systems.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#remainingModuleResistance'},
    )

    remaining_cell_resistance: RemainingResistanceEntityRecord = Field(
        alias='cell',
        description=(
            'Cell resistance refers to the internal resistance of an individual battery '
            'cell expressed in ohms. This attribute is mentioned in the Battery '
            'Regulation 2023/1542 from 12 July 2023 in Annex XIII (4) (b) refers to '
            'Article 14, refers to Annex VII Part A: 5. where possible, the ohmic '
            'resistance.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#remainingCellResistance'},
    )


class DynamicInternalResistanceEntity(BaseModel):
    """Dynamic Internal Resistance Entity.

    Entity for dynamic internal resistance values.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    resistance_increase: ResistanceIncreaseEntity = Field(
        alias='increase',
        description=(
            'The increase as percentage in the battery resistance on the level of the '
            'pack, module (optional) and cell.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#resistanceIncrease'},
    )

    remaining_resistance: RemainingResistanceEntity = Field(
        alias='remaining',
        description=(
            'The remaining resistance in ohms in the battery on the level of the pack, '
            'module (optional) and cell.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#remainingResistance'},
    )


class EnergyEntity(BaseModel):
    """Energy Entity.

    Entity for energy values expressed in a timestamp and a kilowatt-hours value.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    data_record_time: datetime = Field(
        alias='time',
        description=(
            'The entry date and time corresponding to when a specific parameter was '
            'measured. This attribute is mentioned in the Battery regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (4): (d) information and data resulting from '
            'its use, including the number of charging and discharging cycles and '
            'negative events, such as accidents, as well as periodically recorded '
            'information on the operating environmental conditions, including '
            'temperature, and on the state of charge.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dataRecordTime'},
    )

    energy_value: float = Field(
        alias='value',
        description=(
            'Value describing the energy in a specific measurement period, expressed in '
            'kilowatt-hours. Unit: kilowattHour.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#energyValue'},
    )


class DynamicEnergyEntity(BaseModel):
    """Dynamic Energy Entity.

    Entity for dynamic energy values.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    soce: RecordEntity = Field(
        alias='soce',
        description=(
            'The state of certified energy (SOCE) refers to the current measured or '
            'on-board usable battery energy (UBE) performance expressed as a percentage. '
            'This attribute is mentioned in the Battery regulation 2023/1542 from 12 July '
            '2023 in Annex XIII (4)(b) refers to Article 14) and refers to Annex VII Part '
            'A: state of certified energy (SOCE).'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#soce'},
    )

    remaining_energy: EnergyEntity = Field(
        alias='remaining',
        description='The remaining energy in the battery expressed in kilowatt-hours.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#remainingEnergy'},
    )

    energy_throughput: EnergyEntity | None = Field(
        alias='throughput',
        default=None,
        description=(
            'Energy throughput refers to the total amount of energy that passes through a '
            'system over a specific period. This measure encompasses both the energy '
            'input (during charging) and the energy output (during discharging). Energy '
            'throughput is expressed in kilowatt-hours. This attribute is mentioned in '
            'the Battery regulation 2023/1542 from 12 July 2023 in Annex VII Part B: 2. '
            'the energy throughput.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#energyThroughput'},
    )


class DynamicPerformanceEntity(BaseModel):
    """Dynamic Performance Entity.

    Entity for dynamic performance values of the battery.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    state_of_charge: RecordEntity = Field(
        alias='stateOfCharge',
        description=(
            'State of Charge (SOC) refers to the amount of energy remaining in a battery '
            'at a given point in time, expressed as a percentage of the total capacity. '
            'This attribute is mentioned in the Battery regulation 2023/1542 from 12 July '
            '2023 in Annex XIII (4): (d) information and data resulting from its use, '
            'including the number of charging and discharging cycles and negative events, '
            'such as accidents, as well as periodically recorded information on the '
            'operating environmental conditions, including temperature, and on the state '
            'of charge.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#stateOfCharge'},
    )

    full_cycles: FullCycleEntity = Field(
        alias='fullCycles',
        description=(
            'Full cycles include the cumulative and equivalent count of complete charge '
            'and discharge cycles experienced by the battery over its entire life. This '
            'attribute is mentioned in the Battery Regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (4) (d) information and data resulting from its use, including '
            'the number of charging and discharging cycles and negative events, such as '
            'accidents, as well as periodically recorded information on the operating '
            'environmental conditions, including temperature, and on the state of charge. '
            'And in AnnexVII Part B: 5. the number of full equivalent charge-discharge '
            'cycles.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#fullCycles'},
    )

    performance_document: list[DocumentationEntity] | None = Field(
        alias='performanceDocument',
        default=None,
        description=(
            'The performance document lists information regarding the performance of the '
            'battery. This can be an overview about several rated performance attributes. '
            'This attribute is mentioned in the Battery regulation 2023/1542 from 12 July '
            '2023 in Annex XIII (3): [...] results of test reports proving compliance '
            'with the requirements laid down in this Regulation or any delegated or '
            'implementing act adopted pursuant to this Regulation. And Annex XIII (4)(a) '
            'refers to Article 10(1) and refer to Annex IV Part B: 5. Any calculations '
            'performed with the measured parameters, if applicable.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#performanceDocument'},
    )

    self_discharging_rate: float = Field(
        alias='selfDischargingRate',
        description=(
            'The self-discharge rate of a battery refers to the rate at which the battery '
            "loses its stored energy when not in use. It's the discharge of the battery "
            'that occurs internally without any external load recorded in percentage for '
            'every month. This attribute is mentioned in the Battery Regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (4) (b) refers to Article 14, refers to '
            'Annex VII Part A: 4. the evolution of self-discharging rates. Unit: percent.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#selfDischargingRate'},
    )

    dynamic_power: DynamicPowerEntity = Field(
        alias='power',
        description='Values that describe dynamically captured power values.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dynamicPower'},
    )

    dynamic_capacity: DynamicCapacityEntity = Field(
        alias='capacity',
        description='Values that describe dynamically captured capacity values.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dynamicCapacity'},
    )

    dynamic_round_trip_efficiency: DynamicRoundTripEfficiencyEntity = Field(
        alias='roundTripEfficiency',
        description='Dynamic round trip efficiency values.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dynamicRoundTripEfficiency'},
    )

    dynamic_internal_resistance: DynamicInternalResistanceEntity = Field(
        alias='resistance',
        description='Values that describe dynamically captured internal resistance values.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dynamicInternalResistance'},
    )

    dynamic_energy: DynamicEnergyEntity = Field(
        alias='energy',
        description='Values that describe dynamically captured energy values.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dynamicEnergy'},
    )

    negative_events: list[DocumentationEntity] | None = Field(
        alias='negativeEvents',
        default=None,
        description=(
            'Mandatory if applicable. Negative events refers to several possible events '
            "influencing the battery's condition and lifetime such as extreme "
            'temperatures. This attribute is mentioned in the Battery regulation '
            '2023/1542 from 12 July 2023 in Annex XIII (4): (d) information and data '
            'resulting from its use, including the number of charging and discharging '
            'cycles and negative events, such as accidents, as well as periodically '
            'recorded information on the operating environmental conditions, including '
            'temperature, and on the state of charge. And Annex VII Part B: 4. the '
            'tracking of harmful events, such as the number of deep discharge events, '
            'time spent in extreme temperatures, time spent charging in extreme '
            'temperatures.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#negativeEvents'},
    )

    operating_environment: list[DocumentationEntity] | None = Field(
        alias='operatingEnvironment',
        default=None,
        description=(
            'Mandatory if applicable. The operating environment refers to the conditions '
            'in which the battery is designed to function optimally. The environment '
            'includes factors such as temperature, humidity, pressure, and other external '
            'conditions that can impact the performance, safety, and lifespan of the '
            'battery. This attribute is mentioned in the Battery regulation 2023/1542 '
            'from 12 July 2023 in Annex XIII (4): (d) information and data resulting from '
            'its use, including the number of charging and discharging cycles and '
            'negative events, such as accidents, as well as periodically recorded '
            'information on the operating environmental conditions, including '
            'temperature, and on the state of charge. And Annex VII Part B: 4. the '
            'tracking of harmful events, such as the number of deep discharge events, '
            'time spent in extreme temperatures, time spent charging in extreme '
            'temperatures.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#operatingEnvironment'},
    )


class PerformanceEntity(BaseModel):
    """Performance Entity.

    Performance Entity with attributes of the battery including rated and dynamic
    values.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    rated_performance: RatedPerformanceEntity = Field(
        alias='rated',
        description=(
            'Rated performance values of the battery such as voltage, round trip '
            'efficiency, energy, resistance, power, capacity, temperature ranges and '
            'self-discharging rate.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#ratedPerformance'},
    )

    dynamic_performance: DynamicPerformanceEntity = Field(
        alias='dynamic',
        description='Dynamic performance values of the battery.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dynamicPerformance'},
    )


class ConformityEntity(BaseModel):
    """Conformity Entity.

    Entity for conformity documents.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    declaration_of_conformity_id: str | None = Field(
        alias='declarationOfConformityId',
        default=None,
        description=(
            'Identification number of the EU declaration of conformity. This attribute is '
            'mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1): (r) the EU declaration of conformity referred to in Article 18.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#declarationOfConformityId'},
    )

    declaration_of_conformity: list[DocumentationEntity] = Field(
        alias='declarationOfConformity',
        description=(
            'The EU Declaration of Conformity is a document in which the manufacturer or '
            'their authorized representative declares that the battery complies with all '
            'relevant European Union product safety directives and regulations. This '
            'attribute is mentioned in the Battery regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (1): (r) the EU declaration of conformity referred to in '
            'Article 18.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#declarationOfConformity'},
    )

    result_of_test_report: list[DocumentationEntity] = Field(
        alias='resultOfTestReport',
        description=(
            'The result of tests reports refers to the results of various tests conducted '
            'with the battery, testing its life cycle, life span, c-rate and various '
            'other aspects. This attribute is mentioned in the Battery regulation '
            '2023/1542 from 12 July 2023 in Annex XIII (1): (l) temperature range the '
            'battery can withstand when not in use (reference test); and Annex XIII (3): '
            'results of test reports proving compliance with the requirements laid down '
            'in this Regulation or any delegated or implementing act adopted pursuant to '
            'this Regulation.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#resultOfTestReport'},
    )

    third_party_assurance: list[DocumentationEntity] = Field(
        alias='thirdPartyAssurance',
        description=(
            'A summary report from third-parties, covering the verifications. This '
            'attribute is mentioned in the Battery regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (1) (d) refers to the Article 52: 3. The economic operator '
            'referred to in Article 48(1) shall on an annual basis review and make '
            'publicly available, including on the internet, a report on its battery due '
            'diligence policy. [...], as well as a summary report of the third-party '
            'verifications carried out in accordance with Article 51, including the name '
            'of the notified body, with due regard for business confidentiality and other '
            'competitive concerns. That report shall also cover, where relevant, access '
            'to information, public participation in decision-making and access to '
            'justice in environmental matters in relation to the sourcing, processing and '
            'trading of the raw materials present in batteries.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#thirdPartyAssurance'},
    )

    due_diligence_policy: list[DocumentationEntity] = Field(
        alias='dueDiligencePolicy',
        description=(
            'A report containing the information concerning the due diligence policy, a '
            'set of procedures and guidelines the organization follows to thoroughly '
            'assess and evaluate the various aspects of the battery. This attribute is '
            'mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1) (d) refers to the Article 52: 3. The economic operator referred to '
            'in Article 48(1) shall on an annual basis review and make publicly '
            'available, including on the internet, a report on its battery due diligence '
            'policy. That report shall contain, in a manner that is easily comprehensible '
            'for end-users and clearly identifies the batteries concerned, the data and '
            'information on steps taken by that economic operator to comply with the '
            'requirements laid down in Articles 49 and 50, including findings of '
            'significant adverse impacts in the risk categories listed in point 2 of '
            'Annex X, and how they have been addressed, as well as a summary report of '
            'the third-party verifications carried out in accordance with Article 51, '
            'including the name of the notified body, with due regard for business '
            'confidentiality and other competitive concerns. That report shall also '
            'cover, where relevant, access to information, public participation in '
            'decision-making and access to justice in environmental matters in relation '
            'to the sourcing, processing and trading of the raw materials present in '
            'batteries.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dueDiligencePolicy'},
    )


class ExtinguishAgentEntity(BaseModel):
    """Extinguish Agent Entity.

    Entity for the extinguish agents.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    agent_document: list[DocumentationEntity] | None = Field(
        alias='document',
        default=None,
        description='Documentation about the extinguishing agent.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#agentDocument'},
    )

    usable_extinguishing_media: str = Field(
        alias='media',
        description=(
            'The agent used to extinguish a fire, based on the fire class. This attribute '
            'is mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (1)(a) and refers to Annex VI Part A: 9. usable extinguishing agent.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#usableExtinguishingMedia'},
    )

    fire_class: str = Field(
        alias='fireClass',
        description=(
            'Safety classification based on the chemistry and construction of the '
            'battery. It determines the means of handling a fire caused by the battery. '
            'Possible values are A, B and C and a combination of these.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#fireClass'},
    )


class SafetyEntity(BaseModel):
    """Safety Entity.

    Entity with the attributes safety measurements, meaning of labels, safe discharging
    and dismantling. These are all documents. Additionally information about usable
    extinguish agent can be provided.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    usable_extinguish_agent: list[ExtinguishAgentEntity] = Field(
        alias='usableExtinguishAgent',
        description=(
            'The usable extinguish agents for the battery in case of a fire. This '
            'attribute is mentioned in the Battery regulation 2023/1542 from 12 July 2023 '
            'in Annex XIII (1)(a) and refers to Annex VI Part A 9. usable extinguishing '
            'agent.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#usableExtinguishAgent'},
    )

    safety_measures: list[DocumentationEntity] = Field(
        alias='safetyMeasures',
        description=(
            'Safety instruction in the form of a documentation. This attribute is '
            'mentioned in the Battery regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (2): (d) safety measures.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#safetyMeasures'},
    )

    meaning_of_labels: list[DocumentationEntity] = Field(
        alias='meaningOfLabels',
        description=(
            'Documentation on the meaning of labels on a battery which provide '
            'information to help users understand the various symbols, markings, and '
            "information present on the battery's label. This attribute is mentioned in "
            'the Battery regulation 2023/1542 from 12 July 2023 in Annex XIII (1)(s) and '
            'refers to Article 74 (1): (e) the meaning of the labels and symbols on '
            'batteries in accordance with Article 13 or printed on their packaging or in '
            'the documents accompanying batteries [...].'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#meaningOfLabels'},
    )

    safe_discharging: list[DocumentationEntity] | None = Field(
        alias='safeDischarging',
        default=None,
        description=(
            'Safe discharging documentation explaining for example the setting of a '
            'minimum voltage threshold for the battery. Discharging a battery below this '
            'threshold can lead to damage, reduced capacity, and safety hazards.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#safeDischarging'},
    )

    dismantling: list[DocumentationEntity] = Field(
        alias='dismantling',
        description=(
            'Dismantling refers to the proper way of dismantling the battery itself. It '
            'refers to the process of taking apart the battery for various purposes, such '
            'as recycling, disposal, or examination of its components. This attribute is '
            'mentioned in the Battery Regulation 2023/1542 from 12 July 2023 in Annex '
            'XIII (2) (c) dismantling information, including at least: - exploded '
            'diagrams of the battery system/pack showing the location of battery cells, - '
            'disassembly sequences, - type and number of fastening techniques to be '
            'unlocked, - tools required for disassembly, - warnings if risk of damaging '
            'parts exist, - amount of cells used and layout.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#dismantling'},
    )

    removal_from_appliance: list[DocumentationEntity] | None = Field(
        alias='removalFromAppliance',
        default=None,
        description=(
            'Removal refers to the proper process of disassembling a battery from an '
            'appliance, typically for purposes such as repairs, replacements, or '
            'disposal.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#removalFromAppliance'},
    )


class DocumentEntity(BaseModel):
    """Document Entity.

    Document entity with header, content, category and type.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    content: str = Field(
        alias='content',
        description='The content of the document e.g a link.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#content'},
    )

    category: Literal['Product Specifications', 'Manufacturer Information', 'User Manuals and Guides', 'Certifications and Compliance', 'Product Images and Videos', 'Warranty Information', 'Reviews and Ratings', 'Product Variations', 'Supply Chain Information', 'Environmental Impact', 'Compatibility and Accessories', 'FAQs and Support', 'Purchase and Retail Information', 'Privacy and Data Handling', 'Third-Party Integrations', 'Legal Information', 'Safety Information', 'Repair and Installation', 'Waste Generation and Prevention', 'Specific Voluntary Labels', 'Product Packaging', 'Return and Disposal', 'End of Life', 'Material and Substance Information', 'Technical Documentation', 'Treatment facilities', 'Other'] = Field(
        alias='category',
        description=(
            'The category in which the document can be sorted. These are mentioned in the '
            'ESPR proposal from March 30th, 2022 ANNEX III: (e) compliance documentation '
            'and information required under this Regulation or other Union law applicable '
            'to the product, such as the declaration of conformity, technical '
            'documentation or conformity certificates; ANNEX IV states additional '
            'information regarding the content of the technical documentation Further '
            'information on documents are mentioned in the proposal from March 30th, 2022 '
            'ANNEX III: (f) user manuals, instructions, warnings or safety information, '
            'as required by other Union legislation applicable to the product. '
            'Additionally requirements are mentioned in Article 21: (7) Manufacturers '
            'shall ensure that that a product covered by a delegated act adopted pursuant '
            'to Article 4 is accompanied by instructions that enable consumers and other '
            'end-users to safely assemble, install, operate, store, maintain, repair and '
            'dispose of the product in a language that can be easily understood by '
            'consumers and other end-users, as determined by the Member State concerned. '
            'Such instructions shall be clear, understandable and legible and include at '
            'least the information specified in the delegated acts adopted pursuant to '
            'Article 4 and pursuant to Article 7(2)(b), point (ii). Article 7 states '
            'additionally: (2) (b) (ii) information for consumers and other end-users on '
            'how to install, use, maintain and repair the product in order to minimize '
            'its impact on the environment and to ensure optimum durability, as well as '
            'on how to return or dispose of the product at end-of-life; (2) (b) (iii) '
            'information for treatment facilities on disassembly, recycling, or disposal '
            'at end-of-life; (2) (b) (iv) other information that may influence the way '
            'the product is handled by parties other than the manufacturer in order to '
            'improve performance in relation to product parameters referred to in Annex '
            'I. (5) (d) relevant instructions for the safe use of the product.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#category'},
    )

    content_type: str = Field(
        alias='type',
        description=(
            'The type of content which can be expected in the "content" property. '
            'Examples are a link, restricted link, pdf, excel, etc.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#contentType'},
    )

    header: str = Field(
        alias='header',
        description=(
            'The header as a short description of the document with a maximum of 100 '
            'characters. Constrained upstream by HeaderConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#header'},
    )


class MetadataEntity(BaseModel):
    """Metadata Entity.

    Passport Entity to describe version, status, end and issue date.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    version: str = Field(
        alias='version',
        description=(
            'The current version of the product passport. The possibility of '
            'modification/ updating the product passport needs to include versioning of '
            'the dataset. This attribute is an internal versioning from the passport '
            'issuer. This attribute is mentioned in the ESPR provisional agreement from '
            'January 9th, 2024 Article 8: (1) [...] The information in the product '
            'passport shall be accurate, complete, and up to date.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#version'},
    )

    status: Literal['draft', 'approved', 'invalid', 'expired'] | None = Field(
        alias='status',
        default=None,
        description=(
            'The current status of the product passport declared through either: draft, '
            'approved, invalid or expired.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#status'},
    )

    expiration_date: str = Field(
        alias='expirationDate',
        description=(
            'The timestamp in the format (yyyy-mm-dd) for the product passport until when '
            'it is available or a comment describing this period. This attribute is '
            'mentioned in the ESPR provisional agreement from January 9th, 2024 Article '
            '8: (2) (h) the period during which the product passport is to remain '
            'available, which shall correspond to at least the expected lifetime of a '
            'specific product. Constrained upstream by DateConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#expirationDate'},
    )

    issue_date: str = Field(
        alias='issueDate',
        description=(
            'The timestamp in the format (yyyy-mm-dd) since when the product passport is '
            'available. Constrained upstream by DateConstraint; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#issueDate'},
    )

    economic_operator_id: str = Field(
        alias='economicOperatorId',
        description=(
            'The identification of the owner/economic operator of the passport. Proposed, '
            'according to ISO 15459, is the CIN (company identification code). Other '
            'identification numbers like the tax identification number, value added tax '
            'identification number, commercial register number and the like are also '
            'valid entries. In the Catena-X network, the BPNL is used for the '
            'identification of companies and the information stored like contact '
            'information and addresses. This attribute is mentioned in the ESPR proposal '
            'from March 30th, 2022 Annex III: (k) the [...] unique operator identifier '
            'code of the economic operator established in the Union responsible for '
            'carrying out the tasks set out in Article 4 of Regulation (EU) 2019/1020, or '
            'Article 15 of Regulation (EU) on general product safety, or similar tasks '
            'pursuant to other EU legislation applicable to the product. Constrained '
            'upstream by BpnlRegularExpression; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#economicOperatorId'},
    )

    passport_identifier: str = Field(
        alias='passportIdentifier',
        description=(
            'The identifier of the product passport, which is an uuidv4. Constrained '
            'upstream by Uuidv4RegularExpression; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#passportIdentifier'},
    )

    predecessor: str = Field(
        alias='predecessor',
        description=(
            'Identification of the preceding product passport. If there is no preceding '
            'passport, input a dummy value. This attribute is mentioned in the ESPR '
            'provisional agreement from January 9th, 2024 Article 8: (2)(g) [...] Any new '
            'product passport shall be linked to the product passport or passports of the '
            'original product whenever appropriate. Constrained upstream by '
            'Uuidv4RegularExpression; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#predecessor'},
    )

    backup_reference: str = Field(
        alias='backupReference',
        description=(
            'A reference to the data backup of the passport. This mandatory attribute '
            'will be further defined in the future. This attribute is mentioned in the '
            'ESPR provisional agreement from January 9th, 2024 Annex III: (kb) the '
            'reference of the certified independent third-party product passport service '
            'provider hosting the back-up copy of the product passport. Article 10 also '
            'mentions: (c) the data included in the product passport shall be stored by '
            'the economic operator responsible for its creation or by certified '
            'independent third-party product passport service providers authorised to act '
            'on their behalf.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#backupReference'},
    )

    registration_identifier: str | None = Field(
        alias='registrationIdentifier',
        default=None,
        description=(
            'Identifier in the respective registry. This will be further defined in the '
            'future. This attribute is mentioned in the ESPR provisional agreement from '
            'January 9th, 2024 in Article 12: By [2 years from entering into force of '
            'this Regulation], the Commission shall set up and manage a digital registry '
            '("the registry") storing in a secure manner at least the unique product '
            'identifier, the unique operator identifier, the unique facility identifiers. '
            'In case of products intended to be placed under the customs procedure '
            "'release for free circulation', the registry shall also store the product "
            "commodity code. The registry shall also store the batteries' unique "
            'identifiers referred to in Article 77(3) of Regulation (EU) 2023/1542.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#registrationIdentifier'},
    )

    last_modification: str | None = Field(
        alias='lastModification',
        default=None,
        description=(
            'Date of the latest modification. Constrained upstream by DateConstraint; not '
            'enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#lastModification'},
    )


class CommercialEntity(BaseModel):
    """Commercial Entity.

    Commercial information.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    placed_on_market: str | None = Field(
        alias='placedOnMarket',
        default=None,
        description=(
            'The timestamp in the format (yyyy-mm-dd) with or without time zone when the '
            'product was put in the market. Constrained upstream by DateConstraint; not '
            'enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#placedOnMarket'},
    )

    purpose: list[str] = Field(
        alias='purpose',
        description=(
            'One or more intended industry/industries of the product described by the '
            "digital product passport. If exchanged via Catena-X, 'automotive ' is a must "
            'choice included in the list.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#purpose'},
    )


class SourcesEntity(BaseModel):
    """Sources Entity.

    Entity for a possible spare part sources.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    sources_identification: str = Field(
        alias='id',
        description=(
            'The identifier of a spare part producer of the product. In the Catena-X '
            'network, the BPNL is used for the identification of companies and the '
            'information stored for this like contact information and addresses. '
            'Constrained upstream by BpnlRegularExpression; not enforced here.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#sourcesIdentification'},
    )


class PartsEntity(BaseModel):
    """Parts Entity.

    Possible spare parts of the product with identifiers and names.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    manufacturer_part_id: str = Field(
        alias='manufacturerPartId',
        description=(
            'Part ID as assigned by the manufacturer of the part. The part ID identifies '
            'the part in the manufacturer`s dataspace. The part ID references a specific '
            'version of a part. The version number must be included in the part ID if it '
            'is available. The part ID does not reference a specific instance of a part '
            'and must not be confused with the serial number.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.part_type_information:1.0.0#manufacturerPartId'},
    )

    name_at_manufacturer: str = Field(
        alias='nameAtManufacturer',
        description='Name of the part as assigned by the manufacturer.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.part_type_information:1.0.0#nameAtManufacturer'},
    )


class SparePartEntity(BaseModel):
    """Spare Part Entity.

    Information regarding possible spare parts. This is mentioned in the ESPR proposal
    from March 30th, 2022 Annex I: (b) ease of repair and maintenance as expressed
    through: characteristics, availability and delivery time of spare parts, modularity,
    compatibility with commonly available spare parts, availability of repair and
    maintenance instructions, number of materials and components used, use of standard
    components, use of component and material coding standards for the identification of
    components and materials, number and complexity of processes and tools needed, ease
    of non-destructive disassembly and re-assembly, conditions for access to product
    data, conditions for access to or use of hardware and software needed; (c) the
    Global Trade Identification Number as provided for in standard ISO/IEC 15459-6 or
    equivalent of products or their parts.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    spare_part_sources: list[SourcesEntity] = Field(
        alias='producer',
        description='Sources of possible spare parts.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#sparePartSources'},
    )

    spare_part: list[PartsEntity] = Field(
        alias='sparePart',
        description='Possible spare parts of the product.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#sparePart'},
    )


class HandlingEntity(BaseModel):
    """Handling Entity.

    Entity to describe different aspects in relation with the handling of the product
    with attributes if applicable to the product.
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    spare_parts: SparePartEntity = Field(
        alias='content',
        description='The list of spare parts available for the product from various suppliers.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#spareParts'},
    )

    applicable: bool = Field(
        alias='applicable',
        description=(
            'Check whether the connected attributes are applicable to the product. If it '
            'is not applicable (false), dummy data can be delivered.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#applicable'},
    )


class BatteryPass(BaseModel):
    """Battery Passport.

    The battery pass describes information collected during the lifecycle of a battery.
    The battery passport is heavily based on the Regulation (EU) 2023/1542 of the
    European Parliament and of the Council of 12 July 2023 concerning batteries and
    waste batteries, amending Directive 2008/98/EC and Regulation (EU) 2019/1020 and
    repealing Directive 2006/66/EC. Additionally attributes come from the Proposal for
    Ecodesign for Sustainable Products Regulation.

    See https://environment.ec.europa.eu/publications/proposal-ecodesign-sustainable-products-regulation_en

    See https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32023R1542&qid=1693215264963
    """

    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    spec_version: str | None = Field(
        alias='specVersion',
        default=None,
        description=(
            'Specification of the BatteryPass format/data model (name and version '
            'number), which is used.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#specVersion'},
    )

    identification: BatteryPassIdentificationEntity = Field(
        alias='identification',
        description=(
            'Battery identification involves specific battery identifiers, including '
            'those assigned locally by the manufacturer. This attribute is mentioned in '
            'the Battery regulation 2023/1542 from 12 July 2023 in Annex XIII (1)(a) '
            'refers to AnnexVi PartA (2) refers to Article 38 (6): battery batch number '
            'or serial number or product number or another element allowing their '
            'identification.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#identification'},
    )

    operation: OperationEntity = Field(
        alias='operation',
        description=(
            "General operation information includes details such as the manufacturer's "
            'identification and the date of production. This attribute is mentioned in '
            'the Battery regulation 2023/1542 from 12 July 2023 in Annex XIII (1) (a) and '
            'refers to ANNEX VI Part A which refers to Article 38: 7. Manufacturers shall '
            'indicate on the battery their name, registered trade name or registered '
            'trade mark, their postal address, indicating a single contact point, and, if '
            'available, web and e-mail address. From Annex XIII (1) (a) and found in '
            'ANNEX VI Part A : 3. the place of manufacture (geographical location of a '
            'battery manufacturing plant). 4. the date of manufacture (month and year).'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#operation'},
    )

    characteristics: CharacteristicsEntity = Field(
        alias='characteristics',
        description=(
            'Characteristics of the battery, such as the warranty and the physical '
            'dimensions.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#characteristics'},
    )

    sustainability: SustainabilityEntity = Field(
        alias='sustainability',
        description=(
            'Sustainability includes information on the carbon footprint, sustainability '
            'documents and the status of the battery.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#sustainability'},
    )

    materials: ChemicalMaterialEntity = Field(
        alias='materials',
        description=(
            'Chemical materials relevant for the composition of the battery. These '
            'include active, hazardous and critical materials.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#materials'},
    )

    performance: PerformanceEntity = Field(
        alias='performance',
        description='Performance attributes of the battery including rated and dynamic values.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#performance'},
    )

    conformity: ConformityEntity = Field(
        alias='conformity',
        description='Conformity documents for the battery passport.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#conformity'},
    )

    safety: SafetyEntity = Field(
        alias='safety',
        description=(
            'Safety information on the battery. Included are the attributes safety '
            'measurements, meaning of labels, safe discharging and dismantling. These are '
            'all documents. Additionally information about usable extinguish agent can be '
            'provided.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#safety'},
    )

    sources: list[DocumentEntity] | None = Field(
        alias='sources',
        default=None,
        description=(
            'Consider additional available sources to enhance the content of the battery '
            'passport.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.battery.battery_pass:6.1.0#sources'},
    )

    metadata: MetadataEntity = Field(
        alias='metadata',
        description=(
            'Metadata of the product passport. These are mentioned in the ESPR proposal '
            'from March 30th, 2022 and some changed by the provisional agreement from '
            'January 9th, 2024.'
        ),
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#metadata'},
    )

    commercial: CommercialEntity = Field(
        alias='commercial',
        description='Commercial information of the product.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#commercial'},
    )

    handling: HandlingEntity = Field(
        alias='handling',
        description='Properties connected with the handling of the product.',
        json_schema_extra={'urn': 'urn:samm:io.catenax.generic.digital_product_passport:5.0.0#handling'},
    )
