def test_phrase_length():
    phrase = input("Set a phrase: ")
    phrase_length = len(phrase)
    assert phrase_length < 15, f"Длина фразы {phrase_length} символов, а должна быть <15"