from project import get_high_score, Obstacles, get_player


def test_get_high_score():
    assert get_high_score(0) == 0
    assert get_high_score(2) == 2
    assert get_high_score(5) == 5

def test_get_player():
    player = get_player()
    assert player.rect.midbottom == (200,405)
    assert player.gravity == 0
    assert player.is_duck == False

class TestObstacles:
    def test_rect(self):
        enemy = Obstacles("fish")
        assert enemy.rect.y == 343

    def test_snail(self):
        enemy = Obstacles("snail")
        assert enemy.rect.y == 372
