from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class RenameWorkspaceAction:
    store: object

    def execute(self, workspace_id: str, *, rename_to: str):
        workspace = self.store.require(workspace_id)
        return self.store.persist(replace(workspace, name=rename_to))


class WorkspaceBatchRunner:
    def __init__(self):
        self.pool = ThreadPoolExecutor(max_workers=8)

    def schedule(self, action, workspace_id, rename_to):
        return self.pool.submit(action.execute, workspace_id, rename_to=rename_to)