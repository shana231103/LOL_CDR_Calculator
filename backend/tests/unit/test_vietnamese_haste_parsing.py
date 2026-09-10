# File: backend/tests/unit/test_vietnamese_haste_parsing.py

import pytest
from app.infrastructure.external.riot_client import RiotDataDragonClient


def test_parse_vietnamese_item_haste():
    overlay = {
        "3050": {
            "name": "Zeke's Convergence",
            "ultimate_haste": 15.0,
        }
    }

    # 1. Hỏa Ngọc (Kindlegem - 3067): 10 Điểm Hồi Kỹ Năng in stats
    kindlegem_vi = (
        "<mainText><stats><attention>200</attention> Máu<br>"
        "<attention>10</attention> Điểm Hồi Kỹ Năng</stats><br><br></mainText>"
    )
    ah, ult_h, basic_h, summ_h = RiotDataDragonClient._parse_item_haste(kindlegem_vi, 3067, overlay)
    assert ah == 10.0
    assert ult_h == 0.0
    assert basic_h == 0.0
    assert summ_h == 0.0

    # 2. Hỏa Khuẩn (Malignance - 3118): 15 AH in stats + 20 Điểm Hồi Chiêu Cuối in passive
    malignance_vi = (
        "<mainText><stats><attention>85</attention> Sức Mạnh Phép Thuật<br>"
        "<attention>600</attention> Năng Lượng<br>"
        "<attention>15</attention> Điểm Hồi Kỹ Năng</stats><br><br>"
        "<passive>Ai Oán</passive><br>Nhận 20 Điểm Hồi Chiêu Cuối.<br><br>"
        "<passive>Màn Sương Căm Hận</passive><br>Gây sát thương...</mainText>"
    )
    ah, ult_h, basic_h, summ_h = RiotDataDragonClient._parse_item_haste(malignance_vi, 3118, overlay)
    assert ah == 15.0
    assert ult_h == 20.0
    assert basic_h == 0.0
    assert summ_h == 0.0

    # 3. Khiên Hextech Thử Nghiệm (Experimental Hexplate - 3073): 0 AH + 30 Điểm Hồi Kỹ Năng cho Chiêu Cuối
    hexplate_vi = (
        "<mainText><stats><attention>40</attention> Sức Mạnh Công Kích<br>"
        "<attention>20%</attention> Tốc Độ Đánh<br>"
        "<attention>450</attention> Máu</stats><br><br>"
        "<passive>Bùng Nổ Hextech</passive><br>Nhận 30 Điểm Hồi Kỹ Năng cho Chiêu Cuối.<br><br>"
        "<passive>Quá Tải</passive><br>Sau khi sử dụng chiêu cuối...</mainText>"
    )
    ah, ult_h, basic_h, summ_h = RiotDataDragonClient._parse_item_haste(hexplate_vi, 3073, overlay)
    assert ah == 0.0
    assert ult_h == 30.0
    assert basic_h == 0.0
    assert summ_h == 0.0

    # 4. Ngọn Giáo Shojin (Spear of Shojin - 3161): 0 AH in stats + 25 Điểm Hồi Kỹ Năng Cơ Bản
    shojin_vi = (
        "<mainText><stats><attention>45</attention> Sức Mạnh Công Kích<br>"
        "<attention>450</attention> Máu</stats><br><br>"
        "<passive>Long Lực</passive> <br>Nhận 25 Điểm Hồi Kỹ Năng Cơ Bản.<br><br>"
        "<passive>Tâm Lực</passive> <br>Gây sát thương...</mainText>"
    )
    ah, ult_h, basic_h, summ_h = RiotDataDragonClient._parse_item_haste(shojin_vi, 3161, overlay)
    assert ah == 0.0
    assert ult_h == 0.0
    assert basic_h == 25.0
    assert summ_h == 0.0

    # 5. Giày Khai Sáng Ionia (Ionian Boots - 3158): 10 AH in stats + 10 Điểm Hồi Phép Bổ Trợ
    lucidity_vi = (
        "<mainText><stats><attention>10</attention> Điểm Hồi Kỹ Năng<br>"
        "<attention>45</attention> Tốc Độ Di Chuyển</stats><br><br>"
        "<passive>Tinh Túy Ionia</passive><br>Nhận 10 Điểm Hồi Phép Bổ Trợ.<br><br></mainText>"
    )
    ah, ult_h, basic_h, summ_h = RiotDataDragonClient._parse_item_haste(lucidity_vi, 3158, overlay)
    assert ah == 10.0
    assert ult_h == 0.0
    assert basic_h == 0.0
    assert summ_h == 10.0
