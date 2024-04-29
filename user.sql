-- 사용자 데이터 삽입 쿼리
INSERT INTO user (email, name, password, phone_number, birthday, is_superuser, is_staff, created_at, updated_at, deleted_at)
VALUES 
    ('user1@example.com', 'User1', 'password1', '01012345678', '1990-01-01', TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user2@example.com', 'User2', 'password2', '01055555555', '1995-05-05', TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user3@example.com', 'User3', 'password3', '01077777777', NULL, FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user4@example.com', 'User4', 'password4', '01088888888', '2000-12-25', FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user5@example.com', 'User5', 'password5', '01011112222', '1998-03-15', FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user6@example.com', 'User6', 'password6', '01099998888', '1985-08-20', TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user7@example.com', 'User7', 'password7', '01066666666', '1996-09-05', TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user8@example.com', 'User8', 'password8', '01022222222', '1989-06-15', FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user9@example.com', 'User9', 'password9', '01033333333', '1994-10-25', FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user10@example.com', 'User10', 'password10', '01044444444', NULL, TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user11@example.com', 'User11', 'password11', '01012341234', '2002-04-30', FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user12@example.com', 'User12', 'password12', '01098769876', '1997-11-28', TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user13@example.com', 'User13', 'password13', '01054325432', NULL, TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user14@example.com', 'User14', 'password14', '01076547654', NULL, FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user15@example.com', 'User15', 'password15', '01043215432', '1993-07-10', TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user16@example.com', 'User16', 'password16', '01098765432', '2000-02-18', FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user17@example.com', 'User17', 'password17', '01023456789', NULL, TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    ('user18@example.com', 'User18', 'password18', '01087654321', NULL, FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL)



-- 주소 데이터 삽입 쿼리
INSERT INTO address_address (user_id, name, base, detail, created_at, updated_at, deleted_at)
VALUES 
    (1, 'Home', '123 Street', 'Apt 101', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (2, 'Home', '456 Avenue', 'Unit 202', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (3, 'Home', '789 Road', 'Suite 303', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (4, 'Home', '101 Boulevard', 'Floor 4', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (5, 'Home', '210 Lane', 'Room 505', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (6, 'Home', '777 Street', 'Apt 303', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (7, 'Home', '888 Avenue', 'Unit 101', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (8, 'Home', '999 Road', 'Suite 404', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (9, 'Home', '111 Boulevard', 'Floor 2', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (10, 'Home', '222 Lane', 'Room 303', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (11, 'Home', '333 Street', 'Apt 505', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (12, 'Home', '444 Avenue', 'Unit 202', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (13, 'Home', '555 Road', 'Suite 303', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (14, 'Home', '666 Boulevard', 'Floor 4', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (15, 'Home', '777 Lane', 'Room 505', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (16, 'Home', '888 Street', 'Apt 303', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (17, 'Home', '999 Avenue', 'Unit 101', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (18, 'Home', '101 Road', 'Suite 404', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (19, 'Home', '202 Boulevard', 'Floor 2', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL),
    (20, 'Home', '303 Lane', 'Room 303', '2024-04-01 12:00:00', '2024-04-01 12:00:00', NULL);
