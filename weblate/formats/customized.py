# Copyright © Xzonn <Xzonn@outlook.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from django.utils.translation import gettext_lazy
from translate.storage.base import TranslationUnit
from translate.storage.jsonl10n import JsonFile

from weblate.formats.ttkit import JSONFormat


class ParaTranzJsonUnit(TranslationUnit):
    def __init__(
        self, index=0, key=None, source=None, target=None, comments=None, **kwargs
    ):
        self.index = index
        self._id = f"[{index}]" if key is None else key
        self._item = self._id
        self._type = str if source is None else type(source)
        if comments:
            self.notes = comments
        if target:
            self.target = target
        super().__init__(source)

    def setid(self, value):
        self._id = value

    def getid(self):
        return self._id

    def storevalues(self, output):
        value = {
            "translation": self.target,
            "context": self.notes,
        }
        output[self.index].update(value)

    def getvalue(self):
        return {
            "key": self._id,
            "source": self.source,
            "translation": self.target,
            "context": self.notes,
        }

    def getlocations(self):
        return [self.getid()]


class ParaTranzJsonFile(JsonFile):
    UnitClass = ParaTranzJsonUnit

    def __init__(self, inputfile=None, filter=None, **kwargs):
        super().__init__(inputfile, filter, **kwargs)
        self.dump_args["indent"] = 2

    def serialize(self, out):
        units = self._file
        self.serialize_units(units)
        out.write(json.dumps(units, **self.dump_args).encode(self.encoding))

    def _extract_units(
        self,
        data: list[dict[str, str]],
    ):
        for index, item in enumerate(data):
            unit = self.UnitClass(
                index,
                item.get("key"),
                item.get("original"),
                item.get("translation"),
                item.get("context"),
            )
            unit.setid(item.get("key"))
            yield unit


class ParaTranzJsonFormat(JSONFormat):
    name = gettext_lazy("ParaTranz JSON file")
    format_id = "paratranz-json"
    loader = ParaTranzJsonFile
    monolingual = True
    new_translation = "[]\n"
