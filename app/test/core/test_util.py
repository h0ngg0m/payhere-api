from app.core.util import get_chosung


def test_get_chosung_success():
    assert get_chosung("붕어빵") == "ㅂㅇㅃ"
    assert get_chosung("강아지") == "ㄱㅇㅈ"
    assert get_chosung("고양이") == "ㄱㅇㅇ"
    assert get_chosung("토끼") == "ㅌㄲ"
    assert get_chosung("물고기") == "ㅁㄱㄱ"
    assert get_chosung("슈크림 라뗴") == "ㅅㅋㄹ ㄹㄸ"
    assert get_chosung("경주 사과") != "ㄱㅈ ㄱㅅ"
    assert get_chosung("슈크림 라뗴") != "ㅅㄹㅋ ㄹㄸ"
