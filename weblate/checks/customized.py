# Copyright © Xzonn <Xzonn@outlook.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from weblate.checks.base import TargetCheck


class AngleBracketCheck(TargetCheck):
    check_id = "angle_bracket_check"
    name = "角括号检查"
    description = "检查原文与译文是否包含同样数量的角括号"

    def check_single(self, source: str, target: str, unit):
        return (
            (target.count("<") != source.count("<"))
            or (target.count(">") != source.count(">"))
            or (target.count("[") != source.count("["))
            or (target.count("]") != source.count("]"))
            or (target.count("{") != source.count("{"))
            or (target.count("}") != source.count("}"))
        )


class EllipsisEndStopCheck(TargetCheck):
    check_id = "ellipsis_end_stop_check"
    name = "省略号与句号连用检查"
    description = "中文省略号无需与句号连用"

    def check_single(self, source, target, unit):
        if not target:
            return False
        if not unit.translation.language.is_base(("zh",)):
            return False
        return "…。" in target


class WrongEllipsisCheck(TargetCheck):
    check_id = "wrong_ellipsis_check"
    name = "省略号误用检查"
    description = "请使用“……”作为省略号，而非“...”或“。。。”"

    def check_single(self, source, target, unit):
        if not target:
            return False
        if not unit.translation.language.is_base(("zh",)):
            return False
        return "..." in target or "。。" in target


class DobuleLeftQuotationCheck(TargetCheck):
    check_id = "double_left_quotation_check"
    name = "引号数目检查"
    description = "检查左引号数目与右引号数目是否匹配"

    def check_single(self, source, target, unit):
        if not target:
            return False
        if not unit.translation.language.is_base(("zh",)):
            return False
        return (
            target.count("“") - target.count("”") > 1
            or target.count("‘") - target.count("’") > 1
        )


class FullWidthSpaceCheck(TargetCheck):
    check_id = "full_width_space_check"
    name = "全角空格检查"
    description = "检查换行符后是否有全角空格"

    def check_single(self, source, target, unit):
        if not target:
            return False
        if not unit.translation.language.is_base(("zh",)):
            return False
        if not source.count("\n　") or (source.count("\n　") != source.count("\n")):
            return False

        return target.count("\n　") != target.count("\n")
