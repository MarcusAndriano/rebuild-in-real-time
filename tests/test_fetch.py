"""Tests for the acquisition layer.

These cover the logic that must not break quietly: writing, skipping, and
forcing. The network calls themselves are not tested here — they are tested by
the weekly Action going green.
"""

import pandas as pd
import pytest

from src import fetch


@pytest.fixture
def frame():
    return pd.DataFrame(
        {"player": ["Anderson", "Fernández", "Bouaddi"], "minutes": [360, 270, 90]}
    ).set_index("player")


def test_write_creates_file_and_parent_dirs(tmp_path, frame):
    path = tmp_path / "a" / "b" / "player_match.parquet"
    assert fetch._write(frame, path) is True
    assert path.exists()


def test_write_roundtrips_the_index_as_a_column(tmp_path, frame):
    path = tmp_path / "x.parquet"
    fetch._write(frame, path)
    back = pd.read_parquet(path)
    # The index must survive as data — otherwise player identity is lost the
    # moment the archive is re-read months later.
    assert "player" in back.columns
    assert len(back) == 3


def test_write_is_idempotent(tmp_path, frame):
    path = tmp_path / "x.parquet"
    assert fetch._write(frame, path) is True
    assert fetch._write(frame, path) is False, "second write must skip, not overwrite"


def test_force_overwrites(tmp_path, frame):
    path = tmp_path / "x.parquet"
    fetch._write(frame, path)
    bigger = pd.concat([frame, frame])
    assert fetch._write(bigger, path, force=True) is True
    assert len(pd.read_parquet(path)) == 6


def test_cli_rejects_no_subcommand():
    with pytest.raises(SystemExit):
        fetch.main([])


def test_cli_parses_each_subcommand(monkeypatch):
    calls = []
    monkeypatch.setattr(fetch, "fetch_weekly", lambda *a: calls.append(("weekly", a)))
    monkeypatch.setattr(fetch, "fetch_snapshot", lambda *a: calls.append(("snapshot", a)))
    monkeypatch.setattr(fetch, "fetch_historical", lambda *a: calls.append(("hist", a)))

    fetch.main(["weekly", "--season", "2526"])
    fetch.main(["snapshot"])
    fetch.main(["historical", "--seasons", "2425", "2526"])

    assert [c[0] for c in calls] == ["weekly", "snapshot", "hist"]
    assert calls[2][1][0] == ["2425", "2526"]
