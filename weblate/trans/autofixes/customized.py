import re

from weblate.trans.autofixes.base import AutoFix


class JapaneseCharacterFix(AutoFix):
    JAPANESE_TO_CHINESE_DICT = {
        "・": "·",
        "駒": "驹",
        "高校": "高中",
        "特异点": "奇点",
        "……。": "……",
        "~": "～",
        "～。": "～",
    }

    fix_id = "japanese_character"
    name = "检查标点、易错字符和易错词语"

    def fix_single_target(self, target, source, unit):
        if unit.translation.language.base_code != "zh":
            return target, False

        if not target:
            return target, False

        flags = unit.all_flags
        if "ignore-japanese-character" in flags:
            return target, False

        new_target = target
        for k, v in JapaneseCharacterFix.JAPANESE_TO_CHINESE_DICT.items():
            new_target = new_target.replace(k, v)

        new_target = re.sub(r"(“[^“”]+)“", r"\1”", new_target)

        return new_target, new_target != target


class FullWidthSpaceFix(AutoFix):
    fix_id = "full_width_space"
    name = "检查全角空格"

    def fix_single_target(self, target, source, unit):
        if unit.translation.language.base_code != "zh":
            return target, False

        if not target:
            return target, False
        if not source.count("\n　") or (source.count("\n　") != source.count("\n")):
            return target, False
        if target.count("\n　") == target.count("\n"):
            return target, False

        flags = unit.all_flags
        if "ignore-full-width-space" in flags:
            return target, False

        new_target = target.replace("\n", "\n　").replace("\n　　", "\n　")
        return new_target, new_target != target
