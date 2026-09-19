def test_repository_roundtrip(tmp_path):
    from bot.storage.repository import Repository
    r=Repository(tmp_path/"x.db")
    r.init()
    r.log_event("test",{"ok":1})
    assert r.recent(1)[0][0]=="test"
