from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Dict, Optional, Any, List, Tuple


class State(Enum):
    NOT_RUNNING = auto()
    AUTH_PENDING = auto()
    DASHBOARD = auto()
    EDITING_CLEAN = auto()
    EDITING_DIRTY = auto()
    SAVE_PROMPT = auto()
    SEARCH = auto()
    EXPORTING = auto()
    BACKING_UP = auto()
    ERROR = auto()

    # Background sync region (modeled separately)
    SYNC_IDLE = auto()
    SYNC_SYNCING = auto()


class Event(Enum):
    LAUNCH_APP = auto()
    SUBMIT_CREDENTIALS = auto()
    AUTH_OK = auto()
    AUTH_FAIL = auto()
    LOGOUT = auto()
    OPEN_EDITOR = auto()
    TYPE_TEXT = auto()
    SAVE = auto()
    AUTO_SAVE = auto()
    CLOSE_EDITOR = auto()
    OPEN_SEARCH = auto()
    EXIT_SEARCH = auto()
    START_EXPORT = auto()
    EXPORT_DONE = auto()
    EXPORT_ERROR = auto()
    START_BACKUP = auto()
    BACKUP_DONE = auto()
    BACKUP_ERROR = auto()
    RECOVER = auto()

    # Background sync
    SYNC_START = auto()
    SYNC_DONE = auto()
    SYNC_ABORT = auto()


Guard = Callable[["QuietQuillStateMachine", Dict[str, Any]], bool]
Action = Callable[["QuietQuillStateMachine", Dict[str, Any]], None]


@dataclass
class Transition:
    src: State
    event: Event
    dst: State
    guard: Optional[Guard] = None
    action: Optional[Action] = None


@dataclass
class QuietQuillStateMachine:
    state: State = State.NOT_RUNNING
    sync_state: State = State.SYNC_IDLE

    # context/flags (guards consult these)
    encryption_on: bool = True
    network_up: bool = True
    unsaved_changes: bool = False

    # history of foreground state inside a session
    _history_session: Optional[State] = None

    # optional log of transitions
    log: List[Tuple[State, Event, State]] = field(default_factory=list)

    def set_encryption(self, on: bool) -> None:
        self.encryption_on = on

    def set_network(self, up: bool) -> None:
        self.network_up = up

    def _set_unsaved(self, val: bool) -> None:
        self.unsaved_changes = val

    # Guards
    def g_credentials_valid(self, data: Dict[str, Any]) -> bool:
        return bool(data.get("valid", False))

    def g_encryption_on(self, data: Dict[str, Any]) -> bool:
        return self.encryption_on

    def g_network_up(self, data: Dict[str, Any]) -> bool:
        return self.network_up

    def g_has_unsaved(self, data: Dict[str, Any]) -> bool:
        return self.unsaved_changes

    # Actions
    def a_show_login(self, _: Dict[str, Any]) -> None:
        pass  # UI side-effect placeholder

    def a_issue_session(self, _: Dict[str, Any]) -> None:
        pass

    def a_show_dashboard(self, _: Dict[str, Any]) -> None:
        pass

    def a_encrypt_and_persist(self, _: Dict[str, Any]) -> None:
        # pretend to encrypt then persist
        self._set_unsaved(False)

    def a_persist(self, _: Dict[str, Any]) -> None:
        self._set_unsaved(False)

    def a_queue_for_later(self, _: Dict[str, Any]) -> None:
        # would queue a job, keep unsaved true
        pass

    def a_show_error(self, data: Dict[str, Any]) -> None:
        # capture error if provided
        pass

    def a_clear_session(self, _: Dict[str, Any]) -> None:
        self._history_session = None
        self._set_unsaved(False)

    def a_enter_search(self, _: Dict[str, Any]) -> None:
        # remember history to return after search
        self._history_session = self.state

    def a_exit_search_to_history(self, _: Dict[str, Any]) -> None:
        # history fallback to dashboard
        self.state = self._history_session or State.DASHBOARD

    def _record(self, src: State, ev: Event, dst: State) -> None:
        self.log.append((src, ev, dst))

    # Foreground transition table
    def _transitions(self) -> List[Transition]:
        return [
            Transition(State.NOT_RUNNING, Event.LAUNCH_APP, State.AUTH_PENDING, action=lambda s, d: s.a_show_login(d)),

            # Auth flow
            Transition(State.AUTH_PENDING, Event.SUBMIT_CREDENTIALS, State.DASHBOARD, guard=lambda s, d: s.g_credentials_valid(d), action=lambda s, d: s.a_issue_session(d)),
            Transition(State.AUTH_PENDING, Event.SUBMIT_CREDENTIALS, State.AUTH_PENDING, guard=lambda *_: True, action=lambda s, d: s.a_show_error(d)),

            # Dashboard to editor/search/export/backup
            Transition(State.DASHBOARD, Event.OPEN_EDITOR, State.EDITING_CLEAN, action=lambda s, d: s.a_show_dashboard(d)),
            Transition(State.DASHBOARD, Event.OPEN_SEARCH, State.SEARCH, action=lambda s, d: s.a_enter_search(d)),
            Transition(State.DASHBOARD, Event.START_EXPORT, State.EXPORTING, guard=lambda s, d: s.g_encryption_on(d)),
            Transition(State.DASHBOARD, Event.START_BACKUP, State.BACKING_UP, guard=lambda s, d: s.g_network_up(d)),

            # Editor typing/saving
            Transition(State.EDITING_CLEAN, Event.TYPE_TEXT, State.EDITING_DIRTY, action=lambda s, d: s._set_unsaved(True)),
            Transition(State.EDITING_DIRTY, Event.SAVE, State.EDITING_CLEAN, guard=lambda s, d: s.g_encryption_on(d), action=lambda s, d: s.a_encrypt_and_persist(d)),
            Transition(State.EDITING_DIRTY, Event.SAVE, State.EDITING_CLEAN, guard=lambda s, d: not s.encryption_on, action=lambda s, d: s.a_persist(d)),
            Transition(State.EDITING_DIRTY, Event.AUTO_SAVE, State.EDITING_CLEAN, guard=lambda s, d: s.g_network_up(d), action=lambda s, d: s.a_persist(d)),
            Transition(State.EDITING_DIRTY, Event.AUTO_SAVE, State.EDITING_DIRTY, guard=lambda s, d: not s.network_up, action=lambda s, d: s.a_queue_for_later(d)),

            # Close editor with/without unsaved
            Transition(State.EDITING_CLEAN, Event.CLOSE_EDITOR, State.DASHBOARD),
            Transition(State.EDITING_DIRTY, Event.CLOSE_EDITOR, State.SAVE_PROMPT, guard=lambda s, d: s.g_has_unsaved(d)),

            # Save prompt outcomes
            Transition(State.SAVE_PROMPT, Event.SAVE, State.EDITING_CLEAN, action=lambda s, d: s.a_persist(d)),
            Transition(State.SAVE_PROMPT, Event.RECOVER, State.EDITING_DIRTY),  # cancel
            Transition(State.SAVE_PROMPT, Event.CLOSE_EDITOR, State.DASHBOARD, action=lambda s, d: s._set_unsaved(False)),  # discard

            # Search exit returns to last known foreground (history emulation handled in action)
            Transition(State.SEARCH, Event.EXIT_SEARCH, State.DASHBOARD, action=lambda s, d: s.a_exit_search_to_history(d)),

            # Export / backup complete/error
            Transition(State.EXPORTING, Event.EXPORT_DONE, State.DASHBOARD),
            Transition(State.EXPORTING, Event.EXPORT_ERROR, State.ERROR, action=lambda s, d: s.a_show_error(d)),

            Transition(State.BACKING_UP, Event.BACKUP_DONE, State.DASHBOARD),
            Transition(State.BACKING_UP, Event.BACKUP_ERROR, State.ERROR, action=lambda s, d: s.a_show_error(d)),

            # Error recovery
            Transition(State.ERROR, Event.RECOVER, State.DASHBOARD),

            # Logout from any foreground state → Auth pending
            Transition(State.DASHBOARD, Event.LOGOUT, State.AUTH_PENDING, action=lambda s, d: s.a_clear_session(d)),
            Transition(State.EDITING_CLEAN, Event.LOGOUT, State.AUTH_PENDING, action=lambda s, d: s.a_clear_session(d)),
            Transition(State.EDITING_DIRTY, Event.LOGOUT, State.AUTH_PENDING, action=lambda s, d: s.a_clear_session(d)),
            Transition(State.SEARCH, Event.LOGOUT, State.AUTH_PENDING, action=lambda s, d: s.a_clear_session(d)),
            Transition(State.EXPORTING, Event.LOGOUT, State.AUTH_PENDING, action=lambda s, d: s.a_clear_session(d)),
            Transition(State.BACKING_UP, Event.LOGOUT, State.AUTH_PENDING, action=lambda s, d: s.a_clear_session(d)),
            Transition(State.SAVE_PROMPT, Event.LOGOUT, State.AUTH_PENDING, action=lambda s, d: s.a_clear_session(d)),
            Transition(State.ERROR, Event.LOGOUT, State.AUTH_PENDING, action=lambda s, d: s.a_clear_session(d)),
        ]

    # Background sync region transitions
    def _sync_transitions(self) -> List[Transition]:
        return [
            Transition(State.SYNC_IDLE, Event.SYNC_START, State.SYNC_SYNCING, guard=lambda s, d: s.g_network_up(d)),
            Transition(State.SYNC_SYNCING, Event.SYNC_DONE, State.SYNC_IDLE),
            Transition(State.SYNC_SYNCING, Event.SYNC_ABORT, State.SYNC_IDLE),
        ]

    def dispatch(self, event: Event, **data: Any) -> State:
        """Dispatch an event to foreground machine."""
        src = self.state
        for t in self._transitions():
            if t.src == src and t.event == event:
                if t.guard is None or t.guard(self, data):
                    if t.action:
                        t.action(self, data)
                    self.state = t.dst
                    self._record(src, event, t.dst)
                    return self.state
        # No transition matched; remain
        self._record(src, event, src)
        return self.state

    def dispatch_sync(self, event: Event, **data: Any) -> State:
        src = self.sync_state
        for t in self._sync_transitions():
            if t.src == src and t.event == event:
                if t.guard is None or t.guard(self, data):
                    if t.action:
                        t.action(self, data)
                    self.sync_state = t.dst
                    self._record(src, event, t.dst)
                    return self.sync_state
        self._record(src, event, src)
        return self.sync_state

    def status(self) -> Dict[str, Any]:
        return {
            "state": self.state.name,
            "sync_state": self.sync_state.name,
            "encryption_on": self.encryption_on,
            "network_up": self.network_up,
            "unsaved_changes": self.unsaved_changes,
        }
