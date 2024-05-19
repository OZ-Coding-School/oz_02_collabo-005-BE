from enum import Enum, unique

@unique
class StatusCode:
    ### Restaurant(200) ###
    RESTAURANT_SHUT_DOWN = 200000               # 폐업
    RESTAURANT_OPEN = 200001                    # 영업중
    RESTAURANT_PREPARE = 200002                 # 영업 준비
    RESTAURANT_CLOSE = 200003                   # 영업 종료

    ### Menu & Option(210) ###
    MENU_OPTION_AVAILABLE = 210001              # 판매중
    MENU_OPTION_SOLD_OUT = 210002               # 품절
    MENU_OPTION_HIDDEN = 210003                 # 숨김
    MENU_OPTION_MODIFIED_OR_DELETED = 210999    # 변경 또는 삭제

    ### Order(300) ###
    ORDER_PENDING = 300000                      # 주문 확인중
    ORDER_ACCEPTED = 300001                     # 주문 수락
    ORDER_REJECTED = 300002                     # 주문 거절
    ORDER_CANCELLED_BY_STORE = 300091           # 주문 취소 - 가게
    ORDER_CANCELLED_BY_CUSTOMER = 300092        # 주문 취소 - 고객
    ORDER_COOKING = 300101                      # 조리중
    ORDER_COOKED = 300102                       # 조리완료

    ### Payment(310) ###
    PAYMENT_PENDING = 310000                    # 결제 대기
    PAYMENT_SUCCESSFUL = 310001                 # 결제 성공
    PAYMENT_FAILED = 310002                     # 결제 실패
    PAYMENT_ONLINE_CARD = 310101                # 온라인 - 카드
    PAYMENT_ONLINE_CASH = 310102                # 온라인 - 현금
    PAYMENT_OFFLINE_CARD = 310201               # 현장 - 카드
    PAYMENT_OFFLINE_CASH = 310202               # 현장 - 현금
    PAYMENT_INVALID_CARD_INFO = 310400          # 잘못된 카드 정보
    PAYMENT_INSUFFICIENT_BALANCE = 310410       # 잔액 부족
    PAYMENT_SERVER_INTERNAL_ERROR = 310500      # 서버 내부 오류
    PAYMENT_COMMUNICATION_ERROR = 310502        # 결제 통신 오류

    ### Delivery(320) ###
    DELIVERY_DISPATCH_PENDING = 320000          # 배차 대기
    DELIVERY_PICKUP_PENDING = 320001            # 픽업 대기
    DELIVERY_DELIVERING = 320002                # 배달중
    DELIVERY_COMPLETED = 320003                 # 배달완료