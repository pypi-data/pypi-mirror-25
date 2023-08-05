# -*- author: Dimitri Scheftelowitsch -*-
# -*- coding:utf-8 -*-

from collider import ResultLog
from typing import Any, Dict


class RerunPredicate:
    def __init__(self):
        pass

    def rerun(self, stage: str, value: Any) -> bool:
        raise NotImplementedError("Pure virtual class -- use a subclass")


class AlwaysRerun(RerunPredicate):
    def __init__(self):
        RerunPredicate.__init__(self)

    def rerun(self, stage: str, value: Any) -> bool:
        return True


class RerunIfNeeded(RerunPredicate):
    def __init__(self, result_log: ResultLog):
        RerunPredicate.__init__(self)
        self.result_log = result_log

    def rerun(self, stage: str, value: Any) -> bool:
        frame = self.result_log.get_stage_value_results(stage, value)
        return len(frame) == 0


class RerunFromStage(RerunIfNeeded):
    def __init__(self, result_log: ResultLog, stage_order: Dict[str, int], stage: str):
        RerunIfNeeded.__init__(self, result_log)
        self.stage_order = stage_order
        self.stage = stage

    def rerun(self, stage: str, value: Any) -> bool:
        is_greater_or_equal = self.stage_order[stage] >= self.stage_order[self.stage]
        return is_greater_or_equal or RerunIfNeeded.rerun(self, stage, value)


class RerunOnly(RerunIfNeeded):
    def __init__(self, result_log: ResultLog, stage: str):
        RerunIfNeeded.__init__(self, result_log)
        self.stage = stage

    def rerun(self, stage: str, value: Any) -> bool:
        is_equal = self.stage == stage
        return is_equal or RerunIfNeeded.rerun(self, stage, value)