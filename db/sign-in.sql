DELIMITER $$
CREATE DEFINER=root@localhost PROCEDURE validateLogin(
IN p_email VARCHAR(45)
)
BEGIN
    select * from login_credentials where Email = p_email;
END$$
DELIMITER ;