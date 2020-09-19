import re


REQUIRED_COLUMNS = ("NAME", "CONTACTS", "SIGNERS", "PRIMARY_ACTIVITY", "AUTHORIZED_CAPITAL", "EDRPOU", "STAN",
                    "REGISTRATION", "ADDRESS", "REGION")


class SlotDict(object):
    __slots__ = REQUIRED_COLUMNS

    def __init__(self, name):
        [super(SlotDict, self).__setattr__(attribute, None) for attribute in self.__slots__]
        self.NAME = name
        self.SIGNERS = []

    def __setattr__(self, instance, value):
        # Disable rewriting for all attributes except specified
        if getattr(self, instance) is None:
            super(SlotDict, self).__setattr__(instance, value)
        else:
            # print(f'{instance} attribute is already set')
            pass

    def add_signer(self, signer):
        self.SIGNERS.append(signer)

    def get_data(self):
        return [getattr(self, name) for name in self.__slots__]

    def set_region(self):
        region = None

        if self.ADDRESS:
            region = re.search(r'[А-Яа-яёЁЇїІіЄєҐґ]+ (обл\.|ОБЛАСТЬ)', self.ADDRESS) or \
                     re.search(r'місто Київ', self.ADDRESS) #or \
                     # re.search(r'[А-Яа-яёЁЇїІіЄєҐґ]+ ОБЛАСТЬ', self.ADDRESS)



        if region:
            region = region.group()

            if 'обл.' in region or 'ОБЛАСТЬ' in region:
                region = region.split(' ')[0].lower()

            self.REGION = region
        else:
            self.REGION = 'неопределен'