# Copyright © Xzonn <Xzonn@outlook.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from django.utils.translation import gettext_lazy
from translate.storage.jsonl10n import BaseJsonUnit, JsonFile

from weblate.formats.ttkit import JSONFormat


class ParaTranzJsonUnit(BaseJsonUnit):
    ID_FORMAT = "{}"

    def __init__(
        self, source=None, target=None, key=None, notes=None, index=0, **kwargs
    ):
        if not isinstance(index, int):
            raise TypeError("index must be an integer")

        self._index = index
        self._id = f"[{index}]" if key is None else key
        self._item = self._id
        self._type = str if source is None else type(source)
        self.placeholders = None
        self._unitid = None

        if notes:
            self.notes = notes

        if target is not None:
            self.target = target
        elif source is not None:
            self.target = source
        else:
            self.target = ""

        if source is not None:
            self._source = source
        else:
            self._source = ""

    def storevalues(self, output):
        if not isinstance(output, list):
            raise TypeError("output must be a list")

        value = {
            "key": self._id,
            "original": self._source,
            "translation": self.target,
        }
        if self.notes:
            value["context"] = self.notes

        if self._index < len(output) and output[self._index].get("key") == self._id:
            output[self._index].update(value)
            return

        for item in output:
            if item.get("key") == self._id:
                item.update(value)
                break
        else:
            output.append(value)

    def getvalue(self):
        value = {
            "key": self._id,
            "original": self._source,
            "translation": self.target,
        }
        if self.notes:
            value["context"] = self.notes
        return value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        if source is not None:
            self._source = source
        else:
            self._source = ""

    def setid(self, value):
        self._id = value

    def getid(self):
        return self._id

    def getlocations(self):
        return [self.getid()]


class ParaTranzJsonFile(JsonFile):
    UnitClass = ParaTranzJsonUnit

    def __init__(self, inputfile=None, filter=None, **kwargs):
        super().__init__(inputfile, filter, **kwargs)
        self.dump_args["indent"] = 2

    def serialize(self, out):
        units: list[dict] = self._file or []
        for unit in self.unit_iter():
            unit: ParaTranzJsonUnit
            unit.storevalues(units)
        out.write(json.dumps(units, **self.dump_args).encode(self.encoding))

    def _extract_units(
        self,
        data: list[dict[str, str]],
        **args,
    ):
        for index, item in enumerate(data):
            if item.get("trash", False):
                continue
            unit = self.UnitClass(
                item.get("original"),
                item.get("translation"),
                item.get("key"),
                item.get("context"),
                index,
            )
            unit.setid(item.get("key"))
            yield unit


class ParaTranzJsonFormat(JSONFormat):
    name = gettext_lazy("ParaTranz JSON file")
    format_id = "paratranz-json"
    loader = ParaTranzJsonFile
    monolingual = True
    new_translation = "[]"

    def create_unit(self, key, source, target=None):
        unit = super().create_unit(key, source, target)
        if (self.is_template or self.template_store) and unit.target:
            unit.source = unit.target

        return unit
