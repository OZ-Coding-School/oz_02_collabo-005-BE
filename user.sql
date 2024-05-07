INSERT INTO user_user (email, name, password, phone_number, birthday, is_superuser, is_staff, created_at, updated_at)
VALUES
    ('user1@example.com', 'User1', 'password1', '01012345678', '1990-01-01', TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('user2@example.com', 'User2', 'password2', '01055555555', '1995-05-05', TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('user3@example.com', 'User3', 'password3', '01077777777', NULL, FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('user4@example.com', 'User4', 'password4', '01088888888', '2000-12-25', FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('user5@example.com', 'User5', 'password5', '01011112222', '1998-03-15', FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('user6@example.com', 'User6', 'password6', '01099998888', '1985-08-20', TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('user7@example.com', 'User7', 'password7', '01066666666', '1996-09-05', TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('user8@example.com', 'User8', 'password8', '01022222222', '1989-06-15', FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('user9@example.com', 'User9', 'password9', '01033333333', '1994-10-25', FALSE, FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('user10@example.com', 'User10', 'password10', '01044444444', NULL, TRUE, TRUE, '2024-04-01 12:00:00', '2024-04-01 12:00:00');

INSERT INTO user_address (user_id, name, base, detail, created_at, updated_at)
VALUES 
    (1, 'Home', '123 Street', 'Apt 101', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (2, 'Home', '456 Avenue', 'Unit 202', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (3, 'Home', '789 Road', 'Suite 303', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (4, 'Home', '101 Boulevard', 'Floor 4', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (5, 'Home', '210 Lane', 'Room 505', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (6, 'Home', '777 Street', 'Apt 303', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (7, 'Home', '888 Avenue', 'Unit 101', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (8, 'Home', '999 Road', 'Suite 404', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (9, 'Home', '111 Boulevard', 'Floor 2', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (10, 'Home', '222 Lane', 'Room 303', '2024-04-01 12:00:00', '2024-04-01 12:00:00');

INSERT INTO restaurant_restaurant (name, logo, representative_menu, representative_menu_picture, description, notice, delivery_fee, minimum_order_amount, opening_time, closing_time, status, created_at, updated_at)
VALUES 
    ('Restaurant A', 'http://example.com/logo1.jpg', 1, 'http://example.com/menu1.jpg', 'Description for Restaurant A', 'Notice for Restaurant A', 5000, 20000, '09:00:00', '21:00:00', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Restaurant B', 'http://example.com/logo2.jpg', 2, 'http://example.com/menu2.jpg', 'Description for Restaurant B', 'Notice for Restaurant B', 4000, 25000, '10:00:00', '22:00:00', 2, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Restaurant C', 'http://example.com/logo3.jpg', 3, 'http://example.com/menu3.jpg', 'Description for Restaurant C', 'Notice for Restaurant C', 6000, 18000, '08:00:00', '20:00:00', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Restaurant D', 'http://example.com/logo4.jpg', 4, 'http://example.com/menu4.jpg', 'Description for Restaurant D', 'Notice for Restaurant D', 5500, 22000, '11:00:00', '23:00:00', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Restaurant E', 'http://example.com/logo5.jpg', 5, 'http://example.com/menu5.jpg', 'Description for Restaurant E', 'Notice for Restaurant E', 4800, 19000, '07:00:00', '19:00:00', 3, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Restaurant F', 'http://example.com/logo6.jpg', 6, 'http://example.com/menu6.jpg', 'Description for Restaurant F', 'Notice for Restaurant F', 5200, 21000, '09:00:00', '21:00:00', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Restaurant G', 'http://example.com/logo7.jpg', 7, 'http://example.com/menu7.jpg', 'Description for Restaurant G', 'Notice for Restaurant G', 5900, 23000, '10:00:00', '22:00:00', 2, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Restaurant H', 'http://example.com/logo8.jpg', 8, 'http://example.com/menu8.jpg', 'Description for Restaurant H', 'Notice for Restaurant H', 5100, 24000, '12:00:00', '24:00:00', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Restaurant I', 'http://example.com/logo9.jpg', 9, 'http://example.com/menu9.jpg', 'Description for Restaurant I', 'Notice for Restaurant I', 4600, 20000, '08:00:00', '20:00:00', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Restaurant J', 'http://example.com/logo10.jpg', 10, 'http://example.com/menu10.jpg', 'Description for Restaurant J', 'Notice for Restaurant J', 5400, 21000, '10:00:00', '22:00:00', 2, '2024-04-01 12:00:00', '2024-04-01 12:00:00');

INSERT INTO restaurant_hashtag (hashtag, created_at, updated_at)
VALUES 
    ('#food', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('#restaurant', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('#delivery', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('#pizza', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('#burger', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('#sushi', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('#coffee', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('#dessert', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('#healthy', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('#vegetarian', '2024-04-01 12:00:00', '2024-04-01 12:00:00');

INSERT INTO restaurant_restauranthashtag (restaurant_id, hashtag_id, created_at, updated_at)
VALUES 
    (1, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (2, 2, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (3, 3, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (4, 4, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (5, 5, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (6, 6, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (7, 7, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (8, 8, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (9, 9, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (10, 10, '2024-04-01 12:00:00', '2024-04-01 12:00:00');

INSERT INTO restaurant_category (category, created_at, updated_at)
VALUES 
    ('Italian', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Mexican', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Japanese', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Chinese', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Korean', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Indian', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Thai', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('Greek', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('French', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    ('American', '2024-04-01 12:00:00', '2024-04-01 12:00:00');

INSERT INTO restaurant_restaurantcategory (restaurant_id, category_id, created_at, updated_at)
VALUES 
    (1, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (2, 2, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (3, 3, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (4, 4, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (5, 5, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (6, 6, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (7, 7, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (8, 8, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (9, 9, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (10, 10, '2024-04-01 12:00:00', '2024-04-01 12:00:00');

INSERT INTO restaurant_menu_group (restaurant_id, description, created_at, updated_at)
VALUES 
    (1, 'Description for Menu Group 1', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (2, 'Description for Menu Group 2', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (3, 'Description for Menu Group 3', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (4, 'Description for Menu Group 4', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (5, 'Description for Menu Group 5', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (6, 'Description for Menu Group 6', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (7, 'Description for Menu Group 7', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (8, 'Description for Menu Group 8', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (9, 'Description for Menu Group 9', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (10, 'Description for Menu Group 10', '2024-04-01 12:00:00', '2024-04-01 12:00:00');

INSERT INTO restaurant_menu (restaurant_id, menu_group_id, represent, name, price, picture, description, status, created_at, updated_at)
VALUES 
    (1, 1, 'Represent 1', 'Menu 1', 10000, 'http://example.com/menu1.jpg', 'Description for Menu 1', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (2, 2, 'Represent 2', 'Menu 2', 12000, 'http://example.com/menu2.jpg', 'Description for Menu 2', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (3, 3, 'Represent 3', 'Menu 3', 11000, 'http://example.com/menu3.jpg', 'Description for Menu 3', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (4, 4, 'Represent 4', 'Menu 4', 13000, 'http://example.com/menu4.jpg', 'Description for Menu 4', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (5, 5, 'Represent 5', 'Menu 5', 15000, 'http://example.com/menu5.jpg', 'Description for Menu 5', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (6, 6, 'Represent 6', 'Menu 6', 17000, 'http://example.com/menu6.jpg', 'Description for Menu 6', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (7, 7, 'Represent 7', 'Menu 7', 19000, 'http://example.com/menu7.jpg', 'Description for Menu 7', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (8, 8, 'Represent 8', 'Menu 8', 20000, 'http://example.com/menu8.jpg', 'Description for Menu 8', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (9, 9, 'Represent 9', 'Menu 9', 18000, 'http://example.com/menu9.jpg', 'Description for Menu 9', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (10, 10, 'Represent 10', 'Menu 10', 16000, 'http://example.com/menu10.jpg', 'Description for Menu 10', 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00');

INSERT INTO restaurant_option_group (mandatory, choice_mode, maximum, created_at, updated_at, option_name)
VALUES
    (FALSE, 2, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00', 'Option Group 1'),
    (FALSE, 2, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00', 'Option Group 2'),
    (FALSE, 2, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00', 'Option Group 3'),
    (FALSE, 2, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00', 'Option Group 4'),
    (FALSE, 2, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00', 'Option Group 5'),
    (FALSE, 2, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00', 'Option Group 6'),
    (FALSE, 2, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00', 'Option Group 7'),
    (FALSE, 2, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00', 'Option Group 8'),
    (FALSE, 2, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00', 'Option Group 9'),
    (FALSE, 2, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00', 'Option Group 10');

INSERT INTO restaurant_option (option_group_id, name, price, created_at, updated_at)
VALUES
    (1, 'Option 1', 1000, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (2, 'Option 2', 1200, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (3, 'Option 3', 1100, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (4, 'Option 4', 1300, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (5, 'Option 5', 1500, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (6, 'Option 6', 1700, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (7, 'Option 7', 1900, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (8, 'Option 8', 2000, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (9, 'Option 9', 1800, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (10, 'Option 10', 1600, '2024-04-01 12:00:00', '2024-04-01 12:00:00');

INSERT INTO restaurant_option_group_to_menu (menu_id, option_group_id, created_at, updated_at)
VALUES
    (1, 1, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (2, 2, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (3, 3, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (4, 4, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (5, 5, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (6, 6, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (7, 7, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (8, 8, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (9, 9, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (10, 10, '2024-04-01 12:00:00', '2024-04-01 12:00:00');

INSERT INTO order_order (user_id, order_status, cooking_time, delivery_address, total_price, order_time, created_at, updated_at)
VALUES
    (1, 0, '2024-04-01 12:00:00', '123 Main Street', 15000, '2024-04-01 12:00:00', '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (2, 1, '2024-04-02 13:00:00', '456 Elm Street', 20000, '2024-04-02 13:00:00', '2024-04-02 12:00:00', '2024-04-02 12:00:00'),
    (3, 2, '2024-04-03 14:00:00', '789 Oak Street', 25000, '2024-04-03 14:00:00', '2024-04-03 12:00:00', '2024-04-03 12:00:00'),
    (4, 0, '2024-04-04 15:00:00', '101 Maple Street', 18000, '2024-04-04 15:00:00', '2024-04-03 12:00:00', '2024-04-03 12:00:00'),
    (5, 1, '2024-04-05 16:00:00', '202 Pine Street', 22000, '2024-04-05 16:00:00', '2024-04-03 12:00:00', '2024-04-03 12:00:00'),
    (6, 2, '2024-04-06 17:00:00', '303 Cedar Street', 19000, '2024-04-06 17:00:00', '2024-04-03 12:00:00', '2024-04-03 12:00:00'),
    (7, 0, '2024-04-07 18:00:00', '404 Birch Street', 21000, '2024-04-07 18:00:00', '2024-04-03 12:00:00', '2024-04-03 12:00:00'),
    (8, 1, '2024-04-08 19:00:00', '505 Walnut Street', 23000, '2024-04-08 19:00:00', '2024-04-03 12:00:00', '2024-04-03 12:00:00'),
    (9, 2, '2024-04-09 20:00:00', '606 Pineapple Street', 20000, '2024-04-09 20:00:00', '2024-04-03 12:00:00', '2024-04-03 12:00:00'),
    (10, 0, '2024-04-10 21:00:00', '707 Strawberry Street', 24000, '2024-04-10 21:00:00', '2024-04-03 12:00:00', '2024-04-03 12:00:00');

INSERT INTO order_order_detail (order_id, menu_id, quantity, created_at, updated_at)
VALUES 
    (1, 1, 2, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (2, 2, 1, '2024-04-02 12:00:00', '2024-04-02 12:00:00'),
    (3, 3, 3, '2024-04-03 12:00:00', '2024-04-03 12:00:00'),
    (4, 4, 2, '2024-04-04 12:00:00', '2024-04-04 12:00:00'),
    (5, 5, 1, '2024-04-05 12:00:00', '2024-04-05 12:00:00'),
    (6, 6, 3, '2024-04-06 12:00:00', '2024-04-06 12:00:00'),
    (7, 7, 2, '2024-04-07 12:00:00', '2024-04-07 12:00:00'),
    (8, 8, 1, '2024-04-08 12:00:00', '2024-04-08 12:00:00'),
    (9, 9, 3, '2024-04-09 12:00:00', '2024-04-09 12:00:00'),
    (10, 10, 2, '2024-04-10 12:00:00', '2024-04-10 12:00:00');

INSERT INTO order_order_option_group (order_detail_id, order_group_name, mandatory, created_at, updated_at)
VALUES 
    (1, 'Option Group 1', FALSE, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (2, 'Option Group 2', FALSE, '2024-04-02 12:00:00', '2024-04-02 12:00:00'),
    (3, 'Option Group 3', TRUE, '2024-04-03 12:00:00', '2024-04-03 12:00:00'),
    (4, 'Option Group 4', FALSE, '2024-04-04 12:00:00', '2024-04-04 12:00:00'),
    (5, 'Option Group 5', TRUE, '2024-04-05 12:00:00', '2024-04-05 12:00:00'),
    (6, 'Option Group 6', FALSE, '2024-04-06 12:00:00', '2024-04-06 12:00:00'),
    (7, 'Option Group 7', FALSE, '2024-04-07 12:00:00', '2024-04-07 12:00:00'),
    (8, 'Option Group 8', TRUE, '2024-04-08 12:00:00', '2024-04-08 12:00:00'),
    (9, 'Option Group 9', FALSE, '2024-04-09 12:00:00', '2024-04-09 12:00:00'),
    (10, 'Option Group 10', TRUE, '2024-04-10 12:00:00', '2024-04-10 12:00:00');

INSERT INTO order_order_option (order_option_group_id, option_name, option_price, created_at, updated_at)
VALUES 
    (1, 'Extra Cheese', 1000, '2024-04-01 12:00:00', '2024-04-01 12:00:00'),
    (2, 'Extra Sauce', 500, '2024-04-02 12:00:00', '2024-04-02 12:00:00'),
    (3, 'Extra Toppings', 700, '2024-04-03 12:00:00', '2024-04-03 12:00:00'),
    (4, 'Seasonal Vegetables', 300, '2024-04-04 12:00:00', '2024-04-04 12:00:00'),
    (5, 'Spicy Mayo', 1200, '2024-04-05 12:00:00', '2024-04-05 12:00:00'),
    (6, 'Extra Bacon', 800, '2024-04-06 12:00:00', '2024-04-06 12:00:00'),
    (7, 'Avocado', 1300, '2024-04-07 12:00:00', '2024-04-07 12:00:00'),
    (8, 'Garlic Aioli', 1000, '2024-04-08 12:00:00', '2024-04-08 12:00:00'),
    (9, 'Grilled Onions', 1500, '2024-04-09 12:00:00', '2024-04-09 12:00:00'),
    (10, 'Mushroom Sauce', 1100, '2024-04-10 12:00:00', '2024-04-10 12:00:00');

INSERT INTO order_delivery_man (delivery_man_name, delivery_type, created_at, updated_at)
VALUES 
    ('John', 1, NOW(), NOW()),
    ('Alice', 2, NOW(), NOW()),
    ('Michael', 1, NOW(), NOW()),
    ('Emily', 2, NOW(), NOW()),
    ('William', 1, NOW(), NOW()),
    ('Sophia', 2, NOW(), NOW()),
    ('James', 1, NOW(), NOW()),
    ('Olivia', 2, NOW(), NOW()),
    ('Benjamin', 1, NOW(), NOW()),
    ('Emma', 2, NOW(), NOW());

INSERT INTO order_delivery (delivery_man_id, order_id, estimated_time, completion_time, created_at, updated_at)
VALUES 
    (1, 1, NOW(), NOW(), NOW(), NOW()),
    (2, 2, NOW(), NOW(), NOW(), NOW()),
    (3, 3, NOW(), NOW(), NOW(), NOW()),
    (4, 4, NOW(), NOW(), NOW(), NOW()),
    (5, 5, NOW(), NOW(), NOW(), NOW()),
    (6, 6, NOW(), NOW(), NOW(), NOW()),
    (7, 7, NOW(), NOW(), NOW(), NOW()),
    (8, 8, NOW(), NOW(), NOW(), NOW()),
    (9, 9, NOW(), NOW(), NOW(), NOW()),
    (10, 10, NOW(), NOW(), NOW(), NOW());