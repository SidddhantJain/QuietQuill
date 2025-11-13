from __future__ import annotations
from .state_machine import QuietQuillStateMachine, State, Event


def run_demo() -> None:
    sm = QuietQuillStateMachine()

    print("Initial:", sm.status())

    # Launch → login
    sm.dispatch(Event.LAUNCH_APP)
    assert sm.state == State.AUTH_PENDING

    # Submit credentials (valid)
    sm.dispatch(Event.SUBMIT_CREDENTIALS, valid=True)
    assert sm.state == State.DASHBOARD

    # Background sync start
    sm.dispatch_sync(Event.SYNC_START)
    assert sm.sync_state == State.SYNC_SYNCING

    # Open editor & type
    sm.dispatch(Event.OPEN_EDITOR)
    assert sm.state == State.EDITING_CLEAN

    sm.dispatch(Event.TYPE_TEXT)
    assert sm.state == State.EDITING_DIRTY

    # Auto-save with network available
    sm.dispatch(Event.AUTO_SAVE)
    assert sm.state == State.EDITING_CLEAN

    # Close editor, go back to dashboard, then open search and exit back to history
    sm.dispatch(Event.CLOSE_EDITOR)
    assert sm.state == State.DASHBOARD

    sm.dispatch(Event.OPEN_SEARCH)
    assert sm.state == State.SEARCH
    sm.dispatch(Event.EXIT_SEARCH)
    assert sm.state == State.DASHBOARD

    # Export (requires encryption enabled)
    sm.set_encryption(True)
    sm.dispatch(Event.START_EXPORT)
    assert sm.state == State.EXPORTING
    sm.dispatch(Event.EXPORT_DONE)
    assert sm.state == State.DASHBOARD

    # Backup (requires network up)
    sm.set_network(True)
    sm.dispatch(Event.START_BACKUP)
    assert sm.state == State.BACKING_UP
    sm.dispatch(Event.BACKUP_DONE)
    assert sm.state == State.DASHBOARD

    # Sync done
    sm.dispatch_sync(Event.SYNC_DONE)
    assert sm.sync_state == State.SYNC_IDLE

    # Logout
    sm.dispatch(Event.LOGOUT)
    assert sm.state == State.AUTH_PENDING

    print("Final:", sm.status())

    # Print transition log (subset)
    for src, ev, dst in sm.log[:15]:
        print(f"{src.name} --{ev.name}--> {dst.name}")


if __name__ == "__main__":
    run_demo()
